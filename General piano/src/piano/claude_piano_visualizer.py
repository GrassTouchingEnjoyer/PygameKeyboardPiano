"""
Keyboard-piano visualizer (drop-in replacement for gemini_visualizer.py).

API is unchanged:
    key_rects = init_visualizer(keys_mapped)
    draw_visualizer(screen, key_rects, active_keys, font)

Features
  * Layout is computed from the actual window size, so nothing overflows.
  * Correct note labels (derived from OCTAVE_FILES, not from the Sound object).
  * Every octave group has its own colour; sharps get a darker "black key" look.
  * Keys glow when pressed and fade out smoothly on release (matches the 100ms audio fadeout).
  * Little sparks fly off each key when it is struck.
  * Header shows the last note played and how many keys are held down.
"""
import random
import pygame
from sound_loader import OCTAVE_FILES

# ---------------------------------------------------------------- config
KEY_NAMES = {
    pygame.K_BACKQUOTE: "`", pygame.K_MINUS: "-", pygame.K_EQUALS: "=",
    pygame.K_LEFTBRACKET: "[", pygame.K_RIGHTBRACKET: "]", pygame.K_BACKSLASH: "\\",
    pygame.K_SEMICOLON: ";", pygame.K_QUOTE: "'", pygame.K_COMMA: ",",
    pygame.K_PERIOD: ".", pygame.K_SLASH: "/", pygame.K_INSERT: "INS",
    pygame.K_HOME: "HM", pygame.K_PAGEUP: "PGU", pygame.K_DELETE: "DEL",
    pygame.K_END: "END", pygame.K_PAGEDOWN: "PGD", pygame.K_UP: "UP",
    pygame.K_LEFT: "LFT", pygame.K_DOWN: "DN", pygame.K_RIGHT: "RGT",
    pygame.K_KP0: "N0", pygame.K_KP1: "N1", pygame.K_KP2: "N2",
    pygame.K_KP3: "N3", pygame.K_KP4: "N4", pygame.K_KP5: "N5",
    pygame.K_KP6: "N6", pygame.K_KP7: "N7", pygame.K_KP8: "N8", pygame.K_KP9: "N9",
}

# Must match the rows in key_map.py (12 + 13 + 12 + 12 + 12 + 12 + 5 = 78 keys)
KEYS_PER_ROW = [12, 13, 12, 12, 12, 12, 5]

# Assumed piano octave number for each group in sound_loader.OCTAVE_FILES.
# Only affects the label text - change these if your samples differ.
OCTAVE_NUMBERS = {
    "sub_bass_2": 0, "sub_bass_1": 1, "bass": 2, "tenor_1": 3,
    "mid_2": 4, "treble_3": 5, "high_treble_4": 6, "top_end": 7,
}

MARGIN = 20
GAP = 6
HEADER_H = 64

BG = (10, 12, 16)
KEY_BG = (26, 31, 42)
KEY_BG_SHARP = (16, 19, 27)
KEY_BORDER = (55, 63, 82)
TEXT_DIM = (150, 160, 180)
FADE_SPEED = 9.0        # key glow decays in roughly 1/9 s (~110 ms) after release

# ---------------------------------------------------------------- internal state
_fonts = {}
_palette = []
_state = {"last_ms": None, "prev_active": set(), "particles": [],
          "last_note": None, "last_note_level": 0.0}


def _lerp(a, b, t):
    t = max(0.0, min(1.0, t))
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def _make_palette(n):
    colors = []
    for i in range(n):
        c = pygame.Color(0)
        c.hsva = ((i * 360 / n + 190) % 360, 70, 100, 100)
        colors.append((c.r, c.g, c.b))
    return colors


def _build_note_labels():
    """Flatten OCTAVE_FILES in the same order key_map.py assigns keys.
    Returns a list of (label, group_index, is_sharp)."""
    labels = []
    for g_idx, (group, files) in enumerate(OCTAVE_FILES.items()):
        octave = OCTAVE_NUMBERS.get(group, "")
        for f in files:
            stem = f.rsplit(".", 1)[0]
            sharp = stem.endswith("s")          # Cs, c1s, A_2s, "a highs" ...
            letter = stem[0].upper()
            labels.append((f"{letter}{'#' if sharp else ''}{octave}", g_idx, sharp))
    return labels


# ---------------------------------------------------------------- public API
def init_visualizer(keys_mapped):
    global _palette
    surface = pygame.display.get_surface()
    W, H = surface.get_size()

    _fonts["title"] = pygame.font.SysFont("arial", 22, bold=True)
    _fonts["big"] = pygame.font.SysFont("arial", 34, bold=True)
    _fonts["small"] = pygame.font.SysFont("arial", 12, bold=True)
    _fonts["key_cap"] = pygame.font.SysFont("arial", 12, bold=True)
    _fonts["note"] = pygame.font.SysFont("arial", 18, bold=True)

    _palette = _make_palette(len(OCTAVE_FILES))
    labels = _build_note_labels()
    key_codes = list(keys_mapped.keys())

    cols, rows = max(KEYS_PER_ROW), len(KEYS_PER_ROW)
    kw = (W - 2 * MARGIN - (cols - 1) * GAP) // cols
    kh = (H - HEADER_H - MARGIN - (rows - 1) * GAP) // rows

    key_rects = {}
    idx = 0
    y = HEADER_H
    for count in KEYS_PER_ROW:
        row_w = count * kw + (count - 1) * GAP
        x = (W - row_w) // 2                    # centre every row
        for _ in range(count):
            if idx >= len(key_codes):
                break
            code = key_codes[idx]
            label, group, sharp = labels[idx] if idx < len(labels) else ("?", 0, False)
            key_rects[code] = {
                "rect": pygame.Rect(x, y, kw, kh),
                "k_name": KEY_NAMES.get(code, pygame.key.name(code).upper()),
                "n_name": label,
                "color": _palette[group % len(_palette)],
                "sharp": sharp,
                "level": 0.0,                   # 0 = idle, 1 = just pressed
            }
            x += kw + GAP
            idx += 1
        y += kh + GAP

    return key_rects


