"""
TimeAnnouncer - Core logic engine for scheduled time announcements.

Handles time-checking logic with debounce protection to prevent
duplicate announcements within the same minute.
"""

import logging
from datetime import datetime
from pathlib import Path
from typing import Optional

from .config import ConfigManager
from .player import AudioPlayer

logger = logging.getLogger(__name__)


class TimeAnnouncer:
    """
    Core time announcement engine.
    
    Designed to be called every 60 seconds via GLib.timeout_add_seconds.
    Uses debounce logic to prevent double-plays within the same minute.
    """
    
    def __init__(self, config: ConfigManager, player: AudioPlayer, assets_dir: Path):
        """
        Initialize the TimeAnnouncer.
        
        Args:
            config: ConfigManager instance for settings.
            player: AudioPlayer instance for audio playback.
            assets_dir: Base path to the assets directory.
        """
        self.config = config
        self.player = player
        self.assets_dir = Path(assets_dir)
        
        # Debounce tracker: stores the last minute we played audio
        self._last_played_minute: int = -1
        self._last_played_hour: int = -1
        
        logger.info("TimeAnnouncer initialized")
    
    def check_and_announce(self) -> bool:
        """
        Check current time and play announcement if interval matches.
        
        This method is designed to be called by GLib.timeout_add_seconds.
        Returns True to keep the timeout running.
        
        Returns:
            Always True to keep the GLib timeout active.
        """
        # Skip if muted
        if self.config.get("muted"):
            return True
        
        now = datetime.now()
        current_hour = now.hour
        current_minute = now.minute
        interval = self.config.get("interval", 60)
        
        # Check if current minute matches the interval
        # interval=15 → trigger at :00, :15, :30, :45
        # interval=30 → trigger at :00, :30
        # interval=60 → trigger at :00
        if current_minute % interval == 0:
            # Debounce: prevent double-play within the same hour:minute
            if not self._already_played(current_hour, current_minute):
                self._last_played_hour = current_hour
                self._last_played_minute = current_minute
                self._play_time_audio(current_hour, current_minute)
        
        return True  # Keep timeout running
    
    def _already_played(self, hour: int, minute: int) -> bool:
        """
        Check if we already played for this specific hour:minute.
        
        Args:
            hour: Current hour (0-23).
            minute: Current minute (0-59).
            
        Returns:
            True if already played for this time.
        """
        return (self._last_played_hour == hour and 
                self._last_played_minute == minute)
    
    def _play_time_audio(self, hour: int, minute: int) -> None:
        """
        Construct the audio file path and play it.
        
        Args:
            hour: Hour in 24-hour format (0-23).
            minute: Minute (0-59).
        """
        # Convert 24-hour to 12-hour format
        hour_12 = hour % 12
        if hour_12 == 0:
            hour_12 = 12
        
        language = self.config.get("language", "en")
        filename = f"{hour_12:02d}_{minute:02d}.ogg"
        audio_path = self.assets_dir / "audio" / language / filename
        
        if audio_path.exists():
            logger.info(f"Announcing time: {hour_12:02d}:{minute:02d} ({language})")
            self.player.play(audio_path)
        else:
            # Try .mp3 fallback
            audio_path_mp3 = audio_path.with_suffix('.mp3')
            if audio_path_mp3.exists():
                logger.info(f"Announcing time: {hour_12:02d}:{minute:02d} ({language}) [mp3]")
                self.player.play(audio_path_mp3)
            else:
                logger.warning(f"Audio file not found: {audio_path} or {audio_path_mp3}")
    
    def force_announce(self) -> None:
        """
        Force an immediate time announcement (for testing).
        
        Bypasses interval and debounce checks.
        """
        now = datetime.now()
        self._play_time_audio(now.hour, now.minute)
    
    def reset_debounce(self) -> None:
        """Reset the debounce tracker."""
        self._last_played_minute = -1
        self._last_played_hour = -1
