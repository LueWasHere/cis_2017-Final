from sys import version_info
from sys import exit as exit_sys
import mouse_runner.code.process_data as process_data
import mouse_runner.code.display as display
import mouse_runner.code.communications as comms
from os import path, system
from platform import system as os_system
from time import sleep
from colorama import Cursor

def clear_terminal() -> None:
    """
        (FUNCTION) clear_terminal
        
        (DESCRIPTION) Clear the screen based on OS.
        
        (ARGUMENTS) The function takes no arguments

        (RETURNS) The function returns nothing
    """
    
    if os_system() == "Windows":
        system("cls")
        return
    
    system("clear")

    return

def main(dsp_class: display.DSP_Screen_Class, prc_class: process_data.PCS_Data_Class) -> tuple:
    """
    (FUNCTION) main
    
    (DESCRIPTION) The main function. This is where the magic happens.
    
    (ARGUMENTS)

    (CLASS(DSP_Screen_Class)) dsp_class (Description) The display class 
    (CLASS(PRC_Data_Class)) prc_class (Description) The data processing class 

    (RETURNS) The function returns a bool to represent if the program should stop
    """

    try:
        assert version_info >= (2, 5) # Check pyton version
    except AssertionError:
        return -25, "The current python version is outdated. Python version 3.0 or greater is required for this program" # Error if version is not sufficient
    
    dsp_class.read_sprites() # Read sprite data
    prc_class.reset() # Reset data
    
    Game_Running = True # The game is running
    
    prc_class.player_state = "running_1" # The player is running
    
    clear_terminal() # Clear the terminal

    while Game_Running:
        print(f"{Cursor.POS(1, 1)}Your score is: {prc_class.player_score}{' ' * len(str(prc_class.last_score))}") # Print the score
        
        # Process all data, checks, and sprites
        prc_class.move_frame_forward()
        prc_class.check_controls()
        dsp_class.update_slave(prc_class.player_state)
        dsp_class.update_master()
        prc_class.check_collision()
        Game_Running = dsp_class.check_for_events()
        sleep(0.1)
        
    
    return 0, "EXIT_REQUEST" # A normal exit

if __name__ == "__main__":
    # Create an instance of each class
    com_class = comms.communication_class()
    dsp_class = display.DSP_Screen_Class(game_path=path.abspath("mouse_runner"), inter_class_communications=com_class)
    prc_class = process_data.PCS_Data_Class(game_path=path.abspath("mouse_runner"), inter_class_communications=com_class)
    
    status, info = main(dsp_class, prc_class) # Run the main function
    
    if status != 0: # The result of the main function was unexpected
        print("Uh-Oh! Looks like something went wrong!\n")
        print(f"Status code: {status}\n\nDebug information: \n{info}")
    
    exit_sys(status) # Exit