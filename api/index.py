from mangum import Mangum


def get_fastapi_app():
	from app.main import app as _app
	return _app


app = get_fastapi_app()
handler = Mangum(app, lifespan="off")

__all__ = ("app", "handler")
