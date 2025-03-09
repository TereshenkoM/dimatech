from datetime import datetime, timedelta
from jose import jwt, JWTError
from sanic import Blueprint, text
from sanic.exceptions import SanicException
from sanic.response import json as sanic_json
from sqlalchemy import select
from app.database.config import get_async_session
from app.models.user_models import UserORM
from app.core.config import settings

auth_bp = Blueprint("auth", url_prefix="/auth")
JWT_SECRET, JWT_ALGORITHM, JWT_EXP = settings.JWT_CONFIG

@auth_bp.post("/login")
async def login(request):
    data = request.json
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        raise SanicException("Email or password is missing", status_code=400)

    async with get_async_session() as session:
        result = await session.execute(
            select(UserORM).where(UserORM.email == email)
        )
        user = result.scalar_one_or_none()

        if not user or not user.check_password(password):
            raise SanicException("Incorrect email or password", status_code=401)
        
        if not user.is_active:
            raise SanicException("User is not active", status_code=403)

    payload = {
        "sub": str(user.id),
        "exp": datetime.utcnow() + timedelta(seconds=JWT_EXP)
    }
    
    token = jwt.encode(
        payload,
        JWT_SECRET,
        algorithm=JWT_ALGORITHM
    )

    response = sanic_json({
        "message": "Login successful",
        "user_id": str(user.id)
    })
    response.add_cookie(
        key="access_token",
        value=token,
        httponly=True,
        max_age=JWT_EXP,
        samesite="Strict",
        path="/",
    )

    return response


@auth_bp.post("/logout")
async def logout(request):
    response = text("Logged out successfully")
    response.delete_cookie(
        "access_token",
        path="/",
    )

    return response