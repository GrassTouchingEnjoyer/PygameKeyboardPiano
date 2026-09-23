import pygame
import sound_loader as s_l
import key_map as k_m

#⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿ Functions

def mixer_init_check():

    if (pygame.mixer.get_init()):   

        print(f"mixer {pygame.mixer} \ninitialized")
    else:
        print("error while initializing mixer")
#⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿


pygame.init()
#pygame.font.init()
pygame.mixer.init(frequency=44100, size=-16, channels=2 , buffer=2048)      

# initializations and checks 
mixer_init_check()

#channels take in one sound object at a time, having multiple is good for polyphony applications
pygame.mixer.set_num_channels(64)

#load notes into memory (RAM)
octaves_notes = s_l.load_mp3_files_to_memory()
print("notes loaded into RAM")

#map the keys to the sound objects
keys_mapped = k_m.keyboard_default_mapping(octaves_notes)
print("keys mapped")

              
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 500
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pygame Keyboard Piano")

font = pygame.font.SysFont("timesnewroman", 12, bold=True) 
clock = pygame.time.Clock()

# Dict to track active channels
active_channels = {}

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        # (1) KEY DOWN -> Play sound and store the channel
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False

            elif event.key in keys_mapped:         
                sound_obj = keys_mapped[event.key]
                channel = sound_obj.play()
                
                #keep it in the active channel dict
                if channel:
                    active_channels[event.key] = channel
            
            else: continue

        # (2) KEY UP -> In a real piano it stops so I even added a fadeout for realism
        elif event.type == pygame.KEYUP:        
                
            if event.key in active_channels:
                active_channels[event.key].fadeout(100)
                del active_channels[event.key]  # Clean up dictionary

    
    # Cap at 60 FPS to keep CPU usage low
    clock.tick(60)

pygame.quit()