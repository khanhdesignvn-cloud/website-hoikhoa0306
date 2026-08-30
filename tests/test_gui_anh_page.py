from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "gui-anh.html"
INDEX = ROOT / "index.html"


def test_gui_anh_page_has_complete_drive_upload_flow():
    assert PAGE.exists(), "Trang con gui-anh.html chưa được tạo"
    html = PAGE.read_text(encoding="utf-8")
    required = [
        'id="photo-form"',
        'name="hoten"',
        'name="chuyen"',
        'type="file"',
        'accept="image/*"',
        'multiple',
        'id="photo-preview"',
        '/upload-photo',
        'FileReader',
        "split(',')[1]",
        'JSON.stringify({ name: name, chuyen: chuyen, files: fileList })',
        'Ảnh đã lưu vào Google Drive',
    ]
    missing = [item for item in required if item not in html]
    assert not missing, f"Thiếu thành phần upload: {missing}"


def test_gui_anh_page_uses_safe_dom_rendering_for_file_names():
    html = PAGE.read_text(encoding="utf-8")
    assert "textContent = file.name" in html
    assert "innerHTML = file.name" not in html


def test_home_navigation_links_to_photo_subpage():
    html = INDEX.read_text(encoding="utf-8")
    assert '<a href="gui-anh.html">Gửi ảnh</a>' in html
