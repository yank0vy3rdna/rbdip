import configparser
import sys
from dataclasses import dataclass
from enum import Enum
from typing import List

from dacite import from_dict


@dataclass
class TgBot:
    token: str
    admin_id: str


@dataclass
class DbBot:
    db_type: str
    db_name: str
    user: str
    password: str
    host: str
    port: str


@dataclass
class YandexBot:
    folder_id: str


@dataclass
class ClickhouseBot:
    host: str
    database: str
    user: str
    port: str
    password: str


@dataclass
class Redis:
    host: str
    port: str
    db: str
    password: str


@dataclass
class Kafka:
    bootstrap_servers: List[str]


class AppType(Enum):
    BOT = "bot"
    WORKER = "worker"


@dataclass
class App:
    type: AppType


@dataclass
class Config:
    tg_bot: TgBot
    db_bot: DbBot
    yandex_bot: YandexBot
    clickhouse: ClickhouseBot
    redis: Redis
    kafka: Kafka
    app: App


path = sys.argv[1] if len(sys.argv) > 1 else "configuration/application.ini"

config_parser = configparser.ConfigParser()
config_parser.read(path)

tg_bot = dict(config_parser.items("TG_BOT"))
tg_bot = from_dict(data_class=TgBot, data=tg_bot)

db_bot = dict(config_parser.items("DB_BOT"))
db_bot = from_dict(data_class=DbBot, data=db_bot)

yandex_bot = dict(config_parser.items("YANDEX_BOT"))
yandex_bot = from_dict(data_class=YandexBot, data=yandex_bot)

clickhouse = dict(config_parser.items("CLICKHOUSE"))
clickhouse = from_dict(data_class=ClickhouseBot, data=clickhouse)

redis = dict(config_parser.items("REDIS"))
redis = from_dict(data_class=Redis, data=redis)

app = dict(config_parser.items("APP"))
app['type'] = AppType(app['type'])
app = from_dict(data_class=App, data=app)

kafka = dict(config_parser.items("KAFKA"))

config = Config(
    tg_bot,
    db_bot,
    yandex_bot,
    clickhouse,
    redis,
    Kafka(bootstrap_servers=kafka['bootstrap_servers'].split(',')),
    app
)
