from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.templating import Jinja2Templates
from models.db_models import LogEntry
from database import get_db
from sqlalchemy import select

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/admin/logs")
async def view_logs(request: Request, db: AsyncSession = Depends(get_db)):
    """Выводит логи в админ-панель."""
    logs = await db.execute("SELECT * FROM logs ORDER BY created_at DESC LIMIT 100")
    logs = logs.fetchall()
    return templates.TemplateResponse("logs.html", {"request": request, "logs": logs})

@router.get("/logs")
async def get_logs(db: AsyncSession = Depends(get_db)):
    """Get all logs from database."""
    result = await db.execute(select(LogEntry))
    logs = result.scalars().all()
    return {"logs": [
        {
            "id": log.id,
            "endpoint": log.endpoint,
            "model": log.model,
            "created_at": log.created_at
        } for log in logs
    ]}
