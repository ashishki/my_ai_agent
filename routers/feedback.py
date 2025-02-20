from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime, timezone
from models.schemas import Feedback as FeedbackSchema
from models.db_models import Feedback as FeedbackModel
from database import get_db
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/feedback")

@router.post("/")
async def submit_feedback(feedback: FeedbackSchema, db: AsyncSession = Depends(get_db)):
    try:
        # Create new feedback record in DB
        db_feedback = FeedbackModel(
            name=feedback.name,
            email=feedback.email,
            message=feedback.message,
            created_at = datetime.now(timezone.utc)
        )
        
        db.add(db_feedback)
        await db.commit()
        
        return {"status": "success", "message": "Feedback submitted successfully"}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
