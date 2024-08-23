from aiogram.dispatcher.filters.state import StatesGroup, State


class UserState(StatesGroup):
    start = State()
    language = State()
    registration = State()
    update_information = State()
    upload_new_pictures = State()
    download_guides = State()
    set_up_the_call = State()
    ### TODO