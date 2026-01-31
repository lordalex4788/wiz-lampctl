import socket
import json
import argparse
import sys
import os
import time
import locale

# --- SPRACH-EINSTELLUNG ---
def get_system_lang():
    try:
        lang_info = locale.getlocale()
        lang_code = lang_info[0] if lang_info[0] else None
        if not lang_code:
            lang_code = os.environ.get('LANG') or os.environ.get('LC_ALL')
        if lang_code and lang_code.startswith('de'):
            return "de"
    except:
        pass
    return "en"

L = get_system_lang()

# Texte-Wörterbuch
TEXTS = {
    "de": {
        "config_saved": "Konfiguration gespeichert in: ",
        "search_start": "Suche nach WiZ-Lampen im Netzwerk...",
        "lamp_found": "  ✓ Lampe gefunden: ",
        "none_found": "\nKeine WiZ-Lampen gefunden.",
        "check_tips": "Stelle sicher, dass:\n  - Die Lampen eingeschaltet sind\n  - Du im gleichen Netzwerk bist\n  - Keine Firewall die Kommunikation blockiert",
        "found_count": " Lampe(n) gefunden!",
        "update_config": "\nAktualisiere existierende Konfiguration: ",
        "where_save": "\nWo soll die Konfiguration gespeichert werden?",
        "choice": "\nWähle eine Option (1-4): ",
        "invalid": "Ungültige Auswahl. Bitte 1-4 wählen.",
        "saved_lamps": "\nGespeicherte Lampen:",
        "err_no_config": "Fehler: Keine Lampen konfiguriert.",
        "warn_not_exist": "Warnung: Lampe {} existiert nicht.",
        "parser_desc": "WiZ Lampensteuerung - Steuerung per IP über UDP.",
        "h_help": "Zeige diese Hilfe an und beende das Programm",
        "h_search": "Suche nach WiZ-Lampen im Netzwerk und speichere Konfiguration",
        "h_lamp": "Lampennummer(n) (z.B. 1 2 3). Leer lassen für alle.",
        "h_on": "Lampe(n) einschalten",
        "h_off": "Lampe(n) ausschalten",
        "h_dim": "Helligkeit direkt setzen (10-100)",
        "h_color": "Farbe wählen:\n- red, green, blue, yellow, white, black\n- HEX (z.B. FF00FF)",
        "err_no_lamps": "Fehler: Keine Lampen konfiguriert!",
        "err_must_search": "Du musst erst Lampen im Netzwerk finden.",
        "err_usage": "Benutze: python lampctl.py -s",
        "err_color": "Fehler: '{}' ist kein gültiger Modus oder HEX-Code.",
        "opt_title": "Optionen"
    },
    "en": {
        "config_saved": "Configuration saved in: ",
        "search_start": "Searching for WiZ lamps in the network...",
        "lamp_found": "  ✓ Lamp found: ",
        "none_found": "\nNo WiZ lamps found.",
        "check_tips": "Make sure that:\n  - The lamps are switched on\n  - You are in the same network\n  - No firewall is blocking communication",
        "found_count": " lamp(s) found!",
        "update_config": "\nUpdating existing configuration: ",
        "where_save": "\nWhere should the configuration be saved?",
        "choice": "\nChoose an option (1-4): ",
        "invalid": "Invalid choice. Please choose 1-4.",
        "saved_lamps": "\nSaved lamps:",
        "err_no_config": "Error: No lamps configured.",
        "warn_not_exist": "Warning: Lamp {} does not exist.",
        "parser_desc": "WiZ lamp control - Control via IP over UDP.",
        "h_help": "show this help message and exit",
        "h_search": "Search for WiZ lamps in the network and save configuration",
        "h_lamp": "Lamp number(s) (e.g. 1 2 3). Leave blank for all.",
        "h_on": "Switch lamp(s) on",
        "h_off": "Switch lamp(s) off",
        "h_dim": "Set brightness directly (10-100)",
        "h_color": "Choose color:\n- red, green, blue, yellow, white, black\n- HEX (e.g. FF00FF)",
        "err_no_lamps": "Error: No lamps configured!",
        "err_must_search": "You must find lamps in the network first.",
        "err_usage": "Usage: python lampctl.py -s",
        "err_color": "Error: '{}' is not a valid mode or HEX code.",
        "opt_title": "options"
    }
}

# --- KONFIGURATION ---
CONFIG_PATHS = {
    "1": os.path.expanduser("~/.config/lampctl/lamps.json"),
    "2": os.path.expanduser("~/.lampctl.json"),
    "3": os.path.join(os.path.dirname(os.path.abspath(__file__)), "lampctl_config.json"),
    "4": "/etc/lampctl/lamps.json"
}
PORT = 38899
MODI = {
    "red": {"r": 255, "g": 0, "b": 0},
    "green": {"r": 0, "g": 255, "b": 0},
    "blue": {"r": 0, "g": 0, "b": 255},
    "yellow": {"r": 255, "g": 255, "b": 0},
    "white": {"r": 255, "g": 255, "b": 255}
}

def get_config_path():
    for path in CONFIG_PATHS.values():
        if os.path.exists(path):
            return path
    return None

def load_lamps():
    config_path = get_config_path()
    if not config_path: return None
    try:
        with open(config_path, 'r') as f:
            data = json.load(f)
            return data.get('lamps', [])
    except: return None

