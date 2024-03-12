import json
import os
from copy import deepcopy

import aiofiles
from loguru import logger

from loader import db_manager
from source.data import config

from .credentials_generator import CredentialsGenerator


class XrayConfiguration:
    def __init__(self):
        self._config_path = config.xray_config_path
        self._server_ip_and_port = f"{config.server_ip}:443"
        self._config_prefix = config.user_config_prefix

    async def _load_server_config(self) -> dict:
        """Load server config from file

        Returns:
            dict: server config in dict format (json)
        """
        async with aiofiles.open(self._config_path, "r") as f:
            config: dict = json.loads(await f.read())
        return config

    async def _save_server_config(self, config: dict):
        """Save server config to file

        Args:
            config (dict): server config in dict format (json)
        """
        async with aiofiles.open(self._config_path, "w") as f:
            dumped_json_config = json.dumps(config, indent=4)
            await f.write(dumped_json_config)

    async def _restart_xray(self):
        """Restart xray service"""
        os.system("systemctl restart xray")

    async def add_new_user(self, config_name: str, user_telegram_id: int) -> str:
        """Add new user to xray server config

        Returns:
            str: user config as link string
        """
        credentials = CredentialsGenerator().generate_new_person(user_telegram_id=user_telegram_id)
        config = await self._load_server_config()
        updated_config = deepcopy(config)
        updated_config["inbounds"][0]["settings"]["clients"].append(credentials)
        try:
            await self._save_server_config(updated_config)
            await self._restart_xray()
        except Exception as e:
            logger.error(e)
            await self._save_server_config(config)
            await self._restart_xray()
        else:
            await db_manager.insert_new_vpn_config(
                user_id=user_telegram_id,
                config_name=config_name,
                config_uuid=credentials["id"],
            )
            return await self.create_user_config_as_link_string(
                credentials["id"], config_name=config_name
            )

    async def create_user_config_as_link_string(self, uuid: str, config_name: str) -> str:
        link = (
            f"vless://{uuid}@{self._server_ip_and_port}"
            f"?security=reality"
            f"&sni={config.xray_sni}"
            "&fp=chrome"
            f"&pbk={config.xray_publickey}"
            f"&sid={config.xray_shortid}"
            "&type=tcp"
            "&flow=xtls-rprx-vision"
            "&encryption=none"
            "#"
            f"{self._config_prefix}_{config_name}"
        )
        return link

    async def get_all_uuids(self) -> list[str]:
        config = await self._load_server_config()
        uuids = [client["id"] for client in config["inbounds"][0]["settings"]["clients"]]
        return uuids

    async def disconnect_user_by_uuid(self, uuid: str) -> bool:
        """Disconnect user by uuid

        Args:
            uuid (str): user uuid in xray config

        Returns:
            bool: True if user was disconnected, False if not
        """
        config = await self._load_server_config()
        updated_config = deepcopy(config)
        updated_config["inbounds"][0]["settings"]["clients"] = [
            client
            for client in updated_config["inbounds"][0]["settings"]["clients"]
            if client["id"] != uuid
        ]
        try:
            await self._save_server_config(updated_config)
            await self._restart_xray()
        except Exception as e:
            logger.error(e)
            await self._save_server_config(config)
            await self._restart_xray()
            return False
        else:
            await db_manager.delete_one_vpn_config_by_uuid(uuid=uuid)
            return True

    async def disconnect_many_uuids(self, uuids: list[str]) -> bool:
        """Deletes many configs by uuids

        Args:
            uuids (list[str]): list of users uuids in xray config

        Returns:
            bool: True if users was disconnected, False if not
        """
        config = await self._load_server_config()
        updated_config = deepcopy(config)
        updated_config["inbounds"][0]["settings"]["clients"] = [
            client
            for client in updated_config["inbounds"][0]["settings"]["clients"]
            if client["id"] not in uuids
        ]
        try:
            await self._save_server_config(updated_config)
            await self._restart_xray()
        except Exception as e:
            logger.error(e)
            await self._save_server_config(config)
            await self._restart_xray()
            return False
        else:
            await db_manager.delete_many_vpn_configs_by_uuids(uuids=uuids)
            return True

    async def disconnect_user_by_telegram_id(self, telegram_id: int) -> bool:
        """Disconnect user by telegram id

        Args:
            telegram_id (int): user telegram id

        Returns:
            bool: True if user was disconnected, False if not
        """
        user_configs_uuids = await db_manager.get_user_config_names_and_uuids(user_id=telegram_id)
        if user_configs_uuids:
            uuids = [config.config_uuid for config in user_configs_uuids]
            return await self.disconnect_many_uuids(uuids=uuids)
        else:
            return False
