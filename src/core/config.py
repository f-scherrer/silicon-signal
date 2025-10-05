from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
import yaml, os
from pathlib import Path

class Settings(BaseSettings):
    env: str = Field(default="dev")
    data_dir: str = Field(default="./data")
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

def load_yaml(path: str = "config/config.yaml") -> dict:
    with open(path, "r") as f:
        return yaml.safe_load(f) or {}

def get_settings():
    s = Settings()
    cfg = load_yaml()
    # expand ${ENV:default}
    cfg_str = yaml.dump(cfg)
    cfg_str = os.path.expandvars(cfg_str)
    cfg = yaml.safe_load(cfg_str)
    Path(s.data_dir).mkdir(parents=True, exist_ok=True)
    return s, cfg
