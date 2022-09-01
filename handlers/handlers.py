from aiogram import types
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from loader import dp, bot
from config_data.resources import msgs
from config_data.config import AUDIO_DIR
from utils.youtube import get_audio
from keyboards import kb_commands
from states.bot_states import BotState


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    locale = message.from_user.language_code.lower()
    msg = msgs[locale].WELCOME.format(message.from_user.full_name)
    await bot.send_message(message.chat.id, msg, reply_markup=kb_commands)


@dp.message_handler(commands=["help"])
async def chelp(message: types.Message):
    locale = message.from_user.language_code.lower()
    msg = "\n".join(["{0} - {1}".format(key, val) for key, val in msgs[locale].COMMANDS.items()])
    await bot.send_message(message.chat.id, msg)


@dp.message_handler(commands=["audio"])
async def audio(message: types.Message):
    locale = message.from_user.language_code.lower()
    msg = msgs[locale].AUDIO_MODE
    await BotState.url_audio.set()
    await bot.send_message(message.chat.id, msg, reply_markup=ReplyKeyboardRemove())


@dp.message_handler(content_types=["text",])
async def audio_url(message: types.Message):
    url = message.text
    uid = message.chat.id
    file = get_audio(url, AUDIO_DIR, uid)
    with open(file, "rb") as audio:
        await bot.send_audio(message.chat.id, audio)
