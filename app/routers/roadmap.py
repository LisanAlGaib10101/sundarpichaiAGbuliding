from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from app.services.roadmap_generator import generate_roadmap
from app.utils.response_utils import create_response

router = APIRouter()

class RoadmapRequest(BaseModel):
    resume_skills: List[str]
    target_role: str
    target_skills: List[str]

@router.post("/generate")
async def get_roadmap(request: RoadmapRequest):
    try:
        roadmap = generate_roadmap(
            request.resume_skills,
            request.target_role,
            request.target_skills
        )
        
        # TASK 4: Roadmap Endpoint Hardening
        # Ensure Phase 1-5 always exist
        # Check logic in service or enforce here. 
        # The service currently returns a dict with "roadmap" key.
        
        formatted_roadmap = roadmap.get("roadmap", {})
        required_phases = ["phase_1", "phase_2", "phase_3", "phase_4", "phase_5"]
        for phase in required_phases:
            if phase not in formatted_roadmap:
                formatted_roadmap[phase] = [] # Fallback empty list
                
        # If no missing skills, Phases 1-3 might be empty.
        # Ensure meaningful content if completely empty?
        # The service "generate_roadmap" already handles "no missing skills case" by returning specific message,
        # but let's ensure consistency.
        
        roadmap["roadmap"] = formatted_roadmap
        
        return create_response(data=roadmap, message="Career roadmap generated successfully")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
