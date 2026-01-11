from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.routers import resume, ats, jobs, roadmap
from app.utils.response_utils import create_response

app = FastAPI(title="AI-Powered Resume Analyzer", version="1.0.0")

# CORS Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all for dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global Exception Handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content=create_response(success=False, message=f"Internal Server Error: {str(exc)}", data=None)
    )

from fastapi.exceptions import HTTPException
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=create_response(success=False, message=exc.detail, data=None)
    )

# Include Routers
app.include_router(resume.router, prefix="/api/v1/resume", tags=["Resume"])
app.include_router(ats.router, prefix="/api/v1/ats", tags=["ATS"])
app.include_router(jobs.router, prefix="/api/v1/jobs", tags=["Jobs"])
app.include_router(roadmap.router, prefix="/api/v1/roadmap", tags=["Roadmap"])

@app.get("/")
def read_root():
    return create_response(message="Welcome to AI-Powered Resume Analyzer API")
