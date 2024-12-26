from aiogram import types
from aiogram.dispatcher import FSMContext

from handlers.users.states import AgentState
from loader import dp


@dp.callback_query_handler(lambda c: c.data == "SendMailingButton")
async def update_information_handler(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(AgentState.send_mailing.state)
