from sanic import Sanic
from sanic.response import json

app = Sanic()


@app.route('/')
async def home(request):
    return json({"hello ": "sanic"})


if __name__ == "__main__":
    app.run()
