from sanic import Blueprint
from sanic_ext import render

pages_bp = Blueprint("pages", url_prefix="")


@pages_bp.get("/")
async def index_page(request):
    return await render("index.html")

@pages_bp.get("/login")
async def login_page(request):
    return await render("login.html")

@pages_bp.get('/signature')
async def signature_page(request):
    return await render("signature.html")