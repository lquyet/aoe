import os


class Settings:
    TEAM_ID: int = os.getenv("TEAM_ID", 0)
    GAME_ID = os.getenv("GAME_ID", 0)
    URL = os.getenv("URL", "https://procon2023.duckdns.org/api/player")
    TOKEN = os.getenv("TOKEN", "")

    REDIS_PORT = os.getenv("REDIS_PORT", 0)
    REDIS_DB = os.getenv("REDIS_DB", 0)
    REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "")


settings = Settings()
