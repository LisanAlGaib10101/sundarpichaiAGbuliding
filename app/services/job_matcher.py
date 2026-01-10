import csv
import os
from sentence_transformers import SentenceTransformer, util
import torch

JOBS_CSV_PATH = "/home/mark3jaeger/resumeGoogleAntigravity/datasets/jobs.csv"
model = SentenceTransformer('all-MiniLM-L6-v2')

# Cache for jobs and embeddings
cached_jobs = []
cached_embeddings = None

def load_jobs():
    global cached_jobs, cached_embeddings
    
    if cached_jobs:
        return cached_jobs, cached_embeddings
        
    jobs = []
    descriptions = []
    
    if os.path.exists(JOBS_CSV_PATH):
        with open(JOBS_CSV_PATH, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                jobs.append(row)
                descriptions.append(row['description'] + " " + row['required_skills'])
    
    cached_jobs = jobs
    if descriptions:
        cached_embeddings = model.encode(descriptions, convert_to_tensor=True)
    
    return cached_jobs, cached_embeddings

def match_jobs(resume_text: str, top_k: int = 3) -> list:
    """
    Finds top k matching jobs for the resume text using SBERT embeddings.
    """
    jobs, job_embeddings = load_jobs()
    
    if not jobs or job_embeddings is None:
        return []
        
    resume_embedding = model.encode(resume_text, convert_to_tensor=True)
    
    # Compute cosine similarities
    cos_scores = util.cos_sim(resume_embedding, job_embeddings)[0]
    
    # Find top k matches
    top_results = torch.topk(cos_scores, k=min(top_k, len(jobs)))
    
    matches = []
    for score, idx in zip(top_results[0], top_results[1]):
        job = jobs[idx]
        matches.append({
            "job_role": job['job_role'],
            "match_score": round(score.item() * 100, 1),
            "required_skills": job['required_skills'],
            "description": job['description']
        })
        
    return matches
