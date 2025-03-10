from sanic import Blueprint, text
from sanic.exceptions import SanicException
from app.schemas.auth_shemas import LoginRequest
from pydantic import ValidationError
from app.utils.auth_utils import get_jwt_response

auth_bp = Blueprint("auth", url_prefix="/auth")

@auth_bp.post("/login")
async def login(request):
    payload = request.json

    try:
        LoginRequest(**payload)
    except ValidationError as e:
        raise SanicException(
            message=f"Invalid request data: {e.errors()}",
            status_code=400
        )
    email = payload.get("email")
    password = payload.get("password")

    response = await get_jwt_response(email, password)

    return response


@auth_bp.post("/logout")
async def logout(request):
    response = text("Logged out successfully")
    response.delete_cookie(
        "access_token",
        path="/",
    )

    return response