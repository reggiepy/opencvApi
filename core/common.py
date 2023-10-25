# *_*coding:utf-8 *_*
# @Author : Reggie
# @Time : 2023/2/17 13:45
import logging

import fastapi
from fastapi.openapi.docs import get_swagger_ui_oauth2_redirect_html, get_swagger_ui_html, get_redoc_html
from fastapi.routing import APIRouter
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, RedirectResponse
from starlette.staticfiles import StaticFiles

from core import settings
from py3utils.psutil_utils import Psutil

logger = logging.getLogger()

error_logger = logging.getLogger("uvicorn.error")


def init_app(api_router: APIRouter = None):
    app: fastapi.FastAPI = fastapi.FastAPI(
        title="yongfeng manage",
        debug=True,
        docs_url=None,
        redoc_url=None,
    )

    @app.on_event("startup")
    async def startup():
        logger.info(f"机器ID: {Psutil.machine_id_short()}")

    @app.on_event("shutdown")
    async def shutdown():
        pass

    async def catch_exceptions_middleware(request: Request, call_next):
        try:
            return await call_next(request)
        except Exception as e:
            error_logger.error(f"catch an error: {e}", exc_info=True)
            # you probably want some kind of logging here
            return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})

    app.middleware('http')(catch_exceptions_middleware)

    @app.get("/docs", include_in_schema=False)
    async def custom_swagger_ui_html():
        return get_swagger_ui_html(
            openapi_url=app.openapi_url,
            title=app.title + " - Swagger UI",
            oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
            swagger_js_url="/swagger/swagger-ui-bundle.js",
            swagger_css_url="/swagger/swagger-ui.css",
            swagger_favicon_url="/swagger/favicon.png",
        )

    @app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
    async def swagger_ui_redirect():
        return get_swagger_ui_oauth2_redirect_html()

    @app.get("/redoc", include_in_schema=False)
    async def redoc_html():
        return get_redoc_html(
            openapi_url=app.openapi_url,
            title=app.title + " - ReDoc",
            redoc_js_url="/swagger/redoc.standalone.js",
            redoc_favicon_url="/swagger/favicon.png",
            with_google_fonts=False
        )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    if isinstance(api_router, APIRouter):
        app.include_router(api_router)
    app.mount(
        "/", StaticFiles(
            directory=settings.STATIC_DIR,
            html=True
        ),
        name="static"
    )

    # @app.middleware("http")
    # async def add_access_control_allow_origin_header(request: Request, call_next):
    #     response = await call_next(request)
    #     origin = f"{request.url.scheme}://{request.client.host}"
    #     response.headers["access-control-allow-origin"] = origin
    #     response.headers["access-control-allow-origin"] = "http://localhost:8082"
    #     response.headers["Access-Control-Allow-Credentials"] = "false"
    #     return response

    @app.get("/", include_in_schema=False)
    def index():
        return RedirectResponse("/static/index.html")

    return app
