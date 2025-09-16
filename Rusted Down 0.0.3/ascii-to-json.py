import json

CHAR_MAP = {
    ".": {"type": "surface", "char": ".", "walkable": True},
    "=": {"type": "surface", "char": "=", "walkable": True},
    "═": {"type": "wall", "char": "═", "walkable": False},
    "┬": {"type": "wall", "char": "┬", "walkable": False},
    "¤": {"type": "wall", "char": "¤", "walkable": False},
    "║": {"type": "wall", "char": "║", "walkable": False},
    "╔": {"type": "wall", "char": "╔", "walkable": False},
    "╝": {"type": "wall", "char": "╝", "walkable": False},
    "╗": {"type": "wall", "char": "╗", "walkable": False},
    "╚": {"type": "wall", "char": "╚", "walkable": False},
    "═": {"type": "wall", "char": "═", "walkable": False},
    "(": {"type": "wall", "char": "(", "walkable": False},
    ")": {"type": "wall", "char": ")", "walkable": False},
    "]": {"type": "wall", "char": "]", "walkable": False},
    "[": {"type": "wall", "char": "[", "walkable": False},
    "┌": {"type": "wall", "char": "┌", "walkable": False},
    "└": {"type": "wall", "char": "└", "walkable": False},
    "┐": {"type": "wall", "char": "┐", "walkable": False},
    "┘": {"type": "wall", "char": "┘", "walkable": False},
    "─": {"type": "wall", "char": "─", "walkable": False},
    "¦": {"type": "glass", "char": "¦", "walkable": False},
    "¯": {"type": "wall", "char": "¯", "walkable": True},
    "▒": {"type": "wall", "char": "▒", "walkable": False},
    "@": {"type": "player", "char": ".", "walkable": True},  # oyuncu spawn point
    "┼": {"type": "door", "char": "┼", "walkable": True, "exit_to": "region_next"},
    " ": {"type": "wasteland", "char": "░", "walkable": False}
}

def ascii_to_json(txt_path, region_id, output_path):
    with open(txt_path, "r", encoding="utf-8") as f:
        lines = [line.rstrip("\n") for line in f]

    height = len(lines)
    width = max(len(line) for line in lines)

    objects = []
    spawn = None

    for y, line in enumerate(lines):
        for x, ch in enumerate(line):
            if ch not in CHAR_MAP:
                continue
            tile = CHAR_MAP[ch]
            if ch == "@":
                spawn = {"region": region_id, "x": x, "y": y, "type": "player"}
            elif ch == "D":
                obj = {
                    "x": x, "y": y,
                    "type": tile["type"],
                    "char": tile["char"],
                    "walkable": tile["walkable"],
                    "exit_to": tile["exit_to"]
                }
                objects.append(obj)
            elif ch != ".":
                obj = {
                    "x": x, "y": y,
                    "type": tile["type"],
                    "char": tile["char"],
                    "walkable": tile["walkable"]
                }
                objects.append(obj)

    region_json = {
        "id": region_id,
        "size": {"width": width, "height": height},
        "default_tile": {"type": "dirt", "char": ".", "walkable": True},
        "objects": objects
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(region_json, f, indent=2)

    if spawn:
        print(f"Spawn noktası: {spawn}")
    else:
        print("Oyuncu spawn noktası bulunamadı.")

# Kullanım
ascii_to_json("region.txt", "region", "region.json")
