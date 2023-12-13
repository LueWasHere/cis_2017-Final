from sys import version_info
from sys import exit as exit_sys
import mouse_runner.code.process_data as process_data
import mouse_runner.code.display as display
import mouse_runner.code.communications as comms
from os import path
from time import sleep

def main(dsp_class: display.DSP_Screen_Class, prc_class: process_data.PCS_Data_Class):
    try:
        assert version_info >= (2, 5)
    except AssertionError:
        return -25, "The current python version is outdated. Python version 3.0 or greater is required for this program"
    
    dsp_class.read_sprites()
    prc_class.reset()
    dsp_class.init_display()
    
    Game_Running = True
    
    prc_class.player_state = "running_1"
    
    while Game_Running:
        prc_class.move_frame_forward()
        prc_class.check_controls()
        dsp_class.update_slave(prc_class.player_state)
        dsp_class.update_master()
        prc_class.check_collision()
        Game_Running = dsp_class.check_for_events()
        sleep(0.1)
        
    
    return 0, "EXIT_REQUEST"

if __name__ == "__main__":
    com_class = comms.communcation_class()
    dsp_class = display.DSP_Screen_Class(game_path=path.abspath("mouse_runner"), inter_class_communications=com_class)
    prc_class = process_data.PCS_Data_Class(game_path=path.abspath("mouse_runner"), inter_class_communications=com_class)
    
    status, info = main(dsp_class, prc_class)
    
    if status != 0:
        print("Uh-Oh! Looks like something went wrong!\n")
        print(f"Status code: {status}\n\nDebug information: \n{info}")
    
    exit_sys(status)