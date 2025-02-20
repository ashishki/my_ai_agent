from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from jose import JWTError, jwt
from dotenv import load_dotenv
import os
from typing import Annotated
from routers import business, admin, agent_assessment, agent_guide


# Загружаем переменные окружения
load_dotenv()

# Настройки JWT (теперь из .env)
SECRET_KEY = os.getenv("SECRET_KEY", "change-this-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# FastAPI приложение
app = FastAPI(title="AI Business Analysis API")

# Подключаем маршруты
app.include_router(business.router, prefix="/api/v1", tags=["business"])
app.include_router(admin.router, prefix="/admin")
app.include_router(agent_assessment.router, prefix="/api/v1")
app.include_router(agent_guide.router, prefix="/api/v1")
# CORS настройки
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Для продакшена лучше указывать конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Конфигурация OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

# Функция для создания токена
def create_access_token(data: dict):
    expires = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = data.copy()
    to_encode.update({"exp": expires})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Эндпоинт аутентификации (логин)
@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    # Для теста: test/test
    if form_data.username == "test" and form_data.password == "test":
        access_token = create_access_token(
            data={"sub": form_data.username}
        )
        return {"access_token": access_token, "token_type": "bearer"}
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password"
    )

# Функция проверки токена
async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        
        # Проверяем, не истёк ли токен
        exp = payload.get("exp")
        if exp is None or datetime.utcfromtimestamp(exp) < datetime.utcnow():
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
        
        return {"username": username}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

# Защищённый маршрут (требует авторизацию)
@app.get("/protected")
async def protected_route(current_user: dict = Depends(get_current_user)):
    return {"message": "This is protected", "user": current_user}

# Проверка работы API
@app.get("/")
async def root():
    return {"message": "API is running"}
