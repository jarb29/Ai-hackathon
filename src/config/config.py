from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")
    app_host: str = Field(default="0.0.0.0", env="APP_HOST")
    app_port: int = Field(default=9000, env="APP_PORT")
    app_debug: bool = Field(default=False, env="APP_DEBUG")
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    mcp_server_path: str = Field(default="npx", env="MCP_SERVER_PATH")
    mcp_server_args: str = Field(
        default="@modelcontextprotocol/server-chrome-devtools", env="MCP_SERVER_ARGS"
    )

    class Config:
        env_file = ".env"


settings = Settings()