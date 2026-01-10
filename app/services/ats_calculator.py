from sentence_transformers import SentenceTransformer, util

# Load the model once (this might take time on first run)
# We use a lightweight model suitable for this task
model = SentenceTransformer('all-MiniLM-L6-v2')

def calculate_ats_score(resume_text: str, resume_skills: list[str], job_description: str, job_skills: list[str]) -> dict:
    """
    Calculates ATS score based on weighted formula:
    - 40% Skill Match
    - 30% Similarity (SBERT)
    - 20% Formatting (Stubbed)
    - 10% Grammar (Stubbed)
    """
    
    # 1. Skill Match Score (40%)
    # Using Intersection over Union could be one way, but traditionally ATS cares about Missing Skills.
    # So we calculate Recall: (Matches / Required)
    if not job_skills:
        skill_score = 100 # If no skills required, full score? Or 0? Let's say 100 for safety.
    else:
        # Normalize
        r_skills = set([s.lower() for s in resume_skills])
        j_skills = set([s.lower() for s in job_skills])
        
        matches = r_skills.intersection(j_skills)
        missing = j_skills - r_skills
        
        # Score = (Matches / Total Required) * 100
        skill_score = (len(matches) / len(j_skills)) * 100

    # 2. Semantic Similarity Score (30%)
    # Encode both text and compute cosine similarity
    embeddings1 = model.encode(resume_text, convert_to_tensor=True)
    embeddings2 = model.encode(job_description, convert_to_tensor=True)
    cosine_score = util.cos_sim(embeddings1, embeddings2).item() * 100
    # Ensure it's not negative
    cosine_score = max(0, cosine_score)

    # 3. Formatting Score (20%)
    # Simple heuristics: length check, sections checks?
    # We assume 'resume_text' passed here is raw, but we could check length
    formatting_score = 100
    if len(resume_text) < 500: formatting_score -= 20
    if len(resume_text) > 10000: formatting_score -= 10
    # TODO: Check for headers if available.
    
    # 4. Grammar Score (10%)
    # Stub
    grammar_score = 100
    
    # Weighted Sum
    total_score = (
        (skill_score * 0.40) +
        (cosine_score * 0.30) +
        (formatting_score * 0.20) +
        (grammar_score * 0.10)
    )
    
    return {
        "ats_score": round(total_score, 1),
        "breakdown": {
            "skill_match": round(skill_score, 1),
            "similarity": round(cosine_score, 1),
            "formatting": round(formatting_score, 1),
            "grammar": round(grammar_score, 1)
        },
        "matched_skills": list(matches) if job_skills else [],
        "missing_skills": list(missing) if job_skills else [],
    }
