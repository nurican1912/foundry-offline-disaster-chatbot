"""Uygulama ayarları — tüm 'sihirli değerler' (model adı, eşik, yollar) tek yerde.

pydantic-settings'in BaseSettings'i: her alanı önce .env / ortam değişkeninden
okur, yoksa buradaki varsayılanı kullanır ve metni senin verdiğin tipe çevirir.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "emergency_rag"
    chat_model_alias: str = "qwen3-4b"
    embedding_model_alias: str = "qwen3-embedding-0.6b"
    top_k: int = 3
    similarity_threshold: float = 0.5
    db_path: str = "data/emergency.db"
    docs_dir: str = "docs/raw"
    # Model cache dizini. Boşsa Foundry'nin varsayılanı kullanılır.
    # Makineye özel yol (ör. D: sürücüsü) .env'den MODEL_CACHE_DIR ile verilir.
    model_cache_dir: str = ""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
