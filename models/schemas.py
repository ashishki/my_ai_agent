from pydantic import BaseModel, Field, field_validator
from typing import List, Optional

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6, max_length=100)

    model_config = {
        'str_strip_whitespace': True,
        'str_min_length': 3
    }

class UserLogin(BaseModel):
    username: str
    password: str

class BusinessBase(BaseModel):
    """Base business model with common fields"""
    name: str = Field(..., min_length=3)
    industry: str = Field(..., min_length=2)

    model_config = {
        'str_strip_whitespace': True,
        'str_min_length': 3
    }

class BusinessData(BusinessBase):
    """Simple business analysis model"""
    revenue: Optional[float] = None
    employees: Optional[int] = None
    tags: List[str] = []

    @field_validator('tags')
    @classmethod
    def validate_tags(cls, value):
        if not isinstance(value, list):
            raise ValueError("Tags must be a list of strings")
        if any(not isinstance(tag, str) for tag in value):
            raise ValueError("Each tag must be a string")
        return value

class BusinessAnalysisRequest(BusinessBase):
    """Detailed business analysis model"""
    audience: str
    key_tasks: List[str]
    existing_tech: List[str] = []
    budget: str = "Not specified"
    description: Optional[str] = None
    competitors: List[str] = []
    goals: List[str] = []
    pain_points: List[str] = []
    current_solution: Optional[str] = None   


class AgentAssessmentRequest(BaseModel):
    agent_name: str
    log_data: str  # или более структурированный тип, если логи в формате JSON
    response_time: float  # среднее время ответа, в секундах
    error_rate: float     # процент ошибок или неудачных ответов
    user_feedback: Optional[List[str]] = []  # отзывы пользователей

class Feedback(BaseModel):
    user_id: str
    guide_id: Optional[int] = None  # Если сохраняем руководство в БД
    rating: int  # Оценка, например, от 1 до 5
    comment: Optional[str] = None