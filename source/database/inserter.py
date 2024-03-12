from loguru import logger

from .connector import DatabaseConnector


class Inserter(DatabaseConnector):
    def __init__(self) -> None:
        super().__init__()
        logger.debug("Inserter object was initialized")

    async def upsert_user(self, user_id: int, username: str):
        if user_id in self.admins_ids:
            query = f"""--sql
                INSERT INTO users (user_id, username, subscription_end_date)
                VALUES ({user_id},'{username}', DATE '2030-01-01')
                ON CONFLICT (user_id)
                DO UPDATE SET username = '{username}', subscription_end_date = DATE '2030-01-01';
            """
            # on conflict don't update
            admin_bonus_configs_query = f"""--sql
                INSERT INTO bonus_configs_for_users (user_id, bonus_config_count)
                VALUES ({user_id}, 6)
                ON CONFLICT (user_id)
                DO NOTHING;
            """
        else:
            query = f"""--sql
                INSERT INTO users (user_id, username)
                VALUES ({user_id},'{username}')
                ON CONFLICT (user_id)
                DO UPDATE SET username = '{username}';
            """
            admin_bonus_configs_query = None
        await self._execute_query(query)
        if admin_bonus_configs_query:
            await self._execute_query(admin_bonus_configs_query)

        logger.debug(f"User {user_id} was upserted")

    async def insert_new_vpn_config(self, user_id: int, config_name: str, config_uuid: str):
        query = f"""--sql
            INSERT INTO vpn_configs (user_id, config_name, config_uuid)
            VALUES ({user_id}, '{config_name}','{config_uuid}');
        """
        await self._execute_query(query)
        logger.debug(f"VPN config {config_uuid} was inserted")

    async def upsert_new_bonus_config_count_for_user(self, user_id: int, count: int):
        query = f"""--sql
            INSERT INTO bonus_configs_for_users (user_id, bonus_config_count)
            VALUES ({user_id}, {count})
            ON CONFLICT (user_id)
            DO UPDATE SET count = {count};
        """
        await self._execute_query(query)
        logger.debug(f"Bonus config count for user {user_id} was upserted: {count}")
