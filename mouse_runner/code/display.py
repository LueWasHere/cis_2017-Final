import pygame
from pygame.locals import HWSURFACE, DOUBLEBUF, RESIZABLE, VIDEORESIZE, QUIT
from communications import communcation_class

class DSP_Screen_Class:
    """
    (CLASS) DSP_Screen_Class
    
    (DESCRIPTION) Shortened from "Display_Screen_Class", contains all necassary methods to display the sprites contained within the game
    
    (ARGUMENTS) The class takes no arguments
    """
    def __init__(self, inter_class_communications: communcation_class, game_path: str="") -> None:
        pygame.init()
        
        self.screen = pygame.display.set_mode((200, 200),HWSURFACE|DOUBLEBUF|RESIZABLE)
        self.buffer_screen = self.screen.copy()
        
        self.game_path = game_path
    
    def init_display(self) -> None:
        
        return
    
    def read_sprites(self) -> None:
        # Getting all sprites and putting them into animation arrays
        
        
        return
    
    def update_master(self) -> None:
        self.screen.blit(pygame.transform.scale(self.buffer_screen, self.screen.get_rect().size), (0, 0))
        pygame.display.flip()
        return
    
    def update_slave(self, commands) -> None:
        
        for command in commands:
            pass
        
    def check_for_events(self) -> bool:
        for event in pygame.event.get():
            if event.type == QUIT: 
                pygame.display.quit()
                return False
            elif event.type == VIDEORESIZE:
                self.screen = pygame.display.set_mode(event.size, HWSURFACE|DOUBLEBUF|RESIZABLE)
                
        return True