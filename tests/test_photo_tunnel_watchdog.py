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


def test_cloudflared_alive_requires_the_hoikhoa_8088_tunnel(monkeypatch):
    wd = load_watchdog()

    class Result:
        returncode = 0
        stdout = "513 cloudflared tunnel --url http://127.0.0.1:4010 --no-autoupdate\n"

    monkeypatch.setattr(wd.subprocess, "run", lambda *args, **kwargs: Result())
    assert wd.cloudflared_alive() is False

    Result.stdout += "900 cloudflared tunnel --url http://localhost:8088 --no-autoupdate\n"
    assert wd.cloudflared_alive() is True


def test_start_cloudflared_discards_stale_tunnel_url(tmp_path, monkeypatch):
    wd = load_watchdog()
    log = tmp_path / "tunnel.log"
    log.write_text("https://stale.trycloudflare.com\n", encoding="utf-8")
    wd.TUNNEL_LOG = str(log)
    launched = []

    def fake_popen(command, **kwargs):
        launched.append((command, kwargs))
        return object()

    monkeypatch.setattr(wd.subprocess, "Popen", fake_popen)
    wd.start_cloudflared()

    assert "stale.trycloudflare.com" not in log.read_text(encoding="utf-8")
    assert "http://localhost:8088" in launched[0][0]
