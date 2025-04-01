class Config:
    DB_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/contact_book"
    JWT_SECRET = "your_secret_key"
    JWT_ALGORITHM = "HS256"
    JWT_EXPIRATION_SECONDS = 3600
    JWT_REFRESH_EXPIRATION_SECONDS = 3600 * 24 * 7  # 7 days


config = Config
