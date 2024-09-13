<h1 align="center">PheeZz's XTLS-Reality bot</h1>
<p align="center">
<img src = "https://github.com/PheeZz/XTLS-Reality-bot/blob/main/source/data/img/logo/logo_wide.png?raw=true" width = 80%>
</p>

<div align = "center">

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Packaged with Poetry](https://img.shields.io/badge/packaging-poetry-cyan.svg)](https://python-poetry.org/)</br>
[![!Ubuntu](https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)](https://ubuntu.com/)
[![!Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![!PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![!Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)](https://telegram.org/)
[![!Xray](https://img.shields.io/badge/Xray-000000?style=for-the-badge&logo=xray&logoColor=white)](https://xtls.github.io/)
[![XTLS](https://img.shields.io/badge/XTLS-000000?style=for-the-badge&logo=xray&logoColor=white)](https://xtls.github.io/)

</div>

## ❗️Attention: project unmaintained. Please do not use it to bypass your country blocks.


## Tested on
- Ubuntu 22.04 LTS
> RAM: 2GB <br>
> CPU core: 1 <br>
> Storage: 30GB

- Ubuntu 20.04 LTS
> RAM: 2GB <br>
> CPU core: 2 <br>
> Storage: 40GB

## Installation methods
### 1. Using `autoinstall.sh` script (recommended)
```bash
wget https://raw.githubusercontent.com/PheeZz/XTLS-Reality-bot/main/autoinstall.sh && chmod +x autoinstall.sh && ./autoinstall.sh
```

### 2. Manual

#### 2.1 First of all - install dependencies
> git, curl, postgres
```bash
sudo apt install -y git curl postgresql postgresql-contrib
systemctl start postgresql.service
```
> python 3.11, pip, poetry
```bash
sudo apt install -y software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install -y python3.11 python3.11-dev python3.11-distutils python3.11-venv
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3.11 get-pip.py
pip3.11 install poetry
```

> XRAY (or you can install it with not default options, follow [this guide](https://github.com/XTLS/Xray-install))
```bash
bash -c "$(curl -L https://github.com/XTLS/Xray-install/raw/main/install-release.sh)" @ install
```

#### 2.2 Get keypair and shortid

##### 2.2.1 Private and public keys
```bash
/usr/local/bin/xray x25519
```
> Output will be something like:
```text
Private key: CJcqQtcklhCMfiFW8A4BA0XsgKmRJk4-_l42bpnVn0I
Public key: JjAXPY-s2FkvVypfGN2c71NQsCW489Vxjtayo6hLmVM
```

##### 2.2.2 Get shortid
```bash
openssl rand -hex 8
```
> Output will be something like:
```text
0ed36d458733a0bc
```
#### 2.3 Configure XRAY config.json file
> Path: `/usr/local/etc/xray/config.json`
<details>
   <summary><code>config.json</code></summary>

```json
{
    "log": {
        "loglevel": "info"
    },
    "routing": {
        "rules": [],
        "domainStrategy": "AsIs"
    },
    "inbounds": [
        {
            "port": 443,
            "protocol": "vless",
            "tag": "vless_tls",
            "settings": {
                "clients": [],
                "decryption": "none"
            },
            "streamSettings": {
                "network": "tcp",
                "security": "reality",
                "realitySettings": {
                    "show": false,
                    "dest": "dl.google.com:443",
                    "xver": 0,
                    "serverNames": [
                        "dl.google.com"
                    ],
                    "privateKey": "<your private key>",
                    "minClientVer": "",
                    "maxClientVer": "",
                    "maxTimeDiff": 0,
                    "shortIds": [
                        "<your short id>"
                    ]
                }
            },
            "sniffing": {
                "enabled": true,
                "destOverride": [
                    "http",
                    "tls"
                ]
            }
        }
    ],
    "outbounds": [
        {
            "protocol": "freedom",
            "tag": "direct"
        },
        {
            "protocol": "blackhole",
            "tag": "block"
        }
    ]
}

```
</details>

> restart xray service
```bash
systemctl restart xray.service
```
#### 2.4 Optional (!) confugure BBR
To increase performance, you can configure Bottleneck Bandwidth and
Round-trip propagation time (BBR) congestion control algorithm on the server
```bash
echo "net.core.default_qdisc=fq" >> /etc/sysctl.conf
echo "net.ipv4.tcp_congestion_control=bbr" >> /etc/sysctl.conf
sysctl -p
```
#### 2.5 Create postgresql user and database

>enter psql shell
```bash
sudo -u postgres psql
```

>create user and database
```sql
CREATE DATABASE <database_name>;
CREATE USER <user_name> WITH PASSWORD '<password>';
GRANT ALL PRIVILEGES ON DATABASE <database_name> TO <user_name>;
GRANT ALL ON ALL TABLES IN SCHEMA "public" TO <user_name>;
```

> in case of some errors with permission you can make user superuser
```sql
ALTER USER <user_name> WITH SUPERUSER;
```
> exit psql shell
```
\q
```

#### 2.5 Clone this repo
```bash
git clone https://github.com/PheeZz/XTLS-Reality-bot.git
```

#### 2.6 Create venv and install python dependencies
```bash
cd XTLS-Reality-bot
poetry install --no-root
```

#### 2.7 Configure .env file
```bash
nano source/data/.env
```

```ini
#telegram bot token
TG_BOT_TOKEN = "<token>"
#your bank card number, if you will use payments with "handmade" method
PAYMENT_CARD = "<card in string format>"
#your telegram id, you can get it from @userinfobot or @myidbot or @RawDataBot
ADMINS_IDS = "<id/ids>"
#any text you want to show in the start of every peer config file (for example in case MYVPN_Phone.conf - "MYVPN" is prefix)
CONFIGS_PREFIX = "XrayPheeZzVPN"

#how much subscription costs. example: "100₽", "10$"
BASE_SUBSCRIPTION_MONTHLY_PRICE = "100₽"

DB_NAME = "<your db name>"
DB_USER = "<your db user name>"
DB_USER_PASSWORD = "<your db user password>"
#database host, default localhost
DB_HOST = "localhost"
#database port, default 5432
DB_PORT = "5432"

XRAY_CONFIG_PATH = "/usr/local/etc/xray/config.json"
XRAY_PUBLICKEY = "<public key from step 2.2.1>"
XRAY_SHORTID = "<short id from step 2.2.1>"
XRAY_SNI = "dl.google.com"
#default max configs count for each user (admin can give bonus configs to any user through admin panel)
USER_DEFAULT_MAX_CONFIGS_COUNT = "2"
```

#### 2.8 Create database tables
```bash
$(poetry env info --executable) create_database_tables.py
```

#### 2.9 Create .service file for your bot
```bash
nano /etc/systemd/system/xtls-reality-bot.service
```
```ini
[Unit]
Description=XTLS-Reality telegram bot
After=network.target

[Service]
Type=simple
User=root
ExecStart=/bin/bash -c 'cd ~/XTLS-Reality-bot/ && $(poetry env info --executable) app.py'
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

#### 2.10 Enable and start it
```bash
systemctl enable xtls-reality-bot.service
systemctl start xtls-reality-bot.service
```
