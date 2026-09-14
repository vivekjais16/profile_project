"""
WSGI / ASGI compatibility entrypoint for cloud hosting providers
Author: Vivek Jaiswal <vivekjais16@gmail.com>
"""
from app.main import app

# Export application instance
application = app
