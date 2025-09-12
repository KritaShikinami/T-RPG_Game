import math, random, json, os, shutil
from pathlib import Path
from typing import List, Tuple

# --- Zemin tipleri ---
SURFACE_TYPES = {
    "ALUMINUM": {
        "friction": 0.35,
        "line_color": (200, 200, 200),
        "durability": 0.70
    },
    "ALUMINUM-PLATE": {
        "friction": 0.40,
        "line_color": (180, 180, 180),
        "durability": 0.85
    },
    "STEEL": {
        "friction": 0.45,
        "line_color": (160, 160, 160),
        "durability": 0.95
    },
    "STEEL-PLATE": {
        "friction": 0.50,
        "line_color": (140, 140, 140),
        "durability": 0.90
    },
    "STAINLESS-STEEL": {
        "friction": 0.40,
        "line_color": (180, 180, 180),
        "durability": 0.98
    },
    "STAINLESS-STEEL-PLATE": {
        "friction": 0.45,
        "line_color": (160, 160, 160),
        "durability": 0.95
    },
    "COPPER": {
        "friction": 0.55,
        "line_color": (184, 115, 51),
        "durability": 0.80
    },
    "COPPER-PLATE": {
        "friction": 0.60,
        "line_color": (160, 90, 40),
        "durability": 0.85
    },
    "LEAD": {
        "friction": 0.65,
        "line_color": (105, 105, 105),
        "durability": 0.60
    },
    "LEAD-PLATE": {
        "friction": 0.70,
        "line_color": (85, 85, 85),
        "durability": 0.65
    },    
    "BRICK": {
        "friction": 0.65,
        "line_color": (187, 34, 34),
        "durability": 0.75
    },    
    "ASPHALT": {
        "friction": 0.70,
        "line_color": (50, 50, 50),
        "durability": 0.85
    },
    "CONCRETE": {
        "friction": 0.55,
        "line_color": (128, 128, 128),
        "durability": 0.90
    },
    "SAND": {
        "friction": 0.45,
        "line_color": (194, 178, 128),
        "durability": 0.25
    },
    "DIRT": {
        "friction": 0.50,
        "line_color": (101, 67, 33),
        "durability": 0.40
    },
    "GLASS": {
        "friction": 0.35,
        "line_color": (251, 206, 235),
        "durability": 0.50
    },
    "PLASTIC": {
        "friction": 0.20,
        "line_color": (255, 255, 255),
        "durability": 0.60
    },
    "MARBLE": {
        "friction": 0.30,
        "line_color": (220, 220, 220),
        "durability": 0.90
    }
}

OBJECT_TYPES = {
    "HIGHWAYMAN": {
            "weight": 1500,
            "max_speed": 200,
            "wheel_friction": 0.50,
            "total_durability": 1000,
            "front_durability": 500,
            "rear_durability": 500
    }
}

CHARACTER_TYPES = {
    "CHARACTER": {
        "hp_total": 65,
        "the_eyes_hp": 5,
        "the_head_hp": 10,
        "the_body_hp": 20,
        "the_arm_hp": 15,
        "the_leg_hp": 15,
        "action_point": 10
    }
}

GUN_TYPES = {
    "10MM_PISTOL": {
        "max_ammo": 128,
        "magazine": 6,
        "max_damage": 10,
        "min_damage": 5,
        "max_range": 20,
        "ammo_type": "10MM",
        "ap_cost": 5
    },
    "12GAUGE_SHOTGUN": {
        "max_ammo": 42,
        "magazine": 7,
        "max_damage": 20,
        "min_damage": 10,
        "max_range": 10,
        "ammo_type": "12GAUGE",
        "ap_cost": 6
    }
}

COLOR_TYPES = {
    "SILVER": (192, 192, 192),
    "GRAY": (128, 128, 128),
    "DARK_GRAY": (64, 64, 64),
    "WHITE": (255, 255, 255),
    "BLACK": (0, 0, 0),
    "RED": (255, 0, 0),
    "DARK_RED": (139, 0, 0),
    "ORANGE": (255, 165, 0),
    "BROWN": (101, 67, 33),
    "DARK_BROWN": (80, 40, 20),
    "YELLOW": (255, 255, 0),
    "GOLD": (255, 215, 0),
    "LIGHT_YELLOW": (255, 255, 153),
    "GREEN": (0, 128, 0),
    "DARK_GREEN": (0, 100, 0),
    "LIME": (50, 205, 50),
    "BLUE": (0, 0, 255),
    "NAVY": (0, 0, 128),
    "SKY_BLUE": (135, 206, 235),
    "CYAN": (0, 255, 255),
    "TEAL": (0, 128, 128),
    "PURPLE": (128, 0, 128),
    "VIOLET": (238, 130, 238),
    "MAGENTA": (255, 0, 255),
    "PINK": (255, 192, 203),
    "ROSE": (255, 102, 204),
    "BEIGE": (245, 245, 220),
    "SAND": (194, 178, 128),
    "MARBLE": (220, 220, 220),
    "COPPER": (184, 115, 51),
    "BRICK": (187, 34, 34),
    "GLASS": (251, 206, 235)
}

