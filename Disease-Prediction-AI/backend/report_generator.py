from fpdf import FPDF
from datetime import datetime

def generate_pdf(records):
    pdf = FPDF()
    
    for record in records:
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        
        # Remove unwanted fields
        record_data = {k: v for k, v in record.items() 
                      if k not in ['_id', 'processed_input']}
        
        # Header
        pdf.cell(200, 10, txt="Diabetes Prediction Report", ln=True, align="C")
        pdf.ln(10)
        
        # Format timestamp
        if 'timestamp' in record_data:
            if isinstance(record_data['timestamp'], datetime):
                record_data['timestamp'] = record_data['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
        
        # Add data
        for key, value in record_data.items():
            if key == 'prediction':
                risk = "High Risk" if value == 1 else "Low Risk"
                pdf.set_text_color(255, 0, 0) if value == 1 else pdf.set_text_color(0, 128, 0)
                pdf.cell(200, 10, txt=f"Risk Assessment: {risk}", ln=True)
                pdf.set_text_color(0, 0, 0)
            else:
                pdf.cell(200, 10, txt=f"{key.replace('_', ' ').title()}: {value}", ln=True)
        
        pdf.ln(10)
    
    # Return PDF as bytes
    return pdf.output(dest='S').encode('latin-1')