# Vercel serverless function entry point for FastAPI
from app.main import app

# Export the FastAPI app directly
# Vercel's Python runtime will handle ASGI automatically
app = app
