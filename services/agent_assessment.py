from typing import Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession

async def assess_agent_performance(agent_data: Dict[str, Any]) -> str:
    """
    Оценивает работу существующего AI-агента на основе логов, времени ответа, ошибок и отзывов.
    Возвращает структурированную рекомендацию по улучшению.
    """
    # Извлекаем метрики
    agent_name = agent_data.get("agent_name", "Unknown Agent")
    response_time = agent_data.get("response_time", 0)
    error_rate = agent_data.get("error_rate", 0)
    user_feedback = agent_data.get("user_feedback", [])

    # Простая логика оценки
    recommendations = []
    
    if response_time > 3:  # если время ответа больше 3 секунд
        recommendations.append("Оптимизировать обработку запросов для снижения времени ответа.")
    else:
        recommendations.append("Время ответа удовлетворительное.")

    if error_rate > 0.1:  # если ошибки более 10%
        recommendations.append("Провести дообучение модели для повышения точности.")
    else:
        recommendations.append("Показатели точности на должном уровне.")

    # Анализ отзывов (простая обработка)
    if user_feedback:
        positive = sum(1 for fb in user_feedback if "хорошо" in fb.lower() or "отлично" in fb.lower())
        negative = len(user_feedback) - positive
        if negative > positive:
            recommendations.append("Соберите больше отзывов для анализа причин неудовлетворенности.")
        else:
            recommendations.append("Отзывы в целом положительные.")
    else:
        recommendations.append("Нет отзывов, рекомендуется добавить систему обратной связи.")

    # Формируем финальное сообщение
    assessment = (
        f"Оценка работы AI-агента '{agent_name}':\n"
        f"- Среднее время ответа: {response_time} сек.\n"
        f"- Процент ошибок: {error_rate*100:.1f}%.\n"
        f"Рекомендации:\n" + "\n".join(f"- {rec}" for rec in recommendations)
    )

    return assessment

async def save_assessment_to_db(db: AsyncSession, request_data: dict, assessment: str):
    """Save agent assessment to database."""
    # TODO: Implement assessment saving logic
    pass
