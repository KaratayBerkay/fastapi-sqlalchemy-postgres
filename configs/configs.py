import datetime


class Config:
    INSECURE_PATHS = [
        "/",
        "/openapi.json",
        "/openapi.json_files",
        "/docs",
        "/redoc",
    ]
    APP_NAME = "evyos-data-manager-service"
    TITLE = "Data Manager Read API Gateway"
    DESCRIPTION = "Data Manager for live data transfer service. This api is serves only to evyos hardwares."
    # APP_URL = "https://www.hag.evyos.com"


class Auth:
    SECRET_KEY_72 = (
        "t3sUAmjTGeTgDc6dAUrB41u2SNg0ZHzj4HTjem95y3fRH1nZXOHIBj163kib6iLybT0gLaxq"
    )
    SECRET_KEY_96 = "7ct8VpiwaP1hR2bVSet4dEEAgepuTZUOnO1QxOgKyDqBR2PkqNhcubSrbUUigQKoQA1PBoeeQn5ZCo24pESmVtKs76nA4EKq"
    SECRET_KEY_144 = (
        "R2p5Rq6KCr6PCfjFYUeH1keF2VWHFEuqINVjBGGnvRA2m10pYUKqfOtIGBcaj2v5wZmElDndzSHGOS7roQsoTelPSok0"
        + "qqMucurMWE0FGexGpFuJkfPEm9tH2OjMOqegvEetpSVywH0W4Kh4"
    )

    # ALGORITHM = "HS256"
    # TOKEN_EXPIRE_MINUTES_1 = datetime.timedelta(minutes=1)
    # TOKEN_EXPIRE_MINUTES_15 = datetime.timedelta(minutes=15)
    # TOKEN_EXPIRE_MINUTES_30 = datetime.timedelta(minutes=30)
    # TOKEN_EXPIRE_DAY_1 = datetime.timedelta(days=1)
    # TOKEN_EXPIRE_DAY_5 = datetime.timedelta(days=5)
    # TOKEN_EXPIRE_DAY_15 = datetime.timedelta(days=15)
    # TOKEN_EXPIRE_DAY_30 = datetime.timedelta(days=30)


class Database:
    SQL: str = "postgresql+psycopg2"
    # SQL: str = 'postgresql'
    USERNAME: str = "example_user"
    PASSWORD: str = "example_password"
    HOST: str = "postgres_hardware"
    PORT: str = "5432"
    DATABASE_NAME: str = "hag_database"
    DATABASE_URL = f"{SQL}://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE_NAME}"
