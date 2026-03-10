import logging
import os
import sys

import pwnagotchi.plugins as plugins
from pwnagotchi.ui.components import LabeledValue
from pwnagotchi.ui.view import BLACK
import pwnagotchi.ui.fonts as fonts

try:
    sys.path.append(os.path.dirname(__file__))
    from Touch_UI import Touch_Button, Touch_Screen
except ImportError:
    pass


class enable_deauth(plugins.Plugin):
    __author__ = 'Sniffleupagus'
    __version__ = '1.1.0'
    __license__ = 'GPL3'
    __description__ = 'Enable and disable DEAUTH on the fly. Enabled when plugin loads, disabled when plugin unloads.'

    def __init__(self):
        self._agent = None
        self._count = 0
        self.hasTouch = False
        self._touchscreen = None

    def on_loaded(self):
        self._count = 0

    def on_unload(self, ui):
        if not self.hasTouch and self._agent:
            self._agent._config['personality']['deauth'] = False
        try:
            ui.remove_element('deauth_count')
        except Exception as e:
            logging.warning("[Enable_Deauth] %r", e)
        logging.info("[Enable_Deauth] unloading: disabled deauth")

    def on_ready(self, agent):
        self._agent = agent
        self.hasTouch = self._touchscreen and self._touchscreen.running

        if self.hasTouch and self._ui:
            self._ui._state._state['deauth_count'].state = self._agent._config['personality']['deauth']
        else:
            agent._config['personality']['deauth'] = True

        logging.info("[Enable_Deauth] ready: enabled deauth")

    def on_touch_ready(self, touchscreen):
        self._touchscreen = touchscreen
        self.hasTouch = self._touchscreen and self._touchscreen.running
        logging.info("[Enable_Deauth] Touchscreen %r", touchscreen)

    def on_touch_release(self, ts, ui, ui_element, touch_data):
        logging.debug("[Enable_Deauth] Touch release: %r", touch_data)
        try:
            if ui_element == "deauth_count":
                self._agent._config['personality']['deauth'] = self._ui._state._state['deauth_count'].state
                logging.info("[Enable_Deauth] Toggled deauth to %r",
                             self._ui._state._state['deauth_count'].state)
        except Exception as e:
            logging.warning("[Enable_Deauth] %r", e)

    def on_deauthentication(self, agent, access_point, client_station):
        self._count += 1

    def on_ui_setup(self, ui):
        self._ui = ui
        self.hasTouch = self._touchscreen and self._touchscreen.running

        if "position" in self.options:
            pos = self.options['position'].split(',')
            pos = [int(x.strip()) for x in pos]
        else:
            pos = (185, 111, 30, 59)

        try:
            ui.add_element('deauth_count', Touch_Button(
                position=pos, color='#ddddff', alt_color='White',
                outline='DarkGray', state=False,
                text="deauth", value=0, text_color="Black",
                alt_text=None, alt_text_color="Green",
                font=fonts.Medium, alt_font=fonts.Medium,
                shadow="Black", highlight="White",
                event_handler="enable_deauth"))
        except Exception:
            ui.add_element('deauth_count', LabeledValue(
                color=BLACK, label='D', value='', position=pos,
                label_font=fonts.BoldSmall, text_font=fonts.Small))

    def on_ui_update(self, ui):
        ui.set('deauth_count', str(self._count))
