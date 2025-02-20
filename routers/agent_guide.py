from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from models.schemas import AgentAssessmentRequest
from services.agent_assessment import assess_agent_performance  # Функция оценки агента, которую мы уже реализовали
from services.guide_generator import generate_guide, save_guide_to_db  # Add save_guide_to_db
from database import get_db

router = APIRouter(prefix="/agent")

@router.post("/guide")
async def generate_agent_guide(request: AgentAssessmentRequest, db: AsyncSession = Depends(get_db)):
    """
    Принимает данные об AI-агенте и генерирует пошаговое руководство по его улучшению или интеграции.
    """
    # Get agent assessment
    assessment = await assess_agent_performance(request.model_dump())
    
    # Generate guide
    guide = await generate_guide(request.model_dump(), assessment)
    
    # Optional: Save guide to DB
    await save_guide_to_db(db, request.model_dump(), guide)
    
    return {"guide": guide}
