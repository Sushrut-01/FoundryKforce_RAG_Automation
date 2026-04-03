"""
Configuration management for Foundry RAG Testing Framework
Loads settings from .env and validates them
"""

from pydantic import BaseModel, Field
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

class AzureConfig(BaseModel):
    """Azure AI Foundry Configuration"""
    ai_project_endpoint: str = Field(..., alias="AZURE_AI_PROJECT_ENDPOINT")
    subscription_id: str = Field(..., alias="AZURE_SUBSCRIPTION_ID")
    resource_group: str = Field(..., alias="AZURE_RESOURCE_GROUP")
    
    class Config:
        populate_by_name = True

class OpenAIConfig(BaseModel):
    """Azure OpenAI Configuration"""
    api_key: str = Field(..., alias="AZURE_OPENAI_API_KEY")
    endpoint: str = Field(..., alias="AZURE_OPENAI_ENDPOINT")
    model: str = Field(default="gpt-4", alias="AZURE_OPENAI_MODEL")
    deployment_name: str = Field(..., alias="AZURE_OPENAI_DEPLOYMENT_NAME")
    
    class Config:
        populate_by_name = True

class LocalStorageConfig(BaseModel):
    """Local Storage Configuration"""
    kb_path: str = Field(default="./knowledge_base", alias="LOCAL_KB_PATH")
    vector_db_path: str = Field(default="./vector_db/playready", alias="LOCAL_VECTOR_DB_PATH")
    log_path: str = Field(default="./logs", alias="LOCAL_LOG_PATH")
    results_path: str = Field(default="./results", alias="LOCAL_RESULTS_PATH")
    
    class Config:
        populate_by_name = True

class RAGConfig(BaseModel):
    """RAG Configuration"""
    vector_db_path: str = Field(default="./vector_db/playready", alias="VECTOR_DB_PATH")
    knowledge_base_path: str = Field(default="./knowledge_base", alias="KNOWLEDGE_BASE_PATH")
    embedding_model: str = Field(
        default="sentence-transformers/all-MiniLM-L6-v2",
        alias="EMBEDDING_MODEL"
    )
    chunk_size: int = Field(default=1000, alias="CHUNK_SIZE")
    chunk_overlap: int = Field(default=200, alias="CHUNK_OVERLAP")
    
    class Config:
        populate_by_name = True

class TestingConfig(BaseModel):
    """Testing Configuration"""
    timeout: int = Field(default=30, alias="TEST_TIMEOUT")
    concurrent_requests: int = Field(default=10, alias="CONCURRENT_REQUESTS")
    retry_attempts: int = Field(default=3, alias="RETRY_ATTEMPTS")
    test_mode: str = Field(default="local", alias="TEST_MODE")
    
    class Config:
        populate_by_name = True

class FoundryConfig(BaseModel):
    """Foundry Upload Configuration"""
    project_id: Optional[str] = Field(default=None, alias="FOUNDRY_PROJECT_ID")
    experiment_name: Optional[str] = Field(default="playready-rag-testing", alias="FOUNDRY_EXPERIMENT_NAME")
    upload_results: bool = Field(default=True, alias="UPLOAD_RESULTS_TO_FOUNDRY")
    
    class Config:
        populate_by_name = True

class Config(BaseModel):
    """Complete Configuration"""
    azure: AzureConfig
    openai: OpenAIConfig
    local_storage: LocalStorageConfig
    rag: RAGConfig
    testing: TestingConfig
    foundry: FoundryConfig
    
    @staticmethod
    def from_env() -> "Config":
        """Load configuration from environment variables"""
        return Config(
            azure=AzureConfig(
                AZURE_AI_PROJECT_ENDPOINT=os.getenv("AZURE_AI_PROJECT_ENDPOINT"),
                AZURE_SUBSCRIPTION_ID=os.getenv("AZURE_SUBSCRIPTION_ID"),
                AZURE_RESOURCE_GROUP=os.getenv("AZURE_RESOURCE_GROUP")
            ),
            openai=OpenAIConfig(
                AZURE_OPENAI_API_KEY=os.getenv("AZURE_OPENAI_API_KEY"),
                AZURE_OPENAI_ENDPOINT=os.getenv("AZURE_OPENAI_ENDPOINT"),
                AZURE_OPENAI_MODEL=os.getenv("AZURE_OPENAI_MODEL", "gpt-4"),
                AZURE_OPENAI_DEPLOYMENT_NAME=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
            ),
            local_storage=LocalStorageConfig(
                LOCAL_KB_PATH=os.getenv("LOCAL_KB_PATH", "./knowledge_base"),
                LOCAL_VECTOR_DB_PATH=os.getenv("LOCAL_VECTOR_DB_PATH", "./vector_db/playready"),
                LOCAL_LOG_PATH=os.getenv("LOCAL_LOG_PATH", "./logs"),
                LOCAL_RESULTS_PATH=os.getenv("LOCAL_RESULTS_PATH", "./results")
            ),
            rag=RAGConfig(
                VECTOR_DB_PATH=os.getenv("VECTOR_DB_PATH", "./vector_db/playready"),
                KNOWLEDGE_BASE_PATH=os.getenv("KNOWLEDGE_BASE_PATH", "./knowledge_base"),
                EMBEDDING_MODEL=os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2"),
                CHUNK_SIZE=int(os.getenv("CHUNK_SIZE", "1000")),
                CHUNK_OVERLAP=int(os.getenv("CHUNK_OVERLAP", "200"))
            ),
            testing=TestingConfig(
                TEST_TIMEOUT=int(os.getenv("TEST_TIMEOUT", "30")),
                CONCURRENT_REQUESTS=int(os.getenv("CONCURRENT_REQUESTS", "10")),
                RETRY_ATTEMPTS=int(os.getenv("RETRY_ATTEMPTS", "3")),
                TEST_MODE=os.getenv("TEST_MODE", "local")
            ),
            foundry=FoundryConfig(
                FOUNDRY_PROJECT_ID=os.getenv("FOUNDRY_PROJECT_ID"),
                FOUNDRY_EXPERIMENT_NAME=os.getenv("FOUNDRY_EXPERIMENT_NAME", "playready-rag-testing"),
                UPLOAD_RESULTS_TO_FOUNDRY=os.getenv("UPLOAD_RESULTS_TO_FOUNDRY", "true").lower() == "true"
            )
        )

# Load configuration
config = Config.from_env()