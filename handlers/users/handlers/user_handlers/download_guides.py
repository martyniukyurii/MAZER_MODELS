from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InputFile

from handlers.users.start_functions_and_start_filters import login_start

from data.config import lang
from handlers.users.states import UserState
from loader import dp
import os


@dp.callback_query_handler(lambda c: c.data == "DownloadGuidesButton")
async def download_guides_handler(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(UserState.download_guides.state)
    await call.message.delete()
    await download_guides(call.message, state)


@dp.message_handler(state=UserState.download_guides)
async def download_guides(message: types.Message, state: FSMContext):
    data = await state.get_data()
    language = data.get("language")
    l10 = lang.get(language).get("download_our_guides")

    guides_folder = f"./guides/{language}"  # Папка с посібниками. Приклад: ./folder_name/ukr, ./folder_name/eng

    await message.answer(l10.get("text"))

    if os.path.exists(guides_folder) and os.path.isdir(guides_folder):
        files = os.listdir(guides_folder)

        if not files:
            await message.answer(l10.get("error"))
        else:
            for file_name in files:
                file_path = os.path.join(guides_folder, file_name)

                if os.path.isfile(file_path):
                    await message.answer_document(document=InputFile(file_path))
    else:
        await message.answer(l10.get("error"))

    await login_start(message, state)
