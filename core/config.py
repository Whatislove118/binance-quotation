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
    TELEGRAM_API_TOKEN = os.getenv("TELEGRAM_API_TOKEN", "token")

    STREAM_REGISTRY = {}
    CHAT_SET = set()  # database mock

    @classmethod
    def init_config_data(cls, file_path: str = CONFIG_FILE_PATH) -> dict:
        try:
            with open(file_path) as json_file:
                return json.load(json_file)
        except json.JSONDecodeError:
            sys.exit("ERROR: Bad JSON format")
        except FileNotFoundError:
            sys.exit(f"ERROR: File {file_path} not found.")

    @classmethod
    def init_streams(
        cls,
        aggregator: str = "ticker",
        file_path: str = CONFIG_FILE_PATH,
    ) -> None:
        file_data = cls.init_config_data(file_path=file_path)

        for key, data in file_data.items():
            name = "".join(key.split("/")).lower()
            aggregator = data.get("aggregator", aggregator)
            stream = Stream(
                name=name,
                value=data.get("price"),
                operation_type=data.get("trigger"),
                aggregator=aggregator,
            )
            cls.STREAM_REGISTRY[name.upper()] = stream
