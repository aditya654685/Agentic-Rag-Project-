from functools import lru_cache
from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[2]

class Settings(BaseSettings):
    app_name: str = "Enterprise IT Support Agentic RAG Copilot"
    app_env: str = "development"

    # Euron / OpenAI API Configuration
    euri_api_key: str = Field(default="", validation_alias="EURI_API_KEY")
    openai_api_key: str = Field(default="", validation_alias="OPENAI_API_KEY")
    euron_base_url: str = Field(default="https://api.euron.one/api/v1/euri", validation_alias="EURON_BASE_URL")
    
    # Models
    openai_model: str = "gpt-4.1-mini"
    embedding_model: str = "text-embedding-3-small"

    # Tavily Web Search
    tavily_api_key: str = Field(default="", validation_alias="TAVILY_API_KEY")
    travily_api_key: str = Field(default="", validation_alias="TRAVILY_API_KEY")

    # Pinecone Vector Store
    pinecone_api_key: str = ""
    pinecone_index_name: str = "fde-it-support-rag"
    pinecone_namespace: str = "company-it-kb"

    top_k: int = 4
    max_retries: int = 1
    admin_api_key: str = "change-me"
    audit_db_path: str = str(BASE_DIR / "data" / "audit.db")
    upload_dir: str = str(BASE_DIR / "uploads")
    sample_kb_dir: str = str(BASE_DIR / "data" / "sample_kb")

    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env"),
        extra="ignore",
        populate_by_name=True,
    )

    @property
    def resolved_llm_api_key(self) -> str:
        return (self.euri_api_key or self.openai_api_key).strip()

    @property
    def resolved_tavily_api_key(self) -> str:
        return (self.tavily_api_key or self.travily_api_key).strip()


@lru_cache
def get_settings() -> Settings:
    return Settings()
