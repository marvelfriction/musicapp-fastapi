from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str
    token_password_key: str
    cloudinary_cloud_name: str
    cloudinary_api_key: str
    cloudinary_api_secret: str

    model_config = SettingsConfigDict(env_file=".env")

# Singleton-style
settings = Settings()
# This will load the settings from the .env file and make them available globally
