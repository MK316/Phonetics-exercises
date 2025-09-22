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

st.markdown("Read each question carefully and check **all words that match the description**. Try saying the words out loud to identify the initial, medial, or final sound.")

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

# Session state for answers and feedback
if "answers" not in st.session_state:
    st.session_state.answers = [[] for _ in range(len(questions))]
if "checked" not in st.session_state:
    st.session_state.checked = False
if "results" not in st.session_state:
    st.session_state.results = []

# UI for checkboxes
st.subheader("📝 Questions")
for i, (question_text, word_list) in enumerate(zip(questions, options)):
    st.markdown(f"**{i+1}. {question_text[0]}**")
    selected_words = []
    cols = st.columns(len(word_list))
    for j, word in enumerate(word_list):
        with cols[j]:
            if st.checkbox(word, key=f"q{i}_word{j}"):
                selected_words.append(word)
    st.session_state.answers[i] = selected_words

# Answer checking
if st.button("🔍 Check Answers"):
    st.session_state.checked = True
    st.session_state.results = []
    for i, (question, correct) in enumerate(questions):
        selected_set = set(st.session_state.answers[i])
        correct_set = set(correct)
        st.session_state.results.append("✅" if selected_set == correct_set else "❌")

# Display results
if st.session_state.checked:
    st.subheader("✅ Feedback")
    for i, result in enumerate(st.session_state.results):
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

    for i, (question, selected) in enumerate(zip(questions, st.session_state.answers)):
        qtext = f"{i+1}. {question[0]}"
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

# Download PDF
if name and st.button("📄 Download My Report"):
    pdf_bytes = generate_pdf(name, st.session_state.answers, st.session_state.results if st.session_state.checked else None)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    filename = f"ExerciseE_Report_{name.replace(' ', '_')}_{timestamp}.pdf"
    st.download_button("⬇️ Download PDF", data=pdf_bytes, file_name=filename, mime="application/pdf")
