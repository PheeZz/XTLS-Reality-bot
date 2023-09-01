from loguru import logger
from .connector import DatabaseConnector


class Creator(DatabaseConnector):
    def __init__(self):
        super().__init__()
        logger.debug("Creator object was initialized")

    async def recreate_all_tables(self):
        await self._drop_all_tables()
        await self._create_all_tables()

    async def _create_all_tables(self):
        logger.warning("Creating all tables...")
        await self._create_table_users()
        await self._create_table_vpn_configs()
        await self._create_table_bonus_configs_for_users()
        logger.warning("All tables were created")

    async def _drop_all_tables(self):
        table_names = await self._get_all_table_names()
        logger.warning(f"Tables to drop: {table_names}")
        for table_name in table_names:
            await self._drop_table_cascade(table_name)
        logger.warning("All tables were dropped")

    async def _get_all_table_names(self) -> list[str]:
        query = """--sql
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """
        result = await self._execute_query(query)
        return [record["table_name"] for record in result]

    async def _drop_table_cascade(self, table_name: str):
        query = f"""--sql
            DROP TABLE {table_name} CASCADE;
        """
        await self._execute_query(query)
        logger.debug(f"Table {table_name} was dropped")

    async def _create_table_users(self):
        query = """--sql
            CREATE TABLE users (
                user_id INTEGER PRIMARY KEY NOT NULL,
                username VARCHAR(32) DEFAULT NULL,
                is_banned BOOLEAN NOT NULL DEFAULT FALSE,
                subscription_end_date DATE DEFAULT DATE '1970-01-01',
                created_at TIMESTAMP NOT NULL DEFAULT NOW(),
                updated_at TIMESTAMP NOT NULL DEFAULT NOW()
            );
            """

        if await self._execute_query(query) == []:
            logger.debug("Table users was created")
        else:
            logger.error("Error while creating table users")

    async def _create_table_vpn_configs(self):
        query = """--sql
            CREATE TABLE vpn_configs (
                id SERIAL PRIMARY KEY NOT NULL,
                user_id INTEGER NOT NULL REFERENCES users(user_id),
                config_name VARCHAR(32) NOT NULL,
                config_uuid VARCHAR(64) NOT NULL,
                created_at TIMESTAMP NOT NULL DEFAULT NOW()
            );
            """
        if await self._execute_query(query) == []:
            logger.debug("Table vpn_configs was created")
        else:
            logger.error("Error while creating table vpn_configs")

    async def _create_table_bonus_configs_for_users(self):
        """Table for storing bonus configs count for users.
        It's will be used for users who can generate configs over
        default limit (2 configs per user).
        """
        query = """--sql
            CREATE TABLE bonus_configs_for_users (
                id SERIAL PRIMARY KEY NOT NULL,
                user_id INTEGER NOT NULL REFERENCES users(user_id),
                bonus_config_count INTEGER NOT NULL DEFAULT 0
            );
            """
        if await self._execute_query(query) == []:
            logger.debug("Table bonus_configs_for_users was created")
        else:
            logger.error("Error while creating table bonus_configs_for_users")
