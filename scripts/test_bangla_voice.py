#!/usr/bin/env python3
"""
Test script to generate a single Bangla audio file for testing.
Run this first to verify voice quality before generating all files.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# =============================================================================
# CONFIGURATION - Modify these values
# =============================================================================

# Bangla voice ID - User specified
VOICE_ID_BN = "WiaIVvI1gDL4vT4y7qUU"

# Speech speed (0.7 = slower, 1.0 = normal, 1.2 = faster)
SPEECH_SPEED = 0.8

# Model - Eleven v3 (alpha)
MODEL_ID = "eleven_v3"

# Test time to generate
TEST_HOUR = 16  # 4 PM
TEST_MINUTE = 0


# =============================================================================
# BANGLA TEXT GENERATION (same logic as main script)
# =============================================================================

BANGLA_HOURS = {
    1: "একটা", 2: "দুইটা", 3: "তিনটা", 4: "চারটা", 5: "পাঁচটা", 6: "ছয়টা",
    7: "সাতটা", 8: "আটটা", 9: "নয়টা", 10: "দশটা", 11: "এগারোটা", 12: "বারোটা",
}

BANGLA_MINUTES = {
    0: "",
    15: "বেজে পনেরো মিনিট",
    30: "বেজে ত্রিশ মিনিট",
    45: "বেজে পঁয়তাল্লিশ মিনিট",
}


def get_bangla_time_of_day(hour_24: int) -> str:
    if 4 <= hour_24 <= 5:
        return "ভোর"
    elif 6 <= hour_24 <= 11:
        return "সকাল"
    elif 12 <= hour_24 <= 15:
        return "দুপুর"
    elif 16 <= hour_24 <= 17:
        return "বিকেল"
    elif 18 <= hour_24 <= 19:
        return "সন্ধ্যা"
    else:
        return "রাত"


def get_bangla_text(hour_24: int, minute: int) -> str:
    hour_12 = hour_24 % 12
    if hour_12 == 0:
        hour_12 = 12
    
    time_of_day = get_bangla_time_of_day(hour_24)
    hour_word = BANGLA_HOURS[hour_12]
    
    if minute == 0:
        return f"এখন সময় {time_of_day} {hour_word}"
    else:
        minute_phrase = BANGLA_MINUTES[minute]
        return f"এখন সময় {time_of_day} {hour_word} {minute_phrase}"


def main():
    print("=" * 60)
    print("VoiceClock - Bangla Voice Test")
    print("=" * 60)
    print()
    
    # Check API key
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        print("❌ Error: ELEVENLABS_API_KEY not found in .env")
        return
    
    # Import ElevenLabs
    try:
        from elevenlabs.client import ElevenLabs
        from elevenlabs import VoiceSettings, save
    except ImportError:
        print("❌ Error: elevenlabs package not installed")
        return
    
    # Initialize client
    client = ElevenLabs(api_key=api_key)
    print("✅ ElevenLabs client initialized")
    print()
    
    # Generate test text
    text = get_bangla_text(TEST_HOUR, TEST_MINUTE)
    filename = f"{TEST_HOUR:02d}_{TEST_MINUTE:02d}.mp3"
    
    print(f"🎙️ Voice ID: {VOICE_ID_BN}")
    print(f"⚡ Speed: {SPEECH_SPEED}")
    print(f"📝 Text: \"{text}\"")
    print(f"📁 File: {filename}")
    print()
    
    # Configure voice settings for Eleven v3 (alpha)
    # v3 requires stability to be 0.0, 0.5, or 1.0
    voice_settings = VoiceSettings(
        stability=0.5,           # Natural (0.0=Creative, 0.5=Natural, 1.0=Robust)
        similarity_boost=0.8,
        style=0.0,
        speed=SPEECH_SPEED,
        use_speaker_boost=True
    )
    
    # Generate audio
    print("Generating...", end=" ", flush=True)
    try:
        audio = client.text_to_speech.convert(
            voice_id=VOICE_ID_BN,
            text=text,
            model_id=MODEL_ID,
            output_format="mp3_44100_128",
            voice_settings=voice_settings
        )
        
        # Save to file
        output_dir = Path(__file__).parent.parent / "assets" / "audio" / "bn"
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / filename
        
        save(audio, str(output_path))
        print("✅")
        print()
        print(f"🎉 Test file generated: {output_path}")
        print()
        print("Play the file to verify the voice quality.")
        print("If satisfied, tell me to 'generate all' Bangla files.")
        print()
        print("To change the voice, update VOICE_ID_BN in this script.")
        print("To adjust speed, modify SPEECH_SPEED (0.7-1.0 recommended).")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print()
    print("=" * 60)


if __name__ == "__main__":
    main()
