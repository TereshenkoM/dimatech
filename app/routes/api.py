from sanic import Blueprint
from sanic.response import json as sanic_json
from app.daos.payment_dao import PaymentDAO
from app.daos.user_dao import UserDAO
from app.database.config import get_async_session
from hashlib import sha256
from app.core.config import settings
from sanic.exceptions import SanicException

api_bp = Blueprint("api", url_prefix="/api")

@api_bp.get("/user_info")
async def user_info(request):
    user = request.ctx.user

    return sanic_json({
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

        return sanic_json({"accounts": accounts_payload})


@api_bp.get("/transaction")
async def get_transaction(request):
    user = request.ctx.user  
    
    async with get_async_session() as session:
        payment_dao = PaymentDAO(session)
        accounts = await payment_dao.get_account_by_user_id(user.id)

        if not accounts:
            return sanic_json([])

        transactions = await payment_dao.get_transaction_by_accounts(accounts)
        transactions_payload = [
            {
                "id": str(transaction.id),
                "transaction_id": transaction.transaction_id,
                "account_id": str(transaction.account_id),
                "amount": transaction.amount,
                "created_at": transaction.created_at.isoformat()
            } 
            for transaction in transactions]

        return sanic_json({"transactions": transactions_payload})


@api_bp.post("/transaction")
async def create_transaction(request):
    payload = request.json
    secret_key = settings.SECRET_KEY

    transaction_id = payload.get('transaction_id')
    user_id = payload.get('user_id')
    account_id = payload.get('account_id')
    amount = payload.get('amount')
    
    signature = sha256(f'{account_id}{amount}{transaction_id}{user_id}{secret_key}'.encode()).hexdigest()

    if signature != payload.get('signature'):
        raise SanicException("Invalid signature", status_code=400)

    async with get_async_session() as session:
        async with session.begin():
            payment_dao = PaymentDAO(session)
            
            account = await payment_dao.check_user_account(user_id, account_id)
            
            if not account:
                account = await payment_dao.create_user_account(user_id, account_id)
            
            existing_transaction = await payment_dao.check_transaction(transaction_id, account.id)
            if existing_transaction:
                raise SanicException("Transaction already exists", status_code=400)
            
            await payment_dao.create_transaction(account.id, transaction_id, amount)

    return sanic_json({"status": "success"})


@api_bp.post("/signature")
async def signature(request):
    payload = request.json
    secret_key = settings.SECRET_KEY

    transaction_id = payload.get('transaction_id')
    user_id = payload.get('user_id')
    account_id = payload.get('account_id')
    amount = payload.get('amount')
    
    signature = sha256(f'{account_id}{amount}{transaction_id}{user_id}{secret_key}'.encode()).hexdigest()

    return sanic_json({'signature': signature})


@api_bp.get('/admin/users')
async def users(request):
    user = request.ctx.user

    if not user.is_super_user:
        raise SanicException("User dont have an access", status_code=403)

    async with get_async_session() as session:
        user_dao = UserDAO(session)
        users = await user_dao.get_users()

        return sanic_json({
            'users': [
                {
                    "id": str(user.id),
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "father_name": user.father_name,
                } 
                for user in users
            ]
        })


@api_bp.post('/admin/user')
async def create_user(request):
    user = request.ctx.user

    if not user.is_super_user:
        raise SanicException("User dont have an access", status_code=403)

    payload = request.json
    print(payload)

    async with get_async_session() as session:
        user_dao = UserDAO(session)
        email = payload.get('email')
        first_name = payload.get('firstName')
        last_name = payload.get('lastName')
        father_name = payload.get('fatherName')
        password = payload.get('password')
        
        await user_dao.create_user(email, password, first_name, last_name, father_name)

    return sanic_json({"status": "success"})
