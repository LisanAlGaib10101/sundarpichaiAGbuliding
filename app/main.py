from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import resume, ats, jobs, roadmap

app = FastAPI(title="AI-Powered Resume Analyzer", version="1.0.0")

# CORS Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all for dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(resume.router, prefix="/api/v1/resume", tags=["Resume"])
app.include_router(ats.router, prefix="/api/v1/ats", tags=["ATS"])
app.include_router(jobs.router, prefix="/api/v1/jobs", tags=["Jobs"])
app.include_router(roadmap.router, prefix="/api/v1/roadmap", tags=["Roadmap"])

@app.get("/")
def read_root():
    return {"message": "Welcome to AI-Powered Resume Analyzer API"}
