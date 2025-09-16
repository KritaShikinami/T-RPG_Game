from pathlib import Path
import json

def load_npc(npc_id: str) -> dict:
    path = Path("data") / "character" / "npcs" / f"{npc_id}.json"
    print("[DEBUG] NPC dosyası:", path.resolve(), path.exists())  # tam yolu ve var mı yok mu göster
    if not path.exists():
        raise FileNotFoundError(f"NPC dosyası bulunamadı: {path}")
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)
