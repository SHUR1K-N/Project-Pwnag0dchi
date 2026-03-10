from pwnagotchi import plugins
import logging
import subprocess
import shlex
import re
import os
import glob
import threading
import json

from flask import render_template_string, Response


TEMPLATE = """
{% extends "base.html" %}
{% set active_page = "plugins" %}

{% block title %}QuickDic{% endblock %}

{% block styles %}
{{ super() }}
<style>
    .qd-header {
        padding: 20px 0 10px;
    }
    .qd-header h2 {
        font-family: var(--font-pixel);
        color: var(--accent);
        font-size: 1.5rem;
        margin-bottom: 8px;
    }
    .qd-stats {
        display: flex;
        gap: 16px;
        flex-wrap: wrap;
        margin-bottom: 20px;
    }
    .qd-stat {
        background: var(--card-bg);
        border: 1px solid var(--border-color);
        border-radius: 8px;
        padding: 12px 20px;
        text-align: center;
        min-width: 100px;
    }
    .qd-stat .num {
        font-family: var(--font-pixel);
        font-size: 1.8rem;
        font-weight: bold;
    }
    .qd-stat .label {
        font-size: 0.75rem;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .qd-stat.cracked .num { color: #50fa7b; }
    .qd-stat.failed .num { color: #ff5555; }
    .qd-stat.cracking .num { color: #ff9500; }
    .qd-stat.total .num { color: var(--accent); }

    .qd-page .table-container {
        background-color: var(--card-bg);
        border: 1px solid var(--border-color);
        border-radius: 8px;
        overflow: hidden;
        box-shadow: var(--shadow-md);
    }
    .qd-page table {
        width: 100%;
        border-collapse: collapse;
    }
    .qd-page th {
        padding: 14px 16px;
        text-align: left;
        color: var(--accent);
        font-weight: 600;
        font-family: var(--font-pixel);
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-size: 0.85rem;
        border-bottom: 2px solid var(--border-color);
    }
    .qd-page td {
        padding: 12px 16px;
        border-bottom: 1px solid var(--border-color);
        color: var(--text-body);
        font-size: 0.9rem;
    }
    .qd-page tbody tr:hover {
        background-color: rgba(var(--accent-r), var(--accent-g), var(--accent-b), 0.05);
    }
    .qd-badge {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 12px;
        font-size: 0.78rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.3px;
    }
    .qd-badge.cracked { background: rgba(80,250,123,0.15); color: #50fa7b; }
    .qd-badge.failed { background: rgba(255,85,85,0.15); color: #ff5555; }
    .qd-badge.cracking { background: rgba(255,149,0,0.15); color: #ff9500; }
    .qd-badge.pending { background: rgba(136,136,136,0.15); color: #888; }

    .qd-page .pwd { font-family: 'Courier New', monospace; color: #50fa7b; font-weight: bold; }
    .qd-page .empty-state {
        text-align: center;
        padding: 60px 20px;
        color: var(--text-muted);
    }
    .qd-page .empty-state .icon { font-size: 3rem; margin-bottom: 12px; }

    .qd-toolbar {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 20px;
        flex-wrap: wrap;
    }
    .btn-crack {
        padding: 8px 18px;
        border: 1px solid var(--accent);
        border-radius: 6px;
        background: transparent;
        color: var(--accent);
        font-family: var(--font-pixel);
        font-size: 0.9rem;
        cursor: pointer;
        transition: var(--transition);
    }
    .btn-crack:hover { background: var(--accent); color: var(--bg-color); }
    .btn-crack:disabled { opacity: 0.4; cursor: not-allowed; }
    .btn-crack:disabled:hover { background: transparent; color: var(--accent); }
    .btn-crack.small {
        padding: 2px 10px;
        font-size: 0.75rem;
        border-radius: 4px;
    }
    .btn-crack.retry { border-color: #ff5555; color: #ff5555; }
    .btn-crack.retry:hover { background: #ff5555; color: var(--bg-color); }
    .toolbar-msg {
        font-size: 0.82rem;
        color: var(--text-muted);
    }

    @media screen and (max-width: 600px) {
        .qd-stats { gap: 8px; }
        .qd-stat { min-width: 70px; padding: 8px 12px; }
        .qd-stat .num { font-size: 1.3rem; }
        .qd-page th, .qd-page td { padding: 10px 10px; font-size: 0.82rem; }
        .qd-page .bssid-col { display: none; }
    }
</style>
{% endblock %}

{% block content %}
<meta name="csrf-token" content="{{ csrf_token() }}">
<div class="qd-page">
<div class="qd-header">
    <h2>QuickDic - Handshake Cracker</h2>
</div>

<div class="qd-stats" id="stats">
    <div class="qd-stat total"><div class="num" id="s-total">-</div><div class="label">Total</div></div>
    <div class="qd-stat cracked"><div class="num" id="s-cracked">-</div><div class="label">Cracked</div></div>
    <div class="qd-stat failed"><div class="num" id="s-failed">-</div><div class="label">Failed</div></div>
    <div class="qd-stat cracking"><div class="num" id="s-active">-</div><div class="label">Active</div></div>
</div>

<div class="qd-toolbar">
    <button class="btn-crack" id="btn-crack-all" onclick="crackAll()" disabled>Crack All Pending</button>
    <span class="toolbar-msg" id="toolbar-msg"></span>
</div>

<div class="table-container" id="table-wrap">
    <table>
        <thead>
            <tr>
                <th>Network</th>
                <th class="bssid-col">BSSID</th>
                <th>Status</th>
                <th>Password / Action</th>
            </tr>
        </thead>
        <tbody id="results"></tbody>
    </table>
</div>

<div class="empty-state" id="empty" style="display:none;">
    <div class="icon">( ._.)</div>
    <div>No handshakes captured yet. Go hunt some!</div>
</div>
</div>
{% endblock %}

{% block script %}
var csrf = document.querySelector('meta[name="csrf-token"]');
csrf = csrf ? csrf.getAttribute('content') : '';

function escHtml(s) {
    var d = document.createElement('div');
    d.appendChild(document.createTextNode(s));
    return d.innerHTML;
}

function crackFile(filename) {
    fetch('/plugins/better_quickdic/api/crack', {
        method: 'POST',
        headers: {'Content-Type': 'application/json', 'X-CSRFToken': csrf},
        body: JSON.stringify({file: filename})
    })
    .then(function(r) { return r.json(); })
    .then(function(data) {
        document.getElementById('toolbar-msg').textContent = data.message || '';
        refresh();
    })
    .catch(function(e) { console.error('crack error:', e); });
}

function crackAll() {
    var btn = document.getElementById('btn-crack-all');
    btn.disabled = true;
    btn.textContent = 'Starting...';
    fetch('/plugins/better_quickdic/api/crack', {
        method: 'POST',
        headers: {'Content-Type': 'application/json', 'X-CSRFToken': csrf},
        body: JSON.stringify({file: 'all'})
    })
    .then(function(r) { return r.json(); })
    .then(function(data) {
        document.getElementById('toolbar-msg').textContent = data.message || '';
        btn.textContent = 'Crack All Pending';
        refresh();
    })
    .catch(function(e) {
        console.error('crack all error:', e);
        btn.textContent = 'Crack All Pending';
    });
}

var _pendingCount = 0;
var _failedCount = 0;

function refresh() {
    fetch('/plugins/better_quickdic/api/status')
        .then(function(r) { return r.json(); })
        .then(function(data) {
            var hs = data.handshakes;
            var tbody = document.getElementById('results');
            var empty = document.getElementById('empty');
            var tableWrap = document.getElementById('table-wrap');
            var btn = document.getElementById('btn-crack-all');

            document.getElementById('s-total').textContent = data.total;
            document.getElementById('s-cracked').textContent = data.cracked;
            document.getElementById('s-failed').textContent = data.failed;
            document.getElementById('s-active').textContent = data.cracking;

            _pendingCount = data.pending || 0;
            _failedCount = data.failed || 0;
            btn.disabled = (_pendingCount + _failedCount) === 0;

            if (hs.length === 0) {
                tbody.innerHTML = '';
                tableWrap.style.display = 'none';
                empty.style.display = '';
                return;
            }
            tableWrap.style.display = '';
            empty.style.display = 'none';

            var html = '';
            for (var i = 0; i < hs.length; i++) {
                var h = hs[i];
                var badge = '<span class="qd-badge ' + h.status + '">' + h.status + '</span>';
                var action = '';
                if (h.status === 'pending') {
                    action = '<button class="btn-crack small" onclick="crackFile(\\'' + escHtml(h.file) + '\\')">Crack</button>';
                } else if (h.status === 'failed') {
                    action = '<button class="btn-crack small retry" onclick="crackFile(\\'' + escHtml(h.file) + '\\')">Retry</button>';
                } else if (h.password) {
                    action = '<span class="pwd">' + escHtml(h.password) + '</span>';
                } else {
                    action = '-';
                }
                html += '<tr>'
                    + '<td>' + escHtml(h.name) + '</td>'
                    + '<td class="bssid-col">' + escHtml(h.bssid) + '</td>'
                    + '<td>' + badge + '</td>'
                    + '<td>' + action + '</td>'
                    + '</tr>';
            }
            tbody.innerHTML = html;
        })
        .catch(function(e) { console.error('quickdic refresh:', e); });
}

refresh();
setInterval(refresh, 10000);
{% endblock %}
"""


