# Vercel serverless function entry point
from app.main import app

# Vercel requires the app to be named 'app' or export a handler
handler = app
