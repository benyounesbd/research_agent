from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    gemini_api_key: str
    tavily_api_key: str

    langsmith_tracing: bool = False
    langsmith_api_key: str | None = None
    langsmith_project: str = "research-agent"
    langsmith_endpoint: str = "https://eu.api.smith.langchain.com"

    llm_model: str = "gemini-2.5-flash"
    max_sources: int = 3
    max_retries: int = 2

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()