class QuickDic(plugins.Plugin):
    __author__ = 'silentree12th'
    __version__ = '3.0.0'
    __license__ = 'GPL3'
    __description__ = 'Run a quick dictionary scan against captured handshakes with web UI dashboard.'
    __dependencies__ = {
        'apt': ['aircrack-ng'],
    }
    __defaults__ = {
        'enabled': True,
        'wordlist_folder': '/home/pi/wordlists/',
        'face': '(·ω·)',
    }

    def __init__(self):
        self._cracking = set()
        self._cracked = set()
        self._whitelist = set()

    def on_loaded(self):
        logging.info('[quickdic] plugin loaded')

        if 'face' not in self.options:
            self.options['face'] = '(·ω·)'
        if 'wordlist_folder' not in self.options:
            self.options['wordlist_folder'] = '/home/pi/wordlists/'

        # load whitelist from pwnagotchi config
        try:
            import toml
            with open('/etc/pwnagotchi/config.toml', 'r') as f:
                cfg = toml.load(f)
            for entry in cfg.get('main', {}).get('whitelist', []):
                self._whitelist.add(entry.strip())
            if self._whitelist:
                logging.info('[quickdic] whitelist: %d entries', len(self._whitelist))
        except Exception as e:
            logging.warning('[quickdic] could not load whitelist: %s', e)

        try:
            subprocess.run(['/usr/bin/aircrack-ng', '--help'],
                           capture_output=True, timeout=5)
            logging.info('[quickdic] aircrack-ng found')
        except (FileNotFoundError, subprocess.TimeoutExpired):
            logging.warning('[quickdic] aircrack-ng is not installed!')

        # load already-cracked and failed files so we don't re-attempt
        for cracked_file in glob.glob('/home/pi/handshakes/*.cracked'):
            self._cracked.add(cracked_file.replace('.cracked', ''))
        for failed_file in glob.glob('/home/pi/handshakes/*.failed'):
            self._cracked.add(failed_file.replace('.failed', ''))

    def _get_wordlists(self):
        folder = self.options['wordlist_folder']
        wordlists = sorted(glob.glob(os.path.join(folder, '*.txt')))
        return ','.join(wordlists) if wordlists else None

    def _is_whitelisted(self, name, bssid):
        """Check if network is in pwnagotchi's whitelist."""
        if not self._whitelist:
            return False
        return name in self._whitelist or bssid.upper() in self._whitelist

    def _get_handshake_status(self):
        results = []
        for pcap in sorted(glob.glob('/home/pi/handshakes/*.pcap')):
            basename = os.path.basename(pcap)
            # bettercap format: "NetworkName_aabbccddeeff.pcap"
            if '_' in basename:
                name_part = basename.rsplit('_', 1)[0]
                bssid_raw = basename.rsplit('_', 1)[1].replace('.pcap', '')
            else:
                name_part = basename.replace('.pcap', '')
                bssid_raw = ''

            if len(bssid_raw) == 12:
                bssid = ':'.join(bssid_raw[i:i+2] for i in range(0, 12, 2)).upper()
            else:
                bssid = bssid_raw

            if self._is_whitelisted(name_part, bssid):
                continue

            cracked_file = pcap + '.cracked'
            failed_file = pcap + '.failed'

            if os.path.exists(cracked_file):
                try:
                    with open(cracked_file, 'r') as f:
                        password = f.read().strip()
                except OSError:
                    password = '?'
                status = 'cracked'
            elif pcap in self._cracking:
                password = ''
                status = 'cracking'
            elif os.path.exists(failed_file):
                password = ''
                status = 'failed'
            else:
                password = ''
                status = 'pending'

            results.append({
                'name': name_part,
                'bssid': bssid,
                'status': status,
                'password': password,
                'file': basename,
            })
        return results

    def on_webhook(self, path, request):
        if not path or path == '/':
            return render_template_string(TEMPLATE)

        if path == 'api/status':
            handshakes = self._get_handshake_status()
            counts = {'total': len(handshakes), 'cracked': 0, 'failed': 0, 'cracking': 0, 'pending': 0}
            for h in handshakes:
                if h['status'] in counts:
                    counts[h['status']] += 1
            data = {**counts, 'handshakes': handshakes}
            return Response(json.dumps(data), mimetype='application/json')

        if path == 'api/crack' and request.method == 'POST':
            return self._handle_crack_request(request)

        from flask import abort
        abort(404)

    def _handle_crack_request(self, request):
        try:
            data = request.get_json(force=True)
        except Exception:
            return Response(json.dumps({'error': 'bad request'}), status=400, mimetype='application/json')

        target = data.get('file', '')
        handshake_dir = '/home/pi/handshakes'
        queued = 0

        if target == 'all':
            # crack all pending and failed
            for pcap in sorted(glob.glob(os.path.join(handshake_dir, '*.pcap'))):
                # skip whitelisted networks
                bname = os.path.basename(pcap).replace('.pcap', '')
                if '_' in bname:
                    net_name = bname.rsplit('_', 1)[0]
                    bssid_hex = bname.rsplit('_', 1)[1]
                    bssid_fmt = ':'.join(bssid_hex[i:i+2] for i in range(0, 12, 2)).upper() if len(bssid_hex) == 12 else ''
                else:
                    net_name, bssid_fmt = bname, ''
                if self._is_whitelisted(net_name, bssid_fmt):
                    continue
                if pcap in self._cracking:
                    continue
                cracked_file = pcap + '.cracked'
                if os.path.exists(cracked_file):
                    continue
                # remove .failed marker so it can be retried
                failed_file = pcap + '.failed'
                if os.path.exists(failed_file):
                    try:
                        os.remove(failed_file)
                    except OSError:
                        pass
                self._cracked.discard(pcap)
                self._cracking.add(pcap)
                self._cracked.add(pcap)
                t = threading.Thread(target=self._crack_standalone, args=(pcap,), daemon=True)
                t.start()
                queued += 1
            msg = 'Queued %d handshakes for cracking' % queued
        else:
            # crack a specific file
            pcap = os.path.join(handshake_dir, os.path.basename(target))
            if not os.path.exists(pcap):
                return Response(json.dumps({'error': 'file not found'}), status=404, mimetype='application/json')
            if pcap in self._cracking:
                return Response(json.dumps({'message': 'Already cracking'}), mimetype='application/json')
            # remove .failed marker for retry
            failed_file = pcap + '.failed'
            if os.path.exists(failed_file):
                try:
                    os.remove(failed_file)
                except OSError:
                    pass
            self._cracked.discard(pcap)
            self._cracking.add(pcap)
            self._cracked.add(pcap)
            t = threading.Thread(target=self._crack_standalone, args=(pcap,), daemon=True)
            t.start()
            msg = 'Cracking %s' % os.path.basename(target)
            queued = 1

        return Response(json.dumps({'message': msg, 'queued': queued}), mimetype='application/json')

    @staticmethod
    def _bssid_from_filename(filename):
        """Extract BSSID from pcap filename like NetworkName_aabbccddeeff.pcap"""
        basename = os.path.basename(filename).replace('.pcap', '')
        if '_' in basename:
            hex_part = basename.rsplit('_', 1)[1]
            if len(hex_part) == 12:
                return ':'.join(hex_part[i:i+2] for i in range(0, 12, 2)).upper()
        return None

    def _crack_standalone(self, filename):
        """Crack a handshake without agent context (triggered from web UI)."""
        try:
            wordlists = self._get_wordlists()
            if not wordlists:
                logging.warning('[quickdic] no wordlists found in %s', self.options['wordlist_folder'])
                return

            cracked_file = filename + '.cracked'

            cmd = ['nice', '-n', '15', '/usr/bin/aircrack-ng',
                   '-w', wordlists,
                   '-l', cracked_file,
                   '-q']
            bssid = self._bssid_from_filename(filename)
            if bssid:
                cmd.extend(['-b', bssid])
            cmd.append(filename)

            result = subprocess.run(cmd, capture_output=True, timeout=600)

            output = result.stdout.decode('utf-8', errors='replace').strip()

            if 'KEY FOUND' in output:
                key_match = re.search(r'\[(.*)\]', output)
                if key_match:
                    logging.warning('[quickdic] cracked %s: %s', filename, key_match.group(1))
            else:
                logging.info('[quickdic] key not found for %s', filename)
                try:
                    with open(filename + '.failed', 'w') as f:
                        f.write('')
                except OSError:
                    pass

        except subprocess.TimeoutExpired:
            logging.warning('[quickdic] aircrack-ng timed out for %s', filename)
            try:
                with open(filename + '.failed', 'w') as f:
                    f.write('')
            except OSError:
                pass
        except Exception as e:
            logging.error('[quickdic] error cracking %s: %s', filename, e)
        finally:
            self._cracking.discard(filename)

    def _crack_handshake(self, agent, filename, access_point, client_station):
        try:
            wordlists = self._get_wordlists()
            if not wordlists:
                logging.warning('[quickdic] no wordlists found in %s', self.options['wordlist_folder'])
                return

            cracked_file = filename + '.cracked'

            cmd = ['nice', '-n', '15', '/usr/bin/aircrack-ng',
                   '-w', wordlists,
                   '-l', cracked_file,
                   '-q']
            bssid = self._bssid_from_filename(filename)
            if bssid:
                cmd.extend(['-b', bssid])
            cmd.append(filename)

            result = subprocess.run(cmd, capture_output=True, timeout=600)

            output = result.stdout.decode('utf-8', errors='replace').strip()

            if 'KEY FOUND' in output:
                key_match = re.search(r'\[(.*)\]', output)
                if key_match:
                    pwd = key_match.group(1)
                    logging.warning('[quickdic] cracked %s: %s', filename, pwd)

                    display = agent.view()
                    display.set('face', self.options['face'])
                    display.set('status', 'Cracked: ' + pwd)
                    display.update(force=True)
            else:
                logging.info('[quickdic] key not found for %s', filename)
                try:
                    with open(filename + '.failed', 'w') as f:
                        f.write('')
                except OSError:
                    pass

        except subprocess.TimeoutExpired:
            logging.warning('[quickdic] aircrack-ng timed out for %s', filename)
            try:
                with open(filename + '.failed', 'w') as f:
                    f.write('')
            except OSError:
                pass
        except Exception as e:
            logging.error('[quickdic] error cracking %s: %s', filename, e)
        finally:
            self._cracking.discard(filename)

    def on_handshake(self, agent, filename, access_point, client_station):
        # delete handshakes from whitelisted networks (core bug: whitelist
        # only filters attacks, bettercap still captures passively)
        bssid = self._bssid_from_filename(filename) or ''
        basename = os.path.basename(filename).replace('.pcap', '')
        net_name = basename.rsplit('_', 1)[0] if '_' in basename else basename
        if self._is_whitelisted(net_name, bssid):
            logging.info('[quickdic] removing handshake from whitelisted network: %s', basename)
            try:
                os.remove(filename)
            except OSError:
                pass
            return

        if filename in self._cracked or filename in self._cracking:
            return

        self._cracked.add(filename)
        self._cracking.add(filename)

        t = threading.Thread(
            target=self._crack_handshake,
            args=(agent, filename, access_point, client_station),
            daemon=True
        )
        t.start()
        logging.info('[quickdic] cracking %s in background', filename)
