from aiogram.dispatcher.filters.state import StatesGroup, State


class UploadPictureState(StatesGroup):
    name = State()
    country_of_shooting = State()
    team = State()
    links = State()






