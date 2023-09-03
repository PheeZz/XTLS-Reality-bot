from loguru import logger
from .connector import DatabaseConnector


class Deleter(DatabaseConnector):
    def __init__(self) -> None:
        super().__init__()
        logger.debug("Deleter object was initialized")

    async def delete_one_vpn_config_by_uuid(self, uuid: str) -> None:
        query = f"""--sql
            DELETE FROM vpn_configs
            WHERE uuid = '{uuid}';
        """
        await self._execute_query(query)
        logger.debug(f"VPN config {uuid} was deleted")

    async def delete_many_vpn_configs_by_uuids(self, uuids: list[str]) -> None:
        query = f"""--sql
            DELETE FROM vpn_configs
            WHERE uuid IN ({", ".join([f"'{uuid}'" for uuid in uuids])});
        """
        await self._execute_query(query)
        logger.debug(f"VPN configs {uuids} were deleted")
