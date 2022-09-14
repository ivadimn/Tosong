from aiogram import types
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from loader import dp, bot
from config_data.resources import msgs
from config_data.config import AUDIO_DIR
from utils.functions import is_url_valid
from keyboards import kb_commands, kb_yes_no
from states.bot_states import BotState
from utils.media import Audio


@dp.message_handler(commands=["audio"], state="*")
async def audio(message: types.Message, state: FSMContext):
    locale = message.from_user.language_code.lower()
    msg = msgs[locale].AUDIO_MODE
    await state.update_data(locale=locale, id=message.chat.id)
    await BotState.url_audio.set()
    await bot.send_message(message.chat.id, msg, reply_markup=ReplyKeyboardRemove())


@dp.message_handler(content_types=["audio", "document"], state="*")
async def audio_url(message: types.Message):
    print(message.audio.file_id)



@dp.message_handler(content_types=["text",], state=BotState.url_audio)
async def audio_url(message: types.Message, state: FSMContext):
    url = message.text
    if not is_url_valid(url):
        await url_error_message(message, url)
    else:
        await state.update_data(url=url, file="")
        await get(state)


# повторить ввод url видео
@dp.message_handler(content_types=["text", ], state=BotState.repeat_input)
async def repeat_input(message: types.Message, state: FSMContext):
    locale = message.from_user.language_code.lower()
    answer = message.text
    if answer.lower() == "yes" or answer.lower() == "да":
        msg = msgs[locale].AUDIO_MODE
        await BotState.url_audio.set()
        await bot.send_message(message.chat.id, msg, reply_markup=ReplyKeyboardRemove())
    else:
        await state.reset_data()
        await bot.send_message(message.chat.id, msgs[locale].SELECT_COMMAND, reply_markup=kb_commands)


@dp.message_handler(content_types=["text", ], state=BotState.repeat_get)
async def repeat_get(message: types.Message, state: FSMContext):
    locale = message.from_user.language_code.lower()
    answer = message.text
    if answer.lower() == "yes" or answer.lower() == "да":
        await BotState.url_audio.set()
        await bot.send_message(message.chat.id, msgs[locale].ANOTHER_ATTEMPT,  reply_markup=ReplyKeyboardRemove())
        await get(state)
    else:
        await state.reset_data()
        await bot.send_message(message.chat.id, msgs[locale].SELECT_COMMAND, reply_markup=kb_commands)


async def url_error_message(message: types.Message, url: str) -> None:
    locale = message.from_user.language_code.lower()
    msg = "{0}\n{1}".format(msgs[locale].BAD_URL.format(url), msgs[locale].REPEAT_INPUT)
    await BotState.repeat_input.set()
    await bot.send_message(message.chat.id, msg, reply_markup=kb_yes_no.get(locale))


async def send_error_message(state: FSMContext) -> None:
    data = await state.get_data()
    locale = data.get("locale")
    chat_id = data.get("id")
    msg = "{0}\n{1}".format(msgs[locale].STOP_ERROR, msgs[locale].REPEAT)
    await BotState.repeat_get.set()
    await bot.send_message(chat_id, msg, reply_markup=kb_yes_no.get(locale))


async def get(state: FSMContext) -> None:
    data = await state.get_data()

    locale = data.get("locale")
    file = data.get("file")
    chat_id = data.get("id")
    url = data.get("url")
    mp3 = Audio(url, AUDIO_DIR, chat_id)
    edit_msg = await bot.send_message(chat_id, msgs[locale].PROGRESS)
    try:
        if file == "":
            file = mp3.get()
        await bot.delete_message(chat_id, edit_msg.message_id)
        await bot.send_message(chat_id, msgs[locale].COMPLETE)
        await send_result(chat_id, file)
        await state.reset_data()
    except Exception as ex:
        print(str(ex))
        await bot.delete_message(chat_id, edit_msg.message_id)
        BotState.repeat_get.set()
        await send_error_message(state)


async def send_result(chat_id: types.Message, file: str) -> None:
    with open(file, "rb") as a:
        await bot.send_audio(chat_id, a, reply_markup=kb_commands)
