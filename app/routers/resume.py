from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.pdf_parser import extract_text_from_pdf
from app.services.skill_extractor import extract_skills
from app.services.section_detector import detect_sections
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/parse")
async def parse_resume(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF allowed.")
    
    try:
        content = await file.read()
        text = extract_text_from_pdf(content)
        skills = extract_skills(text)
        sections = detect_sections(text)
        
        return {
            "filename": file.filename,
            "extracted_text_length": len(text),
            "skills": skills,
            "sections": sections,
            "text_preview": text[:500] + "..." if len(text) > 500 else text
        }
    except Exception as e:
        logger.error(f"Error parsing resume: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error parsing resume: {str(e)}")
