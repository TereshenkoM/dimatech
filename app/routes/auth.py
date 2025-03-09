from datetime import datetime, timedelta
from jose import jwt
from sanic import Blueprint, text
from sanic.exceptions import SanicException
from sanic.response import json as sanic_json
from app.database.config import get_async_session
from app.core.config import settings
from app.daos.user_dao import UserDAO
from app.schemas.user_shema import LoginRequest, LoginResponse, TokenPayload
from pydantic import ValidationError


auth_bp = Blueprint("auth", url_prefix="/auth")
JWT_SECRET, JWT_ALGORITHM, JWT_EXP = settings.JWT_CONFIG

@auth_bp.post("/login")
async def login(request):
    data = request.json

    try:
        LoginRequest(**data)
    except ValidationError as e:
        raise SanicException(
            message=f"Invalid request data: {e.errors()}",
            status_code=400
        )

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        raise SanicException("Email or password is missing", status_code=400)

    async with get_async_session() as session:
        user_dao = UserDAO(session)
        user = await user_dao.get_user_by_email(email)

        if not user or not user.check_password(password):
            raise SanicException("Incorrect email or password", status_code=401)
        
        if not user.is_active:
            raise SanicException("User is not active", status_code=403)

    token_payload = TokenPayload(
        sub=str(user.id),
        exp=datetime.utcnow() + timedelta(seconds=JWT_EXP)
    )

    token = jwt.encode(
        token_payload.model_dump(),
        JWT_SECRET,
        algorithm=JWT_ALGORITHM
    )

    response = sanic_json(LoginResponse(
        message="Login successful",
        user_id=str(user.id)
    ).model_dump())

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