from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.pdf_parser import extract_text_from_pdf
from app.services.skill_extractor import extract_skills
from app.services.section_detector import detect_sections
from app.utils.response_utils import create_response
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/parse")
async def parse_resume(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        # Handled by global exception handler, but explicit for logic flow
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF allowed.")
    
    try:
        content = await file.read()
        text = extract_text_from_pdf(content)
        
        # TASK 1: Input Validation / OCR Check
        # We intentionally do NOT implement OCR.
        if not text or len(text.strip()) < 50:
             return create_response(
                 success=False, 
                 message="No extractable text found. Please upload a text-based PDF resume. (OCR is not supported)",
                 data=None
             )

        skills = extract_skills(text)
        sections = detect_sections(text)
        
        data = {
            "filename": file.filename,
            "extracted_text_length": len(text),
            "skills": skills,
            "sections": sections,
            "text_preview": text[:500] + "..." if len(text) > 500 else text
        }
        return create_response(data=data, message="Resume parsed successfully")
        
    except Exception as e:
        logger.error(f"Error parsing resume: {str(e)}")
        # Re-raise to let global handler catch it or return specific response
        raise HTTPException(status_code=500, detail=f"Error parsing resume: {str(e)}")
