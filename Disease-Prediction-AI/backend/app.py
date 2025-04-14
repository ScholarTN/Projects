# Add this at the top of your app.py file, before the app instantiation
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import joblib
import uuid
import csv
import os
from fpdf import FPDF
from io import BytesIO
from flask import Flask, request, jsonify, send_file, make_response
from report_generator import generate_pdf
from io import StringIO
from suggestions import generate_suggestion

app = Flask(__name__)
# Enhanced CORS configuration to allow requests from the frontend
CORS(app, supports_credentials=True, resources={r"/*": {"origins": ["http://127.0.0.1:5051", "http://localhost:5051"]}})

# Rest of your code remains unchanged

# MongoDB Atlas Connection
client = MongoClient("mongodb+srv://Scholar:Scholar101!@cluster0.rub78kd.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["Diabetes_App"]
users_collection = db["users"]
predictions_collection = db["predictions"]

# Load trained model
model = joblib.load("/home/scholar/Documents/DOCS/Projects101/Projects/Disease-Prediction-AI/diabetes_model.pkl")

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    role = data.get("role", "user")
    work_id = data.get("workId") if role == "doctor" else None

    if users_collection.find_one({"email": email}):
        return jsonify({"status": "error", "message": "User already exists"}), 400

    hashed_password = generate_password_hash(password)
    user_data = {
        "email": email,
        "password": hashed_password,
        "role": role,
        "token": str(uuid.uuid4())
    }
    
    if role == "doctor":
        if not work_id:
            return jsonify({"status": "error", "message": "Work ID is required for doctors"}), 400
        
        # Check if work ID is already registered
        existing_doctor = users_collection.find_one({"work_id": work_id})
        if existing_doctor:
            return jsonify({"status": "error", "message": "Work ID already registered"}), 400
            
        user_data["work_id"] = work_id
    
    users_collection.insert_one(user_data)
    return jsonify({"status": "success", "message": "User registered successfully"})

@app.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        print("Login request data:", data)
        
        email = data.get("email")
        password = data.get("password")
        work_id = data.get("workId")
        requested_role = data.get("role")

        # Basic validation
        if not email or not password:
            return jsonify({"status": "error", "message": "Email and password are required"}), 400

        user = users_collection.find_one({"email": email})
        if not user:
            return jsonify({"status": "error", "message": "User not found"}), 404

        # Check password
        if not check_password_hash(user["password"], password):
            return jsonify({"status": "error", "message": "Invalid password"}), 401

        # Only enforce role check for doctors
        if requested_role == "doctor" and user["role"] != "doctor":
            return jsonify({
                "status": "error", 
                "message": "Please use the patient portal"
            }), 403

        # Doctor-specific checks
        if user["role"] == "doctor":
            if "work_id" not in user:
                return jsonify({"status": "error", "message": "Invalid doctor account"}), 403
            
            if work_id and work_id != user["work_id"]:
                return jsonify({"status": "error", "message": "Invalid work ID"}), 401

        # Update last login time
        users_collection.update_one(
            {"email": email},
            {"$set": {"last_login": datetime.utcnow()}}
        )

        return jsonify({
            "status": "success",
            "token": user["token"],
            "role": user["role"],
            "email": user["email"],
            "message": "Login successful"
        })

    except Exception as e:
        print("Login error:", str(e))
        return jsonify({"status": "error", "message": f"Login error: {str(e)}"}), 500
    
@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    token = data.get("token")
    user = users_collection.find_one({"token": token})

    if not user or user["role"] != "user":
        return jsonify({"status": "error", "message": "Unauthorized"}), 403

    try:
        # Validate required fields
        required_fields = ['age', 'gender', 'glucose', 'blood_pressure', 'family_history']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({"status": "error", "message": f"Missing required field: {field}"}), 400

        # Get input data with proper defaults
        input_data = {
            "age": int(data.get("age", 0)),
            "gender": data.get("gender"),
            "is_pregnant": int(data.get("is_pregnant", 0)) if data.get("gender") == "female" else 0,
            "height": float(data.get("height", 0)),
            "weight": float(data.get("weight", 0)),
            "bmi": float(data.get("bmi", 0)),
            "glucose": float(data.get("glucose", 0)),
            "blood_pressure": float(data.get("blood_pressure", 0)),
            "family_history": int(data.get("family_history", 0))
        }

        # Calculate BMI if not provided but height/weight are
        if input_data["bmi"] <= 0 and input_data["height"] > 0 and input_data["weight"] > 0:
            input_data["bmi"] = input_data["weight"] / ((input_data["height"]/100) ** 2)

        # Validate BMI
        if input_data["bmi"] <= 0:
            return jsonify({"status": "error", "message": "Please provide BMI or height/weight"}), 400

        # Enhanced Risk Calculation (0-100%)
        risk_score = 5  # Base minimum risk

        # Glucose (0-25 points)
        if input_data["glucose"] >= 200: risk_score += 25
        elif input_data["glucose"] >= 140: risk_score += 15
        elif input_data["glucose"] >= 100: risk_score += 5

        # BMI (0-20 points)
        if input_data["age"] >= 18:
            if input_data["age"] < 65:  # Adults
                if input_data["bmi"] >= 30: risk_score += 20
                elif input_data["bmi"] >= 25: risk_score += 10
                elif input_data["bmi"] < 18.5: risk_score += 5
            else:  # Seniors (65+)
                if input_data["bmi"] >= 27: risk_score += 15
                elif input_data["bmi"] < 23: risk_score += 5

        # Blood Pressure (0-20 points)
        if input_data["blood_pressure"] >= 140: risk_score += 20
        elif input_data["blood_pressure"] >= 130: risk_score += 10
        elif input_data["blood_pressure"] >= 120: risk_score += 5

        # Other factors
        risk_score += 10 if input_data["family_history"] else 0
        risk_score += 10 if input_data["is_pregnant"] else 0
        risk_score += 5 if input_data["age"] > 45 else 0

        # Cap at 100% and determine level
        risk_score = min(risk_score, 100)
        risk_level = "low"
        if risk_score >= 75: risk_level = "very high"
        elif risk_score >= 50: risk_level = "high"
        elif risk_score >= 25: risk_level = "medium"

        # Generate suggestion
        suggestion = generate_suggestion(
            risk_level, risk_score, input_data["glucose"], input_data["bmi"],
            input_data["blood_pressure"], input_data["family_history"],
            input_data["is_pregnant"], input_data["age"]
        )

        # Save prediction
        predictions_collection.insert_one({
            "email": user["email"],
            **input_data,
            "prediction": risk_level,
            "risk_score": risk_score,
            "suggestion": suggestion,
            "timestamp": datetime.utcnow()
        })

        return jsonify({
            "status": "success",
            "prediction": risk_level,
            "risk_score": risk_score,
            "suggestion": suggestion,
            "bmi": input_data["bmi"]
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route("/logs", methods=["GET"])
def logs():
    token = request.args.get("token")
    user = users_collection.find_one({"token": token})

    if not user:
        return jsonify({"status": "error", "message": "Invalid token"}), 403

    user_logs = list(predictions_collection.find(
        {"email": user["email"]},
        {"_id": 0, "email": 0}
    ).sort("timestamp", -1).limit(10))

    return jsonify({"status": "success", "logs": user_logs})

@app.route("/all-records", methods=["GET"])
def all_records():
    token = request.args.get("token")
    user = users_collection.find_one({"token": token})

    if not user or user["role"] != "doctor":
        return jsonify({"status": "error", "message": "Unauthorized"}), 403

    records = list(predictions_collection.find(
        {},
        {"_id": 0}
    ).sort("timestamp", -1).limit(50))

    return jsonify({"status": "success", "records": records})

@app.route("/admin-summary", methods=["GET"])
def admin_summary():
    token = request.args.get("token")
    user = users_collection.find_one({"token": token})

    if not user or user["role"] != "doctor":
        return jsonify({"status": "error", "message": "Unauthorized"}), 403

    total_users = users_collection.count_documents({})
    total_predictions = predictions_collection.count_documents({})
    diabetic_cases = predictions_collection.count_documents({"prediction": 1})
    non_diabetic_cases = total_predictions - diabetic_cases

    return jsonify({
        "status": "success",
        "summary": {
            "total_users": total_users,
            "total_predictions": total_predictions,
            "diabetic_cases": diabetic_cases,
            "non_diabetic_cases": non_diabetic_cases
        }
    })


@app.route("/download", methods=["GET"])
def download():
    token = request.args.get("token")
    report_type = request.args.get("type", "csv")

    user = users_collection.find_one({"token": token})
    if not user or user["role"] != "doctor":
        return jsonify({"status": "error", "message": "Unauthorized"}), 403

    try:
        # Define our expected output fields and defaults
        output_fields = [
            'email', 'age', 'bmi', 'glucose', 'blood_pressure',
            'family_history', 'gender', 'prediction', 'suggestion', 'timestamp'
        ]
        
        # Get raw records from MongoDB
        raw_records = list(predictions_collection.find({}, {"_id": 0}))
        
        if not raw_records:
            return jsonify({"status": "error", "message": "No records found"}), 404

        if report_type == "csv":
            # Process each record to include only our desired fields
            processed_records = []
            for record in raw_records:
                # Create new record with only the fields we want
                clean_record = {
                    field: record.get(field, None)  # Returns None if field doesn't exist
                    for field in output_fields
                }
                
                # Convert special fields
                clean_record['family_history'] = 'Yes' if clean_record.get('family_history') else 'No'
                clean_record['gender'] = 'Male' if clean_record.get('gender') == 1 else 'Female'
                clean_record['prediction'] = 'High Risk' if clean_record.get('prediction') == 1 else 'Low Risk'
                
                # Format timestamp
                if isinstance(clean_record.get('timestamp'), datetime):
                    clean_record['timestamp'] = clean_record['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
                elif clean_record.get('timestamp') is None:
                    clean_record['timestamp'] = 'Unknown date'
                
                processed_records.append(clean_record)

            # Generate CSV
            output = StringIO()
            writer = csv.DictWriter(output, fieldnames=output_fields)
            
            writer.writeheader()
            writer.writerows(processed_records)
            
            response = make_response(output.getvalue())
            response.headers["Content-Disposition"] = "attachment; filename=diabetes_records.csv"
            response.headers["Content-type"] = "text/csv"
            return response

        elif report_type == "pdf":
            pdf_bytes = generate_pdf(raw_records)
            response = make_response(pdf_bytes)
            response.headers["Content-Disposition"] = "attachment; filename=diabetes_records.pdf"
            response.headers["Content-type"] = "application/pdf"
            return response

    except Exception as e:
        app.logger.error(f"Report generation failed: {str(e)}")
        return jsonify({"status": "error", "message": f"Report generation failed: {str(e)}"}), 500

    return jsonify({"status": "error", "message": "Invalid report type"}), 400

if __name__ == "__main__":
    if not os.path.exists("reports"):
        os.makedirs("reports")
    app.run(debug=True, port=5050)
