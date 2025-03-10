from hashlib import sha256

from pydantic import ValidationError
from sanic import Blueprint, response
from sanic.exceptions import SanicException

from app.core.config import settings
from app.daos.payment_dao import PaymentDAO
from app.daos.user_dao import UserDAO
from app.database.config import get_async_session
from app.schemas.api_shemas import (
    AccountInfoResponse, AccountResponse,
    AdminAccountInfo, AdminCreateUserRequest,
    AdminDeleteUserRequest,
    AdminUpdateUserRequest,
    AdminUserListResponse, AdminUserResponse,
    SignatureRequest, TransactionCreateRequest,
    TransactionListResponse,
    TransactionResponse, UserInfoResponse
)

api_bp = Blueprint("api", url_prefix="/api")

@api_bp.get("/user_info")
async def user_info(request):
    user = request.ctx.user
    return response.json(
        UserInfoResponse(
            user_id=str(user.id),
            user_fullname=user.get_fullname(),
            email=user.email
        ).model_dump_json()
    )

@api_bp.get("/account_info")
async def account_info(request):
    user = request.ctx.user

    async with get_async_session() as session:
        payment_dao = PaymentDAO(session)
        accounts = await payment_dao.get_account_by_user_id(user.id)
        
        return response.json(
            AccountInfoResponse(
                accounts=[
                    AccountResponse(
                        id=str(account.id),
                        balance=account.balance,
                        created_at=account.created_at
                    ) for account in accounts
                ]
            ).model_dump_json()
        )

@api_bp.get("/transaction")
async def get_transaction(request):
    user = request.ctx.user

    async with get_async_session() as session:
        payment_dao = PaymentDAO(session)
        accounts = await payment_dao.get_account_by_user_id(user.id)
        transactions = await payment_dao.get_transaction_by_accounts(accounts)
        
        return response.json(
            TransactionListResponse(
                transactions=[
                    TransactionResponse(
                        id=transaction.id,
                        transaction_id=transaction.transaction_id,
                        account_id=transaction.account_id,
                        amount=transaction.amount,
                        created_at=transaction.created_at
                    ) for transaction in transactions
                ]
            ).model_dump_json()
        )

@api_bp.post("/transaction")
async def create_transaction(request):
    try:
        payload = TransactionCreateRequest(**request.json)
    except ValidationError as e:
        raise SanicException(e.json(), status_code=400)

    secret_key = settings.SECRET_KEY
    signature = sha256(
        f'{payload.account_id}{payload.amount}{payload.transaction_id}{payload.user_id}{secret_key}'.encode()
    ).hexdigest()

    if signature != payload.signature:
        raise SanicException("Invalid signature", status_code=400)

    async with get_async_session() as session:
        async with session.begin():
            payment_dao = PaymentDAO(session)
            account = await payment_dao.check_user_account(str(payload.user_id), str(payload.account_id))
            
            if not account:
                account = await payment_dao.create_user_account(str(payload.user_id), str(payload.account_id))
            
            existing_transaction = await payment_dao.check_transaction(payload.transaction_id, account.id)
            if existing_transaction:
                raise SanicException("Transaction already exists", status_code=400)
            
            await payment_dao.create_transaction(account.id, payload.transaction_id, payload.amount)

    return response.json({"status": "success"})

@api_bp.post("/signature")
async def signature(request):
    try:
        payload = SignatureRequest(**request.json)
    except ValidationError as e:
        raise SanicException(e.json(), status_code=400)

    secret_key = settings.SECRET_KEY
    signature = sha256(
        f'{payload.account_id}{payload.amount}{payload.transaction_id}{payload.user_id}{secret_key}'.encode()
    ).hexdigest()

    return response.json({'signature': signature})

@api_bp.get('/admin/users')
async def users(request):
    user = request.ctx.user

    if not user.is_super_user:
        raise SanicException("User don't have access", status_code=403)

    async with get_async_session() as session:
        user_dao = UserDAO(session)
        users_list = await user_dao.get_users()
        payment_dao = PaymentDAO(session)
        
        users_payload = []
        for user in users_list:
            accounts = await payment_dao.get_account_by_user_id(user.id)
            users_payload.append(
                AdminUserResponse(
                    id=str(user.id),
                    email=user.email,
                    first_name=user.first_name,
                    last_name=user.last_name,
                    father_name=user.father_name,
                    accounts=[
                        AdminAccountInfo(
                            account_id=str(account.id),
                            balance=account.balance
                        ) for account in accounts
                    ]
                )
            )

        return response.json(AdminUserListResponse(users=users_payload).model_dump_json())

@api_bp.post('/admin/user')
async def create_user(request):
    user = request.ctx.user
    if not user.is_super_user:
        raise SanicException("User don't have access", status_code=403)

    try:
        payload = AdminCreateUserRequest(**request.json)
    except ValidationError as e:
        raise SanicException(e.json(), status_code=400)

    async with get_async_session() as session:
        user_dao = UserDAO(session)
        await user_dao.create_user(
            email=payload.email,
            password=payload.password,
            first_name=payload.first_name,
            last_name=payload.last_name,
            father_name=payload.father_name
        )

    return response.json({"status": "success"}, status=200)

@api_bp.patch('/admin/user')
async def update_user(request):
    user = request.ctx.user
    if not user.is_super_user:
        raise SanicException("User don't have access", status_code=403)

    try:
        payload = AdminUpdateUserRequest(**request.json)
    except ValidationError as e:
        raise SanicException(e.json(), status_code=400)

    async with get_async_session() as session:
        user_dao = UserDAO(session)
        await user_dao.update_user(
            email=payload.email,
            password=payload.password,
            first_name=payload.first_name,
            last_name=payload.last_name,
            father_name=payload.father_name
        )

    return response.json({"status": "success"}, status=200)

@api_bp.delete('/admin/user')
async def delete_user(request):
    user = request.ctx.user
    if not user.is_super_user:
        raise SanicException("User don't have access", status_code=403)
    print(request.json)
    try:
        payload = AdminDeleteUserRequest(**request.json)
    except ValidationError as e:
        raise SanicException(e.json(), status_code=400)

    async with get_async_session() as session:
        user_dao = UserDAO(session)
        await user_dao.delete_user(str(payload.user_id))

    return response.json({"status": "success"}, status=200)