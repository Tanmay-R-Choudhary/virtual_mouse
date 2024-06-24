from main_window.main_window import MainWindow
from model.run import ModelHandler
import dearpygui.dearpygui as dpg

# create the model handler
model_handler = ModelHandler()

def main():
    # create dpg context
    dpg.create_context()
    
    # create main window
    main_window = MainWindow()
    main_window.setup()
    
    while dpg.is_dearpygui_running():
        dpg.render_dearpygui_frame()
        
        # perform detection conditionally
        model_handler.set_multiplier(dpg.get_value('x_multiplier'), dpg.get_value('y_multiplier'))
        model_handler.run_main_program()
        
    # destroy dpg context
    dpg.destroy_context()
    model_handler.release_resources()
    
if __name__ == '__main__':
    main()
    