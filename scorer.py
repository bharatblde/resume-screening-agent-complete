# scorer.py  (with OpenAI primary + local fallback + caching)
import os
import time
import json
import hashlib
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Try import OpenAI new client
use_openai = False
client = None
try:
    from openai import OpenAI
    OPENAI_KEY = os.environ.get("OPENAI_API_KEY")
    if OPENAI_KEY:
        client = OpenAI(api_key=OPENAI_KEY)
        use_openai = True
except Exception:
    use_openai = False

# Local fallback (sentence-transformers)
local_model = None
def ensure_local_model():
    global local_model
    if local_model is None:
        try:
            from sentence_transformers import SentenceTransformer
        except Exception as e:
            raise RuntimeError(
                "sentence-transformers not installed. Run: pip install sentence-transformers"
            )
        local_model = SentenceTransformer("all-MiniLM-L6-v2")
    return local_model

# Simple on-disk cache directory for embeddings
CACHE_DIR = "emb_cache"
os.makedirs(CACHE_DIR, exist_ok=True)

def _cache_key(text: str, model_name: str):
    h = hashlib.sha256((model_name + "|" + text).encode("utf-8")).hexdigest()
    return os.path.join(CACHE_DIR, f"{h}.npy")

def _save_cache(keypath: str, vec: np.ndarray):
    np.save(keypath, vec)

def _load_cache(keypath: str):
    if os.path.exists(keypath):
        try:
            return np.load(keypath)
        except Exception:
            return None
    return None

# Embedding function that tries OpenAI then local fallback
EMBED_MODEL = "text-embedding-3-small"

def get_embedding(text: str, model: str = EMBED_MODEL):
    # Try cache first (OpenAI model name as part of key)
    key = _cache_key(text, model)
    cached = _load_cache(key)
    if cached is not None:
        return cached.astype(np.float32)

    # Try OpenAI client if available
    if use_openai and client is not None:
        try:
            resp = client.embeddings.create(model=model, input=text)
            vec = np.array(resp.data[0].embedding, dtype=np.float32)
            _save_cache(key, vec)
            return vec
        except Exception as e:
            # Log and fall through to local fallback
            print("OpenAI embeddings failed:", str(e))

    # Local fallback (sentence-transformers)
    try:
        model_local = ensure_local_model()
        embeddings = model_local.encode([text], show_progress_bar=False)
        vec = np.array(embeddings[0], dtype=np.float32)
        # Save to cache (model name reflects local model)
        key_local = _cache_key(text, "all-MiniLM-L6-v2")
        _save_cache(key_local, vec)
        return vec
    except Exception as e:
        raise RuntimeError("No embedding method available: " + str(e))

def score_resume_against_jd(resume_text: str, jd_text: str):
    emb_resume = get_embedding(resume_text)
    emb_jd = get_embedding(jd_text)
    sim = cosine_similarity(emb_resume.reshape(1, -1), emb_jd.reshape(1, -1))[0][0]
    score = float(sim) * 100.0
    return round(score, 2)

def batch_score(resumes: dict, jd_text: str):
    results = []
    emb_jd = get_embedding(jd_text)
    for fname, text in resumes.items():
        if not text or len(text.strip()) == 0:
            results.append({"filename": fname, "score": 0.0, "text": text})
            continue
        emb = get_embedding(text)
        sim = cosine_similarity(emb.reshape(1, -1), emb_jd.reshape(1, -1))[0][0]
        score = round(float(sim) * 100.0, 2)
        results.append({"filename": fname, "score": score, "text": text})
        time.sleep(0.05)
    results = sorted(results, key=lambda x: x["score"], reverse=True)
    return results

# LLM summary generator: try OpenAI chat, else return simple rule-based summary
def generate_candidate_summary(jd_text: str, resume_text: str):
    try:
        # If OpenAI client exists, use it
        if use_openai and client is not None:
            from prompts import summary_prompt
            prompt = summary_prompt.format(jd=jd_text, resume=resume_text)
            resp = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
                max_tokens=400,
            )
            txt = resp.choices[0].message.content
            try:
                return json.loads(txt)
            except Exception:
                return {"raw": txt}
    except Exception as e:
        print("OpenAI chat summary failed:", e)

    # Fallback: simple rule-based summary (safe demo mode)
    jd_words = set([w.lower().strip(".,()") for w in jd_text.split() if len(w) > 2])
    resume_words = set([w.lower().strip(".,()") for w in resume_text.split() if len(w) > 2])
    matches = list(jd_words & resume_words)[:6]
    gaps = list(jd_words - resume_words)[:6]
    summary = f"Auto summary: matches {', '.join(matches[:3]) or 'none'}; gaps {', '.join(gaps[:3]) or 'none'}."
    return {"summary": summary, "matches": matches[:3], "gaps": gaps[:3]}
