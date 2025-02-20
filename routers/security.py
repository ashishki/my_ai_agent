from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import get_db
from models.db_models import User
from models.schemas import UserLogin, UserCreate
from passlib.context import CryptContext
from fastapi_jwt_auth import AuthJWT

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/register")
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    async with db.begin():
        result = await db.execute(select(User).filter(User.username == user.username))
        existing_user = result.scalar_one_or_none()
        if existing_user:
            raise HTTPException(status_code=400, detail="User already exists")

        hashed_password = pwd_context.hash(user.password)
        new_user = User(username=user.username, password_hash=hashed_password)
        db.add(new_user)
        await db.commit()

    return {"message": "User registered"}

@router.post("/login")
async def login(user: UserLogin, db: AsyncSession = Depends(get_db), Authorize: AuthJWT = Depends()):
    async with db.begin():
        result = await db.execute(select(User).filter(User.username == user.username))
        existing_user = result.scalar_one_or_none()

        if not existing_user or not pwd_context.verify(user.password, existing_user.password_hash):
            raise HTTPException(status_code=400, detail="Invalid username or password")

    access_token = Authorize.create_access_token(subject=user.username)
    return {"access_token": access_token}


@router.get("/protected")
async def protected(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
        current_user = Authorize.get_jwt_subject()
        return {"message": f"Hello, {current_user}"}
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")
    



