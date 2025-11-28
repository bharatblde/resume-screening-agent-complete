Resume Screening AI Agent

An intelligent AI-powered system that analyzes resumes, matches them with a job description, and ranks candidates based on relevance.
Built as part of the 48-Hour AI Agent Development Challenge.

🚀 Overview

The Resume Screening Agent helps HR teams and recruiters automatically evaluate candidate resumes.

You simply upload:

✔ A Job Description (JD)
✔ Multiple Resumes (PDF, DOCX, TXT)

The system extracts text, computes embeddings, calculates similarity, and ranks the resumes from highest to lowest match.

If an OpenAI API key is available, the system uses GPT models for high-quality embeddings and AI summaries.
If not, it switches automatically to local offline embedding models using sentence-transformers.

🌟 Features
🔍 AI Resume Scoring

Rank resumes based on similarity to JD

View individual scores

Full resume text preview

📝 Candidate Summary (AI-powered)

Generates a structured summary

Shows:

Top matching skills

Missing skills

Fit analysis

💻 Modern UI (Streamlit)

Clean responsive design

Light/Dark theme support

Download CSV of ranked candidates

📂 File Support

PDF

DOCX

TXT

⚡ Optimized Performance

Embedding cache to avoid recomputation

Local ML model fallback

Fast scoring for multiple resumes

⚠️ Limitations

Scanned (image-only) PDFs may return empty text

Local fallback model is less accurate than GPT embeddings

Large files may take longer to parse

AI summary requires OpenAI key

🧰 Tech Stack
Backend / AI

Python

sentence-transformers (local fallback)

OpenAI API (optional for high-accuracy embeddings & AI chat)

scikit-learn (cosine similarity)

Frontend

Streamlit

Custom CSS for UI styling

Parsing

pdfminer.six

python-docx

Data & Storage

Temp uploads: temp_uploads/

Embedding cache: emb_cache/

Assets: assets/

📦 Folder Structure
resume-screening-agent/
│
├── app.py
├── parser.py
├── scorer.py
├── prompts.py
├── requirements.txt
│
├── assets/
│   ├── logo.svg
│   ├── funny_ai.json (optional)
│   ├── ai_glossy.json (optional)
│   └── job_colorful.json (optional)
│
├── temp_uploads/      (auto created)
├── emb_cache/         (auto created)
├── README.md

🛠 Setup & Run Instructions
1️⃣ Clone the Repo
git clone https://github.com/yourusername/resume-screening-agent.git
cd resume-screening-agent

2️⃣ Create Virtual Environment
python -m venv venv

3️⃣ Activate Environment

Windows:

venv\Scripts\activate


Mac/Linux:

source venv/bin/activate

4️⃣ Install Dependencies
pip install -r requirements.txt

5️⃣ Optional: Set OpenAI Key

(Needed for GPT embeddings + AI summaries)

Windows:

setx OPENAI_API_KEY "your_api_key_here"


Mac/Linux:

export OPENAI_API_KEY="your_api_key_here"

6️⃣ Run the App
streamlit run app.py

🧠 How It Works (Architecture)

Streamlit UI receives uploaded resumes & JD

parser.py extracts text from files

scorer.py generates embeddings (OpenAI or local)

Cosine similarity scores each resume

Results displayed in ranked order

Optional AI summary generated with GPT

🔮 Future Enhancements

Add Pinecone/Chroma vector DB support

Add OCR for scanned PDFs

Add job-role specific scoring templates

Improve UI with animations & charts

Deploy to Streamlit Cloud / Render / HuggingFace

👤 Author

Bharat
Built for the Rooman 48-Hour AI Agent Development Challenge
With ❤️ and Python 🐍
