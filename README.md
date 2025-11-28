# Resume Screening Agent (Complete ZIP)

This is a ready-to-run project for the Resume Screening Agent with a clean, responsive Streamlit UI.
It supports OpenAI embeddings and chat (if you provide an API key), and falls back to a local sentence-transformers model.

## What's included
- `app.py` — Streamlit frontend (dark/light theme, Lottie hooks, badges, download results)
- `scorer.py` — embeddings + scoring (OpenAI primary, local fallback)
- `parser.py` — extract text from PDF / DOCX / TXT
- `prompts.py` — summary prompt for LLM
- `requirements.txt` — packages
- `assets/` — placeholder Lottie JSONs and `logo.svg`
- `sample_jd.txt` and two sample resumes in `sample_resumes/`

## How to run (Windows)
1. Extract the ZIP into `D:\resume-screening-agent-full` (or your chosen folder).
2. Open Command Prompt and activate venv:
   ```cmd
   cd D:\resume-screening-agent-full
   python -m venv venv
   venv\Scripts\activate
   ```
3. Install dependencies:
   ```cmd
   pip install -r requirements.txt
   ```
   If `sentence-transformers` is slow or causes issues, run:
   ```cmd
   pip install streamlit streamlit-lottie pdfminer.six python-docx scikit-learn numpy pandas
   pip install sentence-transformers
   ```
4. (Optional) Install Lottie support:
   ```cmd
   pip install streamlit-lottie
   ```
5. (Optional) Set your OpenAI API key (do not paste secret in code):
   ```cmd
   setx OPENAI_API_KEY "sk-...your_key_here..."
   ```
   Then restart the terminal.
6. Run the app:
   ```cmd
   streamlit run app.py
   ```

## How to run (Linux / macOS)
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Notes & Troubleshooting
- If you want me to include your exact local files (images, previous scorer, sample resumes) upload them here and I'll rebuild a ZIP that contains them.
- The app will fall back to local sentence-transformers if OpenAI API is not configured, but ensure `sentence-transformers` is installed.
- Lottie animations are optional; if `streamlit-lottie` isn't installed the UI still works.
- Do **NOT** commit your OpenAI API key to source control. Use environment variables.

If you want, I can now:
- Replace placeholder Lotties with high-detail animations (I can fetch them if you give links)
- Integrate any files you upload (resume PDFs, your real scorer.py, logo.png)
- Produce a short demo script for your hackathon submission

