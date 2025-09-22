import streamlit as st
import pandas as pd
from datetime import datetime
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet

st.set_page_config(page_title="Ch1 Exercise C: Describe Consonants", layout="wide")

st.title("Chapter 1 – Exercise C")
st.markdown("### 🧩 Describe the consonants in the word **skinflint**")

st.markdown("""
Fill in the five columns for each consonant in the word **skinflint**, using the following labels:

1. **Voiced or voiceless** (e.g., voiced, voiceless)  
2. **Place of articulation** (e.g., alveolar, velar)  
3. **Central or lateral** – use parentheses if optional  
4. **Oral or nasal** – use parentheses if optional  
5. **Articulatory action** (e.g., stop, nasal, fricative, liquid)

✏️ You may wrap items in **parentheses** if you think they may be optional.
""")

name = st.text_input("Enter your name:")

# Fixed input structure
default_data = [
    {"Symbol": "[s]", "1. Voicing": "", "2. Place": "", "3. Centrality": "", "4. Oral or nasal": "", "5. Manner": ""},
    {"Symbol": "[k]", "1. Voicing": "", "2. Place": "", "3. Centrality": "", "4. Oral or nasal": "", "5. Manner": ""},
    {"Symbol": "[n]", "1. Voicing": "", "2. Place": "", "3. Centrality": "", "4. Oral or nasal": "", "5. Manner": ""},
    {"Symbol": "[f]", "1. Voicing": "", "2. Place": "", "3. Centrality": "", "4. Oral or nasal": "", "5. Manner": ""},
    {"Symbol": "[l]", "1. Voicing": "", "2. Place": "", "3. Centrality": "", "4. Oral or nasal": "", "5. Manner": ""},
    {"Symbol": "[n]", "1. Voicing": "", "2. Place": "", "3. Centrality": "", "4. Oral or nasal": "", "5. Manner": ""},
    {"Symbol": "[t]", "1. Voicing": "", "2. Place": "", "3. Centrality": "", "4. Oral or nasal": "", "5. Manner": ""},
]

df = pd.DataFrame(default_data)

# Scrollable table using fixed width and height
with st.container():
    st.markdown("### ✏️ Fill in the chart below:")
    edited_df = st.data_editor(
        df,
        use_container_width=False,
        hide_index=True,
        key="table_input",
        height=380,  # Enables vertical scroll
    )
    # st.caption("↔️ Scroll right for more columns. 🖱 Scroll down for more rows.")

# Hidden answer key
answer_key = [
    {"1": "voiceless", "2": "alveolar", "3": "(central)", "4": "(oral)", "5": "fricative"},
    {"1": "voiceless", "2": "velar", "3": "(central)", "4": "(oral)", "5": "stop"},
    {"1": "voiced", "2": "alveolar", "3": "(central)", "4": "nasal", "5": "nasal"},
    {"1": "voiceless", "2": "labiodental", "3": "(central)", "4": "(oral)", "5": "fricative"},
    {"1": "voiced", "2": "alveolar", "3": "lateral", "4": "(oral)", "5": "liquid"},
    {"1": "voiced", "2": "alveolar", "3": "(central)", "4": "nasal", "5": "nasal"},
    {"1": "voiceless", "2": "alveolar", "3": "(central)", "4": "(oral)", "5": "stop"},
]

def normalize(text):
    """Clean and normalize student input for comparison."""
    return text.lower().replace("(", "").replace(")", "").replace(" ", "").strip()

def check_all_columns(student_df, key):
    check_results = []
    for i, row in student_df.iterrows():
        correct_row = answer_key[i]
        mismatch = False
        for col_idx, col_label in enumerate([
            "1. Voiced or voiceless",
            "2. Place",
            "3. Central or lateral",
            "4. Oral or nasal",
            "5. Articulatory action"
        ], start=1):
            student_val = normalize(row[col_label])
            correct_val = normalize(correct_row[str(col_idx)])
            if student_val != correct_val:
                mismatch = True
                break
        check_results.append("✅" if not mismatch else "❌")
    return check_results

if st.button("🔍 Check My Work"):
    results = check_all_columns(edited_df, answer_key)
    edited_df["Check"] = results
    st.success("Checked! See ❌ for rows to revise.")
    st.dataframe(edited_df, use_container_width=True)

# PDF generation
def generate_pdf(name, table_data):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    elements.append(Paragraph(f"<b>Chapter 1 – Exercise C Report</b>", styles['Title']))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"Name: {name}", styles['Normal']))
    elements.append(Paragraph(f"Timestamp: {timestamp}", styles['Normal']))
    elements.append(Spacer(1, 12))

    if "Check" in table_data.columns:
        table_data = table_data.drop(columns=["Check"])
    data = [list(table_data.columns)] + table_data.values.tolist()

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
    filename = f"skinflint_exerciseC_{name.replace(' ', '_')}_{timestamp}.pdf"
    st.success("✅ PDF generated successfully!")
    st.download_button("⬇️ Download PDF", data=pdf_bytes, file_name=filename, mime="application/pdf")
