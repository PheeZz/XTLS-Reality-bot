Red=$'\e[1;31m'
Green=$'\e[1;32m'
Blue=$'\e[1;34m'
Defaul_color=$'\e[0m'
Orange=$'\e[1;33m'
White=$'\e[1;37m'



sudo apt install -y curl
#clear screen after install curl
clear

#get server external ip
server_ip=$(curl -s ifconfig.me)

if [ -z "$server_ip" ]
then
      echo "$Red Can't get server external ip" | sed 's/\$//g'
      echo "$Red Check your internet connection" | sed 's/\$//g'
      echo "$Red Fail on command: curl -s ifconfig.me" | sed 's/\$//g'
      exit 1
fi

clear
echo $Blue | sed 's/\$//g'
echo "This script will install XTLS-Reality telegram bot on your server"
echo "It will install and configure:"
echo $Orange | sed 's/\$//g'
echo "- XRAY (XTLS-Reality)"
echo "- PostgreSQL"
echo "- Python 3.11"
echo "- Poetry"
echo "- Telegram Bot for manage XRAY"
echo $Red | sed 's/\$//g'
echo "............................................................"
echo "...................made by PheeZz..........................."
echo "............................................................"

echo $White | sed 's/\$//g'

echo "Now need to input some data for bot configuration"
echo "You can change it later in ~/XTLS-Reality-bot/data/.env file"
echo ""


#ask for bot token
echo "Enter bot token:"
echo "You can get it from $Blue @BotFather"
read bot_token

#ask user for payment card
echo "$White" | sed 's/\$//g'
echo "Enter payment card number for manual payments:"
echo "Just press ENTER for use default card [$Blue 4242424242424242 $White]" | sed 's/\$//g'
read payment_card
if [ -z "$payment_card" ]
then
      payment_card="4242424242424242"
fi

#ask user for admins ids
echo ""
echo "Enter admins ids (separated by comma):"
echo "Just press ENTER for use default ids [$Blue 123456789, $White]" | sed 's/\$//g'
echo "You can get your id by sending /id command to @userinfobot"
read admins_ids
if [ -z "$admins_ids" ]
then
      admins_ids="123456789,"
fi

#ask user for Database name
echo ""
echo "Enter Database name:"
echo "Just press ENTER for use default name [$Blue xlts_reality_bot $White]" | sed 's/\$//g'
read database_name
if [ -z "$database_name" ]
then
      database_name="xlts_reality_bot"
fi

#ask user for Database user
current_os_user=$(whoami)
echo ""
echo "Enter Database user:"
echo "Just press ENTER for use default user [$Blue $current_os_user $White]" | sed 's/\$//g'
read database_user
if [ -z "$database_user" ]
then
      database_user=$current_os_user
fi

#ask user for Database password
echo ""
echo "Enter Database user password:"
echo "Just press ENTER for use default password [$Blue bestpassword123 $White]" | sed 's/\$//g'
read database_passwd
if [ -z "$database_passwd" ]
then
      database_passwd="bestpassword123"
fi

#ask user for config name prefix
echo ""
echo "Enter config name prefix:"
echo "Just press ENTER for use default prefix [$Blue XrayPheeZzVPN $White]" | sed 's/\$//g'
read config_prefix

if [ -z "$config_prefix" ]
then
      config_prefix="XrayPheeZzVPN"
fi

#ask user for base subscription monthly price
echo ""
echo "Enter base subscription monthly price:"
echo "Just press ENTER for use default price [$Blue 100₽ $White]" | sed 's/\$//g'
read base_subscription_monthly_price

if [ -z "$base_subscription_monthly_price" ]
then
      base_subscription_monthly_price="100₽"
fi

#ask user for max configs count for each user
echo ""
echo "Enter max configs count for each user:"
echo "P.S admin can give more configs to any user from admin panel"
echo "Just press ENTER for use default count [$Blue 2 $White]" | sed 's/\$//g'
read max_configs_count

if [ -z "$max_configs_count" ]
then
      max_configs_count="2"
fi

#ask user for site url to hide reality
echo ""
echo "Enter site url to hide reality:"
echo "Just press ENTER for use default url [$Blue www.microsoft.com $White]" | sed 's/\$//g'
read site_url

if [ -z "$site_url" ]
then
      site_url="www.microsoft.com"
fi

#all neccessary data is collected
echo ""
echo "All neccessary data is collected"
echo "Now script will install all needed software (it can take some time)"
echo "$White" | sed 's/\$//g'
echo "Wanna update system before install? [y/N]"
echo "$Defaul_color" | sed 's/\$//g'
read update_system

if [ "$update_system" = "y" ]
then
      sudo apt update && sudo apt upgrade -y
fi

#install packages
sudo apt install -y git bat tmux mosh postgresql postgresql-contrib
systemctl start postgresql.service

#install python3.11 and pip
sudo apt install -y software-properties-common
add-sudo apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install -y python3.11 python3.11-dev python3.11-distutils python3.11-venv
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3.11 get-pip.py

