from utils.set_bot_commands import set_default_commands


async def on_startup(dp):
    import filters
    import middlewares

    filters.setup(dp)
    middlewares.setup(dp)

    from utils.notify_admins import on_startup_notify
    
    from handlers.users.handlers.user_handlers.download_guides import download_guides_handler
    from handlers.users.handlers.user_handlers.set_up_the_call import (set_up_the_call_handler, finish_set_up_the_call)
    from handlers.users.handlers.user_handlers.upload_pictures import upload_new_pictures_handler

    dp.register_callback_query_handler(download_guides_handler, lambda c: c.data == "DownloadGuidesButton")
    dp.register_callback_query_handler(set_up_the_call_handler, lambda c: c.data == "SetUpTheCallButton")
    dp.register_callback_query_handler(finish_set_up_the_call, lambda c: c.data in ["AgentButton", "OwnerButton"])
    dp.register_callback_query_handler(upload_new_pictures_handler, lambda c: c.data == "UploadNewPicturesButton")


    await on_startup_notify(dp)
    await set_default_commands(dp)


if __name__ == "__main__":
    from aiogram import executor
    from handlers import dp

    executor.start_polling(dp, on_startup=on_startup)
