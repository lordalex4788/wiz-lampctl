# 💡 WiZ Lampctl

[🇩🇪 Deutsch](#deutsch) | [🇬🇧 English](#english)

---

## Deutsch

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
git clone https://github.com/DEIN-USERNAME/wiz-lampctl.git
cd wiz-lampctl
```

Keine zusätzlichen Dependencies erforderlich - nutzt nur Python Standard-Bibliotheken.

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

# Mehrere Parameter kombinieren
python lampctl.py -lamp 1 2 -on -dim 80 -color warm
```

### 🎨 Verfügbare Farboptionen

**Vordefinierte Farben:**
- `red`, `green`, `blue`, `yellow`, `white`, `black`

**Custom Farben:**
- Beliebige HEX-Farben (z.B. `FF00FF`)

### ⚙️ Konfiguration

Die IP-Adressen der Lampen müssen im Script konfiguriert werden. Öffne `lampctl.py` und passe die Lampen-IPs in der `LAMPEN_LISTE` an:

```python
# Die IP-Adressen deiner drei Lampen (Index 1, 2, 3)
LAMPEN_LISTE = ["192.168.178.240", "192.168.178.241", "192.168.178.242"]
```

Die Lampen werden über UDP am Port 38899 angesprochen.

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
- 🎨 Color control via HEX codes or predefined colors
- 📊 Brightness control (10-100%)
- 🚀 No cloud connection required

### 📦 Installation

```bash
git clone https://github.com/YOUR-USERNAME/wiz-lampctl.git
cd wiz-lampctl
```

No additional dependencies required - uses only Python standard libraries.

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

# Combine multiple parameters
python lampctl.py -lamp 1 2 -on -dim 80 -color warm
```

### 🎨 Available Color Options

**Predefined colors:**
- `red`, `green`, `blue`, `yellow`, `white`, `black`

**Custom colors:**
- Any HEX colors (e.g. `FF00FF`)

### ⚙️ Configuration

Lamp IP addresses must be configured in the script. Open `lampctl.py` and adjust the lamp IPs in the `LAMPEN_LISTE`:

```python
# IP addresses of your three lamps (Index 1, 2, 3)
LAMPEN_LISTE = ["192.168.178.240", "192.168.178.241", "192.168.178.242"]
```

The lamps are controlled via UDP on port 38899.

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
