from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from models.schemas import AgentAssessmentRequest
from services.agent_assessment import assess_agent_performance, save_assessment_to_db
from database import get_db

router = APIRouter(prefix="/agent")

@router.post("/assess")
async def assess_agent(request: AgentAssessmentRequest, db: AsyncSession = Depends(get_db)):
    """
    Принимает данные об AI-агенте (логи, метрики, отзывы) и возвращает оценку его работы с рекомендациями по улучшению.
    """
    # Можно добавить базовую проверку входных данных
    if request.error_rate < 0 or request.response_time < 0:
        raise HTTPException(status_code=400, detail="Invalid metrics provided.")

    assessment = await assess_agent_performance(request.model_dump())
    # При желании можно сохранить оценку в БД (логирование оценки)

    await save_assessment_to_db(db, request.model_dump(), assessment)

    return {"assessment": assessment}
