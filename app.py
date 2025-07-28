import streamlit as st
import fitz  # pymupdf
import os
import tempfile
import pyttsx3
import json
import networkx as nx
import threading
from vosk import Model, KaldiRecognizer
import pyaudio
import time
import base64
import matplotlib.pyplot as plt
from sentence_transformers import SentenceTransformer, util

# Session state for dialog visibility
if "show_dialog" not in st.session_state:
    st.session_state.show_dialog = False
if "dialog_text" not in st.session_state:
    st.session_state.dialog_text = ""

st.set_page_config(layout="wide")
st.title("📄 Voice-Based PDF Assistant (Offline)")

# === Text-to-Speech (TTS) ===
engine = pyttsx3.init()
engine.setProperty('rate', 160)

def speak(text):
    def _speak():
        engine.say(text)
        engine.runAndWait()
    threading.Thread(target=_speak).start()

# === Voice Recognition Setup ===
model_path = "vosk-model-small-en-us-0.15"
if not os.path.exists(model_path):
    st.error("❌ Vosk model not found. Please download and unzip into project dir.")
    st.stop()
model = Model(model_path)

def listen_for_command():
    rec = KaldiRecognizer(model, 16000)
    mic = pyaudio.PyAudio()
    stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
    stream.start_stream()
    st.session_state['voice_command'] = None
    st.session_state['listening'] = True
    st.info("🎧 Voice input active. Say something (say 'stop' to end)...")
    while st.session_state['listening']:
        data = stream.read(4096, exception_on_overflow=False)
        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            command = result.get("text", "")
            if "stop" in command:
                st.session_state['listening'] = False
                break
            elif command.strip() != "":
                st.session_state['voice_command'] = command
                break
    stream.stop_stream()
    stream.close()
    mic.terminate()

# === PDF Utility Functions ===
def extract_text(pdf_path):
    doc = fitz.open(pdf_path)
    paragraphs = []
    for page in doc:
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if "lines" in block:
                block_text = ""
                for line in block["lines"]:
                    for span in line["spans"]:
                        block_text += span["text"] + " "
                block_text = block_text.strip()
                if len(block_text) > 40:
                    paragraphs.append(block_text)
    return paragraphs

def extract_headings(pdf_path):
    doc = fitz.open(pdf_path)
    headings = set()
    for page in doc:
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        text = span["text"].strip()
                        size = span["size"]
                        if text and size > 14 and len(text.split()) <= 10:
                            headings.add(text)
    mindmap = {"Root": [{head: []} for head in sorted(headings)]}
    return mindmap

def visualize_mindmap(mindmap):
    G = nx.DiGraph()
    G.add_node("Root")
    for section in mindmap["Root"]:
        for main, subs in section.items():
            G.add_edge("Root", main)
            for sub in subs:
                G.add_edge(main, sub)
    fig, ax = plt.subplots(figsize=(10, 6))
    pos = nx.spring_layout(G, k=0.5, iterations=50)
    nx.draw(G, pos, with_labels=True, node_size=2000, node_color="skyblue", font_size=10, ax=ax)
    return fig

def show_pdf(file_path):
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode("utf-8")
    st.markdown(f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="800px" type="application/pdf"></iframe>', unsafe_allow_html=True)

def translucent_dialog(text):
    st.session_state.dialog_text = text
    st.session_state.show_dialog = True

def clear_dialog_state():
    st.session_state.show_dialog = False
    st.session_state.dialog_text = ""
    st.session_state.voice_command = None
    st.session_state.last_input = None

def show_action_buttons():
    st.markdown("#### 🔁 Continue Exploring")
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("🔙 Extract Paragraph"):
            translucent_dialog("Which paragraph? (e.g., 1st, 2nd)")
            speak("Which paragraph?")
    with c2:
        if st.button("📚 Extract All Headings"):
            headings_dict = extract_headings(st.session_state['pdf_path'])
            result_lines = [f"🔹 {main}" for section in headings_dict["Root"] for main in section]
            result_text = "\n".join(result_lines) or "No headings found."
            translucent_dialog(result_text)
            speak(result_text)
    with c3:
        if st.button("🧠 Make Mind Map"):
            fig = visualize_mindmap(extract_headings(st.session_state['pdf_path']))
            st.pyplot(fig)
            speak("Here's your mind map.")

# === Main ===
if 'pdf_uploaded' not in st.session_state:
    st.session_state['pdf_uploaded'] = False

uploaded = st.file_uploader("📄 Upload a PDF", type="pdf")
if uploaded and not st.session_state['pdf_uploaded']:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded.read())
        st.session_state['pdf_path'] = tmp_file.name
    st.session_state['pdf_uploaded'] = True
    st.session_state['text_pages'] = extract_text(st.session_state['pdf_path'])
    st.success("PDF uploaded. Click below to view.")

if st.session_state['pdf_uploaded']:
    if st.button("📂 Open PDF"):
        st.session_state['show_pdf'] = True
    if st.session_state.get('show_pdf', False):
        show_pdf(st.session_state['pdf_path'])
    show_action_buttons()

    user_input = st.text_input("💬 Type your query")
    if st.button("Submit Text"):
        st.session_state['last_input'] = user_input.lower()
    if st.button("🎧 Start Voice"):
        threading.Thread(target=listen_for_command).start()

    query = st.session_state.get('voice_command') or st.session_state.get('last_input')

    if query:
        pages = st.session_state['text_pages']
        model = SentenceTransformer('all-MiniLM-L6-v2')
        para_scores = [(util.cos_sim(model.encode([query])[0], model.encode([para])[0]).item(), idx, para.strip())
                       for idx, para in enumerate(pages) if len(para) > 20]
        para_scores.sort(reverse=True)
        top_score, top_idx, top_match = para_scores[0]
        translucent_dialog(top_match)
        speak(top_match)

if st.session_state.show_dialog:
    st.markdown("""
        <style>
        .glass-box {
            position: fixed;
            bottom: 60px;
            left: 50%;
            transform: translateX(-50%);
            background: rgba(30, 30, 30, 0.92);
            color: #00FFD1;
            font-size: 18px;
            line-height: 1.6;
            padding: 25px 30px 20px 30px;
            border-radius: 20px;
            backdrop-filter: blur(14px);
            z-index: 99999;
            max-width: 80%;
            text-align: left;
            box-shadow: 0 0 15px rgba(0,255,255,0.6);
            font-family: 'Segoe UI', sans-serif;
            animation: slideUpFade 0.4s ease-out;
            overflow-y: auto;
            max-height: 40vh;
        }
        .close-button {
            float: right;
            font-size: 22px;
            margin-top: -10px;
            margin-right: -10px;
            background: none;
            border: none;
            color: #FF6B6B;
        }
        </style>
    """, unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="glass-box">', unsafe_allow_html=True)
        close_col, text_col = st.columns([0.05, 0.95])
        with close_col:
            if st.button("×", key="close_dialog_button_inside", help="Close", use_container_width=True):
                clear_dialog_state()
        with text_col:
            st.markdown(st.session_state.dialog_text.replace('\n', '<br>'), unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


