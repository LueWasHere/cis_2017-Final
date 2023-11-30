from time import gmtime
from random import randint, uniform

class PCS_Data_Class:
    """
    (CLASS) PCS_Data_Class
    
    (DESCRIPTION) Shortened from "Process_Data_Class", this contains all the methods and data that is needed to calculate functions relating to player score, speed, and death
    as well as being able to process the obsacles in the game
    
    (ARGUMENTS) The class takes no arguments
    """
    
    def __init__(self) -> None:
        self.player_score = 0
        self.player_speed = 0
        self.player_state = "Running"
        
        local_time = gmtime()
        self.seed = local_time.tm_year+local_time.tm_mon+local_time.tm_mday+local_time.tm_hour+local_time.tm_min+local_time.tm_sec+local_time.tm_wday+local_time.tm_yday
        
        # Ensure* a random number with binary manipulation
        # * A random number cannot 𝘵𝘳𝘶𝘭𝘺 be acheived. This method simply tries to make it a bit more random
        random_assurance = (~self.seed)**2
        random_assurance_shift = random_assurance<<4
        random_assurance = random_assurance ^ random_assurance_shift
        
        self.seed = self.seed ^ random_assurance
        print(self.seed)
        
    def reset(self) -> None:
        
        return
    
    def check_scores(self) -> None:
        
        return