#install poetry
pip3.11 install poetry


echo "$Orange" | sed 's/\$//g'
echo "Installing XRAY (XTLS-Reality)"
echo "............................................................"
echo "$Defaul_color" | sed 's/\$//g'

#install xray
bash -c "$(curl -L https://github.com/XTLS/Xray-install/raw/main/install-release.sh)" @ install

# To increase performance, you can configure
# Bottleneck Bandwidth and
# Round-trip propagation time (BBR) congestion control algorithm on the server
echo "net.core.default_qdisc=fq" >> /etc/sysctl.conf
echo "net.ipv4.tcp_congestion_control=bbr" >> /etc/sysctl.conf
sysctl -p

#execute /usr/local/bin/xray x25519
#and get public and private keys by splitting lines output and
#remove "Private key: " and "Public key: " from output
#and save it to variables
x25519_keys=$(sudo /usr/local/bin/xray x25519)
x25519_private_key=$(echo "$x25519_keys" | sed -n 1p | sed 's/Private key: //g')
x25519_public_key=$(echo "$x25519_keys" | sed -n 2p | sed 's/Public key: //g')


#get short id by using openssl
short_id=$(sudo openssl rand -hex 8)

#configure xray
sudo cat <<EOF > /usr/local/etc/xray/config.json
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
                    "dest": "$site_url:443",
                    "xver": 0,
                    "serverNames": [
                        "$site_url"
                    ],
                    "privateKey": "$x25519_private_key",
                    "minClientVer": "",
                    "maxClientVer": "",
                    "maxTimeDiff": 0,
                    "shortIds": [
                        "$short_id"
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
EOF

#restart xray
systemctl restart xray.service

#configure postgresql
su postgres -c "psql -c \"CREATE USER $database_user WITH PASSWORD '$database_passwd';\""
su postgres -c "psql -c \"CREATE DATABASE $database_name;\""
su postgres -c "psql -c \"GRANT ALL PRIVILEGES ON SCHEMA public TO $database_user;\""
su postgres -c "psql -c \"GRANT ALL PRIVILEGES ON DATABASE $database_name TO $database_user;\""

#clone bot repo
cd ~
git clone https://github.com/PheeZz/XTLS-Reality-bot.git

#create venv and install bot dependencies
cd XTLS-Reality-bot
poetry install
cd

#configure bot .env file
sudo cat <<EOF > ~/XTLS-Reality-bot/source/data/.env
TG_BOT_TOKEN = "$bot_token"
PAYMENT_CARD = "$payment_card"
ADMINS_IDS = "$admins_ids"
CONFIGS_PREFIX = "$config_prefix"
BASE_SUBSCRIPTION_MONTHLY_PRICE = "$base_subscription_monthly_price"

DB_NAME = "$database_name"
DB_USER = "$database_user"
DB_USER_PASSWORD = "$database_passwd"
DB_HOST = "localhost"
DB_PORT = "5432"

XRAY_CONFIG_PATH = "/usr/local/etc/xray/config.json"
XRAY_PUBLICKEY = "$x25519_public_key"
XRAY_SHORTID = "$short_id"
USER_DEFAULT_MAX_CONFIGS_COUNT = "$max_configs_count"
EOF

#try to run create_database_tables.py if it fails, then give db user superuser privileges
cd ~/XTLS-Reality-bot
$(poetry env info --path)/bin/python3.11 create_database_tables.py || -u postgres psql -c "ALTER USER $database_user WITH SUPERUSER;" && $(poetry env info --path)/bin/python3.11 create_database_tables.py
cd

#create systemd service for bot
sudo cat <<EOF > /etc/systemd/system/xtls-reality-bot.service
[Unit]
Description=XTLS-Reality telegram bot
After=network.target

[Service]
Type=simple
User=$current_os_user
ExecStart=bin/bash -c 'cd ~/XTLS-Reality-bot && $(poetry env info --path)/bin/python3.11 app.py'
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF

#enable and start bot service
systemctl daemon-reload
systemctl enable xtls-reality-bot.service
systemctl start xtls-reality-bot.service


echo "$Green Installation completed successfully" | sed 's/\$//g'
echo "$Defaul_color" | sed 's/\$//g'

echo "$Blue Your .env file losudo cated at $Orange ~/XTLS-Reality-bot/source/data/.env" | sed 's/\$//g'
echo "$Blue Do u want to watch it? [ y / $Blue N $White]" | sed 's/\$//g'
read watch_env_file

if [ "$watch_env_file" = "y" ]
then
      batsudo cat ~/XTLS-Reality-bot/source/data/.env
fi

echo "$Blue Your bot logs losudo cated at $Orange ~/XTLS-Reality-bot/logs/" | sed 's/\$//g'
#thanks for install
echo "$Green Thanks for install" | sed 's/\$//g'
echo "$Defaul_color" | sed 's/\$//g'