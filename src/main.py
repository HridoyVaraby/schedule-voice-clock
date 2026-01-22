#!/usr/bin/env python3
"""
VoiceClock - Schedule Voice Clock Application

A lightweight Ubuntu desktop application that announces the time
at configurable intervals in English or Bangla.

This is the main entry point that bootstraps all components.
"""

import logging
import signal
import sys
from pathlib import Path

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib

# Add src to path for absolute imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config import ConfigManager
from src.player import AudioPlayer
from src.scheduler import TimeAnnouncer
from src.tray import SystemTray
from src.settings_window import SettingsWindow

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(name)s: %(message)s'
)
logger = logging.getLogger("VoiceClock")


class VoiceClockApp:
    """
    Main application class.
    
    Orchestrates all components: config, player, scheduler, tray, and settings.
    """
    
    def __init__(self):
        """Initialize the VoiceClock application."""
        logger.info("Starting VoiceClock...")
        
        # Determine paths
        self.app_dir = Path(__file__).parent.parent
        self.config_path = self.app_dir / "data" / "settings.json"
        self.assets_dir = self.app_dir / "assets"
        
        # Initialize components
        self.config = ConfigManager(self.config_path)
        self.player = AudioPlayer()
        self.announcer = TimeAnnouncer(self.config, self.player, self.assets_dir)
        
        # Reference to current settings window (if open)
        self._settings_window = None
        
        # Create system tray
        self.tray = SystemTray(
            config=self.config,
            on_settings=self._show_settings,
            on_quit=self._quit
        )
        
        # Start the scheduler (event-driven, 60-second intervals)
        # GLib.timeout_add_seconds integrates with GTK main loop - zero CPU when idle
        self._scheduler_id = GLib.timeout_add_seconds(60, self._on_scheduler_tick)
        
        # Also check immediately on startup (in case we launch at XX:00)
        GLib.timeout_add_seconds(1, self._initial_check)
        
        logger.info("VoiceClock initialized successfully")
    
    def _on_scheduler_tick(self) -> bool:
        """
        Called every 60 seconds by GLib.timeout.
        
        Returns:
            True to keep the timeout running.
        """
        return self.announcer.check_and_announce()
    
    def _initial_check(self) -> bool:
        """
        Perform initial time check shortly after startup.
        
        Returns:
            False to run only once.
        """
        self.announcer.check_and_announce()
        return False  # Run only once
    
    def _show_settings(self) -> None:
        """Open the settings window."""
        # Avoid opening multiple settings windows
        if self._settings_window is not None:
            self._settings_window.present()
            return
        
        self._settings_window = SettingsWindow(
            config=self.config,
            on_saved=self._on_settings_saved
        )
        self._settings_window.connect("destroy", self._on_settings_closed)
        self._settings_window.show_all()
    
    def _on_settings_saved(self) -> None:
        """Handle settings saved event."""
        # Sync tray mute state
        self.tray.update_mute_state()
        # Reset debounce so new interval takes effect
        self.announcer.reset_debounce()
    
    def _on_settings_closed(self, window) -> None:
        """Handle settings window closed."""
        self._settings_window = None
    
    def _quit(self) -> None:
        """Quit the application."""
        logger.info("Quitting VoiceClock...")
        
        # Remove scheduler
        if hasattr(self, '_scheduler_id'):
            GLib.source_remove(self._scheduler_id)
        
        # Cleanup player
        self.player.cleanup()
        
        # Exit GTK main loop
        Gtk.main_quit()
    
    def run(self) -> None:
        """Run the GTK main loop."""
        # Handle Ctrl+C gracefully
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        
        logger.info("VoiceClock running in system tray")
        Gtk.main()


def main():
    """Application entry point."""
    app = VoiceClockApp()
    app.run()


if __name__ == "__main__":
    main()
