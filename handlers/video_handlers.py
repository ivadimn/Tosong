import os
from aiogram import types
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from loader import dp, bot
from config_data.resources import msgs
from config_data.config import AUDIO_DIR
from utils.functions import is_url_valid
from keyboards import kb_commands, kb_yes_no
from states.bot_states import BotState
from utils.media import Video

@dp.message_handler(commands=["audio"], state="*")
async def audio(message: types.Message, state: FSMContext):
    locale = message.from_user.language_code.lower()
    msg = msgs[locale].AUDIO_MODE
    await state.update_data(locale=locale, id=message.chat.id)
    await BotState.url_audio.set()
    await bot.send_message(message.chat.id, msg, reply_markup=ReplyKeyboardRemove())