#!/bin/bash
#
# VoiceClock Uninstaller
# Removes VoiceClock from your system
#

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}🗑️ Uninstalling VoiceClock...${NC}"

INSTALL_DIR="$HOME/.local/share/voiceclock"
BIN_DIR="$HOME/.local/bin"
AUTOSTART_DIR="$HOME/.config/autostart"

# Remove files
rm -rf "$INSTALL_DIR"
rm -f "$BIN_DIR/voiceclock"
rm -f "$AUTOSTART_DIR/voiceclock.desktop"
rm -f "$HOME/.local/share/applications/voiceclock.desktop"

echo -e "${GREEN}✅ VoiceClock has been uninstalled${NC}"
echo ""
echo "Note: System dependencies (python3-gi, etc.) were not removed."
echo "To remove them manually: sudo apt remove python3-gi gir1.2-gtk-3.0 ..."
