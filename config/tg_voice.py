#!/usr/bin/env python3
"""
Download Telegram voice file and transcribe with Whisper (TR/EN).

Usage: tg_voice.py <bot_token> <file_id> [lang]
  lang: tr (default) | en | auto

Returns transcribed text on stdout.
Exits non-zero on failure.

Requirements:
  pip install openai-whisper  (for local)
  OR: OPENAI_API_KEY env var  (for API-based transcription)
"""

import sys
import os
import json
import tempfile
import urllib.request
import urllib.error

def download_file(token: str, file_id: str) -> str:
    """Download voice file from Telegram, return local path."""
    # Get file path from Telegram API
    url = f"https://api.telegram.org/bot{token}/getFile?file_id={file_id}"
    try:
        with urllib.request.urlopen(url, timeout=15) as resp:
            data = json.load(resp)
    except Exception as e:
        print(f"getFile error: {e}", file=sys.stderr)
        sys.exit(1)

    if not data.get("ok"):
        print(f"getFile failed: {data}", file=sys.stderr)
        sys.exit(1)

    file_path = data["result"]["file_path"]
    dl_url = f"https://api.telegram.org/file/bot{token}/{file_path}"

    # Download to temp file
    suffix = os.path.splitext(file_path)[1] or ".oga"
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    try:
        urllib.request.urlretrieve(dl_url, tmp.name)
    except Exception as e:
        print(f"download error: {e}", file=sys.stderr)
        sys.exit(1)

    return tmp.name


def transcribe_openai_api(audio_path: str, lang: str) -> str:
    """Transcribe using OpenAI Whisper API."""
    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY not set")

    import urllib.request
    import io

    with open(audio_path, "rb") as f:
        audio_data = f.read()

    boundary = "----WavBoundary"
    body_parts = []
    body_parts.append(f"--{boundary}\r\nContent-Disposition: form-data; name=\"model\"\r\n\r\nwhisper-1".encode())
    if lang != "auto":
        body_parts.append(f"--{boundary}\r\nContent-Disposition: form-data; name=\"language\"\r\n\r\n{lang}".encode())
    fname = os.path.basename(audio_path)
    body_parts.append(
        f"--{boundary}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"{fname}\"\r\nContent-Type: audio/ogg\r\n\r\n".encode()
        + audio_data
    )
    body_parts.append(f"--{boundary}--".encode())
    body = b"\r\n".join(body_parts)

    req = urllib.request.Request(
        "https://api.openai.com/v1/audio/transcriptions",
        data=body,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": f"multipart/form-data; boundary={boundary}",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        result = json.load(resp)
    return result.get("text", "").strip()


def transcribe_local_whisper(audio_path: str, lang: str) -> str:
    """Transcribe using local openai-whisper package."""
    try:
        import whisper  # type: ignore
    except ImportError:
        raise RuntimeError("openai-whisper not installed: pip install openai-whisper")

    model = whisper.load_model("base")
    options = {} if lang == "auto" else {"language": lang}
    result = model.transcribe(audio_path, **options)
    return result["text"].strip()


def transcribe(audio_path: str, lang: str) -> str:
    """Try OpenAI API first, fall back to local Whisper."""
    if os.environ.get("OPENAI_API_KEY"):
        try:
            return transcribe_openai_api(audio_path, lang)
        except Exception as e:
            print(f"OpenAI API transcription failed: {e}", file=sys.stderr)

    return transcribe_local_whisper(audio_path, lang)


def main():
    if len(sys.argv) < 3:
        print("Usage: tg_voice.py <bot_token> <file_id> [lang:tr|en|auto]", file=sys.stderr)
        sys.exit(1)

    token = sys.argv[1]
    file_id = sys.argv[2]
    lang = sys.argv[3] if len(sys.argv) > 3 else "tr"

    audio_path = download_file(token, file_id)
    try:
        text = transcribe(audio_path, lang)
        print(text)
    finally:
        try:
            os.unlink(audio_path)
        except OSError:
            pass


if __name__ == "__main__":
    main()
