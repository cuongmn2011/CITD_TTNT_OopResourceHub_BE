from mangum import Mangum
from app.main import app as fastapi_app

# Expose FastAPI app for ASGI-compatible runtimes
app = fastapi_app

# Wrap FastAPI app with Mangum for serverless compatibility
handler = Mangum(fastapi_app, lifespan="off")
