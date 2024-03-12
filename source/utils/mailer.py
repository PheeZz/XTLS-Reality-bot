import asyncio

from aiogram import types
from aiogram.utils.exceptions import BotBlocked
from loguru import logger


class Mailer:
    def __init__(
        self,
        message: types.Message,
    ):
        from loader import config
        from source.database import DatabaseManager

        self._unblocked_user_ids = None
        self._message = message
        self._ADMINS = config.admins_ids
        self._db_manager = DatabaseManager()

        logger.success("[+] Mailer coroutine created and started successfully")

    async def _set_unblocked_users(self) -> None:
        self._unblocked_user_ids = await self._db_manager.get_unblocked_users_ids()

    async def run_mailing_post(self) -> None:
        await self._set_unblocked_users()

        mail_counter = 0
        if not self._unblocked_user_ids:
            for admin in self._ADMINS:
                await self._message.bot.send_message(
                    chat_id=admin,
                    text="Не найдено пользователей для рассылки, все пользователи заблокированы",
                )
            return

        for user_id in self._unblocked_user_ids:
            if mail_counter == 20:
                mail_counter = 0
                await asyncio.sleep(1)
            try:
                await self._send_mail(
                    user_id=user_id,
                )
                mail_counter += 1
            except Exception as e:
                logger.error(f"Error occurred during sending mail to user {user_id}: {e}")

    async def echo(self) -> None:
        """Echo message to user for confirmation of mailing message"""
        await self._send_mail(
            user_id=self._message.from_user.id,
        )

    async def _send_mail(
        self,
        user_id: int,
    ):
        try:
            if self._message.photo:
                await self._message.bot.send_photo(
                    chat_id=user_id,
                    photo=self._message.photo[-1].file_id,
                    caption=self._message.caption,
                    caption_entities=self._message.caption_entities,
                )
            elif self._message.video:
                await self._message.bot.send_video(
                    chat_id=user_id,
                    video=self._message.video.file_id,
                    caption=self._message.caption,
                    caption_entities=self._message.caption_entities,
                )
            else:
                await self._message.bot.send_message(
                    chat_id=user_id,
                    text=self._message.text,
                    entities=self._message.entities,
                )
        except BotBlocked:
            logger.error(f"[-] Error while sending message to user {user_id}: user blocked bot")
        except Exception as err:
            logger.error(f"[-] Error while sending message to user {user_id}: {err}")
