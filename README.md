<div align="center">

<img src="https://files.catbox.moe/f4nnyn.svg" width="100%" height="300">

<br><br>

[![License](https://img.shields.io/badge/License-MIT-A960FF?style=for-the-badge&logo=opensourceinitiative&logoColor=white&labelColor=0D1117)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10+-2CA5E0?style=for-the-badge&logo=python&logoColor=white&labelColor=0D1117)](https://www.python.org)
[![Pyrogram](https://img.shields.io/badge/Pyrogram-Client-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white&labelColor=0D1117)](https://docs.pyrogram.org)

</div>

<br>

<div align="center">

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                   ✦  RUNAK MUSIC BOT  ✦
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

</div>

## 📖 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Project Structure](#-project-structure)
- [Requirements](#-requirements)
- [Environment Variables](#-environment-variables)
- [Setup](#-setup)
- [Commands](#-commands)
- [Notes](#-notes)
- [License](#-license)

<br>

## 〔 ✦ 〕 Overview

> **Runak Music Bot** is a lightweight Telegram Voice Chat Music Bot.
> Built on **Pyrogram** · **PyTgCalls** · **Firebase (Firestore)** — one bot account handles
> commands, and one assistant (userbot) account joins the voice chat and
> streams the audio.

Streams are fetched through the **Meow API** (`MEOW_API_URL` / `MEOW_API_KEY`,
get a key from [@MeowApiRobot](https://t.me/MeowApiRobot) on Telegram) rather
than downloading directly with `yt-dlp`. Every "now playing" message is sent
as a branded thumbnail — the video's YouTube thumbnail with the Runak Music
name, the track title, and the duration burned in — built on the fly with
Pillow.

<br>

## 〔 ✦ 〕 Features

```
✦ YouTube Search & Direct Link Play      ✦ Pause / Resume
✦ Video-Call Play (vplay)                ✦ Skip / Stop / End
✦ Force Play (skip the queue)            ✦ Seek Forward / Backward
✦ Auto Queue + Auto-Advance              ✦ Restart Current Track
✦ Loop Current Track (0–10 times)        ✦ Inline Player Buttons
✦ Owner Broadcast                        ✦ Ping / Latency Check
✦ Branded "Now Playing" Thumbnails       ✦ Meow API Stream Backend
```

<br>

## 〔 ✦ 〕 Project Structure

```
RunakMusic-src/
├── RunakMusic/
│   ├── __init__.py
│   ├── __main__.py        # entry point — run with: python -m RunakMusic
│   ├── command/
│   │   ├── __init__.py
│   │   └── commands.py     # play, vplay, playforce, vplayforce, skip, stop,
│   │                        # end, seek, seekback, resume, pause, loop,
│   │                        # restart, ping, broadcast
│   └── engine/
│       ├── __init__.py
│       ├── data.py          # Firestore — remembers served chats
│       ├── bot.py           # bot client, userbot client, PyTgCalls, inline buttons
│       ├── artist.py        # YouTube search + Meow API streaming, broadcast
│       └── thumbnail.py     # builds the branded "now playing" thumbnail
├── Dockerfile
├── LICENSE
├── README.md
├── config.py
├── requirements.txt
└── sample.env
```

<br>

## 〔 ✦ 〕 Requirements

| Component | Minimum Version / Note |
|:---|:---|
| Python | 3.10 or higher |
| FFmpeg | Latest stable release |
| Firebase Project | With a service-account key (Firestore in Native mode) |
| Telegram Account | For the assistant (string session) |
| Meow API Key | From [@MeowApiRobot](https://t.me/MeowApiRobot) — used to fetch streams |

<br>

## 〔 ✦ 〕 Environment Variables

<div align="center">

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
      Create a  .env  file with these values
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

</div>

| Variable | Required | Description |
|:---|:---:|:---|
| `API_ID` | ✅ | From [my.telegram.org](https://my.telegram.org) |
| `API_HASH` | ✅ | From [my.telegram.org](https://my.telegram.org) |
| `BOT_TOKEN` | ✅ | From [@BotFather](https://t.me/BotFather) |
| `SESSION_STRING` | ✅ | Pyrogram string session for the assistant account |
| `OWNER_ID` | ✅ | Your numeric Telegram user id (needed for `/broadcast`) |
| `FIREBASE_CREDENTIALS_PATH` | ✅* | Path to your Firebase service-account JSON file |
| `FIREBASE_CREDENTIALS_JSON` | ✅* | The service-account JSON pasted as one line (alternative to the path) |
| `MEOW_API_URL` | ✅ | Base URL of the Meow streaming API |
| `MEOW_API_KEY` | ✅ | Your key from [@MeowApiRobot](https://t.me/MeowApiRobot) |
| `DURATION_LIMIT_MIN` | ❌ | Max track length in minutes (default: `60`) |

\* Provide **one** of `FIREBASE_CREDENTIALS_PATH` or `FIREBASE_CREDENTIALS_JSON`, not both.

<br>

## 〔 ✦ 〕 Setup

1. Install dependencies (needs `ffmpeg` and, for the thumbnails' text, a
   font such as `fonts-dejavu-core` installed on the system too):
   ```
   pip install -r requirements.txt
   ```
2. Set up Firestore in the [Firebase Console](https://console.firebase.google.com):
   - Create a project (or pick an existing one).
   - Left sidebar → **Build → Firestore Database** → **Create database** →
     start in **Native mode**, pick a location.
   - Top-left gear icon → **Project settings → Service accounts** →
     **Generate new private key**. This downloads a JSON file — save it as
     `firebase-credentials.json` in the repo root (or point
     `FIREBASE_CREDENTIALS_PATH` at wherever you put it).
3. Copy `sample.env` to `.env` and fill in the variables above, including a
   Meow API key from [@MeowApiRobot](https://t.me/MeowApiRobot).
4. Generate a string session for the assistant account and put it in
   `SESSION_STRING`.
5. Add both the bot and the assistant account to your group, and give the
   assistant permission to start/join the voice chat.
6. Run it from the repo root:
   ```
   python -m RunakMusic
   ```

<br>

## 〔 ✦ 〕 Commands

| Command | Description |
|:---|:---|
| `/play <name\|link>` | Play or queue a song |
| `/vplay <name\|link>` | Play or queue a video |
| `/playforce <name\|link>` | Skip current and play now |
| `/vplayforce <name\|link>` | Skip current and video-play now |
| `/skip` | Play the next track in queue |
| `/pause` | Pause playback |
| `/resume` | Resume playback |
| `/seek <secs>` | Jump forward |
| `/seekback <secs>` | Jump backward |
| `/restart` | Replay current track from 0:00 |
| `/loop <0-10>` | Repeat the current track |
| `/stop` / `/end` | Stop and clear the queue |
| `/ping` | Check bot latency |
| `/broadcast` | Send a message to every served chat (owner only) |

<br>

## 〔 ✦ 〕 Notes

- Queue/loop state is kept in memory per-process — simple on purpose, but it
  resets on restart and won't work across multiple bot instances.
- `py-tgcalls` changes its API a bit between versions. This targets the
  2.x line (`MediaStream`, `AudioQuality`, `calls.play` /
  `calls.change_stream` / `calls.leave_call`). If a call in
  `RunakMusic/command/commands.py` or `RunakMusic/engine/bot.py` doesn't
  match what you have installed, check that package's changelog for the
  equivalent call.
- Streams are fetched from the Meow API, not downloaded directly with
  `yt-dlp` — if a track fails to play, first check that `MEOW_API_KEY` is
  valid and that `MEOW_API_URL` is reachable from your server.
- Served-chat data lives in Firestore, in a `served_chats` collection —
  browse or clear it any time from the
  [Firebase Console](https://console.firebase.google.com) under
  **Firestore Database**.
- `firebase-credentials.json` is a private key for your Firebase project —
  keep it out of version control (add it to `.gitignore`) and never commit
  it or paste it somewhere public.
- Thumbnails are generated once per video id and cached under
  `thumbnails/`; edit `RunakMusic/engine/thumbnail.py` to change the brand
  name, accent color, or layout.
- All bot-facing text is written directly inline in
  `RunakMusic/command/commands.py` — edit the strings there if you want to
  change the wording.
- Renaming the bot and its thumbnails doesn't change who owns the copyright
  in the music it plays — that responsibility (and the terms you're
  streaming under) is on whoever runs and uses the bot.

<br>

## 〔 ✦ 〕 License

Released under the [MIT License](LICENSE).
