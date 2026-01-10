def generate_roadmap(resume_skills: list[str], target_role: str, target_skills: list[str]) -> dict:
    """
    Generates a career roadmap based on missing skills.
    """
    # Normalize
    r_skills = set([s.lower() for s in resume_skills])
    t_skills = set([s.lower() for s in target_skills])
    
    missing_skills = list(t_skills - r_skills)
    
    # If no missing skills
    if not missing_skills:
        return {
            "role": target_role,
            "message": "You have all the required skills for this role! Focus on projects and interview prep.",
            "roadmap": {}
        }
        
    # Heuristic Phasing
    # We can try to categorize skills into phases based on some simple logic or manually defined categories
    # For this MVP, we will distribute them evenly or based on a hardcoded dictionary if we had one.
    # Let's try to map certain keywords to phases.
    
    phases = {
        "phase_1": [], # Foundations
        "phase_2": [], # Core Skills
        "phase_3": [], # Advanced
        "phase_4": [], # Projects (Placeholder logic)
        "phase_5": ["Resume Polish", "Mock Interviews"] # Interview Prep
    }
    
    # Simple logic: Assign based on length? Or just round robin?
    # Let's use round robin for now as we don't have a difficulty database
    
    for i, skill in enumerate(missing_skills):
        if i % 3 == 0:
            phases["phase_1"].append(skill)
        elif i % 3 == 1:
            phases["phase_2"].append(skill)
        else:
            phases["phase_3"].append(skill)
            
    # Add generic project suggestion for Phase 4
    phases["phase_4"].append(f"Build a {target_role} project using {', '.join(phases['phase_2'][:2])}")
    
    return {
        "role": target_role,
        "missing_skills_count": len(missing_skills),
        "roadmap": phases
    }
