import dearpygui.dearpygui as dpg

class MainWindow:
    def __init__(self):
        with dpg.value_registry():            
            dpg.add_bool_value(default_value=False, tag='start_detection')
            dpg.add_bool_value(default_value=False, tag='show_camera')
            dpg.add_float_value(default_value=4.5, tag='x_multiplier')
            dpg.add_float_value(default_value=5.5, tag='y_multiplier')
    
    def setup(self):
        dpg.create_viewport(title='A Virtual Mouse', width=800, height=400, resizable=False) 
    
        def start_detection(sender, app_data):
            dpg.set_value('start_detection', not dpg.get_value('start_detection'))
            dpg.configure_item(item='detection_status_text', default_value='Status: ON' if dpg.get_value('start_detection') else 'Status: OFF')
            
        def reset_multiplier_to_default(sender, app_data):
            dpg.set_value('x_multiplier', value=4.5)
            dpg.set_value('y_multiplier', value=5.5)

        with dpg.window(label='The main window', pos=(0, 0), no_close=True, no_collapse=True, no_move=True, no_resize=True, no_title_bar=True, tag='primary_window'):
            dpg.add_text('Move the mouse with your hand/mouse.\nTo tap, touch the tip of your index and thumb finger once.\nThat is a left click.')
            dpg.add_spacer(height=20)
            dpg.add_text('Do you want to see you camera view when detection is active?')
            dpg.add_checkbox(label='Camera View', source='show_camera')
            dpg.add_spacer(height=20)
            
            dpg.add_separator()
            dpg.add_text("Sensitivity settings:")
            dpg.add_slider_float(label='X multiplier', min_value=1, max_value=6, source='x_multiplier')
            dpg.add_slider_float(label='Y multiplier', min_value=1, max_value=6, source='y_multiplier')
            dpg.add_button(label='Reset Default Multiplier Values', callback=reset_multiplier_to_default)
            dpg.add_spacer(height=20)
            
            dpg.add_separator()
            dpg.add_text('Toggle for controlling mouse using hand. NOTE! This will required a camera pointing at you. A webcam is enough.')
            dpg.add_text('Status: OFF', tag='detection_status_text')
            dpg.add_button(label='Toggle Detection', tag='start_detection_btn', callback=start_detection)
            dpg.add_spacer(height=20)

        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.set_primary_window('primary_window', True)
    