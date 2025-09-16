# vats_console.py
# Konsolda ortalanmış ASCII V.A.T.S. görselleştirmesi (karakter çizimsiz)
import shutil
import time
import os
import random

from core import CHARACTER_TYPES, GUN_TYPES, vats_attack, next_turn, BODY_PARTS, move_character

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

def hp_bar(current, total, width=20):
    filled = int((current / total) * width) if total > 0 else 0
    return "[" + "#" * filled + " " * (width - filled) + f"] {current:.0f}/{total:.0f}"

def show_ui(player, npc, msg=None):
    clear()
    header = "=== V.A.T.S. - SIERRA ENGINE ==="
    lines = []
    lines.append(center(header))
    lines.append("")

    # Target info boxed
    target_lines = [
        f"Target: NPC",
        f"HP: {hp_bar(npc['hp_total'], sum([npc[x+'_hp'] for x in ['the_eyes','the_head','the_body','the_arm','the_leg']]))}",
        f"AP: {npc['action_point']}",
        f"Pozisyon: {npc['position']}",
    ]
    lines.append(center(boxed(target_lines)))
    lines.append("")

    # Player info boxed
    player_lines = [
        f"YOU:",
        f"HP: {hp_bar(player['hp_total'], sum([player[x+'_hp'] for x in ['the_eyes','the_head','the_body','the_arm','the_leg']]))}",
        f"AP: {player['action_point']}",
        f"Pozisyon: {player['position']}",
        f"Accuracy: {player['accuracy']:.2f}"
    ]
    lines.append(center(boxed(player_lines)))
    lines.append("")

    # Body parts and commands (centered)
    bp_list = ", ".join(BODY_PARTS.keys())
    lines.append(center("Hedef bölge seçimleri:"))
    lines.append(center(bp_list))
    lines.append("")
    lines.append(center("Komutlar: FIRE / MOVE / TURN / QUIT"))
    if msg:
        lines.append("")
        lines.append(center(f"> {msg}"))
    print("\n".join(lines))

def prompt_center(prompt_text):
    print()
    return input(prompt_text.center(TERM_WIDTH))

def main():
    # Hazır karakterleri core'dan alıyoruz
    player = CHARACTER_TYPES["CHARACTER"].copy()
    player["accuracy"] = 0.75
    player["position"] = (0, 0)
    player["speed_penalty"] = False

    npc = CHARACTER_TYPES["CHARACTER"].copy()
    npc["accuracy"] = 0.65
    npc["position"] = (12, 0)
    npc["speed_penalty"] = False

    weapon_player = GUN_TYPES["12GAUGE_SHOTGUN"]
    weapon_npc = GUN_TYPES["12GAUGE_SHOTGUN"]

    encounter = {"participants": [player, npc], "turn_index": -1}

    msg = "V.A.T.S. başlıyor..."

    while player["hp_total"] > 0 and npc["hp_total"] > 0:
        current = next_turn(encounter)

        if current is player:
            # oyuncu turu
            while player["action_point"] > 0:
                show_ui(player, npc, msg)
                cmd = prompt_center("Komut (FIRE/MOVE/TURN/QUIT): ").strip().upper()
                msg = None

                if cmd == "FIRE":
                    show_ui(player, npc, "Hedef bölgeleri seçin.")
                    part = prompt_center("Hangi bölgeye ateş? (ör: the_head): ").strip()
                    if part not in BODY_PARTS:
                        msg = "Geçersiz bölge, 'the_body' seçildi."
                        part = "the_body"
                    show_ui(player, npc, f"{part} hedefleniyor...")
                    time.sleep(0.6)
                    result = vats_attack(player, npc, weapon_player, part)
                    msg = result

                elif cmd == "MOVE":
                    sp = prompt_center("Kaç adım? (+ ileri, - geri): ").strip()
                    try:
                        steps = int(sp)
                        result = move_character(player, steps)
                        msg = result
                    except Exception:
                        msg = "Geçersiz sayı."

                elif cmd == "TURN":
                    msg = "Tur sonlandırıldı."
                    break

                elif cmd == "QUIT":
                    show_ui(player, npc, "V.A.T.S. kapatılıyor...")
                    return

                else:
                    msg = "Bilinmeyen komut."

                # güncelle HP toplamı
                for e in (player, npc):
                    e["hp_total"] = sum([e["the_eyes_hp"], e["the_head_hp"],
                                         e["the_body_hp"], e["the_arm_hp"], e["the_leg_hp"]])
                    if e["the_head_hp"] <= 0:
                        e["hp_total"] = 0

                time.sleep(0.3)

                if npc["hp_total"] <= 0 or player["hp_total"] <= 0:
                    break

        else:
            # NPC turu
            show_ui(player, npc, "NPC düşünceli...")
            time.sleep(0.8)
            part = random.choice(list(BODY_PARTS.keys()))
            show_ui(player, npc, f"NPC {part} bölgesine ateş ediyor...")
            time.sleep(0.4)
            result = vats_attack(npc, player, weapon_npc, part)
            msg = result

            for e in (player, npc):
                e["hp_total"] = sum([e["the_eyes_hp"], e["the_head_hp"],
                                     e["the_body_hp"], e["the_arm_hp"], e["the_leg_hp"]])
                if e["the_head_hp"] <= 0:
                    e["hp_total"] = 0

            time.sleep(0.5)

        if player["hp_total"] <= 0:
            show_ui(player, npc, "Oyuncu öldü! GAME OVER")
            break
        if npc["hp_total"] <= 0:
            show_ui(player, npc, "NPC öldü! SEN KAZANDIN")
            break

    print()
    input("Çıkmak için Enter'a basın...")

if __name__ == "__main__":
    main()
