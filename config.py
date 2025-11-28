<<<<<<< HEAD
# app/config.py

class Settings:
    app_name: str = "RESTAPI"
    debug: bool = True

    # БД
    database_url: str = "sqlite:///./sql_app.db"

    # JWT / OAuth2
    secret_key: str = "change_me_in_env"  # ЗАМЕНИТЬ на нормальный секрет
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24  # 1 день


settings = Settings()
=======
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")
SECRET_KEY = os.getenv("SECRET_KEY", "change-me-please-use-env")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
>>>>>>> main
