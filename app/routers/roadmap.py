from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from app.services.roadmap_generator import generate_roadmap

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
        return roadmap
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
