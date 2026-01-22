"""
AudioPlayer - Lightweight GStreamer wrapper for audio playback.

Uses GStreamer's playbin element for native, low-latency audio playback
without subprocess overhead.
"""

import logging
from pathlib import Path

import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GLib

logger = logging.getLogger(__name__)


class AudioPlayer:
    """GStreamer-based audio player for .ogg/.mp3 files."""
    
    def __init__(self):
        """Initialize GStreamer and create playbin element."""
        Gst.init(None)
        
        self._player = Gst.ElementFactory.make("playbin", "voiceclock-player")
        if not self._player:
            raise RuntimeError("Failed to create GStreamer playbin element")
        
        # Connect to bus for error handling
        bus = self._player.get_bus()
        bus.add_signal_watch()
        bus.connect("message::error", self._on_error)
        bus.connect("message::eos", self._on_eos)
        
        logger.info("AudioPlayer initialized with GStreamer playbin")
    
    def play(self, file_path: Path) -> bool:
        """
        Play an audio file.
        
        Args:
            file_path: Path to the audio file (.ogg or .mp3).
            
        Returns:
            True if playback started successfully.
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            logger.warning(f"Audio file not found: {file_path}")
            return False
        
        # Stop any current playback
        self.stop()
        
        # Set the URI and start playing
        uri = file_path.absolute().as_uri()
        self._player.set_property("uri", uri)
        
        result = self._player.set_state(Gst.State.PLAYING)
        
        if result == Gst.StateChangeReturn.FAILURE:
            logger.error(f"Failed to play: {file_path}")
            return False
        
        logger.info(f"Playing: {file_path.name}")
        return True
    
    def stop(self) -> None:
        """Stop current playback."""
        self._player.set_state(Gst.State.NULL)
    
    def _on_error(self, bus, message) -> None:
        """Handle GStreamer error messages."""
        err, debug = message.parse_error()
        logger.error(f"GStreamer error: {err.message}")
        logger.debug(f"Debug info: {debug}")
        self.stop()
    
    def _on_eos(self, bus, message) -> None:
        """Handle end-of-stream (playback finished)."""
        logger.debug("Playback finished")
        self.stop()
    
    def cleanup(self) -> None:
        """Clean up GStreamer resources."""
        self.stop()
        self._player = None
