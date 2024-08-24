# from aiogram import types
# from aiogram.dispatcher import FSMContext
#
# from handlers.users.handlers.registration import register_information
# from handlers.users.states import UserState
# from loader import dp
#
#
# @dp.callback_query_handler(state=UserState.update_information)
# async def update(call: types.CallbackQuery, state: FSMContext):
#     await update_information(call, state)
#
#
# async def update_information(call: types.CallbackQuery, state: FSMContext):
#     data = await state.get_data()
#     # is_user_registered = data.get("is_user_registered")
#
#     is_user_registered = False
#     if is_user_registered:
#         #TODO authorize with database
#         register_data: dict = data.get("register_data")
#     else:
#         register_data: dict = data.get("register_data")
#
#     register_data.pop(call.data)
#
#     await state.set_state(UserState.registration.state)
#     await register_information(message=call.message, state=state, is_information=False)
#
