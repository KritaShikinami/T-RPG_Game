import curses
from core import (
    load_region, load_player_spawn, try_move,
    render_viewport, describe_tile,
    boxed, center, interact_npc
)

MOVES = {
    ord("w"): (0, -1),
    ord("s"): (0, 1),
    ord("a"): (-1, 0),
    ord("d"): (1, 0),
}

def game_loop(stdscr):
    curses.curs_set(0)  # imleç gizle
    stdscr.nodelay(False)
    stdscr.keypad(True)

    region_id, px, py = load_player_spawn()
    region = load_region(region_id)
    pos = (px, py)

    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()

        # Harita viewport
        viewport = render_viewport(region, pos)
        viewport_box = boxed(viewport)
        viewport_centered = center(viewport_box, w)

        # Panel bilgisi
        panel = describe_tile(region, pos)
        panel_box = boxed(panel)
        panel_centered = center(panel_box, w)

        # Yardım metni
        help_text = center("W/A/S/D ile hareket, Q ile çık", w)

        # Ekrana bas
        lines = viewport_centered.splitlines() + [""] + panel_centered.splitlines() + ["", help_text]
        for i, line in enumerate(lines):
            if i < h:
                stdscr.addstr(i, 0, line[:w])

        stdscr.refresh()

        # Input
        key = stdscr.getch()
        if key in (ord("q"), ord("Q")):
            break

        if key in MOVES:
            dx, dy = MOVES[key]
            new_pos = try_move(region, pos, dx, dy, stdscr)

            # 1) Önce geçit kontrolü
            if isinstance(new_pos, tuple) and new_pos[0] == "__region_change__":
                _, new_region_id, new_x, new_y = new_pos
                region = load_region(new_region_id)
                pos = (new_x, new_y)
                continue  # yeni haritayla döngüye dön

            # 2) Artık new_pos koordinat çifti (nx, ny)
            nx, ny = new_pos
            tile = region.grid[ny][nx]

            # 3) NPC etkileşimi
            if getattr(tile, "type", None) == "npc":
                for obj in getattr(region, "objects", []):
                    if obj["x"] == nx and obj["y"] == ny and obj["type"] == "npc":
                        npc_id = obj.get("npc_id", "npc_dockyard_guard")
                        curses.endwin()
                        interact_npc(npc_id)
                        input("\nDevam etmek için Enter'a bas...")
                        curses.initscr()
                        curses.curs_set(0)
                        break

            # 4) Pozisyonu güncelle
            pos = new_pos

def main():
    curses.wrapper(game_loop)

if __name__ == "__main__":
    main()
