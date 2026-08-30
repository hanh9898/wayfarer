"""Regression test cho validate-scripture.py.

Ba defect đầu tiên đều tìm ra khi CHẠY THẬT, không phải khi đọc lại mã.
Mỗi test dưới đây khoá một defect đó lại.
"""
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SCRIPT = REPO / "bin" / "validate-scripture.py"
FIX = REPO / "tests" / "fixtures"


def chay(path, json=False):
    cmd = [sys.executable, str(SCRIPT), str(path)]
    if json:
        cmd.append("--json")
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    return r.returncode, r.stdout


def ma_loi(path):
    import json as J
    _, out = chay(path, json=True)
    kq = J.loads(out)["result"][0]
    return {l["code"] for l in kq["errors"]}, {c["code"] for c in kq["warnings"]}


# ---------------------------------------------------------------- ca sạch

def test_bi_kip_sach_thi_dat():
    ma, _ = chay(FIX / "spec-based-testing")
    assert ma == 0


def test_tan_quyen_khong_can_chuong():
    """Tàn quyển đặt trường sư phạm ở cấp gốc, không có thư mục chuong/."""
    ma, _ = chay(FIX / "fragment-sample")
    assert ma == 0


# ------------------------------------------------- DEFECT 1: rỗng ≠ vắng

def test_mang_rong_khong_phai_thieu_truong():
    """`chi_nhanh: []` và `sai_lam_pho_bien: []` là HỢP LỆ.

    Bản đầu coi [] đồng nghĩa với vắng mặt nên báo `thieu-truong`.
    Quy cách §6 nói rõ một số trường được phép rỗng.
    """
    loi, _ = ma_loi(FIX / "spec-based-testing")
    assert "thieu-truong" not in loi
    assert "truong-rong" not in loi


def test_sai_lam_rong_chi_la_canh_bao():
    """Rỗng thì cảnh báo, không chặn — mức 'đủ dùng' không đòi trường này."""
    _, canh_bao = ma_loi(FIX / "fragment-sample")
    assert "chua-co-sai-lam" in canh_bao
    ma, _ = chay(FIX / "fragment-sample")
    assert ma == 0


# --------------------------------------- DEFECT 2: bộ tham số thiếu khoá

def test_bo_tham_so_thieu_khoa_la_loi():
    """Mỗi bộ phải có đủ khoá mà `khuon` dùng.

    Với `tham_so` cũ (ba danh sách rời) lỗi này KHÔNG phát hiện được ở pha
    kiểm — tổ hợp chỉ sinh lúc chạy. `bo_tham_so` kéo nó về pha validate.
    """
    loi, _ = ma_loi(FIX / "broken-scripture")
    assert "bo-thieu-khoa" in loi


# ---------------------------------------------- DEFECT 3: enum sai giá trị

def test_canh_gioi_ngoai_enum_la_loi():
    loi, _ = ma_loi(FIX / "broken-scripture")
    assert "enum-sai" in loi


# ------------------------------------------------ ràng buộc sư phạm khác

def test_tai_hien_khong_duoc_tro_tieu_chi():
    """Câu tái hiện không tính là bằng chứng nên `do_tieu_chi` phải rỗng."""
    loi, _ = ma_loi(FIX / "broken-scripture")
    assert "tai-hien-tro-tieu-chi" in loi


def test_ma_thoat_1_khi_co_loi():
    ma, _ = chay(FIX / "broken-scripture")
    assert ma == 1


# ------------------- DEFECT 4: đầu ra chết theo code page của máy chạy

def test_in_duoc_khi_code_page_khong_phai_utf8():
    """Script phải in được tiếng Việt dù máy chạy dùng code page cũ.

    Trên Windows, stdout bị chuyển hướng lấy code page hệ thống (cp1252 ·
    cp1258) — không mã hoá nổi tiếng Việt, nên bản đầu CHẾT giữa lúc in với
    UnicodeEncodeError. Người dùng thấy traceback Python thay vì thấy bí kíp
    của mình sai chỗ nào.

    Ép `PYTHONIOENCODING=cp1252` tái hiện đúng ca đó trên cả Linux lẫn Windows.
    """
    import os
    env = {**os.environ, "PYTHONIOENCODING": "cp1252"}
    r = subprocess.run([sys.executable, str(SCRIPT), str(FIX / "spec-based-testing")],
                       capture_output=True, text=True, encoding="utf-8", env=env)
    assert "UnicodeEncodeError" not in r.stderr, r.stderr
    assert r.returncode == 0
    assert "ĐẠT" in r.stdout
