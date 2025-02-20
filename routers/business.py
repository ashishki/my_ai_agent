from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from services.llm import analyze_business_data
from services.mistral import analyze_business_with_mistral
from services.filter import is_safe_response
from services.logger import log_request, save_log_to_db, save_error_log
from models.schemas import BusinessData, BusinessAnalysisRequest
from services.business_logic import analyze_business_request
import logging
from datetime import datetime
import uuid

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/business")

@router.post("/quick-analyze")
async def quick_analyze(
    business: BusinessData, 
    model: str = "openai", 
    db: AsyncSession = Depends(get_db)
):
    """Quick business analysis with basic data."""
    request_id = str(uuid.uuid4())
    start_time = datetime.now()
    
    try:
        logger.info(f"[{request_id}] Received quick-analyze request: {business.model_dump()}")
        
        input_text = f"{business.name} {business.industry} {', '.join(business.tags)}"
        
        if not is_safe_response(input_text):
            raise HTTPException(status_code=400, detail="Запрос содержит запрещённые темы.")

        logger.info(f"[{request_id}] Model selected: {model}")
        
        analysis = await analyze_business_with_mistral(business.model_dump()) if model == "mistral" \
                  else await analyze_business_data(business.model_dump(), request_id=request_id)
        
        # Log timing and response
        duration = (datetime.now() - start_time).total_seconds()
        logger.info(f"[{request_id}] Request completed in {duration}s")
        
        # Save detailed log for fine-tuning
        await save_log_to_db(
            db, 
            endpoint="/quick-analyze",
            request_id=request_id,
            data=business.model_dump(),
            model=model,
            response=analysis,
            duration=duration
        )
        
        return {"model": model, "analysis": analysis}
        
    except Exception as e:
        logger.error(f"[{request_id}] Error: {str(e)}", exc_info=True)
        # Save error log
        await save_error_log(
            db,
            request_id=request_id,
            endpoint="/quick-analyze",
            error=str(e),
            data=business.model_dump()
        )
        raise

@router.post("/detailed-analyze")
async def detailed_analyze(
    request: BusinessAnalysisRequest,
    model: str = "openai",
    db: AsyncSession = Depends(get_db)
):
    """Detailed business analysis with comprehensive data."""
    request_id = str(uuid.uuid4())
    start_time = datetime.now()
    
    input_text = f"{request.name} {request.industry} {request.audience}"
    
    if not is_safe_response(input_text):
        raise HTTPException(status_code=400, detail="Request contains prohibited topics.")
    
    analysis = await analyze_business_request(request.model_dump(), model=model)
    duration = (datetime.now() - start_time).total_seconds()
    
    await save_log_to_db(
        db,
        endpoint="/detailed-analyze",
        request_id=request_id,
        data=request.model_dump(),
        model=model,
        response=analysis,
        duration=duration
    )
    return {"model": model, "analysis": analysis}

