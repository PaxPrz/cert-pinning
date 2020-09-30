from starlette.applications import Starlette
from starlette.responses import JSONResponse, Response, PlainTextResponse
from starlette.routing import Route
from starlette.exceptions import HTTPException
from starlette.middleware.errors import ServerErrorMiddleware
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware

async def error_handler(req, exc):
    print("exception error handler")

async def server_error_handler(req, exc):
    print("Server error handler")
    print(req, exc)

def setup_app(app):
    # app.add_exception_handler(HTTPException, error_handler)
    # app.add_middleware(ServerErrorMiddleware, handler=server_error_handler)
    app.add_middleware(ServerErrorMiddleware)
    app.add_middleware(HTTPSRedirectMiddleware)
    return app

async def home(request):
    return PlainTextResponse('<h1>Hello world!</h1>', status_code=200)

app = Starlette(debug=True)
app = setup_app(app)
app.add_route('/', home, methods=['GET'])

