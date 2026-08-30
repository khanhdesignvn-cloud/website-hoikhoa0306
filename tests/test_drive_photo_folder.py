from pathlib import Path

NEW_FOLDER_ID = "1-glZL1l1TupaanQTTGl0CBtMH7coO4og"
OLD_FOLDER_ID = "1sxVPVgIGZ9FCVZ3xmC6JRETrD2F4e-ZM"
REGISTER_SERVER = Path('/root/.hermes/hoikhoa/register-server.py')
SYNC_SCRIPT = Path('/root/.hermes/hoikhoa/sync-photos.py')


def test_new_photo_uploads_use_requested_drive_folder():
    content = REGISTER_SERVER.read_text(encoding='utf-8')
    assert NEW_FOLDER_ID in content
    assert OLD_FOLDER_ID not in content


def test_gallery_sync_preserves_legacy_folder_and_includes_new_folder():
    content = SYNC_SCRIPT.read_text(encoding='utf-8')
    assert NEW_FOLDER_ID in content
    assert OLD_FOLDER_ID in content
