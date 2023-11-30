import sys
import mouse_runner.code.process_data as process_data
import mouse_runner.code.display as display

def main(dsp_class: display.DSP_Screen_Class, prc_class: process_data.PCS_Data_Class):
    try:
        assert sys.version_info >= (2, 5)
    except AssertionError:
        return -25, "The current python version is outdated. Python version 3.0 or greater is required for this program"
    
    dsp_class.init_display()
    prc_class.reset()
    
    return 0, "EXIT_REQUEST"

if __name__ == "__main__":
    dsp_class = display.DSP_Screen_Class()
    prc_class = process_data.PCS_Data_Class()
    
    status, info = main(dsp_class, prc_class)
    
    if status != 0:
        print("Uh-Oh! Looks like something went wrong!\n")
        print(f"Status code: {status}\n\nDebug information: \n{info}")
    
    exit(status)