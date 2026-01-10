from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from app.services.ats_calculator import calculate_ats_score

router = APIRouter()

class AtsRequest(BaseModel):
    resume_text: str
    resume_skills: List[str]
    job_description: str
    job_skills: List[str]

@router.post("/score")
async def get_ats_score(request: AtsRequest):
    try:
        result = calculate_ats_score(
            request.resume_text,
            request.resume_skills,
            request.job_description,
            request.job_skills
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
