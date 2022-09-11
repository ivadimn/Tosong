from aiogram import types
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from loader import dp, bot
from config_data.resources import msgs
from config_data.config import AUDIO_DIR
from utils.functions import is_url_valid
from keyboards import kb_commands, kb_yes_no_en, kb_yes_no_ru
from states.bot_states import BotState
from utils.media import Audio


@dp.message_handler(commands=["audio"], state="*")
async def audio(message: types.Message):
    locale = message.from_user.language_code.lower()
    msg = msgs[locale].AUDIO_MODE
    await BotState.url_audio.set()
    await bot.send_message(message.chat.id, msg, reply_markup=ReplyKeyboardRemove())


@dp.message_handler(content_types=["text",], state=BotState.url_audio)
async def audio_url(message: types.Message, state: FSMContext):
    url = message.text
    if not is_url_valid(url):
        await url_error_message(message, url)
    else:
        await get(message, state, url)


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


async def url_error_message(message: types.Message, url: str) -> None:
    locale = message.from_user.language_code.lower()
    msg = "{0}\n{1}".format(msgs[locale].BAD_URL.format(url), msgs[locale].REPEAT)
    await BotState.repeat.set()
    if locale == "ru":
        keyb = kb_yes_no_ru
    else:
        keyb = kb_yes_no_en
    await bot.send_message(message.chat.id, msg, reply_markup=keyb)


async def send_error_message(message: types.Message) -> None:
    locale = message.from_user.language_code.lower()
    msg = msgs[locale].STOP_ERROR
    await bot.send_message(message.chat.id, msg, reply_markup=kb_commands)


async def get(message: types.Message, state: FSMContext, url: str) -> None:
    locale = message.from_user.language_code.lower()
    file = ""
    step = 0
    mp3 = Audio(url, AUDIO_DIR, message.chat.id)
    while step < 5:
        try:
            if file == "":
                edit_msg = await bot.send_message(message.chat.id, msgs[locale].PROGRESS)
                file = mp3.get()
                await bot.delete_message(edit_msg.chat.id, edit_msg.message_id)
            await bot.send_message(message.chat.id, msgs[locale].COMPLETE)
            await send_result(message, file)
            await state.reset_data()
        except Exception as ex:
            print(str(ex))
            step += 1
            continue
    else:
        await state.reset_data()
        await send_error_message(message)


async def send_result(message: types.Message, file: str) -> None:
    step = 0
    while step < 10:
        try:
            with open(file, "rb") as a:
                await bot.send_audio(message.chat.id, a, reply_markup=kb_commands)
            break
        except Exception:
            continue
