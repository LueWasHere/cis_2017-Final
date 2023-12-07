from time import gmtime
from random import randint, uniform
from random import seed as setSeed
from .communications import communcation_class

class PCS_Data_Class:
    """
    (CLASS) PCS_Data_Class
    
    (DESCRIPTION) Shortened from "Process_Data_Class", this contains all the methods and data that is needed to calculate functions relating to player score, speed, and death
    as well as being able to process the obsacles in the game
    
    (ARGUMENTS) The class takes no arguments
    """
    
    def __init__(self, inter_class_communications: communcation_class, game_path: str="") -> None:
        self.player_score = 0
        self.player_speed = 0
        self.player_state = "sleeping_1"
        
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
        self.player_state = "sleeping_1"
        return
    
    def move_frame_forward(self) -> None:
        if self.player_state != "falling" and self.player_state != "jumping" and self.player_state != "dead":
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
    
    def check_scores(self) -> None:
        with open(self.game_path+"\\data\\player\\scores.bin", 'ab') as ScoresFile_Check: ScoresFile_Check.close() # Ensure that the file exists by opening it in append binary mode
        with open(self.game_path+"\\data\\player\\scores.bin", 'rb') as ScoresFile: # Actual open, in binary mode
            scores = bytearray(ScoresFile.read())
            ScoresFile.close()
            
        if scores == bytearray():
            pass
            
        return
    
    def check_controls(self) -> None:
        if (self.inter_class_communications.controls_state & 0b01) == 0b01:
            self.reset()
            self.inter_class_communications.controls_state = self.inter_class_communications.controls_state ^ 0b01
        elif (self.inter_class_communications.controls_state & 0b10) == 0b10:
            self.player_state = "jumping"
            self.inter_class_communications.controls_state = self.inter_class_communications.controls_state ^ 0b10
            
        return