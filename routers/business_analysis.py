# routers/business_analysis.py

from fastapi import APIRouter, HTTPException
from models.schemas import BusinessAnalysisRequest
from services.business_logic import analyze_business_request
from services.filter import is_safe_response

router = APIRouter()

@router.post("/analyze")
async def analyze_business(request: BusinessAnalysisRequest):
    """
    Анализирует расширенный бизнес-запрос (BusinessAnalysisRequest)
    и возвращает рекомендации по AI-решению.
    """
    # Формируем текст для проверки безопасности (можно объединить несколько ключевых полей)
    input_text = f"{request.name} {request.industry} {request.audience} {', '.join(request.key_tasks)}"
    
    if not is_safe_response(input_text):
        raise HTTPException(status_code=400, detail="Request contains prohibited topics.")
    
    analysis = await analyze_business_request(request.dict())
    return {"analysis": analysis}
