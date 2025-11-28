# prompts.py
summary_prompt = """
You are an HR assistant. Given this job description and a candidate's resume text, produce:
1) A 2-3 sentence summary of the candidate's fit.
2) Top 3 matching skills/keywords that match JD.
3) Top 3 gaps or missing keywords the candidate lacks relative to JD.

Job Description:
{jd}

Candidate Resume:
{resume}

Answer in JSON with fields: summary (string), matches (list), gaps (list).
"""
