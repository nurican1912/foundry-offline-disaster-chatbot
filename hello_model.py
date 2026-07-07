from foundry_local_sdk import Configuration, FoundryLocalManager

# 1) SDK'yı başlat (singleton). app_name zorunlu.
config = Configuration(app_name="emergency_rag")
FoundryLocalManager.initialize(config)
manager = FoundryLocalManager.instance

# 2) Modeli katalogdan al, indir, belleğe yükle.
alias = "qwen2.5-1.5b"

model = manager.catalog.get_model(alias)
model.download(lambda p: print(f"\rİndiriliyor: {p:.1f}%", end="", flush=True))
print()
model.load()

# 3) Chat istemcisini al ve TEK bir Türkçe soru sor (non-streaming).
chat = model.get_chat_client()
messages = [
    {"role": "user", "content": "Deprem anında ne yapmalıyım? Kısa cevap ver."}
]
completion = chat.complete_chat(messages)
print(completion.choices[0].message.content)

# 4) Belleği boşalt.
model.unload()
