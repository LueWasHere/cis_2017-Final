from time import gmtime, time
from random import choice, randint
from random import seed as setSeed
from .communications import communcation_class

class PCS_Data_Class:
    """
    (CLASS) PCS_Data_Class
    
    (DESCRIPTION) Shortened from "Process_Data_Class", this contains all the methods and data that is needed to calculate functions relating to player score, speed, and death
    as well as being able to process the obstacles in the game
    
    (ARGUMENTS) The class takes no arguments
    """
    
    def __init__(self, inter_class_communications: communcation_class, game_path: str="") -> None:
        self.player_score = 0
        self.player_speed = 0
        self.player_state = "sleeping_1"
        self.player_y = 0
        self.player_falling = False
        self.start_time = time()

        self.tile_states = [[], [], [], [], [], [], [], []]
        self.obstacles = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.tile_offset_x = 0
        
        # Classic method of using the time as the seed
        local_time = gmtime()
        self.seed = local_time.tm_year+local_time.tm_mon+local_time.tm_mday+local_time.tm_hour+local_time.tm_min+local_time.tm_sec+local_time.tm_wday+local_time.tm_yday
        
        # Ensure* a random number with binary manipulation
        # * A random number cannot 𝘵𝘳𝘶𝘭𝘺 be acheived. This method simply tries to make it a bit more random
        random_assurance = (~self.seed)**2
        random_assurance_shift = random_assurance<<4
        random_assurance = random_assurance ^ random_assurance_shift
        # XOR the seed^3 variable with the random_assurance
        self.seed = (self.seed**int(bin(random_assurance)[2::][::-1][0:5], 2)) ^ random_assurance
        
        # Save the path for the game and set the communications class
        self.game_path = game_path
        self.inter_class_communications = inter_class_communications        
        
        setSeed(self.seed)
        
    def reset(self) -> None:
        self.player_score = 0
        self.player_speed = 0
        self.player_state = "running_1"
        self.player_y = 0
        self.player_falling = False
        self.obstacles = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.tile_states = [[], [], [], [], [], [], [], []]
        self.tile_offset_x = 0

        # Generate a random background
        for i in range(0, 8):
            for _ in range(0, 14):
                if i == 7:
                    floors = [background_sprite for background_sprite in self.inter_class_communications.background_sprites.keys() if background_sprite[0:5] == "floor"]
                    self.tile_states[i].append(choice(floors))
                else:
                    walls = [background_sprite for background_sprite in self.inter_class_communications.background_sprites.keys() if background_sprite[0:5] != "floor"]
                    self.tile_states[i].append(choice(walls))
        return
    
    def move_frame_forward(self) -> None:
        if self.player_state == "dead": return
        
        if self.player_state != "falling" and self.player_state != "jumping":
            state_char = self.player_state[0]
            if state_char == 'r' or state_char == 'w':
                state_frame = int(self.player_state[-1])
                state_frame_max = 2
            elif state_char == 's':
                state_frame = int(self.player_state[-1])
                state_frame_max = 4
            
            if state_frame == state_frame_max:
                state_frame = 0
            state_frame += 1
            
            
            self.player_state = self.player_state[0:-1] + str(state_frame)
        elif self.player_state == "jumping":
            self.player_y += 15
            if self.player_y > 40:
                self.player_state = "falling"
        elif self.player_state == "falling":
            self.player_y -= 15
            if self.player_y == 0:
                self.player_state = "running_1"

        self.inter_class_communications.tile_states = self.tile_states
        self.inter_class_communications.player_y = self.player_y
        self.player_score += 1
        self.tile_offset_x += 16 + ((time()-self.start_time)*0.001*(self.player_score*0.1))
        if self.tile_offset_x > 31:
            self.obstacles.pop(0)
            if randint(0, 1):
                if self.obstacles[9:12] == [0, 0, 0]:
                    self.obstacles.append(f"cat_claw_number_{randint(1, 2)}.png")
                else: self.obstacles.append(0)
            else: self.obstacles.append(0)
            self.inter_class_communications.obstacles = self.obstacles
            
            for i, _ in enumerate(self.tile_states):
                self.tile_states[i].pop(0)
                if i == 7:
                    floors = [background_sprite for background_sprite in self.inter_class_communications.background_sprites.keys() if background_sprite[0:5] == "floor"]
                    self.tile_states[i].append(choice(floors))
                else:
                    walls = [background_sprite for background_sprite in self.inter_class_communications.background_sprites.keys() if background_sprite[0:5] != "floor"]
                    self.tile_states[i].append(choice(walls))
            self.tile_offset_x = 0
        self.inter_class_communications.tile_offset_x = self.tile_offset_x
    
    def check_controls(self) -> None:
        if (self.inter_class_communications.controls_state & 0b01) == 0b01:
            self.reset()
            self.inter_class_communications.controls_state = self.inter_class_communications.controls_state ^ 0b01
        elif (self.inter_class_communications.controls_state & 0b10) == 0b10 and self.player_state != "jumping" and self.player_state != "falling" and self.player_state != "dead":
            self.player_state = "jumping"
            self.inter_class_communications.controls_state = self.inter_class_communications.controls_state ^ 0b10
            
        return
    
    def check_collision(self) -> None:
        for i, obstacle in enumerate(self.obstacles):
            if obstacle != 0:
                print(self.player_y)
                if i*32-self.tile_offset_x in range(133, 133+32) and self.player_y < 32:
                    self.player_state = "dead"

        return