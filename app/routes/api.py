from sanic import Blueprint
from sanic.response import json
from app.models.payment_models import AccountORM
from app.daos.payment_dao import PaymentDAO
from app.database.config import get_async_session

api_bp = Blueprint("api", url_prefix="/api")

@api_bp.get("/user_info")
async def user_info(request):
    user = request.ctx.user
    return json({
        "user_id": str(user.id),
        "user_fullname": user.get_fullname(),
        "email": user.email
    })


@api_bp.get("/account_info")
async def account_info(request):
    user = request.ctx.user
    async with get_async_session() as session:
        payment_dao = PaymentDAO(session)
        accounts = await payment_dao.get_account_by_user_id(user.id)
    
        if accounts:
            accounts_payload = [
                {
                    "id": str(account.id),
                    "balance": account.balance,
                    "created_at": account.created_at.isoformat()
                }
                for account in accounts
            ]
        else:
            accounts_payload = []

        return json({"accounts": accounts_payload})
