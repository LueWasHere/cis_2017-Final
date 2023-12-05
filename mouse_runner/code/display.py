import pygame
from pygame.locals import HWSURFACE, DOUBLEBUF, RESIZABLE, VIDEORESIZE, QUIT
from .communications import communcation_class
from os import listdir

class DSP_Screen_Class:
    """
    (CLASS) DSP_Screen_Class
    
    (DESCRIPTION) Shortened from "Display_Screen_Class", contains all necassary methods to display the sprites contained within the game
    
    (ARGUMENTS) The class takes no arguments
    """
    def __init__(self, inter_class_communications: communcation_class, game_path: str="") -> None:
        pygame.init()
        
        self.screen = pygame.display.set_mode((400, 300),HWSURFACE|DOUBLEBUF|RESIZABLE)
        self.buffer_screen = self.screen.copy()
        
        self.ICON = pygame.image.load('mouse_runner/data/icon/mouse_landing_fall_sprite.ico').convert_alpha()
        pygame.display.set_icon(self.ICON)
        
        pygame.display.set_caption("Mouse Runner")
        
        self.game_path = game_path
    
    def init_display(self) -> None:
        
        return
    
    def read_sprites(self) -> None:
        # Getting all sprites and putting them into animation dicts
        self.mouse_sprites = dict()
        self.cat_cutscene_sprites = dict()
        self.cat_sprites = dict()
        for sprite_file in listdir("mouse_runner/data/sprites"):
            if sprite_file[0:5] == "mouse":
                self.mouse_sprites[sprite_file] = pygame.transform.scale(pygame.image.load(f'mouse_runner/data/sprites/{sprite_file}').convert_alpha(), (16, 16))
            elif sprite_file[0:9] == "cat_claw" or sprite_file[0:9] == "cat_wall_":
                self.cat_cutscene_sprites[sprite_file] = pygame.image.load(f'mouse_runner/data/sprites/{sprite_file}').convert_alpha()
    
        return
    
    def update_master(self) -> None:
        self.screen.blit(pygame.transform.scale(self.buffer_screen, self.screen.get_rect().size), (0, 0))
        pygame.display.flip()
        return
    
    def update_slave(self, player_state) -> None:
        self.buffer_screen.fill((255, 255, 255))
        
        decode_state = {
            "running_1": "mouse_firstfram_walking_1_sprite.png",
            "running_2": "mouse_walking_sprite_2.png",
            "jumping": "mouse_jumping_sprite.png",
            "falling": "mouse_landing_fall_sprite.png",
            "sleeping_1": "mouse_sleeping_frame_1.png", 
            "sleeping_2": "mouse_sleeping_frame_2.png",
            "sleeping_3": "mouse_sleeping_frame_3.png",
            "waking_1": "mouse_wakingup_frame_1.png",
            "waking_2": "mouse_wakingup_frame_2.png",
            "dead": "mouse_dead_sprite.png",
        }
        
        self.buffer_screen.blit(self.mouse_sprites[decode_state[player_state]], (133, 200))
        
    def check_for_events(self) -> bool:
        for event in pygame.event.get():
            if event.type == QUIT: 
                pygame.display.quit()
                return False
            elif event.type == VIDEORESIZE:
                self.screen = pygame.display.set_mode(event.size, HWSURFACE|DOUBLEBUF|RESIZABLE)
                
        return True