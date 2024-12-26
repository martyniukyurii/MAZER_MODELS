import os
import re

import flag
import pycountry
from aiogram import types
from aiogram.dispatcher import FSMContext
from googleapiclient.http import MediaFileUpload


from data.config import lang
from handlers.users.states import UserState
from keyboards.default.keyboard import create_keyboard_from_dict
from keyboards.inline.inline_keyboard import create_inline_keyboard_from_dict
from handlers.users.start_functions_and_start_filters import login_start
from data.config import drive_service, TEMP_DIR
from loader import dp


@dp.callback_query_handler(lambda c: c.data == "UploadNewPicturesButton")
async def upload_new_pictures_handler(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(UserState.upload_new_pictures.state)
    await call.message.delete()
    await call.message.answer("Please, upload your pictures.")
    # await upload_pictures_handler(call.message, state)


@dp.message_handler(
    state=UserState.upload_new_pictures,
    # content_types=[types.ContentType.PHOTO, types.ContentType.TEXT],
    content_types=[types.ContentType.PHOTO],
)
async def upload_pictures_handler(message: types.Message, state: FSMContext):
    # await upload_pictures(message, state)
    await upload_photos_to_drive(message, state)


# async def upload_pictures(message: types.Message, state: FSMContext):
#     data = await state.get_data()
#     l10 = (
#         lang.get(data.get("language"))
#         .get("upload_new_pictures")
#         .get("uploading_steps")
#     )
#     common_keys = [key for key in l10.keys()]
#     for key in common_keys:
#         pattern = l10.get(key).get("regex")
#         text = message.text

#         if key == "Q_pictures":
#             text = message.photo[-1].file_id


#         if re.match(pattern, text):
#             await message.answer(l10.get(key).get("success"))
#             continue
#         else:
#             await message.answer(l10.get(key).get("error"))
#             break


async def upload_photos_to_drive(message: types.Message, state: FSMContext):
    data = await state.get_data()
    register_data: dict = data.get("register_data")
    user_full_name = register_data.get("B_full_name")

    folder_id = get_or_create_user_folder(user_full_name)
    
    # if message.media_group_id:
    #     highest_resolution_photos = [photo[-1] for photo in message.photo]
    # else:
    #     highest_resolution_photos = [message.photo[-1]]
        
    photo = message.photo[-1]
    file_id = photo.file_id
    file_info = await message.bot.get_file(file_id)
    file_path = file_info.file_path
    local_file_path = os.path.join(TEMP_DIR, f"{file_id}.jpg")
    await message.bot.download_file(file_path, local_file_path)

    try:
        upload_file_to_drive(folder_id, local_file_path, f"{file_id}.jpg")
    finally:
        os.remove(local_file_path)

    await login_start(message, state)


def get_telegram_bot_folder():
    response = (
        drive_service.files()
        .list(
            q="mimeType='application/vnd.google-apps.folder' and name='telegram-bot'",
            fields="files(id, name)",
        )
        .execute()
    )
    folders = response.get("files", [])
    if folders:
        return folders[0]["id"]
    raise FileNotFoundError("Folder 'telegram-bot' not found on Google Drive")


def create_folder_on_drive(folder_name):
    parent_folder_id = get_telegram_bot_folder()
    file_metadata = {
        "name": folder_name,
        "mimeType": "application/vnd.google-apps.folder",
        "parents": parent_folder_id,
    }
    folder = drive_service.files().create(body=file_metadata, fields="id").execute()
    return folder.get("id")


def get_or_create_user_folder(user_full_name):
    response = (
        drive_service.files()
        .list(
            q=f"mimeType='application/vnd.google-apps.folder' and name='{user_full_name}'",
            fields="files(id, name)",
        )
        .execute()
    )
    folders = response.get("files", [])
    if folders:
        return folders[0]["id"]
    return create_folder_on_drive(user_full_name)


def upload_file_to_drive(folder_id, file_path, file_name):
    print(f"Uploading file: {file_name}")
    print(f"To folder ID: {folder_id}")
    print(f"From path: {file_path}")

    file_metadata = {
        "name": file_name,
        "parents": [folder_id],
    }
    media = MediaFileUpload(file_path, resumable=True)
    uploaded_file = (
        drive_service.files()
        .create(body=file_metadata, media_body=media, fields="id")
        .execute()
    )
    file_id = uploaded_file.get("id")
    print(f"Uploaded file ID: {file_id}")
    return file_id
