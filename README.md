
# 📁 Project: Adobe Voice AI — Offline PDF Assistant 🔊📄

> A completely offline, voice-powered PDF assistant that listens, understands, and speaks back — no internet, no mouse, no keyboard. Just pure CPU magic.

---

## ⚡ Challenge: Adobe India Hackathon 2025 – Round 2, Problem 1A  
Built under strict constraints:
- 💻 **Offline-only**
- 🧠 **≤ 1GB total model size**
- 🖥️ **CPU-only execution**
- 🕒 **≤ 60 seconds per task**
- 📤 **JSON output for each query**

---

## 👾 Features
- 🎤 **Voice-activated commands** using `Vosk` STT
- 📚 **PDF Content Extraction** (headings, paragraphs)
- 🧠 **Mind Map Generator** from PDF structure
- 🗣️ **Text-to-Speech Replies** using `pyttsx3`
- 💡 **Streamlit UI** with translucent dialog overlay
- 🖱️ **Mouse-Free Navigation** — just talk to your PDF
- 📦 100% **offline**, zero external API calls

---

## 🛠️ Tech Stack

| Tool                  | Purpose                          |
|-----------------------|----------------------------------|
| `Streamlit`           | UI Framework                     |
| `PyMuPDF`             | PDF parsing & rendering          |
| `Vosk`                | Offline Speech Recognition       |
| `pyttsx3`             | Offline Text-to-Speech Engine    |
| `SentenceTransformers`| Basic NLP logic                  |
| `json`                | Output formatting                |

---

## 🧠 How It Works

1. **Upload a PDF** 📄  
2. App asks: _“Do you want to open it?”_ (voice-enabled)  
3. **PDF opens** with semi-transparent dialog overlay  
4. Say commands like:
   - “Give me all headings”
   - “Explain the first paragraph”
   - “Generate a mind map”
   - “Stop speaking”
5. 🧠 Processes your query  
6. 📤 Responds visually and verbally — inside the overlay  

---

## 🚀 Getting Started

### 🔧 1. Clone the repo

```bash
git clone https://github.com/your-username/adobe_voice_ai.git
cd adobe_voice_ai
```

### 📦 2. Set up environment

```bash
python -m venv venv
source venv/bin/activate    # or .\venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### 🎙️ 3. Run the app

```bash
streamlit run app.py
```

---

## 📁 Folder Structure

```bash
adobe_voice_ai/
│
├── app.py                   # Main Streamlit App
├── requirements.txt         # Dependencies
├── pdf_parser.py            # Heading/paragraph extraction
├── mind_map.html            # Rendered mind map
├── responses_logic.py       # Query understanding + TTS
├── conversation_logic.py    # Handles back-and-forth convo
├── glossary.json            # NLP fallback definitions
├── sample_docs/             # Test PDFs
├── venv/                    # Ignored in Git
```

---

## 🤖 Sample Voice Commands

| You Say                        | It Does                                   |
|-------------------------------|--------------------------------------------|
| “Give me the headings”        | Extracts all section titles from PDF       |
| “Tell me the first paragraph” | Reads first paragraph aloud + overlay      |
| “Mind map please”             | Generates a mind map with hierarchy        |
| “Stop speaking”               | Silences the TTS output immediately        |

---

## 🧪 Adobe Constraints ✅

| Constraint         | Status       |
|--------------------|--------------|
| Offline-only       | ✅ Fully local |
| ≤1GB Model         | ✅ Vosk small model used |
| CPU-only           | ✅ No GPU needed |
| JSON Output        | ✅ Structured output |
| ≤60 sec/Task       | ✅ Optimized functions |


---

## 👩‍💻 Made with 100% caffeine & chaos by:  
**Yashika , Raj , Vineet — B.E. CSE, Chandigarh University**
