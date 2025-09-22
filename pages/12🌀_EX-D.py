import streamlit as st
from datetime import datetime
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

st.set_page_config(page_title="Ch1 Exercise D: Places of Articulation", layout="centered")

st.title("Chapter 1 – Exercise D")
st.markdown("### 🗣️ Identify Place, Manner, and Example Word")

st.markdown("""
Look at each diagram (**a–g**).  
For each, fill in:
1. **Place of articulation**  
2. **Manner of articulation**  
3. **An English word beginning with the sound**  
""")

name = st.text_input("Enter your name:")

# URLs of diagrams hosted on GitHub (replace with your actual GitHub raw links)
image_urls = {
    "a": "https://github.com/MK316/Phonetics-exercises/blob/main/pages/images/fig-16-a.png",
    "b": "https://github.com/MK316/Phonetics-exercises/blob/main/pages/images/fig-16-a.png",
    "c": "https://github.com/MK316/Phonetics-exercises/blob/main/pages/images/fig-16-a.png",
    "d": "https://github.com/MK316/Phonetics-exercises/blob/main/pages/images/fig-16-a.png",
    "e": "https://github.com/MK316/Phonetics-exercises/blob/main/pages/images/fig-16-a.png",
    "f": "https://github.com/MK316/Phonetics-exercises/blob/main/pages/images/fig-16-a.png",
    "g": "https://github.com/MK316/Phonetics-exercises/blob/main/pages/images/fig-16-a.png",
    "h": "https://github.com/MK316/Phonetics-exercises/blob/main/pages/images/fig-16-a.png"
}

# Keep answers in session
if "responses_D" not in st.session_state:
    st.session_state.responses_D = {k: {"place": "", "manner": "", "example": ""} for k in image_urls.keys()}

# UI: show each image with inputs
for label, url in image_urls.items():
    st.markdown(f"#### ({label}) Diagram")
    st.image(url, caption=f"Figure 1.16 ({label})", width=300)

    st.session_state.responses_D[label]["place"] = st.text_input(
        f"({label}) Place of articulation",
        value=st.session_state.responses_D[label]["place"],
        key=f"place_{label}"
    )
    st.session_state.responses_D[label]["manner"] = st.text_input(
        f"({label}) Manner of articulation",
        value=st.session_state.responses_D[label]["manner"],
        key=f"manner_{label}"
    )
    st.session_state.responses_D[label]["example"] = st.text_input(
        f"({label}) Example word",
        value=st.session_state.responses_D[label]["example"],
        key=f"example_{label}"
    )

    st.markdown("---")

# --- PDF generator ---
def generate_pdf(name, responses):
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

    # Build table
    header = ["Diagram", "Place of Articulation", "Manner of Articulation", "Example Word"]
    rows = [header]
    for k, ans in responses.items():
        rows.append([k, ans["place"], ans["manner"], ans["example"]])

    tbl = Table(rows, repeatRows=1)
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightblue),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
    ]))
    elements.append(tbl)

    doc.build(elements)
    buffer.seek(0)
    return buffer


# --- PDF Export ---
st.markdown("---")
st.subheader("📄 Export Your Report")

if not name:
    st.warning("Please enter your name to enable PDF download.")
else:
    pdf_bytes = generate_pdf(name, st.session_state.responses_D)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    filename = f"ExerciseD_Report_{name.replace(' ', '_')}_{timestamp}.pdf"

    if st.download_button("⬇️ Download PDF", data=pdf_bytes, file_name=filename, mime="application/pdf", key="download_pdf_D"):
        # Reset after download
        for k in list(st.session_state.responses_D.keys()):
            for field in ["place", "manner", "example"]:
                st.session_state.responses_D[k][field] = ""
        st.rerun()
