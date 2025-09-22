import streamlit as st
from datetime import datetime
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

st.set_page_config(page_title="Ch1 Exercise E: Phonetic Word Features", layout="wide")

st.title("Chapter 1 – Exercise E")
st.markdown("### 🎯 Phonetic Identification Task")

st.markdown("Read each question carefully and select **all words that match the description**. Try to say them aloud and focus on their **initial, medial, or final sounds** depending on the prompt.")

name = st.text_input("Enter your name:")

# -- Define Questions and Answer Keys
questions = [
    ("Circle the words that begin with a bilabial consonant.", ["met", "bet", "pet"]),
    ("Circle the words that begin with a velar consonant.", ["got"]),
    ("Circle the words that begin with a labiodental consonant.", ["fat", "vat"]),
    ("Circle the words that begin with an alveolar consonant.", ["zip", "nip", "lip", "sip", "tip", "dip"]),
    ("Circle the words that begin with a dental consonant.", ["thigh", "thy"]),
    ("Circle the words that begin with a palato-alveolar consonant.", ["shy"]),
    ("Circle the words that end with a fricative.", ["race", "wreath", "breathe"]),
    ("Circle the words that end with a nasal.", ["rain", "rang"]),
    ("Circle the words that end with a stop.", ["pill", "lip", "graph", "crab", "back"]),
    ("Circle the words that begin with a lateral.", ["lull"]),
    ("Circle the words that begin with an approximant.", ["we", "you", "run"]),
    ("Circle the words that end with an affricate.", ["much"]),
    ("Circle the words in which the consonant in the middle is voiced.", ["mother", "robber", "leisure", "massive", "razor"]),
    ("Circle the words that contain a high vowel.", ["suit", "meet"]),
    ("Circle the words that contain a low vowel.", ["lad"]),
    ("Circle the words that contain a front vowel.", ["gate"]),
    ("Circle the words that contain a back vowel.", ["coop", "good"]),
    ("Circle the words that contain a rounded vowel.", ["who", "but"])
]

options = [
    ["met", "net", "set", "bet", "let", "pet"],
    ["knot", "got", "lot", "cot", "hot", "pot"],
    ["fat", "cat", "mat", "chat", "vat"],
    ["zip", "nip", "lip", "sip", "tip", "dip"],
    ["pie", "guy", "shy", "thigh", "thy", "high"],
    ["sigh", "shy", "tie", "thigh", "thy", "lie"],
    ["race", "wreath", "bush", "bring", "breathe", "bang", "rave", "real", "ray", "rose", "rough"],
    ["rain", "rang", "dumb", "deaf"],
    ["pill", "lip", "graph", "crab", "dog", "hide", "laugh", "back"],
    ["nut", "lull", "bar", "rob", "one"],
    ["we", "you", "one", "run"],
    ["much", "back", "edge", "ooze"],
    ["tracking", "mother", "robber", "leisure", "massive", "stomach", "razor"],
    ["sat", "suit", "got", "meet", "mud"],
    ["weed", "wad", "load", "lad", "rude"],
    ["gate", "caught", "cat", "kit", "put"],
    ["maid", "weep", "coop", "cop", "good"],
    ["who", "me", "us", "but", "him"]
]

# Store selections
responses = []
check_results = []
feedback_mode = False

if "check_pressed" not in st.session_state:
    st.session_state.check_pressed = False

st.markdown("___")
st.subheader("📝 Questions")

for i, (question, correct_answers) in enumerate(questions):
    st.markdown(f"**{i+1}. {question}**")
    selected = st.multiselect("", options[i], key=f"q{i+1}")
    responses.append((question, selected))

if st.button("🔍 Check Answers"):
    st.session_state.check_pressed = True

# Checking logic
if st.session_state.check_pressed:
    st.subheader("✅ Feedback")
    for i, (question, selected) in enumerate(responses):
        correct_set = set(questions[i][1])
        selected_set = set(selected)
        if selected_set == correct_set:
            result = "✅"
        else:
            result = "❌"
        check_results.append(result)
        st.markdown(f"**{i+1}. {result}** — {'Correct' if result == '✅' else 'Needs review'}")

# PDF generation
def generate_pdf(name, responses, results=None):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    elements.append(Paragraph(f"<b>Chapter 1 – Exercise E Report</b>", styles['Title']))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"Name: {name}", styles['Normal']))
    elements.append(Paragraph(f"Timestamp: {timestamp}", styles['Normal']))
    elements.append(Spacer(1, 12))

    for i, (question, selected) in enumerate(responses):
        qtext = f"{i+1}. {question}"
        selected_text = ", ".join(selected) if selected else "(No selection)"
        feedback = f"Result: {results[i]}" if results else ""
        elements.append(Paragraph(qtext, styles['Normal']))
        elements.append(Paragraph(f"Selected: {selected_text}", styles['Normal']))
        if feedback:
            elements.append(Paragraph(feedback, styles['Normal']))
        elements.append(Spacer(1, 6))

    doc.build(elements)
    buffer.seek(0)
    return buffer

if name and st.button("📄 Download My Report"):
    pdf_bytes = generate_pdf(name, responses, check_results if st.session_state.check_pressed else None)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    filename = f"ExerciseE_Report_{name.replace(' ', '_')}_{timestamp}.pdf"
    st.download_button("⬇️ Download PDF", data=pdf_bytes, file_name=filename, mime="application/pdf")
