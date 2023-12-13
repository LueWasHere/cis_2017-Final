import pygame
from pygame.locals import HWSURFACE, DOUBLEBUF, RESIZABLE, VIDEORESIZE, QUIT, KEYDOWN, K_SPACE, K_ESCAPE
from .communications import communication_class
from os import listdir

class DSP_Screen_Class:
    """
    (CLASS) DSP_Screen_Class
    
    (DESCRIPTION) Shortened from "Display_Screen_Class", contains all necassary methods to display the sprites contained within the game
    
    (ARGUMENTS)
    
    (CLASS(communication_class)) inter_class_communications (DESCRIPTION) The class used for communication between classes
    (STRING) game_path (DESCRIPTION) Where the game is stored on the hard drive.
    """
    def __init__(self, inter_class_communications: communication_class, game_path: str="") -> None: # Inital constructor
        # Initialize pygame and a window
        pygame.init()
        
        self.screen = pygame.display.set_mode((400, 320),HWSURFACE|DOUBLEBUF|RESIZABLE)
        # Make a buffer screen for resizing the image according to the size of the window
        self.buffer_screen = self.screen.copy()
        
        # Set the icon and caption of the window
        self.ICON = pygame.image.load('mouse_runner/data/icon/mouse_landing_fall_sprite.ico').convert_alpha()
        pygame.display.set_icon(self.ICON)
        
        pygame.display.set_caption("Mouse Runner")
        
        # Set the game path and communications class
        self.inter_class_communications = inter_class_communications
        self.game_path = game_path
    
    def read_sprites(self) -> None:
        """
        (FUNCTION) read_sprites
        
        (DESCRIPTION) Read the necessary sprites from the mouse_runner/data/ directory.
        
        (ARGUMENTS) The function takes no arguments

        (RETURNS) The function returns nothing
        """
        # Create empty dicts for the required sprites. The key is the name of the file while the value is the data of the
        # image.
        self.mouse_sprites = dict()
        self.cat_cutscene_sprites = dict()
        self.cat_sprites = dict()
        self.background_sprites = dict()
        # Loop through every sprite in the directory
        for sprite_file in listdir("mouse_runner/data/sprites"):
            if sprite_file[0:5] == "mouse": # Sprite is for the mouse
                self.mouse_sprites[sprite_file] = pygame.transform.scale(pygame.image.load(f'mouse_runner/data/sprites/{sprite_file}').convert_alpha(), (32, 32))
            elif sprite_file[0:9] == "cat_claw_": # Sprite is for the cat
                self.cat_cutscene_sprites[sprite_file] = pygame.transform.scale(pygame.image.load(f'mouse_runner/data/sprites/{sprite_file}').convert_alpha(), (32, 32))
            elif sprite_file[0:5] == "floor" or sprite_file[0:5] == "wood_": # Sprite is for the background
                self.background_sprites[sprite_file] = pygame.transform.scale(pygame.image.load(f'mouse_runner/data/sprites/{sprite_file}').convert_alpha(), (32, 32))
        self.inter_class_communications.background_sprites = self.background_sprites # Set the background sprites in the
                                                                                     # communication class.
        return
    
    def update_master(self) -> None:
        """
        (FUNCTION) update_master
        
        (DESCRIPTION) Resize and write screen data from the buffer screen to the main screen.
        
        (ARGUMENTS) The function takes no arguments

        (RETURNS) The function returns nothing
        """
        
        self.screen.blit(pygame.transform.scale(self.buffer_screen, self.screen.get_rect().size), (0, 0)) # Scale and write data
        pygame.display.flip()
        return
    
    def update_slave(self, player_state: str) -> None:
        """
        (FUNCTION) update_slave
        
        (DESCRIPTION) Write image data to the buffer screen.
        
        (ARGUMENTS) 
        
        (STRING) player_state (DESCRIPTION) The current state of the player.

        (RETURNS) The function returns nothing
        """

        self.buffer_screen.fill((84, 109, 142)) # Fill the screen with the same color as the floor to reduce the amount of drawing required.
        
        decode_state = { # The sprite the player should be using is stored in a state not as the image, this is used to convert it
            "running_1": "mouse_firstfram_walking_1_sprite.png",
            "running_2": "mouse_walking_sprite_2.png",
            "jumping": "mouse_jumping_sprite.png",
            "falling": "mouse_landing_fall_sprite.png",
            "sleeping_1": "mouse_sleeping_frame_1.png", 
            "sleeping_2": "mouse_sleeping_frame_2.png",
            "sleeping_3": "mouse_sleeping_frame_3.png",
            "sleeping_4": "mouse_sleeping_frame_4.png",
            "walking_1": "mouse_wakingup_frame_1.png",
            "walking_2": "mouse_wakingup_frame_2.png",
            "dead": "mouse_dead_sprite.png",
        }

        # Display the background
        for i,row in enumerate(self.inter_class_communications.tile_states):
            for j,tile in enumerate(row):
                if i == 7: # The floor is at a different position
                    self.buffer_screen.blit(self.background_sprites[tile], (j*32-self.inter_class_communications.tile_offset_x, i*32-29))
                else:
                    self.buffer_screen.blit(self.background_sprites[tile], (j*32-self.inter_class_communications.tile_offset_x, i*32))
        
        # Display the obstacles
        for i,obstacle in enumerate(self.inter_class_communications.obstacles):
            if obstacle != 0: # Null is used to represent the absence of an obstacle
                self.buffer_screen.blit(self.cat_cutscene_sprites[obstacle], (i*32-self.inter_class_communications.tile_offset_x, 197))

        # Draw the player, the player's x coordinate never changes.
        self.buffer_screen.blit(self.mouse_sprites[decode_state[player_state]], (133, 197-self.inter_class_communications.player_y))
        
    def check_for_events(self) -> bool:
        """
        (FUNCTION) check_for_events
        
        (DESCRIPTION) Check for certain events in the window.
        
        (ARGUMENTS) The function takes no arguments

        (RETURNS) The function returns a bool to represent if the program should stop
        """
        
        # Loop through the events
        for event in pygame.event.get():
            if event.type == QUIT: # 'X' button was clicked
                pygame.display.quit()
                return False
            elif event.type == VIDEORESIZE: # User resized the window
                self.screen = pygame.display.set_mode(event.size, HWSURFACE|DOUBLEBUF|RESIZABLE)
            elif event.type == KEYDOWN: # User pressed a key
                if event.key == K_SPACE:
                    self.inter_class_communications.controls_state = self.inter_class_communications.controls_state | 0b10
                elif event.key == K_ESCAPE:
                    self.inter_class_communications.controls_state = self.inter_class_communications.controls_state | 0b01
            
        return True # If the quit event is not triggered then this is the default return value