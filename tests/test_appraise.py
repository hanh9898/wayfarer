"""Regression test cho bin/appraise.py.

Mỗi test dưới đây khoá lại một lỗi TÌM RA KHI CHẠY THẬT, không phải khi đọc lại mã:

- `text` lọt ra stdout — cả lý do script này tồn tại.
- Thư mục tên `sach.epub` lọt qua `exists()` rồi bị gán oan là bản hỏng.
- `.EPUB` viết hoa bị từ chối oan vì hằng số chỉ chứa đuôi chữ thường.
- Engine in tiến trình ra stdout, lẫn vào JSON, bên gọi parse gãy.
- Mã thoát của "đường dẫn sai" và "sách hỏng thật" phải KHÁC nhau — mã thoát là
  thứ quyết định có gửi thư sang vai khác hay không.

Test cần một file sách thật. Lấy về theo công thức ở tests/fixtures/sample-books/README.md;
không có thì các test cần sách tự bỏ qua (sách không bao giờ vào repo).
"""
import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
SCRIPT = REPO / "bin" / "appraise.py"
SACH = REPO / "tests" / "fixtures" / "sample-books" / "art-of-war.epub"

can_sach = pytest.mark.skipif(
    not SACH.is_file(),
    reason="chưa lấy sách thử — xem tests/fixtures/sample-books/README.md",
)


def chay(duong_dan):
    """Chạy script, trả (mã thoát, object JSON đã parse từ stdout)."""
    r = subprocess.run(
        [sys.executable, str(SCRIPT), str(duong_dan)],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return r.returncode, json.loads(r.stdout)


@can_sach
def test_khoa_text_khong_bao_gio_ra_stdout():
    """Ràng buộc nặng nhất của cả skill, và là lý do script này tồn tại."""
    ma, d = chay(SACH)
    assert ma == 0
    assert d["status"] == "ok"
    assert "text" not in d["metrics"]
    assert "text" not in json.dumps(d)


@can_sach
def test_stdout_chi_co_json():
    """Engine in tiến trình ra stdout; nếu không chặn thì JSON parse gãy."""
    r = subprocess.run(
        [sys.executable, str(SCRIPT), str(SACH)],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    json.loads(r.stdout)  # gãy ở đây nghĩa là log lẫn vào stdout
    assert "Extracting" in r.stderr  # log vẫn còn, chỉ đổi chỗ


@can_sach
def test_so_lieu_du_khoa_can_dung():
    ma, d = chay(SACH)
    for khoa in ("words", "estimated_tokens", "pages", "pages_label", "chapters_detected", "has_toc"):
        assert khoa in d["metrics"], khoa


@can_sach
def test_duoi_viet_hoa_van_nhan(tmp_path):
    """`.EPUB` không nằm trong SUPPORTED_EXTENSIONS nhưng là sách hợp lệ."""
    hoa = tmp_path / "SACH.EPUB"
    hoa.write_bytes(SACH.read_bytes())
    ma, d = chay(hoa)
    assert ma == 0
    assert d["status"] == "ok"


def test_thu_muc_doi_lot_file_khong_phai_ban_hong(tmp_path):
    """`exists()` trả True cho thư mục này; nó không được lọt xuống engine."""
    d_muc = tmp_path / "thumuc.epub"
    d_muc.mkdir()
    ma, d = chay(d_muc)
    assert ma == 1, "phải là mã chặn sớm, không phải mã bản hỏng"
    assert d["status"] == "not_a_file"


def test_duoi_la_khong_phai_ban_hong(tmp_path):
    f = tmp_path / "ghi-chu.xyz"
    f.write_text("linh tinh", encoding="utf-8")
    ma, d = chay(f)
    assert ma == 1
    assert d["status"] == "unsupported_extension"
    assert ".epub" in d["accepted_extensions"], "danh sách phải lấy từ chính engine"


def test_file_rong_khong_phai_ban_hong(tmp_path):
    f = tmp_path / "rong.epub"
    f.touch()
    ma, d = chay(f)
    assert ma == 1
    assert d["status"] == "empty_file"


def test_duong_dan_khong_ton_tai_khong_phai_ban_hong(tmp_path):
    ma, d = chay(tmp_path / "khong-co-that.epub")
    assert ma == 1
    assert d["status"] == "not_a_file"


@can_sach
def test_ban_hong_that_ra_ma_thoat_rieng(tmp_path):
    """EPUB đổi đuôi thành .pdf: qua cả ba phép kiểm rồi mới hỏng ở engine.

    Đây là ca DUY NHẤT được phép sinh ra một lá thư báo bản hỏng.
    """
    gia = tmp_path / "ban-hong.pdf"
    gia.write_bytes(SACH.read_bytes())
    ma, d = chay(gia)
    assert ma == 2, "phải khác mã chặn sớm — mã thoát quyết định có gửi thư hay không"
    assert d["status"] == "extraction_failed"


@can_sach
def test_duong_dan_tieng_viet_co_dau(tmp_path):
    """Người dùng dự án này đặt tên thư mục bằng tiếng Việt."""
    thu_muc = tmp_path / "Sách của tôi" / "Kiểm thử"
    thu_muc.mkdir(parents=True)
    f = thu_muc / "Binh pháp Tôn Tử.epub"
    f.write_bytes(SACH.read_bytes())
    ma, d = chay(f)
    assert ma == 0
    assert d["metrics"]["words"] > 0


@can_sach
def test_cat_bot_tieu_de_chuong_mau(tmp_path):
    """Một cuốn 300 chương không được tự nó thành một khối lớn trong ngữ cảnh."""
    ma, d = chay(SACH)
    mau = d["metrics"].get("chapter_headings_sample")
    if isinstance(mau, list):
        assert len(mau) <= 5
