import streamlit as st
from datetime import datetime
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

st.set_page_config(page_title="Ch1 Exercise K: Distinct Sounds", layout="centered")

st.title("Chapter 1 – Exercise K")
st.markdown("### 🔊 Count the Distinct Sounds")

st.markdown("""
How many **distinct sounds** (phonemes) are in each of the following words?  
Select the correct number (1–7) for each word.
""")

name = st.text_input("Enter your name:")

# Words and answer key
words = [
    "1. laugh", "2. begged", "3. graphic", "4. fish",
    "5. fishes", "6. fished", "7. batting", "8. quick",
    "9. these", "10. physics", "11. knock", "12. axis"
]

answer_key = {
    "1. laugh": 3, "2. begged": 4, "3. graphic": 6, "4. fish": 3,
    "5. fishes": 5, "6. fished": 4, "7. batting": 5, "8. quick": 4,
    "9. these": 3, "10. physics": 6, "11. knock": 3, "12. axis": 5
}

options = list(range(1, 8))  # 1–7 choices

# --- PDF generator ---
def generate_pdf(name, responses, results=None):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    elements.append(Paragraph("<b>Chapter 1 – Exercise K Report</b>", styles["Title"]))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"Name: {name}", styles["Normal"]))
    elements.append(Paragraph(f"Timestamp: {timestamp}", styles["Normal"]))
    elements.append(Spacer(1, 12))

    # Table rows
    header = ["Word", "Selected", "Result"]
    rows = [header]
    for w in words:
        selected = responses.get(w, "-")
        correct = answer_key[w]
        result_text = "Correct" if selected == correct else "Incorrect"
        rows.append([w, selected, result_text])

    tbl = Table(rows, repeatRows=1)
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightblue),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
    ]

    # Shade wrong answers
    for i, w in enumerate(words, start=1):
        if responses.get(w) != answer_key[w]:
            style_cmds += [
                ("BACKGROUND", (1, i), (1, i), colors.black),
                ("TEXTCOLOR", (1, i), (1, i), colors.white),
            ]

    tbl.setStyle(TableStyle(style_cmds))
    elements.append(tbl)
    doc.build(elements)
    buffer.seek(0)
    return buffer

# --- Collect responses ---
responses = {}
for word in words:
    responses[word] = st.radio(word, options, horizontal=True, key=f"radio_{word}")

# --- Check answers button ---
if st.button("🔍 Check My Work", key="check_button"):
    st.session_state.k_results = []
    for w in words:
        if responses[w] == answer_key[w]:
            st.session_state.k_results.append("✅")
        else:
            st.session_state.k_results.append("❌")

    # Reset radios immediately after checking
    for w in words:
        if f"radio_{w}" in st.session_state:
            del st.session_state[f"radio_{w}"]
    st.rerun()

# --- Show feedback ---
if "k_results" in st.session_state:
    st.markdown("### ✅ Feedback")
    for i, w in enumerate(words):
        res = st.session_state.k_results[i]
        fb = "Correct" if res == "✅" else "Incorrect"
        st.markdown(f"{w} — {fb}")

# --- PDF Export ---
st.markdown("---")
st.subheader("📄 Export Your Report")

if not name:
    st.warning("Please enter your name to enable PDF download.")
else:
    pdf_bytes = generate_pdf(name, responses, st.session_state.k_results if "k_results" in st.session_state else None)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    filename = f"ExerciseK_Report_{name.replace(' ', '_')}_{timestamp}.pdf"
    st.download_button("⬇️ Download PDF", data=pdf_bytes, file_name=filename, mime="application/pdf")
