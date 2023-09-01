from loguru import logger
from .connector import DatabaseConnector
from source.utils.models import User
from datetime import datetime


class Selector(DatabaseConnector):
    def __init__(self) -> None:
        super().__init__()
        logger.debug("Selector object was initialized")

    async def get_user_by_id(self, user_id: int) -> User:
        (
            username,
            is_banned,
            subscription_end_date,
            created_at,
        ) = await self._get_user_base_info_by_id(user_id)
        if not created_at:
            raise ValueError(f"User {user_id} not found")
        created_configs_count = await self._get_created_configs_count_by_user_id(
            user_id
        )
        bonus_configs_count = await self._get_bonus_configs_count_by_user_id(user_id)
        default_configs_count = 2
        unused_configs_count = (
            default_configs_count + bonus_configs_count - created_configs_count
        )
        is_active_subscription: bool = subscription_end_date >= datetime.now().date()
        user = User(
            user_id=user_id,
            username=username,
            is_not_banned="🟢" if not is_banned else "🔴",
            is_active_subscription="🟢" if is_active_subscription else "🔴",
            subscription_end_date=subscription_end_date,
            configs_count=created_configs_count,
            bonus_configs_count=bonus_configs_count,
            unused_configs_count=unused_configs_count,
            created_at=created_at,
        )
        return user

    async def _get_user_base_info_by_id(
        self, user_id: int
    ) -> tuple[str, bool, datetime, datetime] | tuple[None, None, None, None]:
        query = f"""--sql
            SELECT username, is_banned, subscription_end_date, created_at
            FROM users
            WHERE user_id = {user_id};
        """
        result = await self._execute_query(query)
        if result == []:
            logger.error(f"User {user_id} not found")
            return None, None, None, None
        username, is_banned, subscription_end_date, created_at = result[0]
        logger.debug(f"User {user_id} base info was fetched")
        return username, is_banned, subscription_end_date, created_at

    async def _get_created_configs_count_by_user_id(self, user_id: int) -> int:
        query = f"""--sql
            SELECT COUNT(*)
            FROM vpn_configs
            WHERE user_id = {user_id};
        """
        result = await self._execute_query(query)
        logger.debug(
            f"Created configs count for user {user_id} was fetched: {result[0][0]}"
        )
        return result[0][0]

    async def _get_bonus_configs_count_by_user_id(self, user_id: int) -> int:
        query = f"""--sql
            SELECT bonus_config_count
            FROM bonus_configs_for_users
            WHERE user_id = {user_id};
        """
        result = await self._execute_query(query)
        logger.debug(f"Bonus configs count for user {user_id} was fetched: {result}")
        return result[0][0] if result else 0
