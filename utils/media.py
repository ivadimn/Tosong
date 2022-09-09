from typing import Any, Optional, Callable
from moviepy.editor import *
from pytube import YouTube
from aiogram.types import Message
from abc import ABC, abstractmethod
import sys
import os


class Media(ABC):

    def __init__(self, url: str, message: Message, callback: Optional[Callable]) -> None:
        self.url = url
        self.message = message
        self.callback = callback

    def on_progress(self,obj: Any,  buffer: bytes, count: int) -> None:
        msg = "Осталось... {0} байт".format(count)
        #self.callback(self.message, msg)
        sys.stdout.write('\rОсталось...[%10d] байт' % count)
        sys.stdout.flush()

    def on_complete(self, obj: Any, msg: str) -> None:
        print("\n{0} - was loaded!!".format(msg))

    @abstractmethod
    def get(self, path: str, uid: int) -> str: ...

    @abstractmethod
    def save(self, path: str, uid: int, file_name: str) -> str: ...


class Audio(Media):

    def __init__(self, url: str, message: Message, callback: Optional[Callable]) -> None:
        super().__init__(url, message, callback)

    def get(self, path: str, uid: int) -> str:
        abs_path = os.path.join(os.path.abspath(os.path.curdir), path)
        if not os.path.exists(abs_path):
            os.mkdir(abs_path)
        yt = YouTube(self.url, on_complete_callback = self.on_complete, on_progress_callback = self.on_progress)
        audio_streams = yt.streams.get_audio_only()
        print("Loading {0}...".format(audio_streams.title))
        audio_streams.download(abs_path, "audio-{0}.mp4".format(uid))
        return self.save(abs_path, uid, audio_streams.default_filename)

    def save(self, path: str, uid: int, file_name: str) -> str:
        audio = AudioFileClip(os.path.join(path, "audio-{0}.mp4".format(uid)))
        file_name = file_name.replace("mp4", "mp3")
        full_name = os.path.join(path, file_name)
        audio.write_audiofile(full_name)
        audio.close()
        print("{0} was saved".format(file_name))
        os.remove(os.path.join(path, "audio-{0}.mp4".format(uid)))
        return full_name
