
import os
import pygame

# map to all notes
OCTAVE_FILES = {
    "sub_bass_2": ("A_2.mp3", "A_2s.mp3", "B_2.mp3"),
    
    "sub_bass_1": (
        "C_1.mp3", "C_1s.mp3", "D_1.mp3", "D_1s.mp3", "E_1.mp3", "F_1.mp3",
        "F_1s.mp3", "G_1.mp3", "G_1s.mp3", "A_1.mp3", "A_1s.mp3", "B_1.mp3"
    ),
    "bass": (
        "C.mp3", "Cs.mp3", "D.mp3", "Ds.mp3", "E.mp3", "F.mp3",
        "Fs.mp3", "G.mp3", "Gs.mp3", "A.mp3", "As.mp3", "B.mp3"
    ),
    "tenor_1": (
        "c1.mp3", "c1s.mp3", "d1.mp3", "d1s.mp3", "e1.mp3", "f1.mp3",
        "f1s.mp3", "g1.mp3", "g1s.mp3", "a1.mp3", "a1s.mp3", "b1.mp3"
    ),
    "mid_2": (
        "c2.mp3", "c2s.mp3", "d2.mp3", "d2s.mp3", "e2.mp3", "f2.mp3",
        "f2s.mp3", "g2.mp3", "g2s.mp3", "a2.mp3", "a2s.mp3", "b2.mp3"
    ),
    "treble_3": (
        "c3.mp3", "c3s.mp3", "d3.mp3", "d3s.mp3", "e3.mp3", "f3.mp3",
        "f3s.mp3", "g3.mp3", "g3s.mp3", "a3.mp3", "a3s.mp3", "b3.mp3"
    ),
    "high_treble_4": (
        "c4.mp3", "c4s.mp3", "d4.mp3", "d4s.mp3", "e4.mp3", "f4.mp3",
        "f4s.mp3", "g4.mp3", "g4s.mp3", "a4.mp3", "a4s.mp3", "b4.mp3"
    ),
    "top_end": ("c5.mp3", "a high.mp3", "a highs.mp3", "b high.mp3"),
}

def load_mp3_files_to_memory(audio_folder="notes"):
    """This loads the mp3 files into Sound objects, the sound objects are placed inside a list, and the octave
       that references those sound objects become their key (from keys inside that reference dict) and the list becomes
       a tuple.
       
    Returns:
        _type_: (key:[list])
    """
    octaves = {}
    
    for octave, notes in OCTAVE_FILES.items():    
        loaded_notes = []
       
        for note in notes:
            
            note_path = os.path.join(audio_folder, note)
            loaded_notes.append((note,pygame.mixer.Sound(note_path)))
    
        octaves[octave] = tuple(loaded_notes)
    
    return octaves