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
st.markdown("### 🧠 Analyze the medial consonant sound in each word")

st.markdown("""
Define the **consonant sound in the middle** of each of the following words.  
For each word, indicate:
- **Voicing**: voiced or voiceless  
- **Place of articulation**: e.g., alveolar, palato-alveolar, velar...  
- **Manner of articulation**: stop, nasal, fricative, affricate, etc.

The first row (*adder*) is provided as an example.
""")

name = st.text_input("Enter your name:")

# List of words (adder is the example)
words = [
    "adder", "1. father", "2. singing", "3. etching", "4. robber",
    "5. ether", "6. pleasure", "7. hopper", "8. selling", "9. sunny", "10. lodger"
]

# Answer key
answer_key = {
    "adder":   ("voiced", "alveolar", "stop"),
    "1. father":  ("voiced", "dental", "fricative"),
    "2. singing": ("voiced", "velar", "nasal (stop)"),
    "3. etching": ("voiceless", "palato-alveolar", "affricate"),
    "4. robber":  ("voiced", "bilabial", "stop"),
    "5. ether":   ("voiceless", "dental", "fricative"),
    "6. pleasure":("voiced", "palato-alveolar", "fricative"),
    "7. hopper":  ("voiceless", "bilabial", "stop"),
    "8. selling": ("voiced", "alveolar", "lateral"),
    "9. sunny":   ("voiced", "alveolar", "nasal (stop)"),
    "10. lodger":  ("voiced", "palato-alveolar", "affricate"),
}
# Dropdown options
voicing_options = ["voiced", "voiceless"]
place_options = [
    "bilabial", "labiodental", "dental", "alveolar", "palato-alveolar",
    "palatal", "velar", "glottal"
]
manner_options = [
    "stop", "nasal (stop)", "fricative", "affricate", "lateral", "approximant"
]

# ---------------- UI table (selectboxes) ----------------
st.markdown("### 📝 Fill out the table:")

data = []  # (word, voicing, place, manner)

for word in words:
    col1, col2, col3, col4 = st.columns([1.2, 2, 2, 2])
    with col1:
        st.markdown(f"**{word}**")
    if word == "adder":
        # Pre-filled & locked example
        with col2: st.selectbox("Voicing", voicing_options, index=0, disabled=True, key=f"{word}_v")
        with col3: st.selectbox("Place", place_options, index=3, disabled=True, key=f"{word}_p")
        with col4: st.selectbox("Manner", manner_options, index=0, disabled=True, key=f"{word}_m")
        data.append((word, "voiced", "alveolar", "stop"))
    else:
        with col2:
            v = st.selectbox("", voicing_options, key=f"{word}_v")
        with col3:
            p = st.selectbox("", place_options, key=f"{word}_p")
        with col4:
            m = st.selectbox("", manner_options, key=f"{word}_m")
        data.append((word, v, p, m))

# -------- Feedback (optional on-page) -------
if st.button("🔍 Check My Work"):
    st.session_state.f_results = []
    for (w, v, p, m) in data:
        correct = answer_key[w]
        st.session_state.f_results.append("✅" if (v, p, m) == correct else "❌")

if "f_results" in st.session_state:
    st.markdown("### ✅ Feedback")
    for i, (w, _, _, _) in enumerate(data):
        res = st.session_state.f_results[i]
        st.markdown(f"**{i+1}. {w}** — {res} {'Correct' if res=='✅' else 'Needs revision'}")

# ---------------- PDF generation with black cells for incorrect answers ----------------
def generate_pdf(name, table_data):
    """
    Build a PDF. Any cell (Voicing/Place/Manner) that is incorrect is shaded BLACK with WHITE text.
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    elements.append(Paragraph("<b>Chapter 1 – Exercise F Report</b>", styles["Title"]))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"Name: {name}", styles["Normal"]))
    elements.append(Paragraph(f"Timestamp: {timestamp}", styles["Normal"]))
    elements.append(Spacer(1, 12))

    # Build table rows
    header = ["Word", "Voicing", "Place", "Manner"]
    rows = [header] + [[w, v, p, m] for (w, v, p, m) in table_data]

    tbl = Table(rows, repeatRows=1)
    style_cmds = [
        ('BACKGROUND', (0,0), (-1,0), colors.lightblue),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('TEXTCOLOR', (0,0), (-1,-1), colors.black),
    ]

    # Shade incorrect cells (columns 1..3 for each data row)
    # Table coordinates: (col, row); header row is row 0, so data rows start at row 1.
    for idx, (w, v, p, m) in enumerate(table_data, start=1):
        cv, cp, cm = answer_key[w]
        # Compare and shade if incorrect
        if v != cv:
            style_cmds += [
                ('BACKGROUND', (1, idx), (1, idx), colors.black),
                ('TEXTCOLOR',  (1, idx), (1, idx), colors.white),
            ]
        if p != cp:
            style_cmds += [
                ('BACKGROUND', (2, idx), (2, idx), colors.black),
                ('TEXTCOLOR',  (2, idx), (2, idx), colors.white),
            ]
        if m != cm:
            style_cmds += [
                ('BACKGROUND', (3, idx), (3, idx), colors.black),
                ('TEXTCOLOR',  (3, idx), (3, idx), colors.white),
            ]

    tbl.setStyle(TableStyle(style_cmds))
    elements.append(tbl)
    doc.build(elements)
    buffer.seek(0)
    return buffer

# --------- Download PDF UI ----------
st.markdown("---")
st.subheader("📄 Export Your Report")

if not name:
    st.warning("Please enter your name to enable PDF download.")
    st.button("📄 Download My Report", disabled=True)
else:
    if st.button("📄 Download My Report"):
        pdf_bytes = generate_pdf(name, data)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        filename = f"ExerciseF_Report_{name.replace(' ', '_')}_{timestamp}.pdf"
        st.download_button("⬇️ Download PDF", data=pdf_bytes, file_name=filename, mime="application/pdf")
