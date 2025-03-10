from jose import jwt
from sanic import Sanic

from app.core.config import settings
from app.daos.user_dao import UserDAO
from app.database.config import get_async_session


def setup_middlewares(app: Sanic):
    @app.middleware("request")
    async def attach_user(request):
        token = request.cookies.get("access_token")
        if token:
            JWT_SECRET, JWT_ALGORITHM, _ = settings.JWT_CONFIG
            try:
                payload = jwt.decode(
                    token, JWT_SECRET, algorithms=[JWT_ALGORITHM]
                )
                user_id = payload.get("sub")
                if user_id:
                    async with get_async_session() as session:
                        user_dao = UserDAO(session)
                        user = await user_dao.get_user_by_id(user_id)
                        request.ctx.user = user
                else:
                    request.ctx.user = None
            except Exception:
                request.ctx.user = None
        else:
            request.ctx.user = None
