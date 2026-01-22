#!/usr/bin/env python3
"""
ElevenLabs Audio Generator for VoiceClock

Generates voice assets for time announcements in English and Bangla
using the ElevenLabs Text-to-Speech API.

Usage:
    1. Set ELEVENLABS_API_KEY in .env file
    2. Configure VOICE_ID_EN and VOICE_ID_BN below
    3. Set DRY_RUN = True to test text generation
    4. Set DRY_RUN = False to generate audio files
    5. Run: python3 scripts/generate_audio.py
"""

import os
import time
from pathlib import Path
from typing import Generator

from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# =============================================================================
# CONFIGURATION - Modify these values
# =============================================================================

# Set to True to only print text without calling API (saves credits)
DRY_RUN = True

# ElevenLabs Voice IDs (find yours at https://elevenlabs.io/voices)
VOICE_ID_EN = "JBFqnCBsd6RMkjVDRZzb"  # English voice (e.g., "George")
VOICE_ID_BN = "JBFqnCBsd6RMkjVDRZzb"  # Bangla voice (replace with appropriate ID)

# Model ID (eleven_multilingual_v2 supports Bangla)
MODEL_ID = "eleven_multilingual_v2"

# Output format
OUTPUT_FORMAT = "mp3_44100_128"

# Rate limiting delay (seconds between API calls)
API_DELAY = 0.5

# Languages to generate
GENERATE_ENGLISH = True
GENERATE_BANGLA = True

# =============================================================================
# BANGLA NUMBER MAPPINGS
# =============================================================================

# Bangla numerals for hours (1-12)
BANGLA_HOURS = {
    1: "একটা",
    2: "দুইটা",
    3: "তিনটা",
    4: "চারটা",
    5: "পাঁচটা",
    6: "ছয়টা",
    7: "সাতটা",
    8: "আটটা",
    9: "নয়টা",
    10: "দশটা",
    11: "এগারোটা",
    12: "বারোটা",
}

# Bangla minute phrases
BANGLA_MINUTES = {
    0: "",  # No minute suffix for :00
    15: "বেজে পনেরো মিনিট",
    30: "বেজে ত্রিশ মিনিট",
    45: "বেজে পঁয়তাল্লিশ মিনিট",
}


def get_bangla_time_of_day(hour_24: int) -> str:
    """
    Get the Bangla time-of-day phrase based on 24-hour time.
    
    Args:
        hour_24: Hour in 24-hour format (0-23).
        
    Returns:
        Bangla time-of-day string.
    """
    if 4 <= hour_24 <= 5:
        return "ভোর"      # Bhor (Dawn) - 4:00 to 5:59
    elif 6 <= hour_24 <= 11:
        return "সকাল"    # Morning - 6:00 to 11:59
    elif 12 <= hour_24 <= 15:
        return "দুপুর"   # Noon/Afternoon - 12:00 to 15:59
    elif 16 <= hour_24 <= 17:
        return "বিকেল"   # Late Afternoon - 16:00 to 17:59
    elif 18 <= hour_24 <= 19:
        return "সন্ধ্যা"  # Evening - 18:00 to 19:59
    else:
        return "রাত"     # Night - 20:00 to 3:59


def get_bangla_text(hour_24: int, minute: int) -> str:
    """
    Generate Bangla text for a given time.
    
    Args:
        hour_24: Hour in 24-hour format (0-23).
        minute: Minute (0, 15, 30, 45).
        
    Returns:
        Bangla text string for TTS.
    """
    # Convert to 12-hour format
    hour_12 = hour_24 % 12
    if hour_12 == 0:
        hour_12 = 12
    
    time_of_day = get_bangla_time_of_day(hour_24)
    hour_word = BANGLA_HOURS[hour_12]
    
    if minute == 0:
        # "এখন সময় দুপুর দুইটা"
        return f"এখন সময় {time_of_day} {hour_word}"
    else:
        # "এখন সময় দুপুর দুইটা বেজে পনেরো মিনিট"
        minute_phrase = BANGLA_MINUTES[minute]
        # Remove "টা" suffix for minute phrases (use base form)
        hour_base = hour_word.replace("টা", "টা")
        return f"এখন সময় {time_of_day} {hour_base} {minute_phrase}"


# =============================================================================
# ENGLISH TEXT GENERATION
# =============================================================================

ENGLISH_HOURS = {
    1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six",
    7: "seven", 8: "eight", 9: "nine", 10: "ten", 11: "eleven", 12: "twelve",
}

ENGLISH_MINUTES = {
    0: "o'clock",
    15: "fifteen",
    30: "thirty",
    45: "forty-five",
}


def get_english_period(hour_24: int) -> str:
    """
    Get AM/PM and descriptive period for English.
    
    Args:
        hour_24: Hour in 24-hour format (0-23).
        
    Returns:
        Period string (e.g., "in the morning", "PM").
    """
    if 0 <= hour_24 <= 4:
        return "at night"
    elif 5 <= hour_24 <= 11:
        return "in the morning"
    elif hour_24 == 12:
        return "in the afternoon"
    elif 13 <= hour_24 <= 17:
        return "in the afternoon"
    elif 18 <= hour_24 <= 20:
        return "in the evening"
    else:
        return "at night"


