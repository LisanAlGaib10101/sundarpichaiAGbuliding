import csv
import os
import re

SKILLS_CSV_PATH = "/home/mark3jaeger/resumeGoogleAntigravity/datasets/skills.csv"

def load_skills() -> list[str]:
    skills = []
    if os.path.exists(SKILLS_CSV_PATH):
        with open(SKILLS_CSV_PATH, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                skills.append(row['skill'])
    return skills

def extract_skills(text: str) -> list[str]:
    """
    Extracts skills from text using rule-based matching against the loaded CSV.
    """
    text_lower = text.lower()
    skills_db = load_skills()
    extracted_skills = set()

    # Sort skills by length (descending) to match longer phrases first
    # This helps with skills like "Machine Learning" not being just matched as "Machine" if that was a skill
    skills_db.sort(key=len, reverse=True)

    for skill in skills_db:
        # Use regex to match whole words/phrases
        # Escape skill for regex safety
        pattern = r'\b' + re.escape(skill.lower()) + r'\b'
        if re.search(pattern, text_lower):
            extracted_skills.add(skill)
            
    return list(extracted_skills)
