from datetime import datetime

from loguru import logger

from source.data import config
from source.utils.models import GlobalStatistics, UserInfo, VpnConfigDB

from .connector import DatabaseConnector


class Selector(DatabaseConnector):
    def __init__(self) -> None:
        super().__init__()
        logger.debug("Selector object was initialized")

    async def get_user_by_id(self, user_id: int) -> UserInfo:
        (
            username,
            is_banned,
            subscription_end_date,
            created_at,
        ) = await self._get_user_base_info_by_id(user_id)
        if not created_at:
            raise ValueError(f"User {user_id} not found")
        created_configs_count = await self._get_created_configs_count_by_user_id(user_id)
        bonus_configs_count = await self._get_bonus_configs_count_by_user_id(user_id)
        unused_configs_count = (
            config.default_max_configs_count + bonus_configs_count - created_configs_count
        )
        is_active_subscription: bool = subscription_end_date >= datetime.now().date()
        user = UserInfo(
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
        logger.debug(f"Created configs count for user {user_id} was fetched: {result[0][0]}")
        return result[0][0]

    async def _get_bonus_configs_count_by_user_id(self, user_id: int) -> int:
        query = f"""--sql
            SELECT bonus_config_count
            FROM bonus_configs_for_users
            WHERE user_id = {user_id};
        """
        result = await self._execute_query(query)
        bonus_configs_count = result[0][0] if result else 0
        logger.debug(f"Bonus configs count for user {user_id} was fetched: {bonus_configs_count}")
        return bonus_configs_count

    async def is_user_registered(self, user_id: int) -> bool:
        query = f"""--sql
            SELECT EXISTS(
                SELECT 1
                FROM users
                WHERE user_id = {user_id}
            );
        """
        result = await self._execute_query(query)
        logger.debug(f"User {user_id} exist: {result[0][0]}")
        return result[0][0]

    async def is_user_have_any_config(self, user_id: int) -> bool:
        query = f"""--sql
            SELECT EXISTS(
                SELECT 1
                FROM vpn_configs
                WHERE user_id = {user_id}
            );
        """
        result = await self._execute_query(query)
        logger.debug(f"User {user_id} have any config: {result[0][0]}")
        return result[0][0]

    async def get_user_config_names_and_uuids(self, user_id: int) -> list[VpnConfigDB] | None:
        query = f"""--sql
            SELECT id, config_name, config_uuid
            FROM vpn_configs
            WHERE user_id = {user_id};
        """
        result = await self._execute_query(query)
        logger.debug(f"User {user_id} configs: {result}")
        if not result:
            return None
        return [
            VpnConfigDB(
                config_id=record[0],
                user_id=user_id,
                config_name=record[1],
                config_uuid=record[2],
            )
            for record in result
        ]

    async def get_count_of_configs_user_can_create(self, user_id: int) -> int:
        bonus_configs_count = await self._get_bonus_configs_count_by_user_id(user_id)
        created_configs_count = await self._get_created_configs_count_by_user_id(user_id)
        unused_configs_count = (
            config.default_max_configs_count + bonus_configs_count - created_configs_count
        )
        logger.debug(f"User {user_id} can create {unused_configs_count} more configs")
        return unused_configs_count

    async def check_for_user_has_active_subscription_by_config_uuid(self, config_uuid: str) -> bool:
        query = f"""--sql
            SELECT EXISTS(
                SELECT 1
                FROM users
                WHERE subscription_end_date >= NOW()::date
                AND user_id = (
                    SELECT user_id
                    FROM vpn_configs
                    WHERE config_uuid = '{config_uuid}'
                )
            );
        """
        result = await self._execute_query(query)
        logger.debug(f"User with uuid {config_uuid} have active subscription: {result[0][0]}")
        return result[0][0]

    async def check_for_user_has_active_subscription_by_user_id(self, user_id: int) -> bool:
        query = f"""--sql
            SELECT EXISTS(
                SELECT 1
                FROM users
                WHERE subscription_end_date >= NOW()::date
                AND user_id = {user_id}
            );
        """
        result = await self._execute_query(query)
        logger.debug(f"User with id {user_id} have active subscription: {result[0][0]}")
        return result[0][0]

    async def get_users_ids_by_configs_uuids(self, configs_uuid: list[str]) -> list[int]:
        """
        Get users ids by configs uuids

            Args:
                configs_uuid (list[str]): list of configs uuids
            Returns:
                list[int]: list of unique users ids
        """
        query = f"""--sql
            SELECT DISTINCT user_id
            FROM vpn_configs
            WHERE config_uuid = ANY(ARRAY{configs_uuid});
        """
        result = await self._execute_query(query)
        if result:
            users_ids = [record[0] for record in result]
        else:
            users_ids = []
        logger.debug(f"Users ids by configs uuids {configs_uuid}: {users_ids}")
        return users_ids

    async def get_users_ids_with_last_day_left_subscription(self) -> list[int]:
        return await self._get_users_ids_by_subscription_ends_in_days(days=1)

    async def get_users_ids_with_two_days_left_subscription(self) -> list[int]:
        return await self._get_users_ids_by_subscription_ends_in_days(days=2)

    async def _get_users_ids_by_subscription_ends_in_days(self, days: int) -> list[int]:
        query = f"""--sql
            SELECT user_id
            FROM users
            WHERE subscription_end_date = NOW()::date + INTERVAL '{days} days';
        """
        result = await self._execute_query(query)
        logger.debug(f"Users ids with {days} days left subscription: {result}")
        return [record[0] for record in result]

    async def get_user_id_by_username(self, username: str) -> int | None:
        query = f"""--sql
            SELECT user_id
            FROM users
            WHERE username = '{username}';
        """
        result = await self._execute_query(query)
        logger.debug(f"User id by username {username}: {result}")
        return result[0][0] if result else None

    async def check_is_user_banned(self, user_id: int) -> bool:
        query = f"""--sql
            SELECT is_banned
            FROM users
            WHERE user_id = {user_id};
        """
        result = await self._execute_query(query)
        is_banned = result[0][0] if result else False
        logger.debug(f"User {user_id} is banned: {is_banned}")
        return is_banned

    async def get_config_name_by_config_uuid(self, config_uuid: str) -> str:
        query = f"""--sql
            SELECT config_name
            FROM vpn_configs
            WHERE config_uuid = '{config_uuid}';
        """
        result = await self._execute_query(query)
        logger.debug(f"Config name by config uuid {config_uuid}: {result[0][0]}")
        return result[0][0]

    async def get_global_stats(self) -> GlobalStatistics:
        query = """--sql
            SELECT
                (SELECT COUNT(*) FROM users) AS users_registered,
                (SELECT COUNT(*) FROM users WHERE is_banned) AS users_banned,
                (SELECT COUNT(*) FROM users WHERE subscription_end_date >= NOW()::date) AS users_with_active_subscription,
                (SELECT COUNT(*) FROM users WHERE subscription_end_date < NOW()::date) AS users_with_expired_subscription,
                (SELECT COUNT(*) FROM users WHERE subscription_end_date = NOW()::date + INTERVAL '1 day') AS users_with_last_day_left_subscription,
                (SELECT COUNT(*) FROM users WHERE subscription_end_date = NOW()::date + INTERVAL '2 days') AS users_with_two_days_left_subscription,
                (SELECT COUNT(*) FROM vpn_configs) AS active_configs_count
        """
        result = await self._execute_query(query)
        global_stats = GlobalStatistics(
            users_registered=result[0][0],
            users_banned=result[0][1],
            users_with_active_subscription=result[0][2],
            users_with_expired_subscription=result[0][3],
            users_with_last_day_left_subscription=result[0][4],
            users_with_two_days_left_subscription=result[0][5],
            active_configs_count=result[0][6],
        )
        logger.debug(f"Global stats: {global_stats}")
        return global_stats
