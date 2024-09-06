# display-password shows recently cracked passwords on the pwnagotchi display 
#
#
###############################################################
#
# Updates to the famous @nagy_craig code , now handles no files found
#
###############################################################
from pwnagotchi.ui.components import LabeledValue
from pwnagotchi.ui.view import BLACK
import pwnagotchi.ui.fonts as fonts
import pwnagotchi.plugins as plugins
import pwnagotchi
import logging
import os


class DisplayPassword(plugins.Plugin):
    __author__ = '@vanshksingh'
    __version__ = '1.0.0'
    __license__ = 'GPL3'
    __description__ = 'A plugin to display recently cracked passwords'

    def on_loaded(self):
        logging.info("display-password loaded")

    def on_ui_setup(self, ui):
        if ui.is_waveshare_v2():
            h_pos = (0, 95)
            v_pos = (180, 61)
        elif ui.is_waveshare_v4():
            h_pos = (0, 95)
            v_pos = (180, 61)
        elif ui.is_waveshare_v3():
            h_pos = (0, 95)
            v_pos = (180, 61)  
        elif ui.is_waveshare_v1():
            h_pos = (0, 95)
            v_pos = (170, 61)
        elif ui.is_waveshare144lcd():
            h_pos = (0, 92)
            v_pos = (78, 67)
        elif ui.is_inky():
            h_pos = (0, 83)
            v_pos = (165, 54)
        elif ui.is_waveshare27inch():
            h_pos = (0, 153)
            v_pos = (216, 122)
        else:
            h_pos = (0, 91)
            v_pos = (180, 61)

        if self.options['orientation'] == "vertical":
            ui.add_element('display-password', LabeledValue(color=BLACK, label='', value='',
                                                   position=v_pos,
                                                   label_font=fonts.Bold, text_font=fonts.Small))
        else:
            # default to horizontal
            ui.add_element('display-password', LabeledValue(color=BLACK, label='', value='',
                                                   position=h_pos,
                                                   label_font=fonts.Bold, text_font=fonts.Small))

    def on_unload(self, ui):
        with ui._lock:
            ui.remove_element('display-password')

    def on_ui_update(self, ui):
        potfile_path = '/home/pi/handshakes/wpa-sec.cracked.potfile'
    
        try:
            # Execute the shell command to read the last line of the potfile
            last_line = os.popen(f'tail -n 1 {potfile_path} | awk -F: \'{{print $3 "-" $4}}\'').read().rstrip()
            
            # Check if the last line is empty or contains only whitespace
            if not last_line.strip():
                # Set a default message if the last line is empty
                last_line = 'No cracked passwords'
        except Exception as e:
            # Handle exceptions, e.g., file not found, permission issues
            last_line = f'Error: {str(e)}'
        
        ui.set('display-password', last_line)
