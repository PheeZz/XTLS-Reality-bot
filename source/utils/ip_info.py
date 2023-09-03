import requests


class IPInfo:
    def __init__(self):
        self._ipfy_url = "https://api.ipify.org?format=json"
        self._ipapi_url = "http://ip-api.com"

    def get_server_ip(self) -> str:
        """Get server ip

        Returns:
            str: server ip
        """
        response = requests.get(self._ipfy_url)
        return response.json()["ip"]

    def get_server_country_name(self) -> str:
        """Get server ip country name

        Returns:
            tuple[str, str]: tuple of country name and
        """
        server_ip = self.get_server_ip()
        response = requests.get(f"{self._ipapi_url}/json/{server_ip}")
        return response.json()["country"]

    def get_server_country_code(self) -> str:
        """Get server ip country code

        Returns:
            str: server ip country code
        """
        server_ip = self.get_server_ip()
        response = requests.get(f"{self._ipapi_url}/json/{server_ip}")
        return response.json()["countryCode"]


if __name__ == "__main__":
    import asyncio

    ip_info = IPInfo()
    print(ip_info.get_server_country_name())
    print(ip_info.get_server_country_code())
    print(ip_info.get_server_ip())
