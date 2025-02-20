from sqlalchemy import Column, Integer, String, DateTime, func, Float, Text
from database import Base

class LogEntry(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(String, unique=True)
    endpoint = Column(String)
    data = Column(String)
    model = Column(String)
    response = Column(String)
    duration = Column(Float)  # Response time in seconds
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String)  # 'success' or 'error'
    error_message = Column(String, nullable=True)

class ErrorLog(Base):
    __tablename__ = "error_logs"

    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(String)
    endpoint = Column(String)
    error = Column(String)
    data = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    stack_trace = Column(String, nullable=True)

class Feedback(Base):
    __tablename__ = "feedbacks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    email = Column(String(100))
    message = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())