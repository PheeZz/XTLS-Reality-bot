from dotenv import load_dotenv
from loguru import logger
from os import getenv
import os


class DotEnvVariableNotFound(Exception):
    def __init__(self, variable_name: str):
        self.variable_name = variable_name

    def __str__(self):
        return f"Variable {self.variable_name} not found in .env file"


class Configuration:
    def __init__(self):
        load_dotenv()
        self._bot_token: str = self._get_bot_token()
        self._server_cfg_path: str = self._get_server_cfg_path()
        self._admins_ids: list[int] = self._get_admins_ids()
        self._payment_card: str = self._get_payment_card()
        self._user_config_prefix: str = self._get_user_config_prefix()
        self._subscription_monthly_price: str = self._get_subscription_monthly_price()
        self._database_connection_parameters: dict[
            str, str
        ] = self._get_database_connection_parameters()
        self._xray_publickey: str = self._get_xray_publickey()
        self._xray_shortid: str = self._get_xray_shortid()
        self._xray_config_path: str = self._get_xray_config_path()
        self._server_ip: str = self._get_server_ip()

    def _get_bot_token(self) -> str:
        bot_token = getenv("TG_BOT_TOKEN")
        if not bot_token:
            raise DotEnvVariableNotFound("TG_BOT_TOKEN")
        return bot_token

    def _get_server_cfg_path(self) -> str:
        server_cfg_path = getenv("SERVER_CFG_PATH")
        if not server_cfg_path:
            raise DotEnvVariableNotFound("SERVER_CFG_PATH")
        return server_cfg_path

    def _get_admins_ids(self) -> list[int]:
        admins_ids = getenv("ADMINS_IDS")
        if not admins_ids:
            raise DotEnvVariableNotFound("ADMINS_IDS")
        return [int(admin_id) for admin_id in admins_ids.split(",") if admin_id]

    def _get_payment_card(self) -> str:
        payment_card = getenv("PAYMENT_CARD")
        if not payment_card:
            raise DotEnvVariableNotFound("PAYMENT_CARD")
        return payment_card

    def _get_user_config_prefix(self) -> str:
        user_config_prefix = getenv("CONFIGS_PREFIX")
        if not user_config_prefix:
            raise DotEnvVariableNotFound("CONFIGS_PREFIX")
        return user_config_prefix

    def _get_subscription_monthly_price(self) -> str:
        subscription_monthly_price = getenv("BASE_SUBSCRIPTION_MONTHLY_PRICE")
        if not subscription_monthly_price:
            raise DotEnvVariableNotFound("BASE_SUBSCRIPTION_MONTHLY_PRICE")
        return subscription_monthly_price

    def _get_database_connection_parameters(self) -> dict[str, str]:
        for parameter in [
            "DB_HOST",
            "DB_PORT",
            "DB_USER",
            "DB_USER_PASSWORD",
            "DB_NAME",
        ]:
            if not getenv(parameter):
                raise DotEnvVariableNotFound(parameter)

        return {
            "host": getenv("DB_HOST"),
            "port": getenv("DB_PORT"),
            "user": getenv("DB_USER"),
            "password": getenv("DB_USER_PASSWORD"),
            "database": getenv("DB_NAME"),
        }

    def _get_xray_publickey(self) -> str:
        xray_publickey = getenv("XRAY_PUBLICKEY")
        if not xray_publickey:
            raise DotEnvVariableNotFound("XRAY_PUBLICKEY")
        return xray_publickey

    def _get_xray_shortid(self) -> str:
        xray_shortid = getenv("XRAY_SHORTID")
        if not xray_shortid:
            raise DotEnvVariableNotFound("XRAY_SHORTID")
        return xray_shortid

    def _get_xray_config_path(self) -> str:
        xray_config_path = getenv("XRAY_CONFIG_PATH")
        if not xray_config_path:
            raise DotEnvVariableNotFound("XRAY_CONFIG_PATH")
        return xray_config_path

    def _get_server_ip(self) -> str:
        server_ip = os.popen("curl ifconfig.me").read().strip()
        if not server_ip:
            raise RuntimeError(
                "Server ip not found. Check your internet connection and curl package installation"
            )

    @property
    def bot_token(self) -> str:
        return self._bot_token

    @property
    def server_cfg_path(self) -> str:
        return self._server_cfg_path

    @property
    def admins_ids(self) -> list[int]:
        return self._admins_ids

    @property
    def payment_card(self) -> str:
        return self._payment_card

    @property
    def user_config_prefix(self) -> str:
        return self._user_config_prefix

    @property
    def subscription_monthly_price(self) -> str:
        return self._subscription_monthly_price

    @property
    def database_connection_parameters(self) -> dict[str, str]:
        return self._database_connection_parameters

    @property
    def xray_publickey(self) -> str:
        return self._xray_publickey

    @property
    def xray_shorid(self) -> str:
        return self._xray_shortid

    @property
    def xray_config_path(self) -> str:
        return self._xray_config_path

    @property
    def server_ip(self) -> str:
        return self._server_ip
