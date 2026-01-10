import re

def detect_sections(text: str) -> dict:
    """
    Splits the resume text into sections based on keywords.
    Returns a dictionary with 'skills', 'education', 'experience', and 'projects' keys.
    """
    text_lower = text.lower()
    
    # Define keywords for sections
    # Using simple heuristic: looking for the headers
    headers = {
        "education": ["education", "academic", "university", "college"],
        "skills": ["skills", "technical skills", "technologies", "competencies", "stack"],
        "experience": ["experience", "work history", "employment", "internships"],
        "projects": ["projects", "personal projects", "academic projects"]
    }
    
    # We will try to find the starting index of each section
    indices = {}
    for section, keywords in headers.items():
        indices[section] = -1
        for kw in keywords:
            # We look for the keyword followed by optional colon and newlines
            # or just the keyword on its own line/sentence structure
            # To be robust, we just find the first occurrence of the keyword in a context that looks like a header
            # For simplicity in this version: just find the keyword
            idx = text_lower.find(kw)
            if idx != -1:
                if indices[section] == -1 or idx < indices[section]:
                    indices[section] = idx
    
    # Sort sections by their position in text
    sorted_sections = sorted([k for k, v in indices.items() if v != -1], key=lambda k: indices[k])
    
    sections = {
        "skills": "",
        "education": "",
        "experience": "",
        "projects": "",
        "uncategorized": "" # For text before the first section
    }
    
    if not sorted_sections:
        sections["uncategorized"] = text
        return sections
        
    # Extract text slices
    # Text before first section
    first_section_idx = indices[sorted_sections[0]]
    sections["uncategorized"] = text[:first_section_idx].strip()
    
    for i, section in enumerate(sorted_sections):
        start_idx = indices[section]
        if i < len(sorted_sections) - 1:
            end_idx = indices[sorted_sections[i+1]]
            content = text[start_idx:end_idx]
        else:
            content = text[start_idx:]
        
        # Remove the header itself from content (heuristic length)
        # We assume the header is roughly at the start
        # Basic cleanup: remove the first 20 chars which likely contain the header
        # Better approach: regex replace the header keyword
        
        sections[section] = content.strip()
        
    return sections
