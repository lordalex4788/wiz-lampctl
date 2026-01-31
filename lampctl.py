import socket
import json
import argparse
import sys
import os
import time

# --- KONFIGURATION ---
# Mögliche Config-Pfade
CONFIG_PATHS = {
    "1": os.path.expanduser("~/.config/lampctl/lamps.json"),
    "2": os.path.expanduser("~/.lampctl.json"),
    "3": os.path.join(os.path.dirname(os.path.abspath(__file__)), "lampctl_config.json"),
    "4": "/etc/lampctl/lamps.json"
}

# Standard-Port für WiZ-Lampen (UDP Kommunikation)
PORT = 38899

# Definition der Licht-Modi (Farben und Weißtöne)
MODI = {
    "red": {"r": 255, "g": 0, "b": 0},          # Reines Rot
    "green": {"r": 0, "g": 255, "b": 0},        # Reines Grün
    "blue": {"r": 0, "g": 0, "b": 255},         # Reines Blau
    "yellow": {"r": 255, "g": 255, "b": 0},     # Gelb
    "white": {"r": 255, "g": 255, "b": 255}     # Weiß
}

def get_config_path():
    """Findet den Pfad zur Config-Datei"""
    for path in CONFIG_PATHS.values():
        if os.path.exists(path):
            return path
    return None

def load_lamps():
    """Lädt die Lampen-Liste aus der Config-Datei"""
    config_path = get_config_path()
    if not config_path:
        return None
    
    try:
        with open(config_path, 'r') as f:
            data = json.load(f)
            return data.get('lamps', [])
    except:
        return None

def save_lamps(lamps, config_path):
    """Speichert die Lampen-Liste in die Config-Datei"""
    # Erstelle Verzeichnis falls nötig
    dir_path = os.path.dirname(config_path)
    if dir_path and not os.path.exists(dir_path):
        os.makedirs(dir_path, exist_ok=True)
    
    with open(config_path, 'w') as f:
        json.dump({'lamps': lamps}, f, indent=2)
    
    print(f"\nKonfiguration gespeichert in: {config_path}")

def search_lamps():
    """Sucht nach WiZ-Lampen im Netzwerk via UDP-Broadcast"""
    print("Suche nach WiZ-Lampen im Netzwerk...")
    
    # Discovery-Nachricht für WiZ-Lampen
    discovery_msg = {"method": "getPilot", "params": {}}
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.settimeout(0.3)  # Kurzer Timeout für recv
    
    found_lamps = []
    
    try:
        # 10 Runden für maximale Chance alle Lampen zu finden
        for round_num in range(10):
            # Broadcast senden
            sock.sendto(json.dumps(discovery_msg).encode('utf-8'), ('<broadcast>', PORT))
            
            # 2 Sekunden lang auf Antworten warten
            end_time = time.time() + 2
            while time.time() < end_time:
                try:
                    data, addr = sock.recvfrom(1024)
                    ip = addr[0]
                    if ip not in found_lamps:
                        found_lamps.append(ip)
                        print(f"  ✓ Lampe gefunden: {ip}")
                except socket.timeout:
                    continue
            
            # Kurze Pause zwischen den Runden
            if round_num < 9:
                time.sleep(0.2)
    finally:
        sock.close()
    
    if not found_lamps:
        print("\nKeine WiZ-Lampen gefunden.")
        print("Stelle sicher, dass:")
        print("  - Die Lampen eingeschaltet sind")
        print("  - Du im gleichen Netzwerk bist")
        print("  - Keine Firewall die Kommunikation blockiert")
        return None
    
    # Sortiere die Lampen nach IP-Adresse
    found_lamps.sort(key=lambda ip: [int(x) for x in ip.split('.')])
    
    print(f"\n{len(found_lamps)} Lampe(n) gefunden!")
    
    # Prüfe ob bereits eine Config existiert
    existing_config = get_config_path()
    
    if existing_config:
        # Config existiert bereits - einfach aktualisieren
        config_path = existing_config
        print(f"\nAktualisiere existierende Konfiguration: {config_path}")
        save_lamps(found_lamps, config_path)
    else:
        # Keine Config vorhanden - Benutzer fragen wo sie gespeichert werden soll
        print("\nWo soll die Konfiguration gespeichert werden?")
        print("1) ~/.config/lampctl/lamps.json (Linux Standard)")
        print("2) ~/.lampctl.json (Im Home-Verzeichnis)")
        print("3) ./lampctl_config.json (Im Script-Verzeichnis)")
        print("4) /etc/lampctl/lamps.json (Systemweit)")
        
        while True:
            choice = input("\nWähle eine Option (1-4): ").strip()
            if choice in CONFIG_PATHS:
                config_path = CONFIG_PATHS[choice]
                save_lamps(found_lamps, config_path)
                break
            else:
                print("Ungültige Auswahl. Bitte 1-4 wählen.")
    
    print(f"\nGespeicherte Lampen:")
    for i, ip in enumerate(found_lamps, 1):
        print(f"  {i}. {ip}")
    
    return found_lamps

