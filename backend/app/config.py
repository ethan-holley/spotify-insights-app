from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    spotify_client_id: str
    spotify_client_secret: str
    spotify_redirect_uri: str = "http://127.0.0.1:8000/auth/callback"
    frontend_url: str = "http://localhost:5173"
    secret_key: str = "change_me"

    class Config:
        env_file = ".env"


settings = Settings()
