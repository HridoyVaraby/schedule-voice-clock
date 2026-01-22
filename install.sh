#!/bin/bash
#
# VoiceClock Installer
# Installs VoiceClock - Schedule Voice Clock for Ubuntu
#
# Author: Hridoy Varaby (varabit.com)
# License: MIT
#

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║                                                           ║"
echo "║   🕐 VoiceClock Installer                                 ║"
echo "║   Schedule Voice Clock for Ubuntu                        ║"
echo "║                                                           ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Check if running on Ubuntu/Debian
if ! command -v apt &> /dev/null; then
    echo -e "${RED}❌ Error: This installer requires apt (Ubuntu/Debian)${NC}"
    exit 1
fi

# Installation directory
INSTALL_DIR="$HOME/.local/share/voiceclock"
BIN_DIR="$HOME/.local/bin"
AUTOSTART_DIR="$HOME/.config/autostart"

echo -e "${YELLOW}📦 Installing system dependencies...${NC}"
sudo apt update -qq
sudo apt install -y python3-gi gir1.2-gtk-3.0 gir1.2-gstreamer-1.0 \
    gir1.2-ayatanaappindicator3-0.1 gstreamer1.0-plugins-good \
    gstreamer1.0-plugins-base libnotify-bin

echo -e "${GREEN}✅ System dependencies installed${NC}"
echo ""

echo -e "${YELLOW}📁 Creating installation directory...${NC}"
mkdir -p "$INSTALL_DIR"
mkdir -p "$BIN_DIR"
mkdir -p "$AUTOSTART_DIR"

# Copy application files
echo -e "${YELLOW}📋 Copying application files...${NC}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

cp -r "$SCRIPT_DIR/src" "$INSTALL_DIR/"
cp -r "$SCRIPT_DIR/assets" "$INSTALL_DIR/"
mkdir -p "$INSTALL_DIR/data"

echo -e "${GREEN}✅ Application files copied${NC}"
echo ""

# Create launcher script
echo -e "${YELLOW}🚀 Creating launcher...${NC}"
cat > "$BIN_DIR/voiceclock" << 'EOF'
#!/bin/bash
cd "$HOME/.local/share/voiceclock"
python3 src/main.py "$@"
EOF
chmod +x "$BIN_DIR/voiceclock"

echo -e "${GREEN}✅ Launcher created at $BIN_DIR/voiceclock${NC}"
echo ""

# Create desktop entry
echo -e "${YELLOW}🖥️ Creating desktop entry...${NC}"
cat > "$AUTOSTART_DIR/voiceclock.desktop" << EOF
[Desktop Entry]
Name=VoiceClock
Comment=Periodic time announcements in English or Bangla
Exec=$BIN_DIR/voiceclock
Icon=preferences-system-time
Terminal=false
Type=Application
Categories=Utility;Accessibility;
Keywords=time;clock;voice;announcement;accessibility;
StartupNotify=false
X-GNOME-Autostart-enabled=true
EOF

# Also add to applications menu
mkdir -p "$HOME/.local/share/applications"
cp "$AUTOSTART_DIR/voiceclock.desktop" "$HOME/.local/share/applications/"

echo -e "${GREEN}✅ Desktop entry created${NC}"
echo ""

# Add ~/.local/bin to PATH if not already there
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    echo -e "${YELLOW}📝 Adding ~/.local/bin to PATH...${NC}"
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
    echo -e "${GREEN}✅ PATH updated (restart terminal or run: source ~/.bashrc)${NC}"
fi

echo ""
echo -e "${GREEN}╔═══════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║                                                           ║${NC}"
echo -e "${GREEN}║   🎉 Installation Complete!                               ║${NC}"
echo -e "${GREEN}║                                                           ║${NC}"
echo -e "${GREEN}╚═══════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "To start VoiceClock now, run:"
echo -e "  ${BLUE}voiceclock${NC}"
echo ""
echo -e "Or find it in your application menu: ${BLUE}VoiceClock${NC}"
echo ""
echo -e "VoiceClock will start automatically on login."
echo -e "To disable autostart, remove: $AUTOSTART_DIR/voiceclock.desktop"
echo ""
echo -e "${YELLOW}Enjoy! 🕐${NC}"
