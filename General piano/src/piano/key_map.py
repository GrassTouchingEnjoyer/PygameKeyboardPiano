import pygame

KEY_MAP = {} # KEY:NOTE

import pygame

KEYBOARD_KEYS_76 = [
    # 1. Function Row (12 keys)
    pygame.K_F1, pygame.K_F2, pygame.K_F3, pygame.K_F4,
    pygame.K_F5, pygame.K_F6, pygame.K_F7, pygame.K_F8,
    pygame.K_F9, pygame.K_F10, pygame.K_F11, pygame.K_F12,

    # 2. Number Row (13 keys)
    pygame.K_BACKQUOTE, pygame.K_1, pygame.K_2, pygame.K_3,
    pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7,
    pygame.K_8, pygame.K_9, pygame.K_0, pygame.K_MINUS, pygame.K_EQUALS,

    # 3. Top Row (12 keys)
    pygame.K_q, pygame.K_w, pygame.K_e, pygame.K_r,
    pygame.K_t, pygame.K_y, pygame.K_u, pygame.K_i,
    pygame.K_o, pygame.K_p, pygame.K_LEFTBRACKET, pygame.K_RIGHTBRACKET,

    # 4. Home Row (12 keys)
    pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_f,
    pygame.K_g, pygame.K_h, pygame.K_j, pygame.K_k,
    pygame.K_l, pygame.K_SEMICOLON, pygame.K_QUOTE, pygame.K_z,

    # 5. Bottom Row (12 keys)
    pygame.K_x, pygame.K_c, pygame.K_v, pygame.K_b,
    pygame.K_n, pygame.K_m, pygame.K_COMMA, pygame.K_PERIOD,
    pygame.K_SLASH, pygame.K_INSERT, pygame.K_HOME, pygame.K_PAGEUP,

    # 6. Nav & Arrow Row (12 keys)
    pygame.K_DELETE, pygame.K_END, pygame.K_PAGEDOWN,
    pygame.K_UP, pygame.K_LEFT, pygame.K_DOWN, pygame.K_RIGHT,
    pygame.K_KP0, pygame.K_KP1, pygame.K_KP2, pygame.K_KP3, pygame.K_KP4,

    # 7. Numpad Row (3 keys)
    pygame.K_KP5, pygame.K_KP6, pygame.K_KP7, pygame.K_KP8, pygame.K_KP9
]

def keyboard_mapping(octaves_notes):
    index = 0
    tot_keys = len(KEYBOARD_KEYS_76)
    
    for _,notes in octaves_notes.items():
        
        for note in notes:   
            
            if index >= tot_keys: return KEY_MAP
            
            KEY_MAP[KEYBOARD_KEYS_76[index]] = note
            
            index += 1
            
            
    return KEY_MAP