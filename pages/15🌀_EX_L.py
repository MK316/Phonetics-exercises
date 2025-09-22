import streamlit as st
from datetime import datetime
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

st.set_page_config(page_title="Ch1 Exercise L: Odd Vowel Sound", layout="centered")

st.title("Chapter 1 – Exercise L")
st.markdown("### 🔎 Find the Odd Vowel Sound")

st.markdown("""
In each set of words, the vowel sound is the same **except for one**.  
Circle (select) the word that has the **different vowel sound**.
""")

name = st.text_input("Enter your name:")

# --- Questions and correct answers ---
questions = {
    "1. pen / said / death / mess / mean": "mean",
    "2. meat / steak / weak / theme / green": "steak",
    "3. sane / paid / eight / lace / mast": "mast",
    "4. ton / toast / both / note / toes": "ton",
    "5. hoot / good / moon / grew / suit": "good",
    "6. dud / died / mine / eye / guy": "dud"
}

# Split options for display
options = {
    "1. pen / said / death / mess / mean": ["pen", "said", "death", "mess", "mean"],
    "2. meat / steak / weak / theme / green": ["meat", "steak", "weak", "theme", "green"],
    "3. sane / paid / eight / lace / mast": ["sane", "paid", "eight", "lace", "mast"],
    "4. ton / toast / both / note / toes": ["ton", "toast", "both", "note", "toes"],
    "5. hoot / good / moon / grew / suit": ["hoot", "good", "moon", "grew", "suit"],
    "6. dud / died / mine / eye / guy": ["dud", "died", "mine", "eye", "guy"]
}

# --- Keep responses in session ---
if "responses_L" not in st.session_state:
    st.session_state.responses_L = {}

# --- UI: one radio per question ---
for q, opts in options.items():
    st.session_state.responses_L[q] = st.radio(
        q, opts, horizontal=True,
        key=f"L_{q}",
        index=opts.index(st.session_state.responses_L.get(q, opts[0])) if q in st.session_state.responses_L else 0
    )

# --- PDF generator ---
def generate_pdf(name, responses, results):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    elements.append(Paragraph("<b>Chapter 1 – Exercise L Report</b>", styles["Title"]))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"Name: {name}", styles["Normal"]))
    elements.append(Paragraph(f"Timestamp: {timestamp}", styles["Normal"]))
    elements.append(Spacer(1, 12))

    # Build table
    header = ["Question", "Selected", "Result"]
    rows = [header]
    for i, (q, correct) in enumerate(questions.items(), start=1):
        selected = responses.get(q, "-")
        result_text = "Correct" if selected == correct else "Incorrect"
        rows.append([q, selected, result_text])

    tbl = Table(rows, repeatRows=1)
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightblue),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
    ]

    # Shade incorrect
    for i, (q, correct) in enumerate(questions.items(), start=1):
        if responses.get(q) != correct:
            style_cmds += [
                ("BACKGROUND", (1, i), (1, i), colors.black),
                ("TEXTCOLOR", (1, i), (1, i), colors.white),
            ]

    tbl.setStyle(TableStyle(style_cmds))
    elements.append(tbl)
    doc.build(elements)
    buffer.seek(0)
    return buffer


# --- Check answers ---
if st.button("🔍 Check My Work", key="check_button_L"):
    st.session_state.results_L = []
    for q, correct in questions.items():
        selected = st.session_state.responses_L[q]
        st.session_state.results_L.append("✅" if selected == correct else "❌")

    # Save snapshot for PDF
    st.session_state.saved_for_pdf_L = dict(st.session_state.responses_L)

# --- Show feedback ---
if "results_L" in st.session_state:
    st.markdown("### ✅ Feedback")
    for i, (q, correct) in enumerate(questions.items(), start=1):
        res = st.session_state.results_L[i]
        fb = "Correct" if res == "✅" else "Incorrect"
        st.markdown(f"{i}. {q} — {fb}")

# --- PDF Export ---
st.markdown("---")
st.subheader("📄 Export Your Report")

if not name:
    st.warning("Please enter your name to enable PDF download.")
else:
    if "saved_for_pdf_L" in st.session_state:
        pdf_bytes = generate_pdf(name, st.session_state.saved_for_pdf_L, st.session_state.results_L)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        filename = f"ExerciseL_Report_{name.replace(' ', '_')}_{timestamp}.pdf"

        if st.download_button("⬇️ Download PDF", data=pdf_bytes, file_name=filename, mime="application/pdf", key="download_pdf_L"):
            # Reset after download
            for q in questions.keys():
                if f"L_{q}" in st.session_state:
                    del st.session_state[f"L_{q}"]
            for key in ["results_L", "saved_for_pdf_L", "responses_L"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()
    else:
        st.info("👉 First check your work to generate a report.")
