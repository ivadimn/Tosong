from pytube import YouTube
import ffmpeg
from moviepy.editor import *
import sys
import os


def on_progress(obj, buffer: bytes, count: int) -> None:
    sys.stdout.write('\rОсталось...[%10d] байт' % count)
    sys.stdout.flush()


def on_complete(obj, message: str) -> None:
    print("\n{0} - was loaded!!".format(message))


def get_video(link: str, path: str, uid: int) -> None:
    abs_path = os.path.join(os.path.abspath(os.path.curdir), path)
    if not os.path.exists(abs_path):
        os.mkdir(abs_path)
    try:
        yt = YouTube(link, on_complete_callback=on_complete, on_progress_callback=on_progress)
        video_stream = yt.streams.filter(file_extension="mp4").order_by("resolution").desc().first()
        print("Loading {0}...".format(video_stream.title))
        video_stream.download(abs_path, "video-{0}.mp4".format(uid))
        if not video_stream.is_progressive:
            audio_streams = yt.streams.get_audio_only()
            audio_streams.download(abs_path, "audio-{0}.mp4".format(uid))
            combine(abs_path, uid, video_stream.default_filename)
    except Exception as ex:
        print("Error loading: {0}".format(ex))


def get_audio(link: str, path: str, uid: int) -> str:
    abs_path = os.path.join(os.path.abspath(os.path.curdir), path)
    if not os.path.exists(abs_path):
        os.mkdir(abs_path)
    yt = YouTube(link, on_complete_callback=on_complete, on_progress_callback=on_progress)
    audio_streams = yt.streams.get_audio_only()
    print("Loading {0}...".format(audio_streams.title))
    audio_streams.download(abs_path, "audio-{0}.mp4".format(uid))
    return save_audio(abs_path, uid, audio_streams.default_filename)


def combine(path: str, uid: int, file_name: str) -> None:
    video = ffmpeg.input(os.path.join(path, "video-{0}.mp4".format(uid)))
    audio = ffmpeg.input(os.path.join(path, "audio-{0}.mp4".format(uid)))
    ffmpeg.concat(video, audio, v=1, a=1).output(os.path.join(path, file_name)).run()


def save_audio(path: str, uid: int, file_name: str) -> str:
    audio = AudioFileClip(os.path.join(path, "audio-{0}.mp4".format(uid)))
    file_name = file_name.replace("mp4", "mp3")
    full_name = os.path.join(path, file_name)
    audio.write_audiofile(full_name)
    audio.close()
    print("{0} was saved".format(file_name))
    os.remove(os.path.join(path, "audio-{0}.mp4".format(uid)))
    return full_name
