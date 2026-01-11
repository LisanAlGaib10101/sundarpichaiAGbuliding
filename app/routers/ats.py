from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from app.services.ats_calculator import calculate_ats_score
from app.utils.response_utils import create_response

router = APIRouter()

class AtsRequest(BaseModel):
    resume_text: str
    resume_skills: List[str]
    job_description: str
    job_skills: List[str]

@router.post("/score")
async def get_ats_score(request: AtsRequest):
    # TASK 3: ATS Endpoint Hardening
    # Graceful handling of empty skills
    warning = ""
    if not request.job_skills:
        warning = "No job skills provided. Match score might be inaccurate."
    
    if not request.resume_skills:
        # We don't fail, we just calculate (likely low score)
        pass 
        
    try:
        result = calculate_ats_score(
            request.resume_text,
            request.resume_skills,
            request.job_description,
            request.job_skills
        )
        
        message = "ATS score calculated successfully"
        if warning:
            message += f" ({warning})"
            
        return create_response(data=result, message=message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
