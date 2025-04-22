import streamlit as st
from fpdf import FPDF
import base64

st.title("🏋️‍♂️ BMI Calculator with PDF Report")

# User info
username = st.text_input("Enter your name")
user_id = st.text_input("Enter your ID")

# Input: Weight in kg
weight = st.number_input("Enter your weight (kg)", min_value=1.0, step=0.1)

# Input: Height in feet and inches
st.markdown("### Enter your height")
feet = st.number_input("Feet", min_value=0, step=1)
inches = st.number_input("Inches", min_value=0, step=1)

# Convert height to meters
total_inches = (feet * 12) + inches
height_meters = total_inches * 0.0254

# BMI calculation
def calculate_bmi(weight_kg, height_m):
    if height_m <= 0:
        return None
    return round(weight_kg / (height_m ** 2), 2)

# Determine category
def get_bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 24.9:
        return "Normal weight"
    elif 25 <= bmi < 29.9:
        return "Overweight"
    else:
        return "Obese"

# Generate PDF
def generate_pdf(name, uid, w, h_ft, h_in, bmi, category):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="BMI Report", ln=True, align='C')
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Name: {name}", ln=True)
    pdf.cell(200, 10, txt=f"ID: {uid}", ln=True)
    pdf.cell(200, 10, txt=f"Weight: {w} kg", ln=True)
    pdf.cell(200, 10, txt=f"Height: {h_ft} ft {h_in} in", ln=True)
    pdf.cell(200, 10, txt=f"BMI: {bmi}", ln=True)
    pdf.cell(200, 10, txt=f"Category: {category}", ln=True)

    return pdf.output(dest="S").encode("latin1")

# Calculate and show result
if st.button("Calculate BMI"):
    bmi = calculate_bmi(weight, height_meters)

    if bmi is None:
        st.error("Invalid height input.")
    else:
        category = get_bmi_category(bmi)
        st.success(f"Your BMI is: {bmi}")
        st.info(f"Category: {category}")

        # PDF download link
        if username and user_id:
            pdf_data = generate_pdf(username, user_id, weight, feet, inches, bmi, category)
            b64 = base64.b64encode(pdf_data).decode()
            href = f'<a href="data:application/octet-stream;base64,{b64}" download="BMI_Report.pdf">📄 Download BMI Report as PDF</a>'
            st.markdown(href, unsafe_allow_html=True)
        else:
            st.warning("Please enter your name and ID to download the report.")
