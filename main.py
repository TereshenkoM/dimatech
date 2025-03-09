
from sanic import Sanic
from sanic.response import json

app = Sanic("my_first_app")

@app.route('/')
async def hello(request):
    return json({'hello': 'world'})

