from .shared import load_config
from configuration.sections import ServerSectionConfiguration


def test_conf_load_toml():
    c = load_config('src/config.toml')
    assert c
    assert not c.Config.load_failed
    assert "<FastAPIConfiguration object at" in str(c.__repr__)


def test_conf_load_yaml():
    c = load_config('src/config.yaml')
    assert c
    assert not c.Config.load_failed
    assert "<FastAPIConfiguration object at" in str(c.__repr__)


def test_conf_load_ini():
    c = load_config('src/config.ini')
    assert c
    assert not c.Config.load_failed
    assert "<FastAPIConfiguration object at" in str(c.__repr__)


def test_conf_non_existing_config():
    assert not load_config('non_existing.toml')


def test_conf_lost_file_extention():
    assert load_config('non_existing').Config.load_failed, "Cannot catch lost file extention"


def test_conf_unknown_file_extention():
    assert load_config('non_existing.boroda').Config.load_failed, "Cannot catch unknown file extention"


def test_conf_validation_error():
    bad_data: dict = {
        'bind_port': 'bar'
    }
    section = ServerSectionConfiguration()
    assert not section.load(bad_data, 'Server')
