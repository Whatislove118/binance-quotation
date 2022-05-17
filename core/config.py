import json
import os
import sys
from dataclasses import dataclass

from dotenv import load_dotenv

from .stream import Stream

load_dotenv()


@dataclass
class Config:
    CONFIG_FILE_PATH = os.getenv("CONFIG_FILE_PATH", "config.json")
    REMOTE_HOST = os.getenv("REMOTE_HOST", "stream.binance.com")
    REMOTE_PORT = os.getenv("REMOTE_PORT", "9443")
    REMOTE_URL = f"wss://{REMOTE_HOST}:{REMOTE_PORT}/ws"
    STREAM_REGISTRY = {}
    TELEGRAM_API_TOKEN = os.getenv("TELEGRAM_API_TOKEN", "token")
    CHAT_SET = set()  # database mock

    @classmethod
    def init_config_data(cls, file_path: str = CONFIG_FILE_PATH) -> dict:
        try:
            with open(file_path) as json_file:
                return json.load(json_file)
        except json.JSONDecodeError:
            sys.exit("ERROR: Bad JSON format")

    @classmethod
    def init_streams(cls, aggregator: str = "ticker") -> None:
        file_data = cls.init_config_data()

        for key, data in file_data.items():
            name = "".join(key.split("/")).lower()
            stream = Stream(
                name=name,
                value=data.get("price"),
                operation_type=data.get("trigger"),
                aggregator="ticker",
            )
            cls.STREAM_REGISTRY[name.upper()] = stream
