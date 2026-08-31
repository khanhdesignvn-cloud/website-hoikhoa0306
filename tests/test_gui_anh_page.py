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


def test_photo_page_has_grouped_library_and_sender_table():
    html = PAGE.read_text(encoding="utf-8")
    required = [
        'href="https://drive.google.com/drive/folders/1-glZL1l1TupaanQTTGl0CBtMH7coO4og"',
        'target="_blank" rel="noopener">Xem thư viện ảnh',
        'id="thu-vien-anh"',
        'id="photo-slider"',
        'id="sender-table-body"',
        "fetch('photos.json'",
        'function latestPhotos',
        '.slice(0, 6)',
        'function aggregateSenders',
        'function loadSenderTableFromPhotos',
        "var SENDER_REPORT_START = Date.parse('2026-08-30T15:43:35.000Z')",
        '< SENDER_REPORT_START',
    ]
    missing = [item for item in required if item not in html]
    assert not missing, f"Thiếu thư viện hoặc bảng người gửi: {missing}"
    assert 'id="sender-groups"' not in html
    assert "fetch('photo-log.json'" not in html


def test_photo_upload_shows_progress_and_accepts_40_images():
    html = PAGE.read_text(encoding="utf-8")
    required = [
        'Tối đa 40 ảnh',
        'var MAX_FILES = 40',
        'var BATCH_SIZE = 4',
        'id="upload-progress"',
        'id="upload-progress-bar"',
        'id="upload-progress-text"',
        'new XMLHttpRequest()',
        'xhr.upload.onprogress',
        "btn.textContent = 'Đang tải ' + percent + '%'",
    ]
    missing = [item for item in required if item not in html]
    assert not missing, f"Thiếu giới hạn 40 ảnh hoặc tiến độ upload: {missing}"


def test_success_popup_links_to_drive_and_updates_sender_list():
    html = PAGE.read_text(encoding="utf-8")
    required = [
        'id="thank-you-popup"',
        'role="dialog"',
        'id="thank-you-name"',
        'id="thank-you-count"',
        'id="close-thank-you"',
        'href="https://drive.google.com/drive/folders/1-glZL1l1TupaanQTTGl0CBtMH7coO4og"',
        'function showThankYouPopup',
        'function addSenderToTable',
        'addSenderToTable(name, chuyen, uploadedCount)',
        'showThankYouPopup(name, uploadedCount)',
        'setTimeout(loadSenderTableFromPhotos, 30000)',
    ]
    missing = [item for item in required if item not in html]
    assert not missing, f"Thiếu popup cảm ơn hoặc cập nhật người gửi: {missing}"


def test_gallery_is_gentle_clothesline_slider_with_latest_sender():
    html = PAGE.read_text(encoding="utf-8")
    required = [
        'id="latest-sender-card"',
        'id="latest-sender-name"',
        'id="latest-sender-meta"',
        'class="clothesline-frame"',
        'id="photo-slider"',
        'class="clothesline-wire"',
        'class="slider-control slider-prev"',
        'class="slider-control slider-next"',
        'function updateLatestSender',
        'function startGentleSlider',
        'scrollBy({left: step, behavior:\'smooth\'})',
        "window.matchMedia('(prefers-reduced-motion: reduce)')",
        'updateLatestSender(name, chuyen, uploadedCount)',
    ]
    missing = [item for item in required if item not in html]
    assert not missing, f"Thiếu dây ảnh slide hoặc thông tin người vừa gửi: {missing}"


def test_clothesline_autoplays_and_keeps_drive_button_below():
    html = PAGE.read_text(encoding="utf-8")
    required = [
        'setInterval(function()',
        '}, 4800)',
        'class="gallery-drive-link"',
        'Xem toàn bộ thư viện ảnh',
        'target="_blank" rel="noopener"',
    ]
    missing = [item for item in required if item not in html]
    assert not missing, f"Thiếu tự chạy hoặc nút thư viện bên dưới: {missing}"
    assert html.index('class="gallery-drive-link"') > html.index('id="photo-slider"')
