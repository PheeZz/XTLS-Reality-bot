from aiogram import executor


async def set_commands(dp):
    from aiogram import types

    await dp.bot.set_my_commands(
        commands=[
            types.BotCommand(command="/menu", description="Show main menu"),
            types.BotCommand(command="/pay", description="Show payment methods"),
            types.BotCommand(command="/help", description="Show connection help guide"),
        ]
    )


async def on_startup(dp):
    import time

    from loguru import logger

    from source import handlers, middlewares
    from source.utils.shedulers import SubscriptionChecker

    subscription_checker = SubscriptionChecker()
    middlewares.setup(dp)
    await set_commands(dp)
    handlers.setup(dp)

    logger.add(
        f'logs/{time.strftime("%Y-%m-%d__%H-%M")}.log',
        level="DEBUG",
        rotation="500 MB",
        compression="zip",
    )

    logger.success("[+] Bot started successfully")


if __name__ == "__main__":
    # Launch
    from aiogram import executor

    from source.handlers import dp

    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
