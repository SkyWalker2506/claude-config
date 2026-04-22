# Telegram Bridge Plugin

Telegram bot integration for Claude Code — bidirectional bridge supporting text, photo, document, and voice messages.

## Features

- **Text commands** — send Claude Code commands via Telegram
- **Voice transcription** — Whisper-powered TR/EN audio-to-text (OpenAI API + local fallback)
- **Photo/document support** — attach files to Claude sessions
- **Bidirectional** — Claude results delivered back to your Telegram chat

## Requirements

| Requirement | Details |
|-------------|---------|
| Secrets | `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID` |
| Deps | `curl`, `python3` |
| Optional | `openai-whisper` (pip) for local voice transcription |

## Installed Files

| File | Purpose |
|------|---------|
| `config/notify.sh` | Send notifications to Telegram |
| `config/telegram-poll.sh` | Long-polling loop (main bot daemon) |
| `config/telegram-wait.sh` | Wait for user reply |
| `config/telegram-ask.sh` | Send prompt and wait for answer |
| `config/tg_parse.py` | Message parsing |
| `config/tg_send.py` | Send messages/files |
| `config/tg_voice.py` | Whisper voice transcription |

## Usage

```bash
# Start the bot daemon
tgbot-start

# Stop
tgbot-stop

# Check status
tgbot-status
```

## Install

```bash
./install.sh   # installs as part of full claude-config setup
```

Or install standalone via claude-marketplace: `ccplugin-telegram`.