def draw_visualizer(screen, key_rects, active_keys, font=None):
    now = pygame.time.get_ticks()
    dt = 1 / 60 if _state["last_ms"] is None else min((now - _state["last_ms"]) / 1000, 0.05)
    _state["last_ms"] = now

    # --- update per-key state ------------------------------------------------
    newly_pressed = active_keys - _state["prev_active"]
    _state["prev_active"] = set(active_keys)

    for code, info in key_rects.items():
        if code in active_keys:
            info["level"] = 1.0
        else:
            info["level"] = max(0.0, info["level"] - dt * FADE_SPEED)

    for code in newly_pressed:
        info = key_rects.get(code)
        if not info:
            continue
        _state["last_note"] = (info["n_name"], info["color"])
        _state["last_note_level"] = 1.0
        cx, top = info["rect"].centerx, info["rect"].top
        for _ in range(7):
            life = random.uniform(0.5, 1.0)
            _state["particles"].append({
                "x": cx + random.uniform(-14, 14), "y": top + 4,
                "vx": random.uniform(-40, 40), "vy": random.uniform(-190, -70),
                "life": life, "max": life, "color": info["color"],
                "r": random.choice((2, 2, 3)),
            })
    _state["last_note_level"] = max(0.0, _state["last_note_level"] - dt * 0.6)

    # --- background + header -------------------------------------------------
    screen.fill(BG)
    _draw_header(screen, active_keys)

    # --- glow pass (behind all keys) -----------------------------------------
    for info in key_rects.values():
        lvl = info["level"]
        if lvl > 0.02:
            r = info["rect"]
            glow = pygame.Surface((r.w + 28, r.h + 28), pygame.SRCALPHA)
            pygame.draw.rect(glow, (*info["color"], int(80 * lvl)),
                             glow.get_rect(), border_radius=16)
            screen.blit(glow, (r.x - 14, r.y - 14))

    # --- key pass ------------------------------------------------------------
    for info in key_rects.values():
        lvl, col = info["level"], info["color"]
        rect = info["rect"].copy()
        if lvl > 0.5:
            rect.y += 2                         # tiny "pressed" dip

        base = KEY_BG_SHARP if info["sharp"] else KEY_BG
        bg = _lerp(base, col, lvl * 0.9)
        border = _lerp(KEY_BORDER, (255, 255, 255), lvl)

        pygame.draw.rect(screen, bg, rect, border_radius=8)
        pygame.draw.rect(screen, border, rect, width=2, border_radius=8)

        # coloured octave strip along the top edge
        strip = pygame.Rect(rect.x + 8, rect.y + 5, rect.w - 16, 3)
        pygame.draw.rect(screen, _lerp(col, (255, 255, 255), lvl * 0.6) if lvl else _lerp(BG, col, 0.55),
                         strip, border_radius=2)

        cap_col = _lerp(TEXT_DIM, (10, 14, 20), lvl)
        note_col = _lerp(col, (10, 14, 20), lvl)

        s_k = _fonts["key_cap"].render(info["k_name"], True, cap_col)
        s_n = _fonts["note"].render(info["n_name"], True, note_col)
        screen.blit(s_k, (rect.x + 8, rect.y + 12))
        screen.blit(s_n, (rect.centerx - s_n.get_width() // 2,
                          rect.bottom - s_n.get_height() - 8))

    # --- particles (on top) --------------------------------------------------
    alive = []
    for p in _state["particles"]:
        p["life"] -= dt
        if p["life"] <= 0:
            continue
        p["x"] += p["vx"] * dt
        p["y"] += p["vy"] * dt
        p["vy"] += 260 * dt                     # gravity
        c = _lerp(BG, p["color"], p["life"] / p["max"])
        pygame.draw.circle(screen, c, (int(p["x"]), int(p["y"])), p["r"])
        alive.append(p)
    _state["particles"] = alive


def _draw_header(screen, active_keys):
    W = screen.get_width()

    title = _fonts["title"].render("KEYBOARD PIANO", True, (235, 240, 250))
    screen.blit(title, (MARGIN, 16))
    hint = _fonts["small"].render("ESC to quit", True, TEXT_DIM)
    screen.blit(hint, (MARGIN, 42))

    # last note played, fades out slowly
    note = _state["last_note"]
    if note:
        name, col = note
        c = _lerp(BG, col, 0.25 + 0.75 * _state["last_note_level"])
        s = _fonts["big"].render(name, True, c)
        screen.blit(s, (W // 2 - s.get_width() // 2, 12))

    held = _fonts["small"].render(f"{len(active_keys)} KEYS DOWN", True, TEXT_DIM)
    screen.blit(held, (W - MARGIN - held.get_width(), 26))

    pygame.draw.line(screen, (30, 36, 48), (MARGIN, HEADER_H - 8), (W - MARGIN, HEADER_H - 8), 1)