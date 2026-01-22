## 1. Product Overview

**Schedule Voice Clock** is a productivity and accessibility tool for Ubuntu users. It provides periodic voice notifications of the current time, helping users stay mindful of time without looking at a clock.

* **Primary Goal:** Deliver time announcements with zero latency (offline) and minimal RAM usage.
* **Target Platform:** Ubuntu (GNOME Desktop).
* **Core Languages:** English and Bangla.

---

## 2. Target Features

### 2.1 Audio Announcement Engine

* **Offline Playback:** Uses pre-recorded `.mp3` or `.ogg` files generated via ElevenLabs.
* **Language Selection:** Toggle between English and Bangla.
* **Interval Settings:** Choose between 15, 30, or 60-minute increments.
* **Mute Toggle:** A quick "Silent Mode" to pause announcements without closing the app.

### 2.2 User Interface (GUI)

* **Settings Window:** A clean GTK-based window to configure preferences.
* **System Tray Integration:** A persistent icon in the Ubuntu top bar (AppIndicator) for quick access.
* **Visual Feedback:** A simple notification toast (libnotify) when the time is announced.

### 2.3 Background Persistence

* **Daemon Logic:** The app runs as a background process.
* **Autostart:** Option to launch automatically upon user login.

---

## 3. Technical Specifications

| Component | Specification |
| --- | --- |
| **Runtime** | Python 3.x |
| **UI Library** | `PyGObject` (GTK 3/4) |
| **System Integration** | `libappindicator3` (for the tray icon) |
| **Audio Library** | `playsound` or `GStreamer` (for low-latency native playback) |
| **Scheduling** | `GLib.timeout_add` (most resource-efficient for GTK apps) |
| **Storage** | `ConfigParser` (.ini) for user settings |

---

## 4. User Flow

1. **Installation:** User installs the package and opens "VoiceClock" from the App Menu.
2. **Configuration:** User selects "Bangla" and "30 Minutes" and clicks "Apply."
3. **Backgrounding:** The window is closed, but the app stays active in the System Tray.
4. **Announcement:** When the system clock hits `XX:30`, the app fetches `assets/bn/30_min.mp3` and plays it.
5. **Modification:** User clicks the Tray Icon to Mute or change the Language.

---

## 5. Resource Constraints & Optimization

To ensure the app takes "very low resources" (as requested):

* **Event-Driven:** Instead of a `while True` loop that eats CPU, we use the GLib event loop which sleeps until the system clock triggers an event.
* **Memory Management:** The UI window will be destroyed when closed, leaving only the tray icon (minimal footprint) in RAM.
* **Audio Format:** Use `.ogg` or compressed `.mp3` to keep the app installer size under 10MB.

---

## 6. Project Roadmap

* **Phase 1:** Record/Export audio files for both languages (12 hours x 4 intervals = 48 files per language).
* **Phase 2:** Develop the Python background logic (time-checker).
* **Phase 3:** Build the GTK Settings UI and System Tray icon.
* **Phase 4:** Create the `.desktop` entry for Ubuntu integration.