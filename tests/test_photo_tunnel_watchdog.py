import importlib.util
from pathlib import Path

WATCHDOG = Path('/root/.hermes/hoikhoa/watchdog.py')


def load_watchdog():
    spec = importlib.util.spec_from_file_location('hoikhoa_watchdog', WATCHDOG)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_watchdog_updates_register_and_photo_urls(tmp_path):
    wd = load_watchdog()
    index = tmp_path / 'index.html'
    photo = tmp_path / 'gui-anh.html'
    index.write_text("var REGISTER_URL = 'https://old.trycloudflare.com/register';\nvar PHOTO_SCRIPT_URL = 'https://old.trycloudflare.com/upload-photo';", encoding='utf-8')
    photo.write_text("var PHOTO_SCRIPT_URL = 'https://old.trycloudflare.com/upload-photo';", encoding='utf-8')
    wd.INDEX = str(index)
    wd.PHOTO_PAGE = str(photo)

    wd.update_index('https://new.trycloudflare.com')

    assert "https://new.trycloudflare.com/register" in index.read_text(encoding='utf-8')
    assert "https://new.trycloudflare.com/upload-photo" in index.read_text(encoding='utf-8')
    assert "https://new.trycloudflare.com/upload-photo" in photo.read_text(encoding='utf-8')
