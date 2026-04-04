#!/usr/bin/env python3
"""Voice message transcription via local Whisper or whisper.cpp"""
import sys, os, subprocess, shutil, tempfile

def transcribe(audio_path: str, lang: str = "tr") -> str:
    # 1. Try openai-whisper (pip install openai-whisper)
    try:
        import whisper
        model = whisper.load_model("base")
        result = model.transcribe(audio_path, language=lang)
        return result["text"].strip()
    except ImportError:
        pass

    # 2. Try whisper.cpp (brew install whisper-cpp)
    for cmd in ["whisper-cpp", "main"]:
        if shutil.which(cmd):
            model_path = os.path.expanduser("~/.whisper/models/ggml-base.bin")
            if os.path.exists(model_path):
                r = subprocess.run(
                    [cmd, "-m", model_path, "-l", lang, "-f", audio_path, "--output-txt"],
                    capture_output=True, text=True, timeout=60
                )
                if r.returncode == 0:
                    txt_path = audio_path + ".txt"
                    if os.path.exists(txt_path):
                        with open(txt_path) as f:
                            return f.read().strip()
                    return r.stdout.strip()

    # 3. Try ffmpeg + OpenAI API (if key available)
    api_key = os.environ.get("OPENAI_API_KEY") or os.environ.get("OPENROUTER_API_KEY", "")
    if api_key and shutil.which("curl"):
        r = subprocess.run([
            "curl", "-s", "-X", "POST",
            "https://api.openai.com/v1/audio/transcriptions",
            "-H", f"Authorization: Bearer {api_key}",
            "-F", f"file=@{audio_path}",
            "-F", "model=whisper-1",
            "-F", f"language={lang}"
        ], capture_output=True, text=True, timeout=30)
        try:
            import json
            return json.loads(r.stdout).get("text", "").strip()
        except Exception:
            pass

    return ""

if __name__ == "__main__":
    audio = sys.argv[1] if len(sys.argv) > 1 else ""
    lang = sys.argv[2] if len(sys.argv) > 2 else "tr"
    if not audio or not os.path.exists(audio):
        print("❌ Ses dosyası bulunamadı")
        sys.exit(1)
    result = transcribe(audio, lang)
    if result:
        print(result)
    else:
        print("⚠️ Transkripsiyon başarısız — whisper kurulu değil: pip install openai-whisper")
        sys.exit(1)
