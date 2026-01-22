#!/bin/bash
# Script to build Debian package for VoiceClock
# Usage: ./scripts/build_deb.sh [version]

set -e

VERSION=${1:-"1.0.1"}
BUILD_DIR="build/deb"
PKG_NAME="voiceclock"
FULL_PKG_NAME="${PKG_NAME}_${VERSION}_all"
DEB_DIR="$BUILD_DIR/$FULL_PKG_NAME"

echo "📦 Building $FULL_PKG_NAME.deb..."

# Clean build dir
rm -rf "$BUILD_DIR"
mkdir -p "$DEB_DIR/DEBIAN"
mkdir -p "$DEB_DIR/usr/share/voiceclock"
mkdir -p "$DEB_DIR/usr/bin"
mkdir -p "$DEB_DIR/usr/share/applications"
mkdir -p "$DEB_DIR/etc/xdg/autostart"

# Create control file
cat > "$DEB_DIR/DEBIAN/control" << EOF
Package: voiceclock
Version: $VERSION
Section: utils
Priority: optional
Architecture: all
Depends: python3 (>= 3.10), python3-gi, gir1.2-gtk-3.0, gir1.2-gst-1.0, gir1.2-ayatanaappindicator3-0.1, gstreamer1.0-plugins-good, gstreamer1.0-plugins-base, libnotify-bin
Maintainer: Hridoy Varaby <contact@varabit.com>
Homepage: https://varabit.com
Description: Schedule Voice Clock - Time announcements in English and Bangla
 VoiceClock is a lightweight Ubuntu desktop application that announces
 the time at configurable intervals (15, 30, or 60 minutes) in English
 or Bangla. It runs in the system tray and uses minimal resources.
 .
 Features:
  - Time announcements in English and Bangla
  - Configurable intervals (15/30/60 minutes)
  - System tray integration
  - Autostart on login
  - Mute toggle
EOF

# Create postinst script
cat > "$DEB_DIR/DEBIAN/postinst" << EOF
#!/bin/bash
# Post-installation script

# Update desktop database
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database -q /usr/share/applications 2>/dev/null || true
fi

echo ""
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║   🕐 VoiceClock installed successfully!                   ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""
echo "To start: voiceclock"
echo "Or find 'VoiceClock' in your application menu."
echo ""
EOF
chmod 755 "$DEB_DIR/DEBIAN/postinst"

# Create wrapper script
cat > "$DEB_DIR/usr/bin/voiceclock" << EOF
#!/bin/bash
cd /usr/share/voiceclock
exec python3 src/main.py "\$@"
EOF
chmod 755 "$DEB_DIR/usr/bin/voiceclock"

# Copy application files
cp -r src "$DEB_DIR/usr/share/voiceclock/"
cp -r assets "$DEB_DIR/usr/share/voiceclock/"
mkdir -p "$DEB_DIR/usr/share/voiceclock/data"

# Create/Copy desktop entry (ensure correct Exec path for deb installed version)
cat > "$DEB_DIR/usr/share/applications/voiceclock.desktop" << EOF
[Desktop Entry]
Name=VoiceClock
Comment=Periodic time announcements in English or Bangla
Exec=voiceclock
Icon=preferences-system-time
Terminal=false
Type=Application
Categories=Utility;Accessibility;
Keywords=time;clock;voice;announcement;accessibility;bangla;
StartupNotify=false
EOF

# Copy autostart entry
cp "$DEB_DIR/usr/share/applications/voiceclock.desktop" "$DEB_DIR/etc/xdg/autostart/"

# Build the package
dpkg-deb --build "$DEB_DIR"

# Package is created as $BUILD_DIR/$FULL_PKG_NAME.deb automatically

echo "✅ Package built: $BUILD_DIR/$FULL_PKG_NAME.deb"
