import pytest
from src.real_time_face_detection.utils import ConfigLoader


@pytest.fixture(scope="session")
def tmp_dir(tmpdir_factory):
    dir = tmpdir_factory.mktemp("data")
    return dir


@pytest.fixture
def config_file_path_for_testing():
    return "tests/test_config.json"


def test_load_config(config_file_path_for_testing):
    loader = ConfigLoader(filepath=config_file_path_for_testing)

    assert type(loader.config) == dict
    assert len(loader.config) == 3

    config = loader.load_config(filepath=config_file_path_for_testing)
    assert config is loader.config


def test_get_key(config_file_path_for_testing):
    loader = ConfigLoader(filepath=config_file_path_for_testing)

    assert loader.get('test_config1') == 1
    assert loader.get('test_config2') == 5.6
    assert loader.get('test_config3') == 'test'


def test_add_key(config_file_path_for_testing, tmp_dir):
    loader = ConfigLoader(filepath=config_file_path_for_testing)
    loader.filepath = tmp_dir / 'test_config.json'

    loader.set('test_config1', 'key_changed')
    loader.set('test_config4', 'new_key')

    new_config = loader.load_config(loader.filepath)

    assert new_config == {
        "test_config1": 'key_changed',
        "test_config2": 5.6,
        "test_config3": "test",
        "test_config4": "new_key"
    }
