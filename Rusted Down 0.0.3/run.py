import msvcrt
from core import load_region, load_player_spawn, try_move, draw_screen

MOVES = {
    b"w": (0, -1),
    b"s": (0, 1),
    b"a": (-1, 0),
    b"d": (1, 0),
}

def main():
    region_id, px, py = load_player_spawn()
    region = load_region(region_id)
    pos = (px, py)

    while True:
        draw_screen(region, pos)
        print("\nW/A/S/D ile hareket, Q ile çık")

        key = msvcrt.getch().lower()
        if key == b"q":
            break
        if key in MOVES:
            dx, dy = MOVES[key]
            pos = try_move(region, pos, dx, dy)

if __name__ == "__main__":
    main()
