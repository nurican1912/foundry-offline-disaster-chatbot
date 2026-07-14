"""Uygulama ayarları — tüm 'sihirli değerler' (model adı, eşik, yollar) tek yerde.

pydantic-settings'in BaseSettings'i: her alanı önce .env / ortam değişkeninden
okur, yoksa buradaki varsayılanı kullanır ve metni senin verdiğin tipe çevirir.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "emergency_rag"
    chat_model_alias: str = "qwen2.5:3b"          # Ollama; bge-m3'le birlikte 4 GB'a sığar → hızlı. Kalite kritik değil (Q&A'yi Karar 5 yapıyor).
    embedding_model_alias: str = "bge-m3"          # Ollama modeli
    top_k: int = 3
    similarity_threshold: float = 0.46             # bge-m3 ile kalibre (recall öncelikli; telefon gibi sızıntı hibritle çözülecek)
    db_path: str = "data/emergency.db"
    docs_dir: str = "docs/raw"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
