from loguru import logger
from .connector import DatabaseConnector


class Inserter(DatabaseConnector):
    def __init__(self) -> None:
        super().__init__()
        logger.debug("Inserter object was initialized")

    async def upsert_new_user(self, user_id: int, username: str):
        query = f"""--sql
            INSERT INTO users (user_id, username)
            VALUES ({user_id},'{username}')
            ON CONFLICT (user_id)
            DO UPDATE SET username = '{username}';
        """
        await self._execute_query(query)
        logger.debug(f"User {user_id} was upserted")

    async def insert_new_vpn_config(
        self, user_id: int, config_name: str, config_uuid: str
    ):
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
