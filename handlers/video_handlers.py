from urllib.error import URLError   #повторить без запроса
from aiogram import types
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from loader import dp, bot
from config_data.resources import msgs
from config_data.config import VIDEO_DIR