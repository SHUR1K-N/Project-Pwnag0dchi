# Project Pwnag0dchi
These are the slightly customized plugins I use along with their configurations. Complete Pwnagotchi guide + some common troubleshooting steps included.

I'll keep updating this as much as possible, and you can share suggestions or potential corrections via opening up an Issue.

## Table of Contents
- [Features](https://github.com/SHUR1K-N/Project-Pwnag0dchi#features)
- [Installing Plugins & Applying Configurations](https://github.com/SHUR1K-N/Project-Pwnag0dchi/blob/main/README.md#installing-plugins--applying-configurations)
 	- [Initial settings to be changed](https://github.com/SHUR1K-N/Project-Pwnag0dchi#initial-settings-to-be-changed)
- [Parts To Get](https://github.com/SHUR1K-N/Project-Pwnag0dchi#parts-to-get)
- [Initial Setup](https://github.com/SHUR1K-N/Project-Pwnag0dchi#initial-setup)
	- [SSH / Web UI Access Setup](https://github.com/SHUR1K-N/Project-Pwnag0dchi#getting-your-pwnagotchi-to-be-accessible-via-ssh--web-ui)
	- [Setting Up Internet-Sharing](https://github.com/SHUR1K-N/Project-Pwnag0dchi#setting-up-internet-sharing-internet-access-for-pwnagotchi)
- [Massive Plugins List](https://github.com/SHUR1K-N/Project-Pwnag0dchi#massive-plugins-list-names-descriptions-links-etc)
- [Local Handshake Cracking](https://github.com/SHUR1K-N/Project-Pwnag0dchi#local-handshake-cracking-within-the-pwnagotchi-itself-without-internet--wpa-sec)
- [Bluetooth-Tethering](https://github.com/SHUR1K-N/Project-Pwnag0dchi#bluetooth-tethering-tutorial-short--crisp)
- [Using External Wi-Fi Adapters](https://github.com/SHUR1K-N/Project-Pwnag0dchi#using-external-wi-fi-adapters)
	- [Enabling External Wi-Fi Adapter](https://github.com/SHUR1K-N/Project-Pwnag0dchi#enabling-external-wi-fi-adapter)
	- [Disabling External Wi-Fi Adapter](https://github.com/SHUR1K-N/Project-Pwnag0dchi#disabling-external-wi-fi-adapter)
- [Troubleshooting](https://github.com/SHUR1K-N/Project-Pwnag0dchi#troubleshooting)
	- [Internet Sharing Not Working](https://github.com/SHUR1K-N/Project-Pwnag0dchi#internet-sharing-not-working-or-was-previously-working)
	- [Deauths even when "enable_deauth" plugin disabled](https://github.com/SHUR1K-N/Project-Pwnag0dchi#my-gotchi-deauths-even-when-the-enable_deauth-plugin-is-turned-off)
	- [Associations even when "enable_assoc" plugin disabled](https://github.com/SHUR1K-N/Project-Pwnag0dchi#my-gotchi-does-associations-even-when-the-enable_assoc-plugin-is-turned-off)
 	- [I got the tri-color variant of the Waveshare screen, and it sucks. Now what?](https://github.com/SHUR1K-N/Project-Pwnag0dchi#i-got-the-tri-color-variant-of-the-waveshare-screen-and-it-sucks-now-what)

---
# Features
* On-device dictionary attacks automatically upon finding handshakes (against customized, smaller wordlists)
* Individual toggles for association and deauthentication attacks to choose 1 of 3 attack approaches:
	* Fully aggressive (association + deauthentication attacks)
	* Less aggressive (either association or deauthentication attack)
	* Fully passive (no attacks, just passive handshake capture)
* Downloadable handshakes from web UI (fixed)
* UI elements tweaked AF (positions, sizes, fonts, etc.)
* Plugin modifications (for cosmetic purposes, decluttering, and slightly improved functionality (maybe))
* Added information to the screen:
	* Latest cracked handshake in plain-text (as per WPA-sec)
 	* Level & XP bar (collect handshakes to gain XP and level up)
        * Enabled attacks (association, deauthentication, or both, or none)
 	* Hardware monitoring (current memory usage, CPU usage, CPU frequency, and temperature)
  	* Internet connection/sharing status
  	* Current interface's IP address (helps with connecting via SSH / web UI)
* More stuff I may be forgetting
<img src="https://github.com/SHUR1K-N/Project-Pwnag0dchi/assets/42811989/f375ba99-673f-4b7c-b8ad-d2f8dd662270" width="700">

# Installing Plugins & Applying Configurations
1. Download all plugins from the "Plugins" directory here
2. Copy all plugins to `/usr/local/share/pwnagotchi/custom-plugins/`
3. Download all files from the "Configurations" directory here
4. Coopy all files to `/etc/pwnagotchi/`
5. Apply all changes using `sudo systemctl restart pwnagotchi.service`

## Initial settings to be changed
Via web UI: Plugins > web-cfg

Via `/etc/pwnagotchi/config.toml`

Then make the following additions / changes:

1. `main.name` should be whatever you'd like to name your Pwnagotchi (example: Pwnag0dchi)
2. `main.whitelist.#0` & `main.plugins.grid.exclude` should be the SSID of your home Wi-Fi network, so your Pwnagotchi does not attack it (example: Shuriken-WiFi_2.4GHz)
3. `main.plugins.wpa-sec.api_key` should be your WPA-sec API key (go [here first](https://wpa-sec.stanev.org) and click on "Get key" to get your free API key e-mailed to you
	> NOTE: When copy-pasting the API key to `main.plugins.wpa-sec.api_key`, make sure there are no spaces at the beginning or end of the API key

# Parts To Get
* [Waveshare 2.13 inch e-Ink display](https://www.waveshare.com/2.13inch-e-paper-hat.htm)
	* Versions 3 & 4 work best. This is denoted by a small circular sticker on the board ([like this](https://www.reddit.com/r/pwnagotchi/comments/dkwl0f/visual_differences_between_version_2_and_version/))
 	* Ignore the "Rev2.1" that's printed on the board; that has nothing to do with the version
  	* Do NOT get the tri-color variant with black/white/red (variant "B"). Get only the black/white version. Both look pretty much identical and cost the same, so it's easy to purchase the wrong one
<img src="https://github.com/SHUR1K-N/Project-Pwnag0dchi/assets/42811989/94a1b13c-7370-4581-90b6-8bf47cfec131" width="800">

* [Raspberry Pi Zero W](https://www.raspberrypi.com/products/raspberry-pi-zero-w/) (soldering required)
* OR [Raspberry Pi Zero WH](https://www.adafruit.com/product/3708) (no soldering required)
	* This is the same board with pre-soldered pins (The `H` in `WH` is for "Headers")
 	* The `WH` variant may be a little more difficult to find than `W`

 * Micro-SD card — 16GBs best, must be "UHS-I"

# Initial Setup
## Getting your Pwnagotchi to be accessible via SSH / web UI
https://youtu.be/7nj5Euo5Bng?t=135
> NOTE: **Follow only from 2:15 to 4:31**
> 
> NOTE: If you need to install RNDIS drivers manually, download it from this GitHub page ("RNDIS" directory)

## Setting Up Internet-Sharing (Internet access for Pwnagotchi)
0. Connect your Pwnagotchi (data port, not power)
1. Download `win_connection_share.ps1` from this GitHub page ("Internet Sharing" directory)
2. Open PowerShell as an administrator (right-click > "Run as administrator")
3. `cd .\Downloads\`
4. `.\win_connection_share.ps1 -SetPwnagotchiSubnet`
5. Reboot Windows machine
6. `.\win_connection_share.ps1 -EnableInternetConnectionSharing`
7. Start > type "network" > "View network connections"
8. Right-click your Pwnagotchi's RNDIS > Properties > IPv4 configuration > re-add static IP manually (10.0.0.1, 255.255.255.0, 10.0.0.1, 8.8.8.8)
9. Right-click your main ethernet > Properties > "Sharing" tab > check both boxes + select sharing for your Pwnagotchi's RNDIS > OK
10. Reconnect Pwnagotchi (data port, not power)
11. Confirm Internet connectivity after Pwnagotchi initializes completely using `ping google.com`

# Massive Plugins List (names, descriptions, links, etc.)
https://docs.google.com/spreadsheets/d/1os8TRM3Pc9Tpkqzwu548QsDFHNXGuRBiRDYEsF3-w_A

# Local Handshake Cracking (within the Pwnagotchi itself, without Internet / WPA-sec)
The `better_quickdic` plugin is responsible for this. Just add your small custom wordlists to `/home/pi/wordlists/`, and a dictionary attack will be performed using all the wordlists in this directory as soon as a valid handshake is captured
> NOTE: Disable / Remove the `aircrackonly` & `hashie` / `hashieclean` plugins for this to be most effective. I've found in some of my testing that these plugins sometimes get rid of even valid handshakes before `better_quickdic` could start cracking them
>
> NOTE: If a handshake is cracked using this plugin, it will NOT show on the Pwnagotchi screen (even with `display-password` enabled). You'll have to manually check the `/home/pi/handshakes` directory for any files that end in `.pcap.cracked`. If you have tons of handshakes there, you can use `ls /home/pi/handshakes/ | grep crack` to quickly filter out only the ones cracked

# Bluetooth-Tethering Tutorial (short & crisp)
https://www.youtube.com/watch?v=cnmrKCBzDRU

# Using External Wi-Fi Adapters
You can attach an external Wi-Fi adapter to the Pwnagotchi for a significant increase in range, or for 5GHz support, or both.

> NOTE: This would completely depend on your external adapter's chipset. Many chipsets are readily supported by the underlying Linux OS, but others would require you to install the chipset's driver manually via SSH.

> TIP: First, try the below steps and see if your adapter works with the Pwnagotchi (don't forget to reboot). If not, install the drivers manually.

## Enabling External Wi-Fi Adapter
1. `sudo nano /boot/config.txt`
2. uncomment `dtoverlay=disable-wifi` (remove the `#` from the start of the line)
3. comment out `dtoverlay=dwc2` (add a `#` at the start of the line)
4. Reboot Pwnagotchi with Wi-Fi adapter *connected* (data port, not power)

## Disabling External Wi-Fi Adapter
1. `sudo nano /boot/config.txt`
2. comment out `dtoverlay=disable-wifi` (add a `#` at the start of the line)
3. uncomment `dtoverlay=dwc2` (remove the `#` from the start of the line)
4. Reboot Pwnagotchi with Wi-Fi adapter *disconnected* (data port, not power)

# Troubleshooting
## Internet Sharing Not Working (or was previously working)
1. Connect Pwnagotchi (data port, not power)
2. Start > type "network" > "View network connections"
3. Right-click your primary ethernet (Internet) > Properties > "Sharing" tab > uncheck both boxes > OK
4. Right-click your Pwnagotchi's RNDIS > Properties > IPv4 configuration > re-add static IP manually (10.0.0.1, 255.255.255.0, 10.0.0.1, 8.8.8.8) > OK
5. Right-click your main ethernet > Properties > "Sharing" tab > check both boxes + select sharing for your Pwnagotchi's RNDIS > OK
6. Reconnect Pwnagotchi (data port, not power)
7. Test Internet connectivity after Pwnagotchi initializes completely with `ping google.com`

## My 'gotchi deauths even when the "enable_deauth" plugin is turned off
This usually happens with _new_ sessions; the 'gotchi just seems to "forget" what the enable/disable state was when you power it off. Simple fix:
1. Web UI > Plugins
2. Enable and then disable "enable_deauth". This will immediately disable deauth, and the plugin's toggle will now work effectively (at least for the current session)

## My 'gotchi does associations even when the "enable_assoc" plugin is turned off
This usually happens with _new_ sessions; the 'gotchi just seems to "forget" what the enable/disable state was when you power it off. Simple fix:
1. Web UI > Plugins
2. Enable and then disable "enable_assoc". This will immediately disable association, and the plugin's toggle will now work effectively (at least for the current session)

## I got the tri-color variant of the Waveshare screen, and it sucks. Now what?
0. First of all — told you so
1. Connect Pwnagotchi (data port, not power)
2. Web UI > Plugins > web-cfg
3. Look for `ui.fps`, and change the value to `1` or `2`
4. Scroll to the top, hit "Save and restart"
5. Screen should work relatively much better now
