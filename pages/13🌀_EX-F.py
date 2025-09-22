import streamlit as st
import pandas as pd
from datetime import datetime
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

st.set_page_config(page_title="Ch1 Exercise F: Medial Consonant Analysis", layout="wide")

st.title("Chapter 1 – Exercise F")
st.markdown("### Analyze the medial consonant sound in each word")

st.markdown("""
Define the **consonant sound in the middle** of each of the following words.  
For each word, indicate:
- **Voicing**: voiced or voiceless  
- **Place of articulation**: e.g., alveolar, palatal, velar...  
- **Manner of articulation**: stop, nasal, fricative, etc.

The first row (*adder*) is provided as an example.
""")

name = st.text_input("Enter your name:")

# List of words (adder is the example)
words = [
    "adder", "father", "singing", "etching", "robber",
    "ether", "pleasure", "hopper", "selling", "sunny", "lodger"
]

# Answer key
answer_key = {
    "adder":   ("voiced", "alveolar", "stop"),
    "father":  ("voiced", "dental", "fricative"),
    "singing": ("voiced", "velar", "nasal"),
    "etching": ("voiceless", "palato-alveolar", "affricate"),
    "robber":  ("voiced", "bilabial", "stop"),
    "ether":   ("voiceless", "dental", "fricative"),
    "pleasure":("voiced", "palato-alveolar", "fricative"),
    "hopper":  ("voiceless", "bilabial", "stop"),
    "selling": ("voiced", "alveolar", "lateral"),
    "sunny":   ("voiced", "alveolar", "nasal"),
    "lodger":  ("voiced", "palato-alveolar", "affricate"),
}

# Dropdown options
voicing_options = ["voiced", "voiceless"]
place_options = [
    "bilabial", "labiodental", "dental", "alveolar", "palato-alveolar",
    "palatal", "velar", "glottal"
]
manner_options = [
    "stop", "nasal", "fricative", "affricate", "lateral", "approximant"
]

# Table input
st.markdown("### 📝 Fill out the table for the middle sound:")

data = []

for i, word in enumerate(words):
    col1, col2, col3, col4 = st.columns([1, 2, 2, 2])
    with col1:
        st.markdown(f"**{word}**")
    if word == "adder":
        # Pre-filled and locked example
        with col2: st.selectbox("Voicing", voicing_options, index=0, disabled=True, key=f"{word}_v")
        with col3: st.selectbox("Place", place_options, index=3, disabled=True, key=f"{word}_p")
        with col4: st.selectbox("Manner", manner_options, index=0, disabled=True, key=f"{word}_m")
        data.append((word, "voiced", "alveolar", "stop"))
    else:
        with col2:
            voicing = st.selectbox("", voicing_options, key=f"{word}_v")
        with col3:
            place = st.selectbox("", place_options, key=f"{word}_p")
        with col4:
            manner = st.selectbox("", manner_options, key=f"{word}_m")
        data.append((word, voicing, place, manner))

# Feedback check
if st.button("🔍 Check My Work"):
    st.markdown("### ✅ Feedback")
    results = []
    for word, voicing, place, manner in data:
        correct = answer_key.get(word)
        if not correct:
            results.append("✅")  # for adder example
        elif (voicing, place, manner) == correct:
            results.append("✅")
        else:
            results.append("❌")
    for i, (word, _, _, _) in enumerate(data):
        result = results[i]
        feedback = "Correct" if result == "✅" else "Needs revision"
        st.markdown(f"**{i+1}. {word}** — {result} {feedback}")
else:
    results = None

# PDF report generation
def generate_pdf(name, table_data, results=None):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    elements.append(Paragraph("<b>Chapter 1 – Exercise F Report</b>", styles['Title']))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"Name: {name}", styles['Normal']))
    elements.append(Paragraph(f"Timestamp: {timestamp}", styles['Normal']))
    elements.append(Spacer(1, 12))

    # Table content
    header = ["Word", "Voicing", "Place", "Manner"]
    if results:
        header.append("Result")
        rows = [header] + [
            [w, v, p, m, results[i]] for i, (w, v, p, m) in enumerate(table_data)
        ]
    else:
        rows = [header] + [
            [w, v, p, m] for (w, v, p, m) in table_data
        ]

    table = Table(rows, repeatRows=1)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.lightblue),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold')
    ]))

    elements.append(table)
    doc.build(elements)
    buffer.seek(0)
    return buffer

# PDF download
st.markdown("---")
st.subheader("📄 Export Your Report")

if not name:
    st.warning("Please enter your name to enable PDF download.")
    st.button("📄 Download My Report", disabled=True)
else:
    if st.button("📄 Download My Report"):
        pdf_bytes = generate_pdf(name, data, results)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        filename = f"ExerciseF_Report_{name.replace(' ', '_')}_{timestamp}.pdf"
        st.download_button("⬇️ Download PDF", data=pdf_bytes, file_name=filename, mime="application/pdf")
