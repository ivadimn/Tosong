from typing import Any, Optional, Callable
from moviepy.editor import *
from pytube import YouTube
from aiogram.types import Message
from abc import ABC, abstractmethod
from utils.functions import on_progress, on_complete, get_abs_path
import os
import string


class Media(ABC):

    def __init__(self, url: str, path: str, uid: int) -> None:
        self.url = url
        self.abs_path = get_abs_path(path)
        self.uid = uid

    @abstractmethod
    def get(self) -> str: ...

    @abstractmethod
    def save(self, file_name: str) -> str: ...


class Audio(Media):

    def __init__(self, url: str, path: str, uid: int) -> None:
        super().__init__(url, path, uid)

    def get(self) -> str:

        yt = YouTube(self.url, on_complete_callback = on_complete, on_progress_callback = on_progress)
        audio_streams = yt.streams.get_audio_only()
        print("Loading {0}...".format(audio_streams.title))
        audio_streams.download(self.abs_path, "audio-{0}.mp4".format(self.uid))
        return self.save(audio_streams.default_filename)

    def save(self, file_name: str) -> str:
        audio = AudioFileClip(os.path.join(self.abs_path, "audio-{0}.mp4".format(self.uid)))
        file_name = file_name.replace("mp4", "mp3")
        full_name = os.path.join(self.abs_path, file_name)
        audio.write_audiofile(full_name)
        audio.close()
        print("{0} was saved".format(file_name))
        os.remove(os.path.join(self.abs_path, "audio-{0}.mp4".format(self.uid)))
        return full_name


class Video(Media):

    def __init__(self, url: str, path: str, uid: int) -> None:
        super().__init__(url, path, uid)

    def get(self) -> str:
        yt = YouTube(self.url, on_complete_callback=on_complete, on_progress_callback=on_progress)
        print("Loading {0}...".format(yt.title))
        filters = yt.streams.filter(progressive=True, file_extension='mp4')
        filename = yt.title.translate(str.maketrans("", "", string.punctuation))
        filters.get_highest_resolution().download(self.abs_path, filename=filename)
        return os.path.join(self.abs_path, filename)

    def save(self, file_name: str) -> str:
        pass
