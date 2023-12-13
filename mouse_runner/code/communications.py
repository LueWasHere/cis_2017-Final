class communication_class():
    """
    (CLASS) communication_class
    
    (DESCRIPTION) A class containing a couple variables that are used between the display and process classes to avoid using
    global variables
    
    (ARGUMENTS) The class takes no arguments
    """
    
    def __init__(self) -> None: # Inital constructor
        self.global_kill = ("ALIVE", 0) # Stops the program if this is equal to anything else
        self.controls_state = 0b00 # Bit mask for the state of the controls. The most significant bit is for the state of
                                   # the escape key, the other is for the state of the space bar; Little endian
        self.player_y = 0 # The current y-offset of the player
        self.tile_states = [] # Where the background and floor tiles are located
        self.tile_offset_x = 0 # How far to draw the tiles
        self.background_sprites = dict() # The background sprites
        self.obstacles = [] # The locations of the obstacles