def save_lamps(lamps, config_path):
    dir_path = os.path.dirname(config_path)
    if dir_path and not os.path.exists(dir_path):
        os.makedirs(dir_path, exist_ok=True)
    with open(config_path, 'w') as f:
        json.dump({'lamps': lamps}, f, indent=2)
    print(f"{TEXTS[L]['config_saved']}{config_path}")

def search_lamps():
    print(TEXTS[L]["search_start"])
    discovery_msg = {"method": "getPilot", "params": {}}
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.settimeout(0.3)
    found_lamps = []
    try:
        for round_num in range(10):
            sock.sendto(json.dumps(discovery_msg).encode('utf-8'), ('<broadcast>', PORT))
            end_time = time.time() + 2
            while time.time() < end_time:
                try:
                    data, addr = sock.recvfrom(1024)
                    ip = addr[0]
                    if ip not in found_lamps:
                        found_lamps.append(ip)
                        print(f"{TEXTS[L]['lamp_found']}{ip}")
                except socket.timeout: continue
            if round_num < 9: time.sleep(0.2)
    finally: sock.close()
    if not found_lamps:
        print(TEXTS[L]["none_found"])
        print(TEXTS[L]["check_tips"])
        return None
    found_lamps.sort(key=lambda ip: [int(x) for x in ip.split('.')])
    print(f"\n{len(found_lamps)}{TEXTS[L]['found_count']}")
    existing_config = get_config_path()
    if existing_config:
        config_path = existing_config
        print(f"{TEXTS[L]['update_config']}{config_path}")
        save_lamps(found_lamps, config_path)
    else:
        print(TEXTS[L]["where_save"])
        print("1) ~/.config/lampctl/lamps.json\n2) ~/.lampctl.json\n3) ./lampctl_config.json\n4) /etc/lampctl/lamps.json")
        while True:
            choice = input(TEXTS[L]["choice"]).strip()
            if choice in CONFIG_PATHS:
                config_path = CONFIG_PATHS[choice]
                save_lamps(found_lamps, config_path)
                break
            else: print(TEXTS[L]["invalid"])
    print(TEXTS[L]["saved_lamps"])
    for i, ip in enumerate(found_lamps, 1): print(f"  {i}. {ip}")
    return found_lamps

def send_wiz(payload, selected_indices=None, lampen_liste=None):
    if lampen_liste is None:
        print(TEXTS[L]["err_no_config"])
        return
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        if selected_indices is None: targets = lampen_liste
        else:
            targets = []
            for i in selected_indices:
                if 1 <= i <= len(lampen_liste): targets.append(lampen_liste[i-1])
                else: print(TEXTS[L]["warn_not_exist"].format(i))
        for ip in targets:
            sock.sendto(json.dumps(payload).encode('utf-8'), (ip, PORT))
    finally: sock.close()

def main():
    # Parser Setup mit lokalisierter Hilfe
    parser = argparse.ArgumentParser(
        description=TEXTS[L]["parser_desc"],
        formatter_class=argparse.RawTextHelpFormatter,
        add_help=False
    )
    
    # Gruppen-Titel lokalisieren
    parser._optionals.title = TEXTS[L]["opt_title"]

    parser.add_argument("-h", "--help", action="help", help=TEXTS[L]["h_help"])
    parser.add_argument("-s", "--search", action="store_true", help=TEXTS[L]["h_search"])
    parser.add_argument("-l", "--lamp", type=int, nargs='+', dest='lamp', help=TEXTS[L]["h_lamp"])
    parser.add_argument("-on", action="store_true", help=TEXTS[L]["h_on"])
    parser.add_argument("-off", action="store_true", help=TEXTS[L]["h_off"])
    parser.add_argument("-d", "--dim", type=int, help=TEXTS[L]["h_dim"])
    parser.add_argument("-c", "--color", type=str, help=TEXTS[L]["h_color"])

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()
    if args.search:
        search_lamps()
        return
    
    lampen_liste = load_lamps()
    if not lampen_liste:
        print(TEXTS[L]["err_no_lamps"])
        print(TEXTS[L]["err_must_search"])
        print(TEXTS[L]["err_usage"])
        sys.exit(1)

    if args.on: send_wiz({"method": "setState", "params": {"state": True}}, args.lamp, lampen_liste)
    if args.off: send_wiz({"method": "setState", "params": {"state": False}}, args.lamp, lampen_liste)
    if args.dim: send_wiz({"method": "setState", "params": {"dimming": args.dim}}, args.lamp, lampen_liste)
    if args.color:
        choice = args.color.lower()
        if choice == "black": send_wiz({"method": "setState", "params": {"state": False}}, args.lamp, lampen_liste)
        elif choice in MODI: send_wiz({"method": "setState", "params": MODI[choice]}, args.lamp, lampen_liste)
        else:
            try:
                c = choice.lstrip('#')
                rgb = {"r": int(c[0:2], 16), "g": int(c[2:4], 16), "b": int(c[4:6], 16)}
                send_wiz({"method": "setState", "params": rgb}, args.lamp, lampen_liste)
            except: print(TEXTS[L]["err_color"].format(args.color))

if __name__ == "__main__":
    main()