LIQUID_TYPES = {
    "WATER": {
        "scale": 2.41e-5,
        "activation": 247.8,
        "correction_coefficient": 140
    },
    "ETHANOL": {
        "scale": 1.20e-4,
        "activation": 420.0,
        "correction_coefficient": 140
    },
    "METHANOL": {
        "scale": 7.20e-5,
        "activation": 370.0,
        "correction_coefficient": 145
    },
    "GLYCERIN": {
        "scale": 1.10e-2,
        "activation": 900.0,
        "correction_coefficient": 150
    },
    "HONEY": {
        "scale": 2.50e-2,
        "activation": 1200.0,
        "correction_coefficient": 160
    },
    "ENG_OIL_O": {
        "scale": 3.50e-3,
        "activation": 700.0,
        "correction_coefficient": 160
    },
    "ENG_OIL_S": {
        "scale": 1.80e-3,
        "activation": 600.0,
        "correction_coefficient": 160
    }
}

# --- Fizik fonksiyonları ---
def Friction(q, m, a, g):
    if (m * a) > (q * m * g):
        return (m * a) - (q * m * g)
    else:
        return (q * m * g) - (m * a)

def Friction_Static(q, m, g):
    return max(q * m * g, 0)

def collision(m1, m2, v1, v2, type):
    if (type == 1):
        v1f = ((m1 - m2) / (m1 + m2)) * v1 + (2 * m2 / (m1 + m2)) * v2
        v2f = (2 * m1 / (m1 + m2)) * v1 + ((m2 - m1) / (m1 + m2)) * v2
        return v1f, v2f
    elif (type == 0):
        return ((m1 * v1) + (m2 * v2)) / (m1 + m2)
    else:
        return "ERROR 1: Parametreler yanlış (Muhtemel 'TYPE' girdisi)"

def collision_result(v1d, v2d, v1m, v2m, v1f, v2f, vf, type):
    if (type == 1):
        return v1f, v2f
    elif (type == 0):
        if (v1m == v2m):
            energy = 0.5 * v1m * (vf ** 2)
            damage_v1 = energy * (1 - v1d)
            damage_v2 = energy * (1 - v2d)
            return damage_v1, damage_v2
        else:
            energy = 0.5 * ((v1m + v2m) / 2) * (vf ** 2)
            energy = 0.5 * v1m * (vf ** 2)
            damage_v1 = energy * (1 - v1d)
            damage_v2 = energy * (1 - v2d)
            return damage_v1, damage_v2
    else:
        return "ERROR 2: Parametreler yanlış (Muhtemel 'TYPE' girdisi)"

def check_collision(box1, box2, m1, m2, v1, v2):
    if box1.colliderect(box2):
        return collision(m1, m2, v1, v2)
    return v1, v2

def liquid_friction(s, a, c, t, m, ac):
    p = s * (10 ** (a / t - c))
    f = (m * ac) - p
    return f

def acceleration(q, v, m, g): # Araç için
    F_Force = Friction_Static(q, m, g)
    D_Force = m * v
    if (D_Force > F_Force):
        N_Force = (D_Force - F_Force)
        return N_Force / m
    else:
        N_Force = (F_Force - D_Force)
        return N_Force / m

# --- V.A.T.S. ---

BODY_PARTS = {
    "the_eyes": {"hit_chance": 0.25, "damage_multiplier": 2.0, "effect": "accuracy_down"},
    "the_head": {"hit_chance": 0.50, "damage_multiplier": 1.5, "effect": None},
    "the_body": {"hit_chance": 0.85, "damage_multiplier": 1.0, "effect": None},
    "the_arm": {"hit_chance": 0.65, "damage_multiplier": 0.8, "effect": "accuracy_down"},
    "the_leg": {"hit_chance": 0.60, "damage_multiplier": 0.9, "effect": "speed_down"}
}

def calculate_distance(pos1, pos2):
    return math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)

