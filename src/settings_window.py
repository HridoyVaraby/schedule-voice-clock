"""
SettingsWindow - GTK3 settings dialog for VoiceClock.

Provides a clean UI for configuring language and interval preferences.
Window is destroyed on close to minimize RAM usage.
"""

import logging

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib

from .config import ConfigManager

logger = logging.getLogger(__name__)


class SettingsWindow(Gtk.Window):
    """
    Settings dialog window.
    
    Destroyed on close to free RAM (not hidden).
    """
    
    # Available options
    LANGUAGES = [
        ("en", "English"),
        ("bn", "বাংলা (Bangla)")
    ]
    
    INTERVALS = [
        (15, "Every 15 minutes"),
        (30, "Every 30 minutes"),
        (60, "Every hour")
    ]
    
    def __init__(self, config: ConfigManager, on_saved: callable = None):
        """
        Initialize the settings window.
        
        Args:
            config: ConfigManager instance.
            on_saved: Optional callback after settings are saved.
        """
        super().__init__(title="VoiceClock Settings")
        
        self.config = config
        self._on_saved = on_saved
        
        # Window properties
        self.set_default_size(350, 200)
        self.set_border_width(20)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_resizable(False)
        
        # Destroy on close (not hide) for RAM efficiency
        self.connect("delete-event", self._on_delete)
        
        # Build UI
        self._build_ui()
        
        logger.info("SettingsWindow opened")
    
    def _build_ui(self) -> None:
        """Construct the UI components."""
        # Main vertical box
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=16)
        self.add(vbox)
        
        # --- Header ---
        header = Gtk.Label()
        header.set_markup("<b>🕐 VoiceClock Settings</b>")
        header.set_halign(Gtk.Align.START)
        vbox.pack_start(header, False, False, 0)
        
        # --- Language Selection ---
        lang_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        lang_label = Gtk.Label(label="Language:")
        lang_label.set_halign(Gtk.Align.START)
        lang_label.set_size_request(100, -1)
        lang_box.pack_start(lang_label, False, False, 0)
        
        self.lang_combo = Gtk.ComboBoxText()
        current_lang = self.config.get("language", "en")
        active_index = 0
        for i, (code, name) in enumerate(self.LANGUAGES):
            self.lang_combo.append(code, name)
            if code == current_lang:
                active_index = i
        self.lang_combo.set_active(active_index)
        lang_box.pack_start(self.lang_combo, True, True, 0)
        
        vbox.pack_start(lang_box, False, False, 0)
        
        # --- Interval Selection ---
        interval_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        interval_label = Gtk.Label(label="Interval:")
        interval_label.set_halign(Gtk.Align.START)
        interval_label.set_size_request(100, -1)
        interval_box.pack_start(interval_label, False, False, 0)
        
        self.interval_combo = Gtk.ComboBoxText()
        current_interval = self.config.get("interval", 60)
        active_index = 2  # Default to 60 min
        for i, (minutes, label) in enumerate(self.INTERVALS):
            self.interval_combo.append(str(minutes), label)
            if minutes == current_interval:
                active_index = i
        self.interval_combo.set_active(active_index)
        interval_box.pack_start(self.interval_combo, True, True, 0)
        
        vbox.pack_start(interval_box, False, False, 0)
        
        # --- Spacer ---
        vbox.pack_start(Gtk.Box(), True, True, 0)
        
        # --- Buttons ---
        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        button_box.set_halign(Gtk.Align.END)
        
        cancel_btn = Gtk.Button(label="Cancel")
        cancel_btn.connect("clicked", lambda _: self.destroy())
        button_box.pack_start(cancel_btn, False, False, 0)
        
        save_btn = Gtk.Button(label="Save")
        save_btn.get_style_context().add_class("suggested-action")
        save_btn.connect("clicked", self._on_save_clicked)
        button_box.pack_start(save_btn, False, False, 0)
        
        vbox.pack_start(button_box, False, False, 0)
    
    def _on_save_clicked(self, button: Gtk.Button) -> None:
        """
        Handle save button click.
        
        Saves settings to config and shows notification.
        """
        # Get selected values
        lang_id = self.lang_combo.get_active_id()
        interval_id = self.interval_combo.get_active_id()
        
        if lang_id:
            self.config.set("language", lang_id, auto_save=False)
        
        if interval_id:
            self.config.set("interval", int(interval_id), auto_save=False)
        
        # Save to disk
        self.config.save()
        
        logger.info(f"Settings saved: language={lang_id}, interval={interval_id}")
        
        # Show notification
        self._show_notification("Settings saved successfully!")
        
        # Callback
        if self._on_saved:
            self._on_saved()
        
        # Close window
        self.destroy()
    
    def _show_notification(self, message: str) -> None:
        """
        Show a brief notification toast.
        
        Args:
            message: The notification message.
        """
        try:
            import subprocess
            subprocess.Popen([
                "notify-send",
                "VoiceClock",
                message,
                "-i", "preferences-system-time",
                "-t", "2000"
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception as e:
            logger.debug(f"Could not show notification: {e}")
    
    def _on_delete(self, widget, event) -> bool:
        """Handle window close."""
        logger.info("SettingsWindow closed")
        return False  # Allow destruction
