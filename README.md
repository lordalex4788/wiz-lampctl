# 💡 WiZ Lampctl

[🇩🇪 Deutsch](#deutsch) | [🇬🇧 English](#english)

---

## Deutsch

### Beschreibung

**lampctl** ist ein Kommandozeilen-Tool zur Steuerung von WiZ Smart-Lampen über UDP. Steuere deine Beleuchtung direkt aus dem Terminal - schnell, einfach und ohne Cloud-Verbindung.

### ✨ Features

- 🔌 Direkte Steuerung über lokales Netzwerk (UDP)
- 💡 Ein/Ausschalten einzelner oder mehrerer Lampen
- 🎨 Farbsteuerung via HEX-Codes oder Presets
- 📊 Helligkeitsregelung (10-100%)
- 🎯 Vordefinierte Modi (TV, Normal, Cleanup, Warm)
- 🚀 Keine Cloud-Verbindung erforderlich

### 📦 Installation

```bash
git clone https://github.com/DEIN-USERNAME/wiz-lampctl.git
cd wiz-lampctl
# Installation der Abhängigkeiten (falls vorhanden)
pip install -r requirements.txt
```

### 🚀 Verwendung

```bash
# Hilfe anzeigen
python lampctl.py -h

# Alle Lampen einschalten
python lampctl.py -on

# Lampe 1 und 3 ausschalten
python lampctl.py -lamp 1 3 -off

# Helligkeit auf 75% setzen
python lampctl.py -dim 75

# Farbe auf Rot setzen
python lampctl.py -color red

# Custom HEX-Farbe
python lampctl.py -color FF00FF

# TV-Modus aktivieren
python lampctl.py -color tv

# Mehrere Parameter kombinieren
python lampctl.py -lamp 1 2 -on -dim 80 -color warm
```

### 🎨 Verfügbare Farben & Modi

**Presets:**
- `tv` - TV-Modus
- `norm` - Normal
- `cleanup` - Aufräumen/Arbeiten
- `warm` - Warmes Licht

**Farben:**
- `red`, `green`, `blue`, `yellow`
- Beliebige HEX-Farben (z.B. `FF00FF`)

### ⚙️ Konfiguration

Die IP-Adressen der Lampen müssen im Script konfiguriert werden. Öffne `lampctl.py` und passe die Lampen-IPs an:

```python
# Beispiel
LAMPS = {
    1: "192.168.1.100",
    2: "192.168.1.101",
    3: "192.168.1.102"
}
```

### 📋 Systemanforderungen

- Python 3.6+
- Zugriff auf lokales Netzwerk (UDP)
- WiZ Smart Lampen im selben Netzwerk

### 🤝 Beitragen

Contributions sind willkommen! Öffne gerne Issues oder Pull Requests.

### 📄 Lizenz

MIT License - siehe LICENSE Datei für Details.

---

## English

### Description

**lampctl** is a command-line tool for controlling WiZ Smart Bulbs via UDP. Control your lighting directly from the terminal - fast, simple, and without cloud connection.

### ✨ Features

- 🔌 Direct control via local network (UDP)
- 💡 Turn individual or multiple lamps on/off
- 🎨 Color control via HEX codes or presets
- 📊 Brightness control (10-100%)
- 🎯 Predefined modes (TV, Normal, Cleanup, Warm)
- 🚀 No cloud connection required

### 📦 Installation

```bash
git clone https://github.com/YOUR-USERNAME/wiz-lampctl.git
cd wiz-lampctl
# Install dependencies (if any)
pip install -r requirements.txt
```

### 🚀 Usage

```bash
# Show help
python lampctl.py -h

# Turn on all lamps
python lampctl.py -on

# Turn off lamps 1 and 3
python lampctl.py -lamp 1 3 -off

# Set brightness to 75%
python lampctl.py -dim 75

# Set color to red
python lampctl.py -color red

# Custom HEX color
python lampctl.py -color FF00FF

# Activate TV mode
python lampctl.py -color tv

# Combine multiple parameters
python lampctl.py -lamp 1 2 -on -dim 80 -color warm
```

### 🎨 Available Colors & Modes

**Presets:**
- `tv` - TV mode
- `norm` - Normal
- `cleanup` - Cleanup/Work mode
- `warm` - Warm light

**Colors:**
- `red`, `green`, `blue`, `yellow`
- Any HEX colors (e.g. `FF00FF`)

### ⚙️ Configuration

Lamp IP addresses must be configured in the script. Open `lampctl.py` and adjust the lamp IPs:

```python
# Example
LAMPS = {
    1: "192.168.1.100",
    2: "192.168.1.101",
    3: "192.168.1.102"
}
```

### 📋 Requirements

- Python 3.6+
- Access to local network (UDP)
- WiZ Smart Bulbs on the same network

### 🤝 Contributing

Contributions are welcome! Feel free to open issues or pull requests.

### 📄 License

MIT License - see LICENSE file for details.

---

**Made with ❤️ for the command line**