def vats_attack(attacker, target, weapon, body_part):
    part_data = BODY_PARTS[body_part]
    distance = calculate_distance(attacker["position"], target["position"])

    if distance > weapon["max_range"]:
        return f"Target out of range! ({distance:.1f} > {weapon['max_range']})"

    if attacker["action_point"] < weapon["ap_cost"]:
        return "Yetersiz AP!"

    hit_roll = random.random()
    effective_hit_chance = part_data["hit_chance"] * attacker["accuracy"]

    crit = random.random() <= 0.10

    if hit_roll <= effective_hit_chance:
        damage = random.randint(weapon["min_damage"], weapon["max_damage"])
        damage *= part_data["damage_multiplier"]
        if crit:
            damage *= 2

        target[body_part + "_hp"] = max(0, target[body_part + "_hp"] - damage)
        attacker["action_point"] -= weapon["ap_cost"]
        if part_data["effect"] == "accuracy_down":
            target["accuracy"] = max(0.1, target["accuracy"] - 0.2)
        elif part_data["effect"] == "speed_down":
            target["speed_penalty"] = True

        if crit:
            return f"CRITICAL! {body_part} is hit! {damage:.1f} damage dealt. Distance: {distance:.1f}"
        else:
            return f"{body_part} is hit! {damage:.1f} damage dealt. Distance: {distance:.1f}"
    else:
        attacker["action_point"] -= weapon["ap_cost"]
        return f"{body_part} missed. Distance: {distance:.1f}"

def move_character(character, steps):
    if abs(steps) > 10:
        return "Max 10 adım ileri/geri gidebilirsin."
    cost = abs(steps)
    if character["action_point"] < cost:
        return "Yetersiz AP!"
    character["position"] = (character["position"][0] + steps, character["position"][1])
    character["action_point"] -= cost
    return f"{steps} adım hareket ettin. Yeni pozisyon: {character['position']}"

def next_turn(encounter):
    encounter["turn_index"] = (encounter["turn_index"] + 1) % len(encounter["participants"])
    current = encounter["participants"][encounter["turn_index"]]
    current["action_point"] = 10
    return current

# --- RENDER MAP ---

DATA = Path("data")

def load_json(p: Path):
    with p.open("r", encoding="utf-8") as f:
        return json.load(f)

class Tile:
    def __init__(self, ch: str, walkable: bool, ttype: str = "grass"):
        self.char = ch
        self.walkable = walkable
        self.type = ttype

class Region:
    def __init__(self, region_id: str, width: int, height: int, default_tile: Tile):
        self.id = region_id
        self.width = width
        self.height = height
        self.grid: List[List[Tile]] = [
            [Tile(default_tile.char, default_tile.walkable, default_tile.type) for _ in range(width)]
            for _ in range(height)
        ]

    def apply_objects(self, objects: List[dict]):
        for obj in objects:
            x, y = obj["x"], obj["y"]
            if 0 <= x < self.width and 0 <= y < self.height:
                ch = obj.get("char", "#")
                walk = obj.get("walkable", False)
                ttype = obj.get("type", "obstacle")
                self.grid[y][x] = Tile(ch, walk, ttype)

    def in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def can_walk(self, x: int, y: int) -> bool:
        return self.in_bounds(x, y) and self.grid[y][x].walkable

def load_region(region_id: str) -> Region:
    regions_cfg = load_json(DATA / "map" / "regions.json")
    region_meta = next(r for r in regions_cfg["regions"] if r["id"] == region_id)

    w = region_meta["size"]["width"]
    h = region_meta["size"]["height"]
    dt = region_meta["default_tile"]
    default_tile = Tile(dt.get("char", "."), dt.get("walkable", True), dt.get("type", "grass"))

    region = Region(region_id, w, h, default_tile)

    # Optional sparse objects
    region_file = DATA / "map" / "regions" / f"{region_id}.json"
    if region_file.exists():
        region_data = load_json(region_file)
        region.apply_objects(region_data.get("objects", []))

    return region

def load_player_spawn() -> Tuple[str, int, int]:
    spawns = load_json(DATA / "map" / "spawn_points.json")
    player_spawn = next(s for s in spawns["spawns"] if s["type"] == "player")
    return player_spawn["region"], player_spawn["x"], player_spawn["y"]

def render(region: Region, player_pos: Tuple[int, int]):
    px, py = player_pos
    lines = []
    for y in range(region.height):
        row = []
        for x in range(region.width):
            if x == px and y == py:
                row.append("@")
            else:
                row.append(region.grid[y][x].char)
        lines.append("".join(row))
    screen = "\n".join(lines)
    print(screen)

def try_move(region: Region, pos: Tuple[int, int], dx: int, dy: int) -> Tuple[int, int]:
    nx, ny = pos[0] + dx, pos[1] + dy
    if region.can_walk(nx, ny):
        return nx, ny
    return pos

# --- THE UI ---


# =========================
# Terminal UI Fonksiyonları
# =========================
TERM_WIDTH = shutil.get_terminal_size((80, 24)).columns

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def center(text, width=TERM_WIDTH):
    lines = text.splitlines()
    return "\n".join(line.center(width) for line in lines)

def boxed(lines):
    """Çerçeveli metin, ortalanmış"""
    w = max(len(l) for l in lines)
    top = "┌" + "─" * (w + 2) + "┐"
    bot = "└" + "─" * (w + 2) + "┘"
    mid = [f"│ {l.ljust(w)} │" for l in lines]
    return "\n".join([top] + mid + [bot])

# =========================
# Veri Yükleme Fonksiyonları
# =========================
DATA = Path("data")

def load_json(p: Path):
    with p.open("r", encoding="utf-8") as f:
        return json.load(f)

# =========================
# Harita ve Tile Sınıfları
# =========================
class Tile:
    def __init__(self, ch: str, walkable: bool, ttype: str = "grass"):
        self.char = ch
        self.walkable = walkable
        self.type = ttype

class Region:
    def __init__(self, region_id: str, width: int, height: int, default_tile: Tile):
        self.id = region_id
        self.width = width
        self.height = height
        self.grid: List[List[Tile]] = [
            [Tile(default_tile.char, default_tile.walkable, default_tile.type) for _ in range(width)]
            for _ in range(height)
        ]

    def apply_objects(self, objects: List[dict]):
        for obj in objects:
            x, y = obj["x"], obj["y"]
            if 0 <= x < self.width and 0 <= y < self.height:
                ch = obj.get("char", "#")
                walk = obj.get("walkable", False)
                ttype = obj.get("type", "obstacle")
                self.grid[y][x] = Tile(ch, walk, ttype)

    def in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def can_walk(self, x: int, y: int) -> bool:
        return self.in_bounds(x, y) and self.grid[y][x].walkable

# =========================
# Harita Yükleme
# =========================
def load_region(region_id: str) -> Region:
    regions_cfg = load_json(DATA / "map" / "regions.json")
    region_meta = next(r for r in regions_cfg["regions"] if r["id"] == region_id)

    w = region_meta["size"]["width"]
    h = region_meta["size"]["height"]
    dt = region_meta["default_tile"]
    default_tile = Tile(dt.get("char", "."), dt.get("walkable", True), dt.get("type", "grass"))

    region = Region(region_id, w, h, default_tile)

    # Sparse obje verisi
    region_file = DATA / "map" / "regions" / f"{region_id}.json"
    if region_file.exists():
        region_data = load_json(region_file)
        region.apply_objects(region_data.get("objects", []))

    return region

def load_player_spawn() -> Tuple[str, int, int]:
    spawns = load_json(DATA / "map" / "spawn_points.json")
    player_spawn = next(s for s in spawns["spawns"] if s["type"] == "player")
    return player_spawn["region"], player_spawn["x"], player_spawn["y"]

# =========================
# Hareket Sistemi
# =========================
def try_move(region: Region, pos: Tuple[int, int], dx: int, dy: int) -> Tuple[int, int]:
    nx, ny = pos[0] + dx, pos[1] + dy
    if region.can_walk(nx, ny):
        return nx, ny
    return pos

# =========================
# Konum Bilgisi
# =========================
def describe_tile(region: Region, pos: Tuple[int, int]) -> List[str]:
    px, py = pos
    tile = region.grid[py][px]
    info = [
        f"Konum: ({px}, {py})",
        f"Zemin: {tile.type}",
        f"Geçilebilir: {'Evet' if tile.walkable else 'Hayır'}"
    ]

    # Yakındaki engeller/objeler
    nearby = []
    for dy in [-1, 0, 1]:
        for dx in [-1, 0, 1]:
            nx, ny = px + dx, py + dy
            if region.in_bounds(nx, ny):
                t = region.grid[ny][nx]
                if not t.walkable and (dx != 0 or dy != 0):
                    nearby.append(f"{t.type} ({nx},{ny})")

    if nearby:
        info.append("Yakında: " + ", ".join(nearby))
    else:
        info.append("Yakında dikkat çeken bir şey yok.")

    return info

# --- THE END ---

def __main__ ():
    print("SIERRA ENGINE IS RUNNED SUCCESFULLY.")

__main__()