def get_english_text(hour_24: int, minute: int) -> str:
    """
    Generate natural English text for a given time.
    
    Args:
        hour_24: Hour in 24-hour format (0-23).
        minute: Minute (0, 15, 30, 45).
        
    Returns:
        English text string for TTS.
    """
    # Convert to 12-hour format
    hour_12 = hour_24 % 12
    if hour_12 == 0:
        hour_12 = 12
    
    hour_word = ENGLISH_HOURS[hour_12]
    period = get_english_period(hour_24)
    
    if minute == 0:
        # "It is two o'clock in the afternoon"
        return f"It is {hour_word} o'clock {period}"
    else:
        # "It is two fifteen in the afternoon"
        minute_word = ENGLISH_MINUTES[minute]
        return f"It is {hour_word} {minute_word} {period}"


# =============================================================================
# AUDIO GENERATION
# =============================================================================

def generate_time_slots() -> Generator[tuple[int, int], None, None]:
    """
    Generate all time slots for a 24-hour cycle at 15-minute intervals.
    
    Yields:
        Tuples of (hour, minute) for each time slot.
    """
    for hour in range(24):
        for minute in (0, 15, 30, 45):
            yield hour, minute


def generate_audio_file(
    client,
    text: str,
    voice_id: str,
    output_path: Path
) -> bool:
    """
    Generate audio file using ElevenLabs API.
    
    Args:
        client: ElevenLabs client instance.
        text: Text to convert to speech.
        voice_id: Voice ID to use.
        output_path: Path to save the audio file.
        
    Returns:
        True if successful.
    """
    try:
        from elevenlabs import save
        
        audio = client.text_to_speech.convert(
            voice_id=voice_id,
            text=text,
            model_id=MODEL_ID,
            output_format=OUTPUT_FORMAT,
        )
        
        # Ensure directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Save to file
        save(audio, str(output_path))
        
        return True
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False


def main():
    """Main entry point."""
    print("=" * 60)
    print("VoiceClock Audio Generator")
    print("=" * 60)
    print()
    
    if DRY_RUN:
        print("🔍 DRY RUN MODE - No API calls will be made")
        print("   Review the generated text below, then set DRY_RUN = False")
        print()
    else:
        # Import and initialize ElevenLabs client
        try:
            from elevenlabs.client import ElevenLabs
        except ImportError:
            print("❌ Error: elevenlabs package not installed")
            print("   Run: pip install elevenlabs python-dotenv")
            return
        
        api_key = os.getenv("ELEVENLABS_API_KEY")
        if not api_key:
            print("❌ Error: ELEVENLABS_API_KEY not found in .env file")
            print("   Create a .env file with: ELEVENLABS_API_KEY=your_key_here")
            return
        
        client = ElevenLabs(api_key=api_key)
        print("✅ ElevenLabs client initialized")
        print()
    
    # Get script directory and project root
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    assets_dir = project_root / "assets" / "audio"
    
    # Count totals
    total_files = 24 * 4  # 96 files per language
    generated = 0
    failed = 0
    
    # Generate English files
    if GENERATE_ENGLISH:
        print("📁 ENGLISH FILES")
        print("-" * 40)
        
        for hour, minute in generate_time_slots():
            filename = f"{hour:02d}_{minute:02d}.mp3"
            output_path = assets_dir / "en" / filename
            text = get_english_text(hour, minute)
            
            if DRY_RUN:
                print(f"  {filename}: \"{text}\"")
            else:
                print(f"  Generating {filename}...", end=" ", flush=True)
                if generate_audio_file(client, text, VOICE_ID_EN, output_path):
                    print("✅")
                    generated += 1
                else:
                    failed += 1
                time.sleep(API_DELAY)
        
        print()
    
    # Generate Bangla files
    if GENERATE_BANGLA:
        print("📁 BANGLA FILES (বাংলা)")
        print("-" * 40)
        
        for hour, minute in generate_time_slots():
            filename = f"{hour:02d}_{minute:02d}.mp3"
            output_path = assets_dir / "bn" / filename
            text = get_bangla_text(hour, minute)
            
            if DRY_RUN:
                print(f"  {filename}: \"{text}\"")
            else:
                print(f"  Generating {filename}...", end=" ", flush=True)
                if generate_audio_file(client, text, VOICE_ID_BN, output_path):
                    print("✅")
                    generated += 1
                else:
                    failed += 1
                time.sleep(API_DELAY)
        
        print()
    
    # Summary
    print("=" * 60)
    if DRY_RUN:
        print("DRY RUN COMPLETE")
        print(f"Total files to generate: {total_files * (GENERATE_ENGLISH + GENERATE_BANGLA)}")
        print()
        print("Next steps:")
        print("  1. Review the text output above")
        print("  2. Set your Voice IDs in the configuration section")
        print("  3. Set DRY_RUN = False")
        print("  4. Run this script again")
    else:
        print("GENERATION COMPLETE")
        print(f"  ✅ Generated: {generated}")
        print(f"  ❌ Failed: {failed}")
        print(f"  📁 Output: {assets_dir}")
    print("=" * 60)


if __name__ == "__main__":
    main()
