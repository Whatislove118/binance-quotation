import json
import os
import sys
from dataclasses import dataclass

from core.stream import Stream


@dataclass
class Config:
    CONFIG_FILE_PATH = os.getenv("CONFIG_FILE_PATH", "config.json")
    REMOTE_HOST = os.getenv("REMOTE_HOST", "stream.binance.com")
    REMOTE_PORT = os.getenv("REMOTE_PORT", "9443")
    REMOTE_URL = f"wss://{REMOTE_HOST}:{REMOTE_PORT}/ws"
    STREAM_REGISTRY = {}
    TELEGRAM_API_TOKEN = os.getenv("TELEGRAM_API_TOKEN", "token")

    def init_config_data(self, file_path: str = CONFIG_FILE_PATH) -> dict:
        try:
            with open(file_path) as json_file:
                return json.load(json_file)
        except json.JSONDecodeError:
            sys.exit("ERROR: Bad JSON format")

    def init_streams(self, aggregator: str = "ticker") -> None:
        file_data = self.init_config_data()

        convert_name = lambda x: "".join(x.split("/")).lower()

        for key, data in file_data.items():
            name = convert_name(key)
            stream = Stream(
                name=name,
                value=data.get("price"),
                operation_type=data.get("trigger"),
                aggregator="ticker",
            )
            Config.STREAM_REGISTRY[name.upper()] = stream
