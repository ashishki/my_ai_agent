from loguru import logger
import os
from sqlalchemy.ext.asyncio import AsyncSession
from models.db_models import LogEntry, ErrorLog
import json
import traceback

# Создаём папку logs, если её нет
LOGS_DIR = "logs"
if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)

# Настроим логирование в файл и консоль
logger.add(f"{LOGS_DIR}/app.log", rotation="10 MB", retention="7 days", level="INFO")

def log_request(endpoint: str, data: dict, model: str, response: str):
    """Логирует входные данные и ответ от модели."""
    logger.info(
        f"📌 Запрос -> {endpoint}\n"
        f"💡 Данные: {data}\n"
        f"🧠 Модель: {model}\n"
        f"📥 Ответ: {response[:300]}..."  # Обрезаем длинные ответы
    )


async def save_log_to_db(
    db: AsyncSession,
    endpoint: str,
    request_id: str,
    data: dict,
    model: str,
    response: str,
    duration: float,
    status: str = 'success'
) -> None:
    """Сохраняет лог запроса в БД."""
    log_entry = LogEntry(
        request_id=request_id,
        endpoint=endpoint,
        data=str(data),
        model=model,
        response=response,
        duration=duration,
        status=status
    )
    db.add(log_entry)
    await db.commit()

async def save_error_log(
    db: AsyncSession,
    request_id: str,
    endpoint: str,
    error: str,
    data: dict,
    stack_trace: str = None
) -> None:
    """Сохраняет лог ошибки в БД."""
    error_log = ErrorLog(
        request_id=request_id,
        endpoint=endpoint,
        error=error,
        data=str(data),
        stack_trace=stack_trace
    )
    db.add(error_log)
    await db.commit()