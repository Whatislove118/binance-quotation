import pytest

from core.config import Config


def test_file():
    Config.init_config_data()


def test_file_not_exists():
    path = "./config"
    with pytest.raises(SystemExit):
        Config.init_config_data(file_path=path)


def test_file_wrong_format(create_file, filename, tmp_path):
    with pytest.raises(SystemExit):
        Config.init_config_data(file_path=tmp_path / filename)


@pytest.mark.parametrize("content", ['"BTCUSDT": {"trigger": "more", "price": "00.1"}'])
def test_file_wrong_content(tmp_path, content):
    path = tmp_path / "test.json"
    path.write_text(content)
    with pytest.raises(SystemExit):
        Config.init_config_data(file_path=path)


@pytest.mark.parametrize(
    "content", ['{ "BTCUSDT": {"trigger": "diff", "price": "00.1"} }']
)
def test_file_wrong_trigger_type(tmp_path, content):
    path = tmp_path / "test.json"
    path.write_text(content)
    with pytest.raises(SystemExit):
        Config.init_streams(file_path=path)


@pytest.mark.parametrize(
    "content", ['{ "BTCUSDT": {"trigger": "diff", "price": "price"} }']
)
def test_file_wrong_price_type(tmp_path, content):
    path = tmp_path / "test.json"
    path.write_text(content)
    with pytest.raises(SystemExit):
        Config.init_streams(file_path=path)
