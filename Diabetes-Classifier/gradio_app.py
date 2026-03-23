import gradio as gr
import requests

API_URL = "http://127.0.0.1:8000"


def predict_diabetes(pregnancies, glucose, blood_pressure, skin_thickness,
                     insulin, bmi, diabetes_pedigree, age):
    """Send data to FastAPI and return prediction"""
    try:
        payload = {
            "pregnancies": pregnancies,
            "glucose": glucose,
            "blood_pressure": blood_pressure,
            "skin_thickness": skin_thickness,
            "insulin": insulin,
            "bmi": bmi,
            "diabetes_pedigree": diabetes_pedigree,
            "age": age
        }
        res = requests.post(f"{API_URL}/predict", json=payload)
        data = res.json()

        result     = data["result"]
        confidence = data["confidence"]
        risk       = data["risk_level"]

        # Format output
        emoji = "🔴" if data["prediction"] == 1 else "🟢"
        output = f"""
{emoji} **Prediction: {result}**

📊 **Confidence Scores:**
- Not Diabetic: {confidence['not_diabetic']}%
- Diabetic: {confidence['diabetic']}%

⚠️ **Risk Level: {risk}**
        """.strip()

        return output

    except Exception as e:
        return f"❌ Error connecting to API: {e}\n\nMake sure FastAPI is running on port 8000."


def get_model_metrics():
    """Fetch and display model metrics"""
    try:
        res = requests.get(f"{API_URL}/metrics")
        data = res.json()

        cm = data["confusion_matrix"]
        fi = data["feature_importance"]
        fi_sorted = sorted(fi.items(), key=lambda x: x[1], reverse=True)

        output = f"""
📈 **Model Performance**
- Accuracy: {data['accuracy']}%
- Training samples: {data['train_size']}
- Test samples: {data['test_size']}

🧩 **Confusion Matrix**
```
              Predicted
              No    Yes
Actual No  [ {cm[0][0]:3d}   {cm[0][1]:3d} ]
Actual Yes [ {cm[1][0]:3d}   {cm[1][1]:3d} ]
```

🌟 **Feature Importance (ranked)**
""".strip()

        for feat, imp in fi_sorted:
            bar = "█" * int(imp * 30)
            output += f"\n{feat:<28} {bar} {imp:.4f}"

        return output
    except Exception as e:
        return f"❌ Error: {e}"


# ── Gradio UI ────────────────────────────────────────────────────

with gr.Blocks(
    title="Diabetes Predictor",
    theme=gr.themes.Soft(),
    css="""
        .gradio-container { max-width: 900px !important; }
        .result-box { font-size: 1.1em; }
    """
) as demo:

    gr.Markdown("""
    # 🩺 Diabetes Risk Predictor
    ### Decision Tree Classifier · FastAPI + Gradio
    Enter patient details below to predict diabetes risk.
    """)

    with gr.Tabs():

        # ── Prediction Tab ──
        with gr.TabItem("🔍 Predict"):
            gr.Markdown("### Patient Information")

            with gr.Row():
                pregnancies = gr.Slider(0, 20, value=1, step=1, label="Pregnancies")
                age         = gr.Slider(1, 120, value=30, step=1, label="Age")

            with gr.Row():
                glucose        = gr.Slider(0, 300, value=120, step=1, label="Glucose (mg/dL)")
                blood_pressure = gr.Slider(0, 200, value=70, step=1, label="Blood Pressure (mmHg)")

            with gr.Row():
                bmi              = gr.Slider(0, 70, value=25.0, step=0.1, label="BMI")
                skin_thickness   = gr.Slider(0, 100, value=20, step=1, label="Skin Thickness (mm)")

            with gr.Row():
                insulin          = gr.Slider(0, 900, value=80, step=1, label="Insulin (mu U/ml)")
                diabetes_pedigree = gr.Slider(0.0, 3.0, value=0.5, step=0.01, label="Diabetes Pedigree Function")

            predict_btn = gr.Button("🔍 Predict Diabetes Risk", variant="primary", size="lg")
            result_output = gr.Markdown(label="Prediction Result", elem_classes=["result-box"])

            predict_btn.click(
                fn=predict_diabetes,
                inputs=[pregnancies, glucose, blood_pressure, skin_thickness,
                        insulin, bmi, diabetes_pedigree, age],
                outputs=result_output
            )

            gr.Markdown("""
            ---
            **Sample values to try:**
            - High risk: Glucose=180, BMI=35, Age=50, Pregnancies=5
            - Low risk: Glucose=90, BMI=22, Age=25, Pregnancies=0
            """)

        # ── Metrics Tab ──
        with gr.TabItem("📊 Model Metrics"):
            gr.Markdown("### Model Performance & Feature Importance")
            metrics_btn    = gr.Button("📊 Load Metrics", variant="primary")
            metrics_output = gr.Markdown()
            metrics_btn.click(fn=get_model_metrics, outputs=metrics_output)

        # ── About Tab ──
        with gr.TabItem("ℹ️ About"):
            gr.Markdown("""
            ### About This Project

            **Dataset:** Pima Indians Diabetes Dataset (768 patients)

            **Features used:**
            | Feature | Description |
            |---------|-------------|
            | Pregnancies | Number of pregnancies |
            | Glucose | Plasma glucose concentration |
            | Blood Pressure | Diastolic blood pressure |
            | Skin Thickness | Triceps skin fold thickness |
            | Insulin | 2-Hour serum insulin |
            | BMI | Body mass index |
            | Diabetes Pedigree | Diabetes pedigree function |
            | Age | Age in years |

            **Model:** Decision Tree Classifier (max_depth=5)

            **Tech Stack:** Python · Scikit-learn · FastAPI · Gradio
            """)


if __name__ == "__main__":
    demo.launch(server_port=7860, share=False)
