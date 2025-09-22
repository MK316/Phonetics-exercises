import streamlit as st
import pandas as pd
from datetime import datetime
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet

st.set_page_config(page_title="Ch1 Exercise B: Consonant Description", layout="centered")

st.title("Chapter 1 - Exercise B")
st.markdown("### 🧩 Describe the consonants in the word **skinflint**")

st.markdown("""
Use the chart below. Fill in all five columns:

- **Symbol**: Use IPA symbols (e.g., [s], [k], [n], etc.)
- **Place**: Where the sound is articulated (e.g., alveolar, velar)
- **Manner**: Type of articulation (e.g., stop, nasal, fricative)
- **Voicing**: Voiced or voiceless
- **Other**: Optional (e.g., aspiration, syllabic, etc.)

Wrap terms in **parentheses** if they might be omitted (e.g., *(alveolar)*).
""")

name = st.text_input("Enter your name:")
submitted = False

# Default student input
default_data = [
    {"Symbol": "[s]", "Place": "", "Manner": "", "Voicing": "", "Other": ""},
    {"Symbol": "[k]", "Place": "", "Manner": "", "Voicing": "", "Other": ""},
    {"Symbol": "[n]", "Place": "", "Manner": "", "Voicing": "", "Other": ""},
    {"Symbol": "[f]", "Place": "", "Manner": "", "Voicing": "", "Other": ""},
    {"Symbol": "[l]", "Place": "", "Manner": "", "Voicing": "", "Other": ""},
    {"Symbol": "[n]", "Place": "", "Manner": "", "Voicing": "", "Other": ""},
    {"Symbol": "[t]", "Place": "", "Manner": "", "Voicing": "", "Other": ""},
]

df = pd.DataFrame(default_data)

edited_df = st.data_editor(df, use_container_width=True, num_rows="fixed", key="table_input")

# Hidden answer key (7 consonants)
answer_key = [
    {"Symbol": "[s]", "Place": "alveolar", "Manner": "fricative", "Voicing": "voiceless", "Other": ""},
    {"Symbol": "[k]", "Place": "velar", "Manner": "stop", "Voicing": "voiceless", "Other": ""},
    {"Symbol": "[n]", "Place": "alveolar", "Manner": "nasal", "Voicing": "voiced", "Other": ""},
    {"Symbol": "[f]", "Place": "labiodental", "Manner": "fricative", "Voicing": "voiceless", "Other": ""},
    {"Symbol": "[l]", "Place": "alveolar", "Manner": "liquid", "Voicing": "voiced", "Other": ""},
    {"Symbol": "[n]", "Place": "alveolar", "Manner": "nasal", "Voicing": "voiced", "Other": ""},
    {"Symbol": "[t]", "Place": "alveolar", "Manner": "stop", "Voicing": "voiceless", "Other": ""},
]

def normalize(text):
    """Clean up for comparison: remove spaces, parentheses, lowercase."""
    return text.lower().replace("(", "").replace(")", "").replace(" ", "").strip()

def check_answers(student_df, key):
    check_results = []
    for i, row in student_df.iterrows():
        if i >= len(key):
            check_results.append("⚠️")
            continue
        row_correct = True
        for col in ["Place", "Manner", "Voicing"]:
            student_val = normalize(row[col])
            correct_val = normalize(key[i][col])
            if student_val != correct_val:
                row_correct = False
                break
        check_results.append("✅" if row_correct else "❌")
    return check_results

if st.button("🔍 Check My Work"):
    results = check_answers(edited_df, answer_key)
    edited_df["Check"] = results
    st.success("Checked! See ❌ for items to revise.")
    st.dataframe(edited_df, use_container_width=True)

# Generate PDF of student work only
def generate_pdf(name, table_data):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    elements.append(Paragraph(f"<b>Chapter 1 – Exercise B Report</b>", styles['Title']))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"Name: {name}", styles['Normal']))
    elements.append(Paragraph(f"Timestamp: {timestamp}", styles['Normal']))
    elements.append(Spacer(1, 12))

    # Remove 'Check' column if present
    display_df = table_data.drop(columns=["Check"]) if "Check" in table_data.columns else table_data
    data = [list(display_df.columns)] + display_df.values.tolist()

    table = Table(data, repeatRows=1)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.lightblue),
        ('TEXTCOLOR', (0,0), (-1,0), colors.black),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ]))
    elements.append(table)
    doc.build(elements)
    buffer.seek(0)
    return buffer

if name and st.button("📄 Generate PDF Report"):
    pdf_bytes = generate_pdf(name, edited_df)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    filename = f"skinflint_exercise_{name.replace(' ', '_')}_{timestamp}.pdf"
    st.success("✅ PDF generated successfully!")
    st.download_button("⬇️ Download PDF", data=pdf_bytes, file_name=filename, mime="application/pdf")