def send_wiz(payload, selected_indices=None, lampen_liste=None):
    """
    Sendet den JSON-Befehl (payload) per UDP an die Lampen.
    selected_indices: Liste der Lampen-Nummern (z.B. [1, 3]). Wenn None, dann alle.
    lampen_liste: Liste der Lampen-IPs
    """
    if lampen_liste is None:
        print("Fehler: Keine Lampen konfiguriert.")
        return
    
    # UDP-Socket erstellen
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Falls keine Lampen gewählt wurden (-lamp fehlt), nimm alle aus der Liste
        if selected_indices is None:
            targets = lampen_liste
        else:
            # Erstelle Liste der Ziel-IPs basierend auf den eingegebenen Nummern
            targets = []
            for i in selected_indices:
                # Prüfen, ob die Nummer gültig ist (1 bis Länge der Liste)
                if 1 <= i <= len(lampen_liste):
                    targets.append(lampen_liste[i-1]) # -1 da Listen bei 0 starten
                else:
                    print(f"Warnung: Lampe {i} existiert nicht.")
        
        # Den Befehl an jede ermittelte IP-Adresse senden
        for ip in targets:
            sock.sendto(json.dumps(payload).encode('utf-8'), (ip, PORT))
    finally:
        # Socket schließen, um Ressourcen freizugeben
        sock.close()

def main():
    # Parser für die Kommandozeilen-Argumente erstellen
    parser = argparse.ArgumentParser(
        description="WiZ Lampensteuerung - Steuerung per IP über UDP.",
        formatter_class=argparse.RawTextHelpFormatter
    )

    # Definition der verfügbaren Parameter
    parser.add_argument("-s", "--search", action="store_true", help="Suche nach WiZ-Lampen im Netzwerk und speichere Konfiguration")
    parser.add_argument("-l", "--lamp", type=int, nargs='+', dest='lamp', help="Lampennummer(n) (z.B. 1 2 3). Leer lassen für alle.")
    parser.add_argument("-on", action="store_true", help="Lampe(n) einschalten")
    parser.add_argument("-off", action="store_true", help="Lampe(n) ausschalten")
    parser.add_argument("-d", "--dim", type=int, help="Helligkeit direkt setzen (10-100)")
    parser.add_argument("-c", "--color", type=str, help="""Farbe wählen:
- red, green, blue, yellow, white, black
- HEX (z.B. FF00FF)""")

    # Wenn das Script ohne Argumente gestartet wird, zeige die Hilfe
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    # Argumente einlesen
    args = parser.parse_args()
    
    # Wenn -s/--search, dann Lampen suchen
    if args.search:
        search_lamps()
        return
    
    # Lampen aus Config laden
    lampen_liste = load_lamps()
    
    # Prüfen ob Lampen konfiguriert sind
    if not lampen_liste:
        print("Fehler: Keine Lampen konfiguriert!")
        print("Du musst erst Lampen im Netzwerk finden.")
        print("Benutze: python lampctl.py -s")
        sys.exit(1)

    # Logik: An/Aus Befehle senden
    if args.on:
        send_wiz({"method": "setState", "params": {"state": True}}, args.lamp, lampen_liste)
    
    if args.off:
        send_wiz({"method": "setState", "params": {"state": False}}, args.lamp, lampen_liste)

    # Logik: Dimmer-Wert senden
    if args.dim:
        send_wiz({"method": "setState", "params": {"dimming": args.dim}}, args.lamp, lampen_liste)

    # Logik: Modus oder Farbe senden
    if args.color:
        choice = args.color.lower()
        # Spezialfall: black schaltet die Lampe aus
        if choice == "black":
            send_wiz({"method": "setState", "params": {"state": False}}, args.lamp, lampen_liste)
        # Prüfen, ob das Wort in der MODI-Liste oben steht
        elif choice in MODI:
            send_wiz({"method": "setState", "params": MODI[choice]}, args.lamp, lampen_liste)
        else:
            # Wenn nicht in Liste, versuchen wir es als HEX-Farbe zu interpretieren
            try:
                c = choice.lstrip('#')
                # HEX in RGB umrechnen
                rgb = {"r": int(c[0:2], 16), "g": int(c[2:4], 16), "b": int(c[4:6], 16)}
                send_wiz({"method": "setState", "params": rgb}, args.lamp, lampen_liste)
            except:
                print(f"Fehler: '{args.color}' ist kein gültiger Modus oder HEX-Code.")

# Script-Einstiegspunkt
if __name__ == "__main__":
    main()
