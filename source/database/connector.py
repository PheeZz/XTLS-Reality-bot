import os

import asyncpg
from loguru import logger

from source.data import Configuration


class DatabaseConnector(Configuration):
    def __init__(self) -> None:
        super().__init__()
        logger.debug("Database connector object was created")

    async def _create_connection(self) -> asyncpg.connection.Connection:
        try:
            conn = await asyncpg.connect(**self.database_connection_parameters)
        except asyncpg.exceptions.InvalidCatalogNameError:
            logger.error(
                f"Database {self.database_connection_parameters.get('database')} not found, creating new one..."
            )
            self._create_database()
            conn = await asyncpg.connect(**self.database_connection_parameters)
        logger.debug(
            f"Connection to {self.database_connection_parameters.get('database')} database established"
        )
        return conn

    def _create_database(self):
        db_user = self.database_connection_parameters.get("user")
        db_name = self.database_connection_parameters.get("database")

        os.system(
            f"sudo -u postgres psql -c 'CREATE DATABASE {self.database_connection_parameters.get('database')}'"
        )
        logger.debug(f"Database {db_name} was created")
        # grant all privileges on database {db_name} to {db_user};
        os.system(
            f"sudo -u postgres psql -c 'GRANT ALL PRIVILEGES ON DATABASE {db_name} TO {db_user}'"
        )
        logger.debug(f"Privileges on database {db_name} were granted")

    async def _execute_query(self, query: str, *args) -> list[asyncpg.Record] | bool:
        """Executes query and returns result or None if error occurred

        Args:
            query (str): SQL query to execute
            *args (tuple): arguments for query

        Returns:
            list[asyncpg.Record] | None: result of query execution
        """
        conn = await self._create_connection()

        try:
            result = await conn.fetch(query, *args)
        except asyncpg.exceptions.PostgresError as e:
            logger.error(f"Error while executing query: {e.__class__.__name__} {e}")
            logger.error(f"Query: {query}")
            return False

        finally:
            await conn.close()

        return result

    async def _execute_query_with_returning_one(self, query: str, *args) -> asyncpg.Record | bool:
        """Executes query and returns first row of result or None if error occurred

        Args:
            query (str): SQL query to execute
            *args (tuple): arguments for query

        Returns:
            list[asyncpg.Record] | None: result of query execution
        """
        conn = await self._create_connection()

        try:
            result = await conn.fetchrow(query, *args)
        except asyncpg.exceptions.PostgresError as e:
            logger.error(f"Error while executing query: {e.__class__.__name__} {e}")
            logger.error(f"Query: {query}")
            return False
        finally:
            await conn.close()

        return result
