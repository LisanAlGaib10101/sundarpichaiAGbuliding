from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.job_matcher import match_jobs

router = APIRouter()

class MatchRequest(BaseModel):
    resume_text: str
    top_k: int = 3

@router.post("/match")
async def get_job_matches(request: MatchRequest):
    try:
        matches = match_jobs(request.resume_text, request.top_k)
        return {"matches": matches}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/")
async def get_all_jobs():
    from app.services.job_matcher import load_jobs
    jobs, _ = load_jobs()
    # Return minimal info for dropdown
    return [{"job_role": j['job_role'], "id": i} for i, j in enumerate(jobs)]
