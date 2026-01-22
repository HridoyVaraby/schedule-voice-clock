#!/usr/bin/env python3
"""
Audio Filename Generator Utility

Generates a checklist of all audio filenames needed for VoiceClock.
This helps when recording/generating audio files with ElevenLabs.

Output: 48 filenames per language (12 hours × 4 intervals)
Format: HH_MM.ogg (01_00.ogg, 01_15.ogg, ..., 12_45.ogg)
"""


def generate_filenames(interval: int = 15) -> list[str]:
    """
    Generate all required audio filenames for a 12-hour cycle.
    
    Args:
        interval: Minutes between announcements (15, 30, or 60).
        
    Returns:
        List of filenames in HH_MM.ogg format.
    """
    filenames = []
    
    for hour in range(1, 13):  # 1 to 12
        for minute in range(0, 60, interval):
            filename = f"{hour:02d}_{minute:02d}.ogg"
            filenames.append(filename)
    
    return filenames


def main():
    """Print all required filenames as a checklist."""
    print("=" * 60)
    print("VoiceClock Audio Filename Checklist")
    print("=" * 60)
    print()
    
    # Generate for 15-minute intervals (covers all possible times)
    filenames = generate_filenames(interval=15)
    
    print(f"Total files needed per language: {len(filenames)}")
    print()
    print("📁 English files (assets/audio/en/):")
    print("-" * 40)
    for i, name in enumerate(filenames, 1):
        print(f"  [ ] {name}")
    
    print()
    print("📁 Bangla files (assets/audio/bn/):")
    print("-" * 40)
    for i, name in enumerate(filenames, 1):
        print(f"  [ ] {name}")
    
    print()
    print("=" * 60)
    print("TIP: Use ElevenLabs to generate these voice clips.")
    print("     Example text for 01_15.ogg: 'The time is one fifteen'")
    print("     Example text for 12_00.ogg: 'The time is twelve o'clock'")
    print("=" * 60)
    
    # Also output as a simple list for scripting
    print()
    print("📋 Plain list (for scripting):")
    print("-" * 40)
    print(", ".join(filenames))


if __name__ == "__main__":
    main()
