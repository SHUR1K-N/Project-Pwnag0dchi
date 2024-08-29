import glob
import json
import logging
import os
import zipfile
from io import BytesIO

import pwnagotchi
import pwnagotchi.plugins as plugins
from flask import abort
from flask import render_template_string
from flask import send_file
from flask import send_from_directory

TEMPLATE = """
{% extends "base.html" %}
{% set active_page = "handshakes" %}

{% block title %}
    {{ title }}
{% endblock %}

{% block styles %}
    {{ super() }}
    <style>
        #filter {
            width: 100%;
            font-size: 16px;
            padding: 12px 20px 12px 40px;
            border: 1px solid #ddd;
            margin-bottom: 12px;
        }
    </style>
{% endblock %}
{% block script %}
    var shakeList = document.getElementById('list');
    var filter = document.getElementById('filter');
    var filterVal = filter.value.toUpperCase();

    filter.onkeyup = function() {
        document.body.style.cursor = 'progress';
        var table, tr, tds, td, i, txtValue;
        filterVal = filter.value.toUpperCase();
        li = shakeList.getElementsByTagName("li");
        for (i = 0; i < li.length; i++) {
            txtValue = li[i].textContent || li[i].innerText;
            if (txtValue.toUpperCase().indexOf(filterVal) > -1) {
                li[i].style.display = "list-item";
            } else {
                li[i].style.display = "none";
            }
        }
        document.body.style.cursor = 'default';
    }

{% endblock %}

{% block content %}
    <a class="ui-btn" href="/plugins/handshakes-dl/all">Download Zip</a>
    <input type="text" id="filter" placeholder="Search for ..." title="Type in a filter">
    <ul id="list" data-role="listview" style="list-style-type:disc;">
        {% for handshake in handshakes %}
            <li class="file">
                <a href="/plugins/handshakes-dl/{{handshake}}">{{handshake}}</a>
            </li>
        {% endfor %}
    </ul>
{% endblock %}
"""


class HandshakesDL(plugins.Plugin):
    __author__ = "me@sayakb.com"
    __version__ = "0.2.2"
    __license__ = "GPL3"
    __description__ = "Download handshake captures from web-ui."

    def __init__(self):
        self.ready = False

    def on_loaded(self):
        logging.info("[HandshakesDL] plugin loaded")

    def on_config_changed(self, config):
        self.config = config
        self.ready = True

    def on_webhook(self, path, request):
        if not self.ready:
            return "Plugin not ready"

        if path == "/" or not path:
            handshakes = glob.glob(
                os.path.join(self.config["bettercap"]["handshakes"], "*.pcap"))
            handshakes = [os.path.basename(path)[:-5] for path in handshakes]
            return render_template_string(
                TEMPLATE,
                title="Handshakes | " + pwnagotchi.name(),
                handshakes=handshakes,
            )
        elif path == "all":
            logging.info(f"[HandshakesDL] creating Zip-File in memory")
            memory_file = BytesIO()
            with zipfile.ZipFile(memory_file, "w") as zf:
                files = glob.glob(
                    os.path.join(self.config["bettercap"]["handshakes"],
                                 "*.pcap"))
                try:
                    for individualFile in files:
                        zf.write(individualFile)
                except Exception as e:
                    logging.error(f"[HandshakesDL] {e}")
                    abort(404)
            memory_file.seek(0)
            logging.info(f"[HandshakesDL] serving handshakes.zip")
            return send_file(memory_file,
                             attachment_filename="handshakes.zip",
                             as_attachment=True)
        else:
            dir = self.config["bettercap"]["handshakes"]
            try:
                logging.info(f"[HandshakesDL] serving {dir}/{path}.pcap")
                return send_from_directory(directory=dir,
                                           path=path + ".pcap",
                                           as_attachment=True)
            except FileNotFoundError:
                abort(404)
