# VseMangaBot

[![wakatime](https://wakatime.com/badge/github/vsecoder/VseMangaBot.svg)](https://wakatime.com/badge/github/vsecoder/VseMangaBot)
![Telegram](https://img.shields.io/badge/Telegram-blue?style=flat&logo=telegram)
[![DeepSource](https://deepsource.io/gh/vsecoder/VseMangaBot.svg/?label=active+issues&show_trend=true&token=tEWO-7pQW5lP2AsQq9tNLIK1)](https://deepsource.io/gh/vsecoder/VseMangaBot/?ref=repository-badge)
[![CodeFactor](https://www.codefactor.io/repository/github/vsecoder/VseMangaBot/badge)](https://www.codefactor.io/repository/github/vsecoder/VseMangaBot)
![CodeStyle](https://img.shields.io/badge/code%20style-black-black)
![PythonVersions](https://img.shields.io/pypi/pyversions/aiogram)

## [bot](https://t.me/VseMangaBot)

## Features

* ![aiogram 3](https://img.shields.io/badge/dev--3.x-aiogram-blue) as a main library
* ![tortoise](https://img.shields.io/badge/last-tortoise-yellow) as ORM

## Run bot

### Dev

```bash
git clone https://github.com/vsecoder/VseMangaBot.git
cd VseMangaBot
python3 -m venv manga
source manga/bin/activate
pip install -r requirements.txt
cp example.toml config.toml
nano config.toml # <= edit config (token, admins, etc.)
python3 -m app
```

### Prod

```bash
git clone https://github.com/vsecoder/VseMangaBot.git
cd VseMangaBot
nano config.toml #  <= edit config (token, admins, etc.)
```

```bash
python3 -m venv manga
source manga/bin/activate
pip3 install -r requirements.txt

sudo nano /etc/systemd/system/manga.service
```

Enter this:

```
Description=VseMangaBot
[Service]
WorkingDirectory=/home/<USERNAME>/VseMangaBot
nvironment=PYTHONPATH=/home/<USERNAME>/VseMangaBot
ExecStart=/home/<USERNAME>/VseMangaBot/manga/bin/python3 -m app
Type=simple
Restart=always
RestartSec=1
User=<USERNAME>
[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable manga
sudo systemctl start manga # <= start bot
sudo systemctl status manga # <= get status

sudo systemctl start manga # <= stop bot
```