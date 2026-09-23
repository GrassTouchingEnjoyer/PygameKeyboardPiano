import pygame


def print_key_eq_note(key,note):
    
    x = f"{key} = {note}"
    legth_of_char=len(x) * "_" ;
    print(f"{legth_of_char}\n{x}\n{legth_of_char}\n")


def print_octave(octave):

    legth_of_char=len(octave) * "⣿" ;
    print(f"{legth_of_char}\n{octave}\n{legth_of_char}\n")


"""
KEY_MAP is the final dictionary 
and ready to use in the piano.py

(ex:67: sound_obj)
"""
KEY_MAP = {} # KEY:NOTE

"""
(ex:K_f7 : 67)
gets all keys from locals pygame

syntax: ex: [x for x in range(10) if x % 2 == 0]
"""
import pygame

KEYBOARD_KEYS_default = [
    # 1. Function Row (12 keys)
    pygame.K_F1, pygame.K_F2, pygame.K_F3, pygame.K_F4,
    pygame.K_F5, pygame.K_F6, pygame.K_F7, pygame.K_F8,
    pygame.K_F9, pygame.K_F10, pygame.K_F11, pygame.K_F12,

    # 2. Number Row (14 keys: ` to Backspace)
    pygame.K_BACKQUOTE, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4,
    pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9,
    pygame.K_0, pygame.K_MINUS, pygame.K_EQUALS, pygame.K_BACKSPACE,

    # 3. Top Row (14 keys: Tab to \)
    pygame.K_TAB, pygame.K_q, pygame.K_w, pygame.K_e, pygame.K_r,
    pygame.K_t, pygame.K_y, pygame.K_u, pygame.K_i, pygame.K_o,
    pygame.K_p, pygame.K_LEFTBRACKET, pygame.K_RIGHTBRACKET, pygame.K_BACKSLASH,

    # 4. Home Row (13 keys: Caps Lock to Enter)
    pygame.K_CAPSLOCK, pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_f,
    pygame.K_g, pygame.K_h, pygame.K_j, pygame.K_k, pygame.K_l,
    pygame.K_SEMICOLON, pygame.K_QUOTE, pygame.K_RETURN,

    # 5. Bottom Row (12 keys: Left Shift to Right Shift)
    pygame.K_LSHIFT, pygame.K_z, pygame.K_x, pygame.K_c, pygame.K_v,
    pygame.K_b, pygame.K_n, pygame.K_m, pygame.K_COMMA, pygame.K_PERIOD,
    pygame.K_SLASH, pygame.K_RSHIFT,

    # 6. Control Row (2 keys)
    pygame.K_LCTRL, pygame.K_RCTRL,

    # 7. Navigation Top (3 keys: next to Backspace)
    pygame.K_INSERT, pygame.K_HOME, pygame.K_PAGEUP,

    # 8. Navigation Bottom (3 keys: next to \)
    pygame.K_DELETE, pygame.K_END, pygame.K_PAGEDOWN,

    # 9. Arrow Cluster (4 keys: next to Right Shift / Right Ctrl)
    pygame.K_UP, pygame.K_LEFT, pygame.K_DOWN, pygame.K_RIGHT,

    # 10. Alt Keys (2 keys)
    pygame.K_LALT, pygame.K_RALT
]

#def keyboard_costum_mapping():

def keyboard_default_mapping(octaves_notes):
    """
    octaves_notes:(octave_type : note_list) 
    octave_type can be used for costum costumization
    but can also help default
    
    octave points to a list
    """
    
    index = 0
    tot_notes = sum(len(notes) for _,notes in octaves_notes.items())
    print(f"{tot_notes}")
    
    for octave,notes in octaves_notes.items():
        
        print_octave(octave)
        
        for name,note in notes:   
            
            if index >= tot_notes: return KEY_MAP
            
            code = KEYBOARD_KEYS_default[index] 
            
            print_key_eq_note(pygame.key.name(KEYBOARD_KEYS_default[index]),name)
            
            KEY_MAP[code] = note
            
            index += 1
            
            
    return KEY_MAP

    


#def keyboard_default_mapping(octaves_notes):
#    """
#    REFACTORED:
    
#    """
    