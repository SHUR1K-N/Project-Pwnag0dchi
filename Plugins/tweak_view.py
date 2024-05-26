import logging
import os, time, sys
import html
import json

import pwnagotchi.plugins as plugins
from pwnagotchi.ui.components import *
from pwnagotchi.ui.view import BLACK
from PIL import ImageFont
import pwnagotchi.ui.fonts as fonts
import pwnagotchi.utils as utils

try:
    sys.path.append(os.path.dirname(__file__))    
    from Touch_UI import Touch_Button as Button
except Exception as e:
    pass
    #logging.warn(repr(e))

from textwrap import TextWrapper

from flask import abort
from flask import render_template_string

class Tweak_View(plugins.Plugin):
    __author__ = 'Sniffleupagus'
    __version__ = '1.0.0'
    __license__ = 'GPL3'
    __description__ = 'Edit the UI layout. Ugly interface, no guardrails. Be careful!!!'

    # load from save file, parse JSON. dict maps from view_state_state key to new val
    # store originals when tweaks are applie
    #
    # have multiple base tweak files (for different display types, whatever)
    # and choose from them in config
    # - tweaks can be "system-wide" or associated with a specific base
    # - when updating the display, create a dict adding base tweaks, system-wide mods, base-specific mods
    #   so specific overrides global
    #

    def __init__(self):
        self._agent = None
        self._start = time.time()
        self._logger = logging.getLogger(__name__)
        self._tweaks = {}
        self._untweak = {}
        self._already_updated = []

        self.myFonts = {"Small": fonts.Small,
                   "BoldSmall": fonts.BoldSmall,
                   "Medium": fonts.Medium,
                   "Bold": fonts.Bold,
                   "BoldBig": fonts.BoldBig,
                   "Huge": fonts.Huge
        }

        pass

    def show_tweaks(self, request):
        res = ""
        res += '<form method=POST action="%s/delete_mods"><input id="csrf_token" name="csrf_token" type="hidden" value="{{ csrf_token() }}">\n' % request.path
        res += '<ul>\n'

        for tw, val in self._tweaks.items():
            res += '<li><input type=checkbox name=delete_me id="%s" value="%s"> %s: %s\n' % (tw, tw, tw, repr(val))
            if tw in self._untweak:
                res += '(orig: %s)\n' % repr(self._untweak[tw])
        res += '</ul>'
        res += '<input type=submit value="Delete Selected Mods"></form>'

        return res


    def dump_item(self, name, item, prefix=""):
        self._logger.debug("%s[[[%s:%s]]]" % (prefix, name, type(item)))
        res = ""
        if type(item) is int: 
            res += '%s: <input type=text name="%s%s" value="%s">' % (name, prefix, name, item)
        elif type(item) is str: 
            if item.startswith("{"):
                #print("********************\n%s JSON %s" % (prefix, item))
                try:
                    j = json.loads(item)
                    res += "%sJSON\n" % prefix, json.dumps(j, sort_keys=True,indent=4)
                except Exception as inst:
                    res += "%s%s = '%s'\n" % (prefix, name, item)
                else:
                    res += '%s: <input type=text name="%s%s" value="%s">' % (name, prefix, name, item)
                    res += "%s%s = '%s'\n" % (prefix, name, item)
        elif type(item) is float: 
            res += "%s%s = %s\n" % (prefix, name, item)
            res += '%s: <input type=text name="%s%s" value="%s">' % (name, prefix, name, item)
        elif type(item) is bool: 
            res += "%s%s is %s\n" % (prefix, name, item)
        elif type(item) is list: 
            #if (prefix is ""): 
            if len(item) > 1: res += "\n"
            res += "%s[%s]\n" % (prefix, name)
            i = 0
            for key in item:
                i=i+1
                self._logger.debug("%s<%i> %s\n" % (prefix, i, key))
                res += self.dump_item("{%i}" % (i), key, "  %s %s" % (" " * len(prefix), name)) + "\n"

            if (prefix is ""): 
                res += "%s[%s END]\n" % (prefix, name)

        elif type(item) is dict: 
            #res += "Dict: [%s] [%s]<ul>\n" % (prefix, name)
            for key in item:
                self._logger.debug("%s>>> %s:%s" % (prefix, key, type(item[key])))
                res += "<li>" + self.dump_item("%s" % (key), item[key], "%s%s" % (prefix, name)) + "\n"
                #prefix = " " * len(prefix)
                #name = " " * len(name)
            res += "</ul>"
        elif isinstance(item, Widget):
            res += "<b>%s:</b> %s\n<ul>" % (html.escape(str(type(item).__name__)), name)
            try:
                for key in dir(item):
                    val = getattr(item, key)
                    if key.startswith("__"):
                        pass
                    elif key is "value":
                        res += '<li>%s.%s = "%s"\n' % (name, html.escape(key), html.escape(str(val)))
                    elif key is "draw":
                        pass
                    elif key is "xy": # n-tuple of coordinates, 2 for text & label, 4 for line
                        res += '<li>%s.xy: <input type=text name="%s.%s.xy" value="%s">' % (name, prefix, name, html.escape(",".join(map(str,val))))
                    elif key in ("label", "label_spacing"):
                        res += '<li>%s.%s: <input type=text name="%s.%s.%s" value="%s"><br>' % (name, html.escape(key), prefix, name, html.escape(key), html.escape(str(val)))
                    elif type(val) in (int, str):
                        res += '<li>%s.%s: <input type=text name="%s.%s.%s" value="%s"><br>' % (name, html.escape(key), prefix, name, html.escape(key), html.escape(str(val)))
                    elif "font" in key:
                        tag = "%s.%s.%s" % (prefix, name, html.escape(key))
                        res += '<li>%s.%s: <select id="%s" name="%s">\n' % (name, html.escape(key), tag, tag)

                        for l,f in self.myFonts.items():
                            if val == f:
                                res += '  <option value="%s" selected>%s</option>' % (l, l)
                            else:
                                res += '  <option value="%s">%s</option>' % (l, l)
                        res += "</select>"
                    else:
                        res += '<li>%s["%s"].%s = %s\n' % (prefix, name, html.escape(key),  html.escape("<" + str(type(val).__name__) + ">"))
                        #res += self.dump_item('%s["%s"].%s' % (prefix, name, html.escape(key)), val)
                    
            except Exception as inst:
                res += "*%s] Error processing %s<br>\n" % (prefix,name)
                res += "%s, %s<br>\n" % (prefix, type(inst))
                res += "%s %s<br>\n" % (prefix, inst.args)
                res += "%s %s<br>\n" % (prefix, inst)
            res += "</ul>"
        else:
            try:
                res += "%sUnknown type %s<br>\n" % (prefix,name)
                res += "%s %s is a %s<br><ul>\n" % (prefix, name, html.escape(str(type(item))))
                for key in dir(item):
                    val = getattr(item, key)
                    if key.startswith("__"):
                        res += "<li>%s%s.%s = %s\n" % (prefix, name, key, html.escape(repr(getattr(item, key))))
                        pass
                    else:
                        self._logger.debug("%s>>> %s:%s" % (prefix, key, html.escape(str(type(getattr(item, key))))))
                        res += "<li>%s%s.%s = %s %s\n" % (prefix, name, key, html.escape("<"+ str(type(val).__name__) + ">"), html.escape(repr(val)))
                        #res += self.dump_item("%s" % (key), repr(getattr(item, key), "%s%s." % (prefix, name)) + "\n"
                res += "</ul>"
            except Exception as inst:
                res += "*%s] Error processing %s\n" % (prefix,name)
                res += "%s, %s\n" % (prefix, type(inst))
                res += "%s %s\n" % (prefix, inst.args)
                res += "%s %s\n" % (prefix, inst)


        return res


    def update_from_request(self, request):
        res = "<ul>"
        changed = False
        try:
            view = self._agent.view()
            for k,val in request.form.items():
                if k.startswith("VSS."):
                    key = k.split(".")
                    key = [ x.strip() for x in key]
                    #res += "<li> %s" % "-".join(key)
                    if key[2] in dir(view._state._state[key[1]]):
                        oldval = eval("view._state._state[key[1]].%s" % key[2])
                        if "font" in key[2]:
                            if oldval != self.myFonts[val]:
                                oldf = "unknown %s" % repr(oldval)
                                for n,f in self.myFonts.items():
                                    if f == oldval:   # found existing font
                                        oldf = n
                                        res += "<li>%s.%s == %s, %s" % (key[1], key[2], html.escape(val), html.escape(oldf))
                                self._tweaks[k] = val
                                changed = True
                        elif "color" in key[2]:
                            if val != "%s" % oldval:
                                res += "<li>*%s.%s : new %s, old %s" % (key[1], key[2], html.escape(repr(val)), html.escape(repr(oldval)))
                                # validate that it is actual color?
                                if self._ui:
                                    self._ui._state._state[key[1]].color = val
                                self._tweaks[k] = val
                                changed = True
                        elif "xyz" in key[2]:
                            old_xy = ",".join(map(str,oldval))
                            new_xy = val.split(",")
                            new_xy = [float(x.strip()) for x in new_xy]
                            for i in range(len(oldval)):
                                if oldval[i] != new_xy[i]:
                                    res += "<li>-%s.%s != %s, %s" % (key[1], key[2], html.escape(repr(new_xy)), html.escape(repr(oldval)))
                                    res += "<li>-%s.%s != %s, %s" % (key[1], key[2], val, old_xy)
                                    break
                        elif type(oldval) in (list, tuple):
                            for i in range(len(oldval)):
                                new_xy = val.split(",")
                                new_xy = [int(float(x.strip())) for x in new_xy]
                                if float(oldval[i]) != new_xy[i]:
                                    res += "<li>LIST %s.%s != %s, %s" % (key[1], key[2], html.escape(repr(val)), html.escape(repr(oldval)))
                                    self._tweaks[k] = val
                                    changed = True
                                    res += "<li>Tweak %s -> %s" % (k, self._tweaks[k])
                        elif type(oldval) is int:
                            if oldval != int(float(val)):
                                res += "<li>*%s.%s != %s, %s" % (key[1], key[2], html.escape(repr(val)), html.escape(repr(oldval)))
                                self._tweaks[k] = int(float(val))
                                changed = True
                        elif type(oldval) is str:
                            if oldval != str(val):
                                res += "<li>S%s.%s != %s, %s (%s)" % (key[1], key[2], html.escape(str(val)), html.escape(str(oldval)), html.escape(str(type(val))))
                                self._tweaks[k] = val
                                changed = True
                        elif str(val) != str(oldval):
                            res += "<li>^%s.%s != %s, %s (%s)" % (key[1], key[2], html.escape(str(val)), html.escape(str(oldval)), html.escape(str(type(val))))

                        if changed:
                            if key[1] in self._already_updated:
                                self._already_updated.remove(key[1])
                            
            if changed:
                try:
                    with open(self._conf_file, "w") as f:
                        f.write(json.dumps(self._tweaks, indent=4))
                except Exception as err:
                    ret += "<li><b>Unable to save settings:</b> %s" % repr(err)

                            
        except Exception as err:
            res += "<li><b>update from request err:</b> %s" % repr(err)
        res += "</ul>"
        return res
    
    # called when http://<host>:<port>/plugins/<plugin>/ is called
    # must return a html page
    # IMPORTANT: If you use "POST"s, add a csrf-token (via csrf_token() and render_template_string)
    def on_webhook(self, path, request):
        try:
            if request.method == "GET":
                if path == "/" or not path:
                    
                    ret = '<html><head><title>Tweak view. Woohoo!</title><meta name="csrf_token" content="{{ csrf_token() }}"></head>'
                    ret += "<body><h1>Tweak View</h1>"
                    ret += '<img src="/ui?%s">' % int(time.time())
                    if path: ret += "<h2>Path</h2><code>%s</code><p>" % repr(path)
                    #ret += "<h2>Request</h2><code>%s</code><p>" % self.dump_item("Request", request)
                    if self._agent:
                        view = self._agent.view()
                        ret += '<h2>Available View Elements</h2><pre><form method=post><input id="csrf_token" name="csrf_token" type="hidden" value="{{ csrf_token() }}">'
                        ret += "%s" % (self.dump_item("VSS", view._state._state ))
                        ret += '<input type=submit name=submit value="Update View"></form></pre><p>'
                        ret += "</body></html>"
                    return render_template_string(ret)
                else:
                    abort(404)
            elif request.method == "POST":
                if path == "update":
                    ret = '<html><head><title>Tweak view. Update!</title><meta name="csrf_token" content="{{ csrf_token() }}"></head>'
                    ret += "<body><h1>Tweak View Update</h1>"
                    ret += '<img src="/ui?%s">' % int(time.time())
                    ret += "<h2>Path</h2><code>%s</code><p>" % repr(path)
                    ret += "<h2>Request</h2><code>%s</code><p>" % self.dump_item("Request", request.values)
                    ret += "<h2>Current Mods</h2>%s<p>" % self.show_tweaks(request)
                    ret += "</body></html>"
                elif path == "delete_mods":
                    ret = '<html><head><title>Tweak view. Update!</title><meta name="csrf_token" content="{{ csrf_token() }}"></head>'
                    ret += "<body><h1>Tweak View Update</h1>"
                    ret += '<img src="/ui?%s">' % int(time.time())
                    if "delete_me" in request.form:
                        ret += "<h2>Delete Mods</h2><ul>\n"
                        changed = False
                        for d in request.form.getlist("delete_me"):
                            if d in self._untweak:
                                try:
                                    ret += "<li>Revert %s: %s" % (d, repr(self._untweak[d]))
                                    vss, element, key = d.split(".")
                                    ui = self._agent.view()
                                    if hasattr(ui._state._state[element], key):
                                        value = self._untweak[d]
                                        setattr(ui._state._state[element], key, value)
                                        ret += "<li>Reverted %s %s to %s\n" % (element, key, repr(value))
                                        self._logger.info("Reverted %s xy to %s" % (element, repr(getattr(ui._state._state[element], key))))
                                        del(self._untweak[d])
                                except Exception as err:
                                    ret += "<li>Revert %s failed: %s" % (d, repr(err))
                            else:
                                ret += "<li>%s not in backups\n" % d

                            if d in self._tweaks:
                                try:
                                    del(self._tweaks[d])
                                    ret += "<li>Removed mod %s\n" % d
                                    changed = True
                                except Exception as err:
                                    ret += "<li>Error deleting %s: %s" % (d, repr(err))
                        if changed:
                            try:
                                with open(self._conf_file, "w") as f:
                                    f.write(json.dumps(self._tweaks, indent=4))
                                    ret += "<li>Saved mods\n"
                            except Exception as err:
                                ret += "<li><b>Unable to save settings:</b> %s" % repr(err)
                            
                        ret += "</ul>\n"
                    ret += "<h2>Path</h2><code>%s</code><p>" % repr(path)
                    ret += "<h2>Request</h2><code>%s</code><p>" % self.dump_item("Request", request.values)
                    ret += "<h2>Current Mods</h2>%s<p>" % self.show_tweaks(request)
                    ret += "</body></html>"
                else:
                    ret = '<html><head><title>Tweak view. Result!</title><meta name="csrf_token" content="{{ csrf_token() }}"></head>'
                    ret += "<body><h1>Tweak View POST</h1>"
                    ret += '<img src="/ui?%s">' % int(time.time())
                    ret += "<h2>Path</h2><code>%s</code><p>" % repr(path)
                    #ret += "<h2>Request</h2><code>%s</code><p>" % self.dump_item("request", request)
                    ret += "<h2>Form</h2><code>%s</code><p>" % self.update_from_request(request)
                    ret += "<h2>Current Mods</h2>%s<p>" % self.show_tweaks(request)
                    ret += "</body></html>"
                return render_template_string(ret)
            else:
                ret = '<html><head><title>Tweak view. Woohoo!</title><meta name="csrf_token" content="{{ csrf_token() }}"></head>'
                ret += "<body><h1>Tweak View</h1>"
                ret += '<img src="/ui?%s">' % int(time.time())
                if path: ret += "<h2>Path</h2><code>%s</code><p>" % repr(path)
                ret += "</body></html>"
                return render_template_string(ret)
                
                    
        except Exception as err:
            self._logger.warning("webhook err: %s" % repr(err))
            return "<html><head><title>oops</title></head><body><code>%s</code></body></html>" % html.escape(repr(err))

    # called when the plugin is loaded
    def on_loaded(self):
        self._start = time.time()
        self._state = 0
        self._next = 0


    # called when everything is ready and the main loop is about to start
    def on_ready(self, agent):
        self._agent = agent


    # called before the plugin is unloaded
    def on_unload(self, ui):
        try:
            state = ui._state._state
            # go through list of untweaks
            for tag, value in self._untweak.items():
                vss,element,key = tag.split(".")
                self._logger.debug("Reverting: %s to %s" % (tag, repr(value)))
                if key in dir(ui._state._state[element]):
                    if key == "xy":
                        ui._state._state[element].xy = value
                        self._logger.debug("Reverted %s xy to %s" % (element, repr(ui._state._state[element].xy)))
                    else:
                        try:
                            self._logger.debug("Trying to revert %s" % tag)
                            if hasattr(state, key):
                                setattr(ui._state._state[element], key, value)
                                self._logger.debug("Reverted %s xy to %s" % (element, repr(getattr(ui._state._state[element], key))))
                        except Exception as err:
                            self._logger.warning("revert %s: %s, %s" % (tag, repr(err), repr(ui)))                            
        except Exception as err:
            self._logger.warning("ui unload: %s, %s" % (repr(err), repr(ui)))



    # called to setup the ui elements
    # look at config. Move items around as desired
    def on_ui_setup(self, ui):
        self._ui = ui

        self.myFonts = {"Small": fonts.Small,
                   "BoldSmall": fonts.BoldSmall,
                   "Medium": fonts.Medium,
                   "Bold": fonts.Bold,
                   "BoldBig": fonts.BoldBig,
                   "Huge": fonts.Huge
        }

        # include lots more sizes
        for p in [6, 7, 8, 9, 10, 11, 12, 14, 16, 18, 20, 24, 25, 28, 30, 35, 42, 48, 52, 54, 60, 69, 72, 80, 90, 100, 120]:
            self.myFonts["Deja %s" % p] = ImageFont.truetype('DejaVuSansMono', p)
            self.myFonts["DejaB %s" % p] = ImageFont.truetype('DejaVuSansMono-Bold', p)
            self.myFonts["DejaO %s" % p] = ImageFont.truetype('DejaVuSansMono-Oblique', p)

        # load a config file... /etc/pwnagotchi/tweak_view.json for default
        self._conf_file = self.options["filename"] if "filename" in self.options else "/etc/pwnagotchi/tweak_view.json"

        try:
            if os.path.isfile(self._conf_file):
                with open(self._conf_file, 'r') as f:
                    self._tweaks = json.load(f)
                    for i in self._tweaks:
                        self._logger.debug ("Ready tweak %s -> %s" % (i, self._tweaks[i]))

            self._already_updated = []
            self._logger.info("Tweak view ready.")

        except Exception as err:
            self._logger.warn("TweakUI loading failed: %s" % repr(err))

        try:
            self.update_elements(ui)
        except Exception as err:
            self._logger.warning("ui setup: %s" % repr(err))

    def on_ui_update(self, ui):
        self.update_elements(ui)
        
    def update_elements(self, ui):
        # update those elements
        try:
            state = ui._state._state
            # go through list of tweaks
            updated = []
            for tag, value in self._tweaks.items():
                vss,element,key = tag.split(".")
                try:
                    if element not in self._already_updated and element in state and key in dir(state[element]):
                        if tag not in self._untweak:
                            #self._untweak[tag] = eval("ui._state._state[element].%s" % key)
                            self._untweak[tag] = getattr(ui._state._state[element], key)
                            self._logger.debug("Saved for unload: %s = %s" % (tag, self._untweak[tag]))

                        if key == "xy":
                            new_xy = value.split(",")
                            new_xy = [int(float(x.strip())) for x in new_xy]
                            if new_xy[0] < 0: new_xy[0] = ui.width() + new_xy[0]
                            if new_xy[1] < 0: new_xy[1] = ui.height() + new_xy[1]
                            if ui._state._state[element].xy != new_xy:
                                ui._state._state[element].xy = new_xy
                                self._logger.debug("Updated xy to %s" % repr(ui._state._state[element].xy))
                        elif key == "font":
                            if value in self.myFonts:
                                ui._state._state[element].font = self.myFonts[value]
                        elif key == "text_font":
                            if value in self.myFonts:
                                ui._state._state[element].text_font = self.myFonts[value]
                        elif key == "alt_font":
                            if value in self.myFonts:
                                ui._state._state[element].alt_font = self.myFonts[value]
                        elif key == "label_font":
                            if value in self.myFonts:
                                ui._state._state[element].label_font = self.myFonts[value]
                        elif key == "color":
                            logging.debug("Color: %s = %s" % (element, value))
                            ui._state._state[element].color = value
                        elif key == "label":
                            ui._state._state[element].label = value
                        elif key == "label_spacing":
                            ui._state._state[element].label_spacing = int(value)
                        elif key == "max_length":
                            uie = ui._state._state[element]
                            uie.max_length = int(value)
                            uie.wrapper = TextWrapper(width=int(value), replace_whitespace=False) if uie.wrap else None
                        if element not in updated:
                            updated.append(element)
                    elif element in self._already_updated and not element in state:
                        # like a plugin unloaded
                        self._already_updated.remove(element)
                except Exception as err:
                    self._logger.warn("tweak failed for key %s: %s" % (tag, repr(err)))

            for element in updated:
                if element not in self._already_updated:
                    self._already_updated.append(element)
        except Exception as err:
            self._logger.warning("ui update: %s, %s" % (repr(err), repr(ui)))
