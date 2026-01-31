# 💡 WiZ Lampctl

[🇩🇪 Deutsch](#deutsch) | [🇬🇧 English](#english)

---

<div align="center">
	<h2>Deutsch</h2>
</div>

### Beschreibung

**lampctl** ist ein Kommandozeilen-Tool zur Steuerung von WiZ Smart-Lampen über UDP. Steuere deine Beleuchtung direkt aus dem Terminal - schnell, einfach und ohne Cloud-Verbindung.

### ✨ Features

- 🔌 Direkte Steuerung über lokales Netzwerk (UDP)
- 💡 Ein/Ausschalten einzelner oder mehrerer Lampen
- 🎨 Farbsteuerung via HEX-Codes oder vordefinierten Farben
- 📊 Helligkeitsregelung (10-100%)
- 🚀 Keine Cloud-Verbindung erforderlich

### 📦 Installation

```bash
git clone https://github.com/lordalex4788/wiz-lampctl
cd wiz-lampctl
```

Keine zusätzlichen Dependencies erforderlich - nutzt nur Python Standard-Bibliotheken.

### 🚀 Verwendung

```bash
# Hilfe anzeigen
python lampctl.py -h, --help

# Suche nach WiZ-Lampen im Netzwerk und speichere Konfiguration
python -s, --search          

# Alle Lampen einschalten
python lampctl.py -on

# Lampe 1 und 3 ausschalten
python lampctl.py -off -l 1 3 ,--lamp 1 3

# Helligkeit auf 75% setzen
python lampctl.py -d 75,-dim 75

# Farbe auf Rot setzen
python lampctl.py -c red, -color red

# Custom HEX-Farbe
python lampctl.py -c FF00FF, --color FF00FF | ff ooder FF ist egal

# Mehrere Parameter kombinieren
python lampctl.py -on -l 1 2 -d 80 -c red, -on --lamp 1 2 --dim80 --color red
```

### 🎨 Verfügbare Farboptionen

**Vordefinierte Farben:**
- `red`, `green`, `blue`, `yellow`, `white`, `black`

**Custom Farben:**
- Beliebige HEX-Farben (z.B. `FF00FF`)

### ⚙️ Konfiguration

Suche nach WiZ-Lampen im Netzwerk und speichere Konfiguration

`python -s` 

Die Lampen werden über UDP am Port 38899 angesprochen.

Mögliche Pfade zur Konfigurationsdatei wobei `~/` für das  Home verzeichnis des aktuellen benutzers Zielt.

- 1: `~/.lampctl.json`
- 2: `~/.config/lampctl/lamps.json`
- 3: `/etc/lampctl/lamps.json`

- 4: Pfad zeigt auf `lampctl_config.json`, die im selben Ordner liegt wie das Python-Skript.

### 📋 Systemanforderungen

- Python 3.6+
- Zugriff auf lokales Netzwerk (UDP)
- WiZ Smart Lampen im selben Netzwerk

### 🤝 Beitragen

Contributions sind willkommen! Öffne gerne Issues oder Pull Requests.

### 📄 Lizenz

GPL3 License - siehe LICENSE Datei für Details.

---

## Made with ❤️  for the command line

---

## English

### Description

**lampctl** is a command-line tool for controlling WiZ Smart Bulbs via UDP. Control your lighting directly from the terminal - fast, simple, and without cloud connection.

### ✨ Features

- 🔌 Direct control via local network (UDP)
- 💡 Turn individual or multiple lamps on/off
- 🎨 Color control via HEX codes or predefined colors
- 📊 Brightness control (10-100%)
- 🚀 No cloud connection required

### 📦 Installation

```bash
git clone https://github.com/lordalex4788/wiz-lampctl
cd wiz-lampctl
```

No additional dependencies required - uses only Python standard libraries.

### 🚀 Usage

```bash
# Show help
python lampctl.py -h, --help

# Search all Wiz-Lamps and Save Config
python -s, --search     

# Turn on all lamps
python lampctl.py -on

# Turn off lamps 1 and 3
python lampctl.py -off -l 1 3 ,--lamp 1 3

# Set brightness to 75%
python lampctl.py -d 75,-dim 75

# Set color to red
python lampctl.py -c red, -color red

# Custom HEX color
python lampctl.py -c FF00FF, --color FF00FF | ff or FF dont mater

# Combine multiple parameters
python lampctl.py -on -l 1 2 -d 80 -c red, -on --lamp 1 2 --dim80 --color red
```

### 🎨 Available Color Options

**Predefined colors:**
- `red`, `green`, `blue`, `yellow`, `white`, `black`

**Custom colors:**
- Any HEX colors (e.g. `FF00FF`)

### ⚙️ Configuration

Search all Wiz-Lamps and Save Config

`python -s`

The lamps are controlled via UDP on port 38899.

Possible paths to the configuration file, where ~/ targets the home directory of the current user.

- 1: `~/.lampctl.json`
- 2: `~/.config/lampctl/lamps.json`
- 3: `/etc/lampctl/lamps.json`

- 4: Path points to lampctl_config.json, which is located in the same folder as the Python script.


### 📋 Requirements

- Python 3.6+
- Access to local network (UDP)
- WiZ Smart Bulbs on the same network

### 🤝 Contributing

Contributions are welcome! Feel free to open issues or pull requests.

### 📄 License

GPL3 License - see LICENSE file for details.

---

## Made with ❤️  for the command line

---
