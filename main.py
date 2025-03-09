from sanic import Sanic
from sanic_ext import Extend
from app.routes.pages import pages_bp
from app.routes.auth import auth_bp
from app.routes.api import api_bp
from app.middlewares import setup_middlewares 

app = Sanic("PaymentApp")

app.config.TEMPLATING_ENABLE_ASYNC = True
app.config.TEMPLATING_PATH_TO_TEMPLATES = "app/templates"

Extend(app)

setup_middlewares(app)

app.blueprint([pages_bp, auth_bp, api_bp])
app.static("/static", "app/static")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True, auto_reload=True)
