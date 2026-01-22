"""
SystemTray - AppIndicator system tray integration for Ubuntu.

Provides a persistent tray icon with menu for quick access to settings,
mute toggle, and quit functionality.
"""

import logging

import gi
gi.require_version('Gtk', '3.0')

# Try AyatanaAppIndicator3 first (modern Ubuntu 22.04+), fall back to AppIndicator3
try:
    gi.require_version('AyatanaAppIndicator3', '0.1')
    from gi.repository import AyatanaAppIndicator3 as AppIndicator
    INDICATOR_TYPE = "Ayatana"
except (ValueError, ImportError):
    try:
        gi.require_version('AppIndicator3', '0.1')
        from gi.repository import AppIndicator3 as AppIndicator
        INDICATOR_TYPE = "AppIndicator3"
    except (ValueError, ImportError):
        AppIndicator = None
        INDICATOR_TYPE = None

from gi.repository import Gtk

from .config import ConfigManager

logger = logging.getLogger(__name__)


class SystemTray:
    """
    System tray icon with dropdown menu.
    
    Uses AyatanaAppIndicator3 on modern Ubuntu, with fallback to AppIndicator3.
    """
    
    def __init__(
        self, 
        config: ConfigManager, 
        on_settings: callable, 
        on_quit: callable
    ):
        """
        Initialize the system tray.
        
        Args:
            config: ConfigManager instance for mute state.
            on_settings: Callback when "Settings" is clicked.
            on_quit: Callback when "Quit" is clicked.
        """
        self.config = config
        self._on_settings = on_settings
        self._on_quit = on_quit
        
        if AppIndicator is None:
            logger.error("AppIndicator not available - tray icon disabled")
            self.indicator = None
            return
        
        # Create the indicator
        self.indicator = AppIndicator.Indicator.new(
            "voiceclock",
            "preferences-system-time",  # Use a standard system icon
            AppIndicator.IndicatorCategory.APPLICATION_STATUS
        )
        self.indicator.set_status(AppIndicator.IndicatorStatus.ACTIVE)
        self.indicator.set_title("VoiceClock")
        
        # Build and attach menu
        self.indicator.set_menu(self._build_menu())
        
        logger.info(f"SystemTray initialized using {INDICATOR_TYPE}")
    
    def _build_menu(self) -> Gtk.Menu:
        """
        Build the tray dropdown menu.
        
        Returns:
            The constructed Gtk.Menu.
        """
        menu = Gtk.Menu()
        
        # Settings item
        item_settings = Gtk.MenuItem(label="⚙️ Settings")
        item_settings.connect("activate", lambda _: self._on_settings())
        menu.append(item_settings)
        
        # Separator
        menu.append(Gtk.SeparatorMenuItem())
        
        # Mute toggle (checkable)
        self.item_mute = Gtk.CheckMenuItem(label="🔇 Mute")
        self.item_mute.set_active(self.config.get("muted", False))
        self.item_mute.connect("toggled", self._on_mute_toggled)
        menu.append(self.item_mute)
        
        # Separator
        menu.append(Gtk.SeparatorMenuItem())
        
        # Quit item
        item_quit = Gtk.MenuItem(label="❌ Quit")
        item_quit.connect("activate", lambda _: self._on_quit())
        menu.append(item_quit)
        
        menu.show_all()
        return menu
    
    def _on_mute_toggled(self, widget: Gtk.CheckMenuItem) -> None:
        """
        Handle mute toggle.
        
        Args:
            widget: The CheckMenuItem that was toggled.
        """
        muted = widget.get_active()
        self.config.set("muted", muted)
        status = "muted" if muted else "unmuted"
        logger.info(f"VoiceClock {status}")
    
    def update_mute_state(self) -> None:
        """Sync the mute checkbox with config (e.g., after settings change)."""
        if hasattr(self, 'item_mute'):
            self.item_mute.set_active(self.config.get("muted", False))
