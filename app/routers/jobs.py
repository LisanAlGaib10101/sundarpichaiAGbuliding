from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.job_matcher import match_jobs
from app.utils.response_utils import create_response

router = APIRouter()

class MatchRequest(BaseModel):
    resume_text: str
    top_k: int = 3

@router.post("/match")
async def get_job_matches(request: MatchRequest):
    try:
        matches = match_jobs(request.resume_text, request.top_k)
        return create_response(data={"matches": matches}, message="Job matches found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/")
async def get_all_jobs():
    try:
        from app.services.job_matcher import load_jobs
        jobs, _ = load_jobs()
        # Return minimal info for dropdown
        data = [{"job_role": j['job_role'], "id": i} for i, j in enumerate(jobs)]
        return create_response(data=data, message="Job list retrieved")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
