from sanic import Blueprint
from sanic.response import redirect
from sanic_ext import render

pages_bp = Blueprint("pages", url_prefix="")


@pages_bp.get("/")
async def index_page(request):
    user = request.ctx.user 
    
    if not user:
        return redirect("/login")
    
    return await render("index.html")


@pages_bp.get("/login")
async def login_page(request):
    return await render("login.html")


@pages_bp.get('/signature')
async def signature_page(request):
    user = request.ctx.user
    
    if not user:
        return redirect("/login")
    
    return await render("signature.html")


@pages_bp.get('/admin')
async def admin_page(request):
    user = request.ctx.user

    if not user:
        return redirect("/login")
    if not user.is_super_user:
        return redirect("/")

    return await render("admin.html")


