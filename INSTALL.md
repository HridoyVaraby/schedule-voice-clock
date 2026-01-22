# 📥 Installation Guide

## Option 1: Install from .deb Package (Recommended)

The easiest way to install VoiceClock on Ubuntu/Debian:

```bash
# Download the .deb package
wget https://github.com/HridoyVaraby/schedule-voice-clock/releases/download/v1.0.0/voiceclock_1.0.0_all.deb

# Install
sudo dpkg -i voiceclock_1.0.0_all.deb

# Fix any missing dependencies
sudo apt-get install -f
```

That's it! VoiceClock is now installed and will autostart on login.

---

## Option 2: Install from Tarball

### 1. Download the Latest Release

```bash
# Download and extract the latest release
wget https://github.com/HridoyVaraby/schedule-voice-clock/releases/download/v1.0.0/voiceclock-v1.0.0.tar.gz
tar -xzf voiceclock-v1.0.0.tar.gz
cd schedule-voice-clock
```

Or clone from GitHub:
```bash
git clone https://github.com/HridoyVaraby/schedule-voice-clock.git
cd schedule-voice-clock
```

### 2. Run the Installer

```bash
./install.sh
```

This will:
- ✅ Install system dependencies (GTK, GStreamer, AppIndicator)
- ✅ Copy app files to `~/.local/share/voiceclock/`
- ✅ Create `voiceclock` command
- ✅ Add to application menu
- ✅ Enable autostart on login

### 3. Start VoiceClock

```bash
voiceclock
```

Or find **VoiceClock** in your application menu.

---

## Manual Installation

If you prefer manual installation:

### Step 1: Install Dependencies

```bash
sudo apt update
sudo apt install python3-gi gir1.2-gtk-3.0 gir1.2-gstreamer-1.0 \
    gir1.2-ayatanaappindicator3-0.1 gstreamer1.0-plugins-good \
    gstreamer1.0-plugins-base libnotify-bin
```

### Step 2: Clone Repository

```bash
git clone https://github.com/HridoyVaraby/schedule-voice-clock.git
cd schedule-voice-clock
```

### Step 3: Run Directly

```bash
python3 src/main.py
```

---

## Configuration

After launching, click the **tray icon** to access:

| Option | Description |
|--------|-------------|
| ⚙️ **Settings** | Choose language (English/Bangla) and interval (15/30/60 min) |
| 🔇 **Mute** | Toggle announcements on/off |
| ❌ **Quit** | Close the application |

Settings are saved to `~/.local/share/voiceclock/data/settings.json`

---

## Autostart

VoiceClock starts automatically on login by default.

### Disable Autostart

```bash
rm ~/.config/autostart/voiceclock.desktop
```

### Re-enable Autostart

```bash
cp ~/.local/share/applications/voiceclock.desktop ~/.config/autostart/
```

---

## Uninstall

```bash
./uninstall.sh
```

Or manually:
```bash
rm -rf ~/.local/share/voiceclock
rm ~/.local/bin/voiceclock
rm ~/.config/autostart/voiceclock.desktop
rm ~/.local/share/applications/voiceclock.desktop
```

---

## Troubleshooting

### Tray icon not visible

On some GNOME setups, you may need the [AppIndicator extension](https://extensions.gnome.org/extension/615/appindicator-support/).

### No sound playing

Ensure GStreamer plugins are installed:
```bash
sudo apt install gstreamer1.0-plugins-good gstreamer1.0-plugins-base
```

### Settings not saving

Check write permissions:
```bash
ls -la ~/.local/share/voiceclock/data/
```

---

## Support

- 🐛 [Report Issues](https://github.com/HridoyVaraby/schedule-voice-clock/issues)
- 💬 [Discussions](https://github.com/HridoyVaraby/schedule-voice-clock/discussions)
- 🌐 [varabit.com](https://varabit.com)
