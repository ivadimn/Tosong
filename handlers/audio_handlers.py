from aiogram import types
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from loader import dp, bot
from config_data.resources import msgs
from config_data.config import AUDIO_DIR
from utils.youtube import get_audio, is_url_valid
from keyboards import kb_commands, kb_yes_no_en, kb_yes_no_ru
from states.bot_states import BotState
from errors.errors import BadUrlError


@dp.message_handler(commands=["audio"])
async def audio(message: types.Message):
    locale = message.from_user.language_code.lower()
    msg = msgs[locale].AUDIO_MODE
    await BotState.url_audio.set()
    await bot.send_message(message.chat.id, msg, reply_markup=ReplyKeyboardRemove())


@dp.message_handler(content_types=["text",], state=BotState.url_audio)
async def audio_url(message: types.Message, state: FSMContext):
    locale = message.from_user.language_code.lower()
    url = message.text
    uid = message.chat.id
    try:
        if not is_url_valid(url):
            raise BadUrlError(msgs[locale].BAD_URL.format(url))
        file = get_audio(url, AUDIO_DIR, uid)

        with open(file, "rb") as a:
            await bot.send_audio(message.chat.id, a, reply_markup=kb_commands)
        await state.reset_data()
    except Exception as ex:
        print(str(ex))
        await send_error_message(message, str(ex))


@dp.message_handler(content_types=["text", ], state=BotState.repeat)
async def repeat(message: types.Message, state: FSMContext):
    locale = message.from_user.language_code.lower()
    answer = message.text
    if answer.lower() == "yes" or answer.lower() == "да":
        msg = msgs[locale].AUDIO_MODE
        await BotState.url_audio.set()
        await bot.send_message(message.chat.id, msg, reply_markup=ReplyKeyboardRemove())
    else:
        await state.reset_data()
        await bot.send_message(message.chat.id, msgs[locale].SELECT_COMMAND, reply_markup=kb_commands)


async def send_error_message(message: types.Message, error_msg: str) -> None:
    locale = locale = message.from_user.language_code.lower()
    msg = "{0}\n{1}".format(error_msg, msgs[locale].REPEAT)
    await BotState.repeat.set()
    if locale == "ru":
        keyb = kb_yes_no_ru
    else:
        keyb = kb_yes_no_en
    await bot.send_message(message.chat.id, msg, reply_markup=keyb)
