import streamlit as st
from datetime import datetime
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

st.set_page_config(page_title="Ch1 Exercise D: Places of Articulation", layout="centered")

st.title("Chapter 1 – Exercise D")
st.markdown("### 🗣️ Identify Place, Manner, and an Example Word")

st.markdown("""
For each diagram (**a–g**), fill in:
1) **Place of articulation**  
2) **Manner of articulation**  
3) **An English word beginning with the sound**  
""")

name = st.text_input("Enter your name: (In English)")


# URLs of diagrams hosted on GitHub (replace with your actual GitHub raw links)
image_urls = {
    "a": "https://github.com/MK316/Phonetics-exercises/raw/main/pages/images/fig-16-a.png",
    "b": "https://github.com/MK316/Phonetics-exercises/raw/main/pages/images/fig-16-b.png",
    "c": "https://github.com/MK316/Phonetics-exercises/raw/main/pages/images/fig-16-c.png",
    "d": "https://github.com/MK316/Phonetics-exercises/raw/main/pages/images/fig-16-d.png",
    "e": "https://github.com/MK316/Phonetics-exercises/raw/main/pages/images/fig-16-e.png",
    "f": "https://github.com/MK316/Phonetics-exercises/raw/main/pages/images/fig-16-f.png",
    "g": "https://github.com/MK316/Phonetics-exercises/raw/main/pages/images/fig-16-g.png"
}

letters = list(image_urls.keys())

# --- Session state ---
if "responses_D" not in st.session_state:
    st.session_state.responses_D = {k: {"place": "", "manner": "", "example": ""} for k in letters}
if "d_index" not in st.session_state:
    st.session_state.d_index = 0

# --- Navigation ---
colA, colC = st.columns([1,1])
with colA:
    if st.button("⬅️ Previous", use_container_width=True, disabled=st.session_state.d_index == 0):
        st.session_state.d_index = max(0, st.session_state.d_index - 1)
with colC:
    if st.button("Next ➡️", use_container_width=True, disabled=st.session_state.d_index == len(letters) - 1):
        st.session_state.d_index = min(len(letters) - 1, st.session_state.d_index + 1)

letter = letters[st.session_state.d_index]
st.markdown(f"#### Diagram ({letter})")
st.image(image_urls[letter], caption=f"Figure 1.16 ({letter})", width=360)

# --- Inputs for this diagram ---
st.session_state.responses_D[letter]["place"] = st.text_input(
    "Place of articulation",
    value=st.session_state.responses_D[letter]["place"],
    key=f"place_{letter}",
)
st.session_state.responses_D[letter]["manner"] = st.text_input(
    "Manner of articulation",
    value=st.session_state.responses_D[letter]["manner"],
    key=f"manner_{letter}",
)
st.session_state.responses_D[letter]["example"] = st.text_input(
    "Example word (begins with this sound)",
    value=st.session_state.responses_D[letter]["example"],
    key=f"example_{letter}",
)

st.markdown("---")
st.subheader("Summary (auto-saves)")
summary_rows = [["Diagram", "Place", "Manner", "Example"]]
for k in letters:
    a = st.session_state.responses_D[k]
    summary_rows.append([k, a["place"], a["manner"], a["example"]])

st.table(summary_rows)

# --- PDF generator ---
def generate_pdf(name: str, responses: dict) -> bytes:
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    elements.append(Paragraph("<b>Chapter 1 – Exercise D Report</b>", styles["Title"]))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"Name: {name}", styles["Normal"]))
    elements.append(Paragraph(f"Timestamp: {timestamp}", styles["Normal"]))
    elements.append(Spacer(1, 12))

    table_header = ["Diagram", "Place of Articulation", "Manner of Articulation", "Example Word"]
    table_data = [table_header]
    for k in letters:
        ans = responses.get(k, {"place": "", "manner": "", "example": ""})
        table_data.append([k, ans["place"], ans["manner"], ans["example"]])

    tbl = Table(table_data, repeatRows=1)
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightblue),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
    ]))
    elements.append(tbl)

    doc.build(elements)
    buffer.seek(0)
    return buffer.getvalue()

# --- PDF Export ---
st.markdown("---")
st.subheader("📄 Export Your Report")

if not name:
    st.warning("Please enter your name to enable PDF download.")
else:
    pdf_bytes = generate_pdf(name, st.session_state.responses_D)
    ts = datetime.now().strftime("%Y%m%d_%H%M")
    filename = f"ExerciseD_Report_{name.replace(' ', '_')}_{ts}.pdf"

    if st.download_button("⬇️ Download PDF", data=pdf_bytes, file_name=filename, mime="application/pdf"):
        # Reset after download
        for k in letters:
            st.session_state.responses_D[k] = {"place": "", "manner": "", "example": ""}
        st.session_state.d_index = 0
        st.success("Report downloaded. The exercise has been reset.")
        st.rerun()
