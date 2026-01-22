# 🕐 VoiceClock - Schedule Voice Clock

A lightweight Ubuntu desktop application that announces the time at configurable intervals in **English** and **বাংলা (Bangla)**.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-green.svg)](https://python.org)
[![GTK 3](https://img.shields.io/badge/GTK-3-orange.svg)](https://gtk.org)

---

## ✨ Features

- 🕐 **Time Announcements** — Hear the time spoken aloud at 15, 30, or 60-minute intervals
- 🌍 **Bilingual Support** — English and বাংলা (Bangla) with native pronunciation
- 🔇 **Quick Mute** — Toggle announcements from the system tray
- ⚡ **Lightweight** — Event-driven design uses virtually zero CPU when idle
- 🖥️ **System Tray** — Runs quietly in your Ubuntu top panel
- 🎙️ **High-Quality Voices** — Generated with ElevenLabs AI

---

## 📦 Installation

### System Dependencies (Ubuntu/Debian)

```bash
sudo apt install python3-gi gir1.2-gtk-3.0 gir1.2-gst-1.0 \
    gir1.2-ayatanaappindicator3-0.1 gstreamer1.0-plugins-good libnotify-bin
```

### Python Dependencies

```bash
pip install -r requirements.txt
```

---

## 🚀 Usage

### Run the Application

```bash
python3 src/main.py
```

The app starts in the system tray. Click the tray icon to access:
- **⚙️ Settings** — Configure language and interval
- **🔇 Mute** — Toggle announcements on/off
- **❌ Quit** — Exit the application

### Enable Autostart

To start VoiceClock automatically on login:

```bash
cp voiceclock.desktop ~/.config/autostart/
```

---

## 🎙️ Audio Files

The project includes 192 pre-generated MP3 files:
- **96 English files** — Natural speech ("It is two fifteen in the afternoon")
- **96 Bangla files** — Native pronunciation with time-of-day context (সকাল, দুপুর, বিকেল, সন্ধ্যা, রাত)

### Regenerate Audio (Optional)

If you want to generate your own audio files:

1. Get an API key from [ElevenLabs](https://elevenlabs.io)
2. Create `.env` file: `ELEVENLABS_API_KEY=your_key_here`
3. Run: `python3 scripts/generate_audio.py`

---

## 📁 Project Structure

```
schedule-voice-clock/
├── assets/audio/          # Audio files (en/, bn/)
├── data/                  # User settings (settings.json)
├── scripts/               # Utility scripts
│   ├── generate_audio.py  # ElevenLabs audio generator
│   └── file_namer.py      # Filename checklist generator
├── src/
│   ├── main.py            # Entry point
│   ├── config.py          # Settings management
│   ├── player.py          # GStreamer audio playback
│   ├── scheduler.py       # Time checking logic
│   ├── tray.py            # System tray icon
│   └── settings_window.py # GTK settings dialog
└── voiceclock.desktop     # Desktop integration
```

---

## 🤝 Contributing

This project is **open source** and contributions are welcome!

### Ways to Contribute

- 🐛 **Report Bugs** — Open an issue if something doesn't work
- 💡 **Suggest Features** — Have an idea? Let us know!
- 🌍 **Add Languages** — Help translate to other languages
- 🎙️ **Improve Voices** — Contribute better audio recordings
- 📖 **Documentation** — Help improve the docs
- 🔧 **Code** — Submit pull requests

### Development Setup

```bash
git clone https://github.com/varabit/schedule-voice-clock.git
cd schedule-voice-clock
pip install -r requirements.txt
python3 src/main.py
```

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

You are free to:
- ✅ Use commercially
- ✅ Modify
- ✅ Distribute
- ✅ Use privately

---

## 👨‍💻 Author

**Hridoy Varaby**

- 🌐 Website: [varabit.com](https://varabit.com)
- 💼 GitHub: [@varabit](https://github.com/varabit)

---

## 🙏 Acknowledgments

- [ElevenLabs](https://elevenlabs.io) — AI voice generation
- [PyGObject](https://pygobject.gnome.org) — Python GTK bindings
- [GStreamer](https://gstreamer.freedesktop.org) — Multimedia framework

---

<p align="center">
  Made with ❤️ in Bangladesh 🇧🇩
</p>
