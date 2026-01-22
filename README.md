# VoiceClock - Schedule Voice Clock

A lightweight Ubuntu desktop application that announces the time at configurable intervals in English or Bangla.

## Features

- 🕐 **Time Announcements**: Hear the time spoken aloud at 15, 30, or 60-minute intervals
- 🌍 **Bilingual**: Supports English and বাংলা (Bangla)
- 🔇 **Mute Toggle**: Quick mute/unmute from the system tray
- ⚡ **Lightweight**: Event-driven design uses virtually zero CPU when idle
- 🖥️ **System Tray**: Runs quietly in your Ubuntu top panel

## Requirements

### System Dependencies (Ubuntu)

```bash
sudo apt install python3-gi gir1.2-gtk-3.0 gir1.2-gst-1.0 \
    gir1.2-ayatanaappindicator3-0.1 gstreamer1.0-plugins-base \
    gstreamer1.0-plugins-good libnotify-bin
```

### Python Dependencies

```bash
pip install -r requirements.txt
```

## Usage

### Run the Application

```bash
python3 src/main.py
```

The app will start in the system tray. Click the tray icon to access:
- **Settings**: Configure language and interval
- **Mute**: Toggle announcements on/off
- **Quit**: Exit the application

### Generate Audio Filename Checklist

```bash
python3 scripts/file_namer.py
```

This outputs a checklist of all 48 audio files needed per language.

## Audio Files

Place your audio files in:
- `assets/audio/en/` - English audio files
- `assets/audio/bn/` - Bangla audio files

File naming format: `HH_MM.ogg` (e.g., `01_00.ogg`, `01_15.ogg`, `12_45.ogg`)

Supported formats: `.ogg` (preferred) or `.mp3`

## Autostart

To start VoiceClock automatically on login:

1. Update the `Exec` path in `voiceclock.desktop`:
   ```ini
   Exec=python3 /full/path/to/schedule-voice-clock/src/main.py
   ```

2. Copy to autostart:
   ```bash
   cp voiceclock.desktop ~/.config/autostart/
   ```

## Project Structure

```
schedule-voice-clock/
├── assets/audio/          # Audio files (en/, bn/)
├── data/                  # User settings (settings.json)
├── scripts/               # Utility scripts
├── src/
│   ├── main.py            # Entry point
│   ├── config.py          # Settings management
│   ├── player.py          # GStreamer audio playback
│   ├── scheduler.py       # Time checking logic
│   ├── tray.py            # System tray icon
│   └── settings_window.py # GTK settings dialog
└── voiceclock.desktop     # Desktop integration
```

## License

MIT License
