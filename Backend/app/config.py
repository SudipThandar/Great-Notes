from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # Supabase Configuration
    supabase_url: str
    supabase_key: str
    supabase_service_key: str
    supabase_jwt_secret: str
    
    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    debug: bool = True
    
    # CORS Configuration
    cors_origins: str = "http://localhost:5173"
    
    # Share Configuration
    share_base_url: str = "http://localhost:5173/share"
    
    # Validation Limits
    max_title_length: int = 500
    max_content_length: int = 50000
    
    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.cors_origins.split(",")]
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
