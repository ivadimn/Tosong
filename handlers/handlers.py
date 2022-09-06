from aiogram import types
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from loader import dp, bot
from config_data.resources import msgs
from config_data.config import AUDIO_DIR
from utils.youtube import get_audio, is_url_valid
from keyboards import kb_commands
from states.bot_states import BotState
from errors.errors import BadUrlError


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




