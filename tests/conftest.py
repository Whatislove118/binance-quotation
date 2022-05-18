import pytest


@pytest.fixture(params=["config.yaml", "config.xml"])
def filename(request):
    return request.param


@pytest.fixture
def create_file(tmp_path, filename: str, content: str = ""):
    p = tmp_path / filename
    p.write_text(content)
