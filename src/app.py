from fastapi import FastAPI
from src.common.api.common import router as common_api_router
from src.config import config


def create_app() -> FastAPI:
    app = FastAPI(
        title='Call Service',
        docs_url='/api/docs',
        debug=config.debug,
        version=config.version,
        redirect_slashes=False,
    )

    include_routers(app=app)

    return app

def include_routers(*, app: FastAPI) -> None:
    app.include_router(common_api_router)