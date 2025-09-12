import msvcrt  # Windows'ta anlık tuş okuma
from core import load_region, load_player_spawn, try_move, describe_tile, center, boxed, clear

MOVES = {
    b"w": (0, -1),
    b"s": (0, 1),
    b"a": (-1, 0),
    b"d": (1, 0),
}

def main():
    # Oyuncu başlangıç konumu
    region_id, px, py = load_player_spawn()
    region = load_region(region_id)
    pos = (px, py)

    while True:
        clear()
        info_lines = describe_tile(region, pos)
        print(center(boxed(info_lines)))
        print("\nW/A/S/D ile hareket, Q ile çık")

        key = msvcrt.getch().lower()  # Enter beklemeden tek tuş okur

        if key == b"q":
            break
        if key in MOVES:
            dx, dy = MOVES[key]
            pos = try_move(region, pos, dx, dy)

if __name__ == "__main__":
    main()
