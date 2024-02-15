import os
import uvicorn

from configs import Config

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from fastapi.openapi.utils import get_openapi

from starlette import status
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from starlette.exceptions import HTTPException
from sqlalchemy.exc import SQLAlchemyError


from db.database import session
from routers import *

ALL_ROUTERS = [any_route]
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_app():
    api_app = FastAPI(title=str(Config.TITLE), default_response_class=JSONResponse)

    @api_app.get("/", include_in_schema=False, summary=str(Config.DESCRIPTION))
    async def home():
        return RedirectResponse(url="/docs")

    for router in list(ALL_ROUTERS):
        api_app.include_router(router)

    openapi_schema = get_openapi(
        title=Config.TITLE,
        description=Config.DESCRIPTION,
        version="0.0.1",
        routes=api_app.routes,
    )

    if "components" in openapi_schema:
        openapi_schema["components"]["securitySchemes"] = {
            "Bearer Auth": {
                "type": "apiKey",
                "in": "header",
                "name": "Authorization",
                "description": "Enter: **'Bearer &lt;JWT&gt;'**, where JWT is the access token",
            }
        }

    for route in api_app.routes:
        path = str(getattr(route, "path"))
        if route.include_in_schema:
            methods = [method.lower() for method in getattr(route, "methods")]
            for method in methods:
                if path not in Config.INSECURE_PATHS:
                    openapi_schema["paths"][path][method]["security"] = [
                        {"Bearer Auth": []}
                    ]
                    openapi_schema["paths"][path][method]["responses"]["403"] = {
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        },
                        "description": "Returned if user is unauthorized.",
                    }

    api_app.openapi_schema = openapi_schema
    return api_app


def http_error_handler(request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code, content={"message": str(exc.detail)}
    )


def http_expection_handler(request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST, content={"message": exc.__str__()}
    )


app = create_app()
app.add_middleware(
    CORSMiddleware,
    **{
        "allow_origins": ["*"],
        "allow_credentials": True,
        "allow_methods": ["*"],
        "allow_headers": ["*"],
    }
)
# app.add_middleware(AuthHeaderMiddleware)

app.add_exception_handler(SQLAlchemyError, http_expection_handler)
app.add_exception_handler(HTTPException, http_error_handler)
app.add_exception_handler(Exception, http_error_handler)


def update_alembic():
    from sqlalchemy import text

    try:
        result = session.execute(
            text(
                "SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = "
                "'alembic_version') AS table_existence;"
            )
        )
        if result.first()[0]:
            session.execute(text("delete from alembic_version;"))
            session.commit()
    except Exception as e:
        print(e)
    finally:
        run_command = "python -m alembic stamp head;"
        run_command += (
            "python -m alembic revision --autogenerate;python -m alembic upgrade head;"
        )
        os.system(run_command)


if __name__ == "__main__":
    update_alembic()
    uvicorn_config = {
        "app": "app:app",
        "host": "0.0.0.0",
        "port": 41556,
        "log_level": "info",
        "reload": True,
    }
    uvicorn.Server(uvicorn.Config(**uvicorn_config)).run()
