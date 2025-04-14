def generate_suggestion(risk_level, risk_score, glucose, bmi, blood_pressure, family_history, is_pregnant, age):
    suggestions = []
    
    # Risk level based suggestions
    risk_messages = {
        "very high": "You're at very high risk of diabetes. Please consult a doctor immediately.",
        "high": "You're at high risk of diabetes. We recommend seeing a healthcare provider soon.",
        "medium": "You have moderate risk factors for diabetes. Consider lifestyle changes.",
        "low": "Your risk is low, but maintain healthy habits to prevent future risks."
    }
    suggestions.append(risk_messages.get(risk_level, "Risk assessment completed."))
    
    # Glucose level suggestions
    if glucose >= 140:
        suggestions.append(f"Your glucose level ({glucose} mg/dL) is high. Reduce sugar intake.")
    elif glucose >= 100:
        suggestions.append(f"Your glucose level ({glucose} mg/dL) is elevated. Monitor your sugar consumption.")
    
    # BMI suggestions
    if bmi >= 30:
        suggestions.append(f"Your BMI ({bmi:.1f}) indicates obesity. Weight loss would significantly reduce your risk.")
    elif bmi >= 25:
        suggestions.append(f"Your BMI ({bmi:.1f}) indicates overweight. Maintaining a healthy weight would help.")
    elif bmi < 18.5:
        suggestions.append(f"Your BMI ({bmi:.1f}) indicates underweight. Consult a nutritionist.")
    
    # Blood pressure suggestions
    if blood_pressure >= 140:
        suggestions.append(f"Your blood pressure ({blood_pressure} mmHg) is high. Consider reducing sodium intake.")
    elif blood_pressure >= 130:
        suggestions.append(f"Your blood pressure ({blood_pressure} mmHg) is elevated. Regular monitoring is advised.")
    
    # Additional factors
    if family_history:
        suggestions.append("Since you have a family history of diabetes, regular screening is important.")
    
    if is_pregnant:
        suggestions.append("As you're pregnant, monitor for gestational diabetes with your obstetrician.")
    
    if age > 45:
        suggestions.append("People over 45 should have regular diabetes screenings.")
    
    return " ".join(suggestions)