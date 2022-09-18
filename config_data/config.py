import os
from dotenv import find_dotenv, load_dotenv

if not find_dotenv():
    exit("Environment variables not loaded, file .env not found")
else:
    load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
AUDIO_DIR = "audios"
VIDEO_DIR = "videos"
COMMANDS = (
    ('start', "Start bot"),
    ('audio', "Load audio track for video from YouTube"),
    ('image', "Image processing"),
    ('help', "Show help")
)
