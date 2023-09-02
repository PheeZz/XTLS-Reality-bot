import os
import json
import aiofiles
from loguru import logger

from .credentials_generator import CredentialsGenerator
from source.data import config
from loader import db_manager
from pprint import pprint
from copy import deepcopy


class XrayConfiguiration:
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
        credentials = CredentialsGenerator().generate_new_person()
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
            return await self.create_user_config_as_link_string(credentials["id"])

    async def create_user_config_as_link_string(self, uuid: str):
        link = (
            f"vless://{uuid}@{self._server_ip_and_port}"
            f"?security=reality"
            "&fp=chrome"
            f"&pbk={config.xray_publickey}"
            f"&sid={config.xray_shortid}"
            "&type=tcp"
            "&flow=xtls-rprx-vision"
            "&encryption=none"
            "#"
            f"{self._config_prefix}_{uuid}"
        )
        return link
