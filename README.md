# Project Pwnag0dchi
Created this since a lot of people were asking about the customized plugins & configurations I use. Following this guide, your Pwnagotchi will look *exactly* as seen on my socials & YouTube videos in ~5mins tops.

You'll also find a complete Pwnagotchi noob build guide + some common troubleshooting methods here.

*I'll keep updating this as much as possible. If you have a suggestion or run into problems using this project, open up a GitHub Issue and we can talk about it!*

## Table of Contents
- [Project Pwnag0dchi Modifications](https://github.com/SHUR1K-N/Project-Pwnag0dchi#Project-Pwnag0dchi-modifications)
	- [Features](https://github.com/SHUR1K-N/Project-Pwnag0dchi#features)
	- [Showcase & Tutorial Video](https://github.com/SHUR1K-N/Project-Pwnag0dchi#sick-feature-showcase--tutorial-video)
	- [Installing Project Pwnag0dchi](https://github.com/SHUR1K-N/Project-Pwnag0dchi#installing-project-pwnag0dchi)
		- [Login Credentials (Web UI)](https://github.com/SHUR1K-N/Project-Pwnag0dchi#login-credentials-web-ui) 
 		- [Initial settings to be changed](https://github.com/SHUR1K-N/Project-Pwnag0dchi#initial-settings-to-be-changed)
---
- [Pwnagotchi Noob Guide](https://github.com/SHUR1K-N/Project-Pwnag0dchi#pwnagotchi-noob-guide)
    - [Parts To Get](https://github.com/SHUR1K-N/Project-Pwnag0dchi#parts-to-get)
    - [Installation](https://github.com/SHUR1K-N/Project-Pwnag0dchi#installation)
    - [SSH / Web UI Access Setup](https://github.com/SHUR1K-N/Project-Pwnag0dchi#getting-your-pwnagotchi-to-be-accessible-via-ssh--web-ui)
    - [FTP Access Setup](https://github.com/SHUR1K-N/Project-Pwnag0dchi#getting-your-pwnagotchi-to-be-accessible-via-ftp)
    - [Setting Up Internet-Sharing](https://github.com/SHUR1K-N/Project-Pwnag0dchi#setting-up-internet-sharing-internet-access-for-pwnagotchi)
    - [Local Handshake Cracking](https://github.com/SHUR1K-N/Project-Pwnag0dchi#local-handshake-cracking-within-the-pwnagotchi-itself-without-internet--wpa-sec)
    - [Bluetooth Tethering Setup](https://github.com/SHUR1K-N/Project-Pwnag0dchi#bluetooth-tethering-short--crisp)
    - [Using External Wi-Fi Adapters](https://github.com/SHUR1K-N/Project-Pwnag0dchi#using-external-wi-fi-adapters)
        - [Enabling External Wi-Fi Adapter](https://github.com/SHUR1K-N/Project-Pwnag0dchi#enabling-external-wi-fi-adapter)
        - [Disabling External Wi-Fi Adapter](https://github.com/SHUR1K-N/Project-Pwnag0dchi#disabling-external-wi-fi-adapter)

---

- [Additional Customizations](https://github.com/SHUR1K-N/Project-Pwnag0dchi#additional-customizations)
   - [Custom Faces](https://github.com/SHUR1K-N/Project-Pwnag0dchi#custom-pwnagotchi-faces-tutorial)
   - [Massive Plugins List](https://github.com/SHUR1K-N/Project-Pwnag0dchi#massive-plugins-list-names-descriptions-links-etc)
---
- [Troubleshooting](https://github.com/SHUR1K-N/Project-Pwnag0dchi#troubleshooting)
	- [Internet Sharing Not Working](https://github.com/SHUR1K-N/Project-Pwnag0dchi#internet-sharing-not-working-or-was-previously-working)
 	- [Can't connect 'gotchi to computer since switching to external adapter](https://github.com/SHUR1K-N/Project-Pwnag0dchi#cannot-connect-my-gotchi-to-my-computer-since-switching-to-external-adapter)
	- [Deauths even when "enable_deauth" plugin disabled](https://github.com/SHUR1K-N/Project-Pwnag0dchi#my-gotchi-deauths-even-when-the-enable_deauth-plugin-is-turned-off)
	- [Associations even when "enable_assoc" plugin disabled](https://github.com/SHUR1K-N/Project-Pwnag0dchi#my-gotchi-does-associations-even-when-the-enable_assoc-plugin-is-turned-off)
 	- [I got the tri-color variant of the Waveshare screen, and it sucks. Now what?](https://github.com/SHUR1K-N/Project-Pwnag0dchi#i-got-the-tri-color-variant-of-the-waveshare-screen-and-it-sucks-now-what)
  	- [I don't like dark mode, how do I make the UI white like default?](https://github.com/SHUR1K-N/Project-Pwnag0dchi#i-dont-like-the-dark-mode-ui-how-do-i-make-the-ui-white-like-default)
  	- [memtemp-plus elements get cut-off](https://github.com/SHUR1K-N/Project-Pwnag0dchi#memtemp-plus-elements-get-cut-off)

---
# Project Pwnag0dchi Modifications
## Features
* On-device dictionary attacks automatically upon finding handshakes (against customized, smaller wordlists)
* Individual toggles for association and deauthentication attacks to choose 1 of 3 attack approaches:
	* Fully aggressive (association + deauthentication attacks)
	* Less aggressive (either association or deauthentication attack)
	* Fully passive (no attacks, just passive handshake capture)
* Downloadable handshakes from web UI (fixed)
* UI elements tweaked AF (positions, sizes, fonts, etc.)
	* Space added to "CH" value to accomodate 5GHz channels without overlap
* Plugin modifications (for cosmetic purposes, decluttering, and slightly improved functionality (maybe))
* Added information to the screen:
	* Latest cracked handshake in plain-text (as per WPA-sec)
 	* Level & XP bar (collect handshakes to gain XP and level up)
	* Enabled attacks (association, deauthentication, or both, or none)
 	* Hardware monitoring (current memory usage, CPU usage, CPU frequency, and temperature)
  	* Internet connection/sharing status
  	* Current interface's IP address (helps with connecting via SSH / web UI)
* More stuff I may be forgetting

## Sick Feature Showcase & Tutorial Video

[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/rNAYWvSMP6o/maxresdefault.jpg)](https://www.youtube.com/watch?v=rNAYWvSMP6o)

## Installing Project Pwnag0dchi
1. Copy the files from the ″Plugins″ directory of this GitHub repo to `/usr/local/share/pwnagotchi/custom-plugins/`
2. Copy the files from the ″Configurations″ directory of this GitHub repo to `/etc/pwnagotchi/`
3. Apply all changes by restarting your Pwnagotchi

### Login Credentials (Web UI)
`changeme:changeme`

### Initial settings to be changed
Via web UI: Plugins > webcfg

Via `/etc/pwnagotchi/config.toml`

Then make the following additions / changes:

1. `main.name` should be whatever you'd like to name your Pwnagotchi (example: Pwnag0dchi)
2. `main.whitelist.#0` & `main.plugins.grid.exclude` should be the SSID of your home Wi-Fi network, so your Pwnagotchi does not attack it (example: Shuriken-WiFi_2.4GHz)
3. `main.plugins.wpa-sec.api_key` should be your WPA-sec API key (go [here first](https://wpa-sec.stanev.org) and click on "Get key" to get your free API key e-mailed to you
	> NOTE: When copy-pasting the API key to `main.plugins.wpa-sec.api_key`, make sure there are no spaces at the beginning or end of the API key
4. Restart the Pwnagotchi service to apply changes using `sudo systemctl restart pwnagotchi.service`. On the web UI, this can be done by clicking ″Save and Restart″ at the top in the webcfg plugin

---
---

# Pwnagotchi Noob Guide
## Parts To Get
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

## Installation
1. Attach the Waveshare display to the Pi Zero (hardware part done!)
2. Download a [jayofelony's](https://github.com/jayofelony/pwnagotchi) v2.8.9 release image (thoroughly tested) or v2.9.3 release image (works as far as tested)
3. Download / Install [Balena Etcher](https://etcher.balena.io/#download-etcher)
4. Insert your Pwnagotchi's micro-SD into a card-reader, and into your computer
5. Open Balena Etcher
6. Select the downloaded Pwnagotchi image file
7. Also carefully select the inserted micro-SD card
8. Flash!
9. After flashing completes, insert the micro-SD card into your Pwnagotchi and power it on
10. **On the first boot, your Pwnagotchi will need some time to initialize (anywhere from 2 to even 30 minutes). During this initialization period, do not panic if you see nothing on the display or a `"Generating keys, do not turn off..."` message. Once this process is complete, your Pwnagotchi will restart by itself and be ready to use**
    > NOTE: This only applies to the first boot. You will not have to wait for more than ~2-3 minutes for any future boot-ups
11. IT'S ALIIIIIVE!

## Getting your Pwnagotchi to be accessible via SSH / web UI
Tutorial: https://youtu.be/7nj5Euo5Bng?t=135
> NOTE: **Follow only from 2:15 to 4:31**
> 
> NOTE: If you need to install RNDIS drivers manually, download it from this GitHub repo ("RNDIS Driver" directory)

`ssh pi@10.0.0.2` or `ssh pi@10.002` for short (password = `raspberry`)

## Getting your Pwnagotchi to be accessible via FTP
To FTP into your Pwnagotchi as a root user, you'll first need to initialize the root user account and also enable root FTP logins:

1. SSH into your Pwny as the pi user (as usual)
2. `sudo passwd root`
3. Enter *pi* user's password if asked (raspberry)
4. Enter a new password for *root* user
5. Save and exit. You'll now have a root user. Time to enable root FTP logins
6. `sudo nano /etc/ssh/sshd_config`
   > NOTE: `sshd_config`, not `ssh_config`
7. Change the `PermitRootLogin prohibit-password` line to `PermitRootLogin yes` and uncomment the line if it's commented (remove the `#` from the start of the line)
8. Save and exit
9. `sudo service ssh restart`

Tutorial: https://www.youtube.com/watch?v=X-5jN0WjurQ&t=88s


## Setting Up Internet-Sharing (Internet access for Pwnagotchi)
1. Connect your Pwnagotchi (data port, not power)
2. Download `win_connection_share.ps1` from this GitHub repo ("Internet Sharing" directory)
3. Open PowerShell as an administrator (right-click > "Run as administrator")
4. `cd .\Downloads\`
5. `.\win_connection_share.ps1 -SetPwnagotchiSubnet`
6. Reboot Windows machine
7. `.\win_connection_share.ps1 -EnableInternetConnectionSharing`
8. Start > type "network" > "View network connections"
9. Right-click your Pwnagotchi's RNDIS > Properties > IPv4 configuration > re-add static IP manually (10.0.0.1, 255.255.255.0, 10.0.0.1, 8.8.8.8)
10. Right-click your main ethernet > Properties > "Sharing" tab > check both boxes + select sharing for your Pwnagotchi's RNDIS > OK
11. Reconnect Pwnagotchi (data port, not power)
12. Command Prompt > `ssh pi@10.0.0.2` (password = `raspberry`)
13. Confirm Internet connectivity after Pwnagotchi initializes completely using `ping google.com`

#### Still no Internet?
1. `sudo chattr +i /etc/resolv.conf`
2. `sudo nano /etc/resolv.conf`
3. The content of this file should only be this single line:
   `nameserver    8.8.8.8`

## Local Handshake Cracking (within the Pwnagotchi itself, without Internet / WPA-sec)
The `better_quickdic` plugin is responsible for this. Just add your **small** custom wordlists to `/home/pi/wordlists/`, and an offline dictionary attack will be performed using all the wordlists in this directory as soon as a valid handshake is captured
> NOTE: Disable / Remove the `aircrackonly` & `hashie` / `hashieclean` plugins for this to be most effective. I've found in some of my testing that these plugins sometimes get rid of even valid handshakes before `better_quickdic` could start cracking them
>
> NOTE: If a handshake is cracked using this plugin, it will NOT show on the Pwnagotchi screen (even with `display-password` enabled). You'll have to manually check the `/home/pi/handshakes` directory for any files that end in `.pcap.cracked`. If you have tons of handshakes there, you can use `ls /home/pi/handshakes/ | grep crack` to quickly filter out only the ones cracked

You can use a simple lil' wordlist like the one from this GitHub repo ("Wordlists" directory). I created the wordlist based on the most common non-complex and default passwords I found during my tests. This could be different in your case due to your region / language / awareness / requirements / defaults ― so it's always better to use multiple, small, customized wordlists.

## Bluetooth-Tethering (short & crisp)
Tutorial: https://www.youtube.com/watch?v=cnmrKCBzDRU

## Using External Wi-Fi Adapters
You can attach an external Wi-Fi adapter to the Pwnagotchi for a significant increase in range, or for 5GHz support, or both.

> NOTE: You will *NOT* be able to SSH into your Pwnagotchi via USB when the external Wi-Fi adapter is enabled because the data USB port gets allotted to the external Wi-Fi adapter. Hence, it is highly recommended to first set up and confirm [Bluetooth-tethering](https://github.com/SHUR1K-N/Project-Pwnag0dchi#bluetooth-tethering-short--crisp) is working so you can access your Pwnagotchi via web UI or SSH *without* the need of a USB cable. When the external Wi-Fi adapter is *disabled*, you can access your Pwnagotchi as normal using a USB cable

> NOTE: Compatibility of external Wi-Fi adapters would completely depend on your adapter's chipset. Many chipsets are readily supported by the underlying Linux OS, but others would require you to install the chipset's driver manually via SSH. First, try the below steps and see if your adapter works with the Pwnagotchi (don't forget to reboot). If not, install the drivers manually

### Enabling External Wi-Fi Adapter
1. SSH into your Pwnagotchi
2. `sudo nano /boot/config.txt`
3. Locate the `[all]` section
4. Uncomment `dtoverlay=disable-wifi` (remove the `#` from the start of the line)
5. Comment out `dtoverlay=dwc2` (add a `#` at the start of the line)
6. Reboot Pwnagotchi with Wi-Fi adapter *connected* (data port, not power)

### Disabling External Wi-Fi Adapter
1. SSH into your Pwnagotchi
2. `sudo nano /boot/config.txt`
3. Locate the `[all]` section
4. Comment out `dtoverlay=disable-wifi` (add a `#` at the start of the line)
5. Uncomment `dtoverlay=dwc2` (remove the `#` from the start of the line)
6. Reboot Pwnagotchi with Wi-Fi adapter *disconnected* (data port, not power)

---
---

# Additional Customizations

## Custom Pwnagotchi faces tutorial
[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/X-5jN0WjurQ/maxresdefault.jpg)](https://www.youtube.com/watch?v=X-5jN0WjurQ)

## Massive Plugins List (names, descriptions, links, etc.)
https://docs.google.com/spreadsheets/d/1os8TRM3Pc9Tpkqzwu548QsDFHNXGuRBiRDYEsF3-w_A

---
---

# Troubleshooting
## Internet-Sharing Not Working (or was previously working)
1. Connect Pwnagotchi (data port, not power)
2. Start > type "network" > "View network connections"
3. Right-click your primary ethernet (Internet) > Properties > "Sharing" tab > uncheck both boxes > OK
4. Right-click your Pwnagotchi's RNDIS > Properties > IPv4 configuration > re-add static IP manually (10.0.0.1, 255.255.255.0, 10.0.0.1, 8.8.8.8) > OK
5. Right-click your main ethernet > Properties > "Sharing" tab > check both boxes + select sharing for your Pwnagotchi's RNDIS > OK
6. No need to restart anything. Verify Internet connectivity using `ping google.com` via SSH

## Cannot connect my 'gotchi to my computer since switching to external adapter
You'll need to disable the external Wi-Fi adapter to connect your Pwnagotchi to your computer via the data port.

1. Connect Pwnagotchi via Bluetooth tethering (power port, not data)
2. SSH into your Pwnagotchi (using an app like Termux)
3. `sudo nano /boot/config.txt`
4. Locate the `[all]` section
5. Comment out `dtoverlay=disable-wifi` (add a `#` at the start of the line)
6. Uncomment `dtoverlay=dwc2` (remove the `#` from the start of the line)
7. Power down Pwnagotchi
8. Connect to your computer via USB cable (data port, not power)

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
2. Web UI > Plugins > webcfg
3. Look for `ui.fps`, and change the value to `1` or `2`
4. Scroll to the top, hit "Save and Restart". The screen should work relatively much better now

## I don't like the dark mode UI, how do I make the UI white like default?
1. Connect Pwnagotchi (data port, not power)
2. Web UI > Plugins > webcfg
3. Look for `ui.invert`, and change the value to `True`
4. Scroll to the top, hit "Save and Restart"

## memtemp-plus elements get cut-off
1. Either change to the following values in the tweak_view plugin or add them in `/etc/pwnagotchi/tweak_view.json`:
```
"VSS.memtemp_header.xy": "145,82",
"VSS.memtemp_data.xy": "145,95",
"VSS.Lv.xy": "151,72"
```
