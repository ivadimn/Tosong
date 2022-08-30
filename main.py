from youtube import get_video, get_audio

url = "https://www.youtube.com/watch?v=EIxsPBbZ_b8"
VIDEO_DIR = "videos"
AUDIO_DIR = "audios"

if __name__ == '__main__':
    get_audio(url, AUDIO_DIR, 10)


