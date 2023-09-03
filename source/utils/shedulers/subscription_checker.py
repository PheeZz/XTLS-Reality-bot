from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram.utils.exceptions import BotBlocked
from loguru import logger
import asyncio


from loader import db_manager, bot
from source.utils.xray import xray_config
from source.utils import localizer
from source.utils.models import SubscriptionStatus


class SubscriptionChecker:
    def __init__(self):
        self._scheduler = AsyncIOScheduler()
        # start checking subscriptions every day at 00:00
        self._scheduler.add_job(self._check_subscriptions, "cron", hour=0, minute=0)
        self._scheduler.start()
        logger.info("Subscription checker was started...")

    async def _check_subscriptions(self):
        """Check subscriptions and delete expired"""
        logger.info("Checking subscriptions...")
        await self._find_disconnect_and_notify_users_with_expired_subscription()
        await self._find_and_notify_users_with_last_day_left_subscription()
        await self._find_and_notify_users_with_two_days_left_subscription()

    async def _find_disconnect_and_notify_users_with_expired_subscription(self):
        """Find, disconnect and notify users with expired subscription"""
        all_configs_uuid = await xray_config.get_all_uuids()
        expired_configs_uuid = [
            uuid
            for uuid in all_configs_uuid
            if not await db_manager.check_for_user_has_active_subscription_by_config_uuid(
                uuid=uuid
            )
        ]
        await self._disconnect_expired_configs_and_notify_users(
            configs_uuid=expired_configs_uuid
        )

    async def _find_and_notify_users_with_last_day_left_subscription(self):
        """Find and notify users with last day left subscription"""
        users_ids_with_last_day_left_subscription = (
            await db_manager.get_users_ids_with_last_day_left_subscription()
        )
        await self._notify_users_about_subscription_status(
            users_ids=users_ids_with_last_day_left_subscription,
            status=SubscriptionStatus.last_day_left.value,
        )

    async def _find_and_notify_users_with_two_days_left_subscription(self):
        """Find and notify users with two days left subscription"""
        users_ids_with_two_days_left_subscription = (
            await db_manager.get_users_ids_with_two_days_left_subscription()
        )
        await self._notify_users_about_subscription_status(
            users_ids=users_ids_with_two_days_left_subscription,
            status=SubscriptionStatus.two_days_left.value,
        )

    async def _disconnect_expired_configs_and_notify_users(
        self, configs_uuid: list[str]
    ):
        """Disconnect expired configs and notify their owners about it"""
        users_ids_with_expired_subscription = (
            await db_manager.get_users_ids_by_configs_uuids(configs_uuid=configs_uuid)
        )
        await xray_config.disconnect_many_users_by_uuids(uuids=configs_uuid)
        await self._notify_users_about_subscription_status(
            users_ids=users_ids_with_expired_subscription,
            status=SubscriptionStatus.expired.value,
        )

    async def _notify_users_about_subscription_status(
        self, users_ids: list[int], status: str
    ):
        """Notify users about subscription status

        Args:
            users_ids (list[int]): list of users ids to notify
            status (str): subscription status, one of SubscriptionStatus enum values

        Raises:
            ValueError: if status is not one of SubscriptionStatus enum values
        """
        match status:
            case SubscriptionStatus.expired.value:
                message_text = localizer.message.subscription_expired_notification
            case SubscriptionStatus.last_day_left.value:
                message_text = localizer.message.subscription_last_day_left_notification
            case SubscriptionStatus.two_days_left.value:
                message_text = localizer.message.subscription_two_days_left_notification
            case _:
                raise ValueError(f"Unknown subscription status: {status}")
        messages_limits_counter = 0
        for user_id in users_ids:
            try:
                user = (
                    await bot.get_chat_member(chat_id=user_id, user_id=user_id)
                ).user
                await bot.send_message(
                    chat_id=user_id,
                    text=localizer.get_user_localized_text(
                        user_language_code=user.language_code,
                        text_localization=message_text,
                    ).format(user=user.full_name),
                )
            except BotBlocked:
                logger.error(f"Bot was blocked by user {user_id}")
            except Exception as e:
                logger.error(e)
            finally:
                messages_limits_counter += 1
                if messages_limits_counter == 20:
                    await asyncio.sleep(1)
                    messages_limits_counter = 0
