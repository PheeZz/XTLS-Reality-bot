import os


class CredentialsGenerator:
    def __init__(self) -> None:
        self._xray_executable_path = "/usr/local/bin/xray"

    def generate_uuid(self) -> str:
        return os.popen(f"{self._xray_executable_path} uuid").read().strip()

    def generate_new_person(self) -> dict[str, str]:
        uuid = self.generate_uuid()
        return {
            "id": uuid,
            "email": f"{uuid}@this_server_vpn",
            "flow": "xtls-rprx-vision",
        }
