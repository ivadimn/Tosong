import sys
import os
from typing import Any
from urllib.request import urlopen


def on_progress(obj: Any, buffer: bytes, count: int) -> None:
    sys.stdout.write('\rLeft to download...[%10d] bytes' % count)
    sys.stdout.flush()


def on_complete(obj: Any, msg: str) -> None:
    print("\n{0} - was loaded!!".format(msg))


def get_abs_path(path: str) -> str:
    abs_path = os.path.join(os.path.abspath(os.path.curdir), path)
    if not os.path.exists(abs_path):
        os.mkdir(abs_path)
    return abs_path


def is_url_valid(url: str) -> bool:
    try:
        urlopen(url)
        return True
    except Exception:
        return False