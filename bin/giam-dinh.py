#!/usr/bin/env python3
"""giam-dinh.py — rút thử chữ khỏi một cuốn sách và trả về CHỈ số liệu giám định.

Lý do script này tồn tại, không phải để tiện: `book_to_skill.extract_single_file`
trả về một dict có khoá `text` giữ TOÀN BỘ nội dung cuốn sách — một cuốn kỹ thuật
500 trang cho gần 200 nghìn token nằm gọn trong đúng khoá đó. Nếu skill gọi thẳng
API, ràng buộc "không được đưa `text` vào ngữ cảnh" chỉ là một lời dặn, và không có
gì bắt được nếu nó bị vi phạm. Script này chặn ở chỗ khác: `text` không bao giờ ra
tới stdout, nên nội dung sách không còn đường nào vào ngữ cảnh cả.

Nó cũng làm ba phép kiểm đường dẫn trước khi gọi engine, vì cùng một lý do: engine
ném đúng MỘT loại lỗi cho mọi kiểu hỏng, nên phân biệt "đường dẫn sai" với "sách
hỏng thật" bằng cách đọc chuỗi lỗi là không đáng tin. Ở đây hai ca đó ra hai mã
thoát khác nhau — và mã thoát là thứ quyết định có gửi thư báo bản hỏng sang vai
khác hay không. Báo sai làm bẩn dữ liệu của vai khác, không chỉ làm phiền màn hình.

Dùng:
    giam-dinh.py <đường-dẫn-sách>

Đầu ra: luôn một object JSON trên stdout, luôn có khoá `trang_thai`.

Mã thoát:
    0  ok — rút được chữ, `so_lieu` có đủ các khoá số liệu
    1  chặn sớm: `khong_phai_file` · `duoi_khong_ho_tro` · `file_rong`
       → hỏi lại đường dẫn. KHÔNG phải bản hỏng, KHÔNG gửi thư.
    2  khong_rut_duoc_chu — ba phép kiểm đã qua mà engine vẫn không rút được
       → đây mới là bản hỏng thật.
    3  engine_chua_cai — chưa `import` được engine.

Phụ thuộc: book-to-skill (ghim theo SHA trong requirements-dev.txt).
"""

import contextlib
import json
import sys
from pathlib import Path

# Đầu ra luôn UTF-8, không phụ thuộc code page của máy chạy. Trên Windows, khi
# stdout bị chuyển hướng — đúng cách skill gọi script rồi bắt đầu ra — Python lấy
# code page hệ thống, và cp1258 không mã hoá nổi tên sách tiếng Việt.
for _luong in (sys.stdout, sys.stderr):
    if hasattr(_luong, "reconfigure"):
        _luong.reconfigure(encoding="utf-8")

# Đúng những khoá được phép ra khỏi script. Danh sách CHO PHÉP, không phải danh
# sách cấm: bản engine sau thêm khoá mới thì khoá đó bị bỏ qua, thay vì lọt ra
# vì chưa ai kịp thêm nó vào danh sách cấm. `text` không có tên ở đây, và đó là
# toàn bộ điểm của file này.
METRIC_KEYS = (
    "filename",
    "source_file",
    "format",
    "extraction_method",
    "pages",
    "pages_label",
    "spine_items",
    "words",
    "chars",
    "file_size_mb",
    "estimated_tokens",
    "chapters_detected",
    "chapters_method",
    "chapter_headings_sample",
    "has_toc",
    "images_dropped",
)

# Tiêu đề chương trích ra làm mẫu — cắt ở đây để một cuốn 300 chương không tự nó
# thành một khối lớn trong ngữ cảnh.
SAMPLE_TITLE_COUNT = 5


def emit(trang_thai, ma_thoat, **them):
    """In đúng một object JSON rồi thoát. Không có đường nào khác ra khỏi script."""
    print(json.dumps({"trang_thai": trang_thai, **them}, ensure_ascii=False, indent=2))
    sys.exit(ma_thoat)


def main():
    if len(sys.argv) != 2:
        emit("thieu_tham_so", 1, thong_diep="Dùng: giam-dinh.py <đường-dẫn-sách>")

    try:
        import book_to_skill
        from book_to_skill import config
    except ImportError as e:
        emit(
            "engine_chua_cai",
            3,
            thong_diep=str(e),
            cach_cai="pip install -r requirements-dev.txt",
        )

    # Chuẩn hoá về tuyệt đối trước mọi phép kiểm: `is_file()` trên đường dẫn tương
    # đối phụ thuộc thư mục làm việc, mà thư mục làm việc của skill không đoán được.
    duong_dan = Path(sys.argv[1]).expanduser()
    try:
        duong_dan = duong_dan.resolve()
    except OSError as e:
        emit("khong_phai_file", 1, duong_dan=str(duong_dan), thong_diep=str(e))

    # Phép kiểm 1 — là file thật, không phải thư mục.
    # `exists()` trả True cho một thư mục tên `sach.epub`; nó sẽ lọt xuống engine
    # rồi lĩnh ExtractionError và bị gán oan là bản hỏng.
    if not duong_dan.is_file():
        emit("khong_phai_file", 1, duong_dan=str(duong_dan))

    # Phép kiểm 2 — đuôi nằm trong danh sách engine nhận, SO SAU KHI HẠ CHỮ THƯỜNG.
    # Hằng số chỉ chứa đuôi chữ thường, nên so thẳng sẽ từ chối oan một `.EPUB` tốt.
    duoi = duong_dan.suffix.lower()
    if duoi not in config.SUPPORTED_EXTENSIONS:
        emit(
            "duoi_khong_ho_tro",
            1,
            duong_dan=str(duong_dan),
            duoi=duong_dan.suffix,
            duoi_nhan_duoc=sorted(config.SUPPORTED_EXTENSIONS),
        )

    # Phép kiểm 3 — kích thước lớn hơn 0.
    if duong_dan.stat().st_size == 0:
        emit("file_rong", 1, duong_dan=str(duong_dan))

    # Engine in tiến trình ("Extracting EPUB: ...", "Trying pypdf...") thẳng ra
    # stdout. Không chặn thì nó lẫn vào JSON và bên gọi parse gãy — đã gặp thật ở
    # lượt chạy đầu tiên của script này. Đẩy sang stderr: người chạy tay vẫn thấy,
    # còn stdout giữ đúng một object JSON.
    try:
        with contextlib.redirect_stdout(sys.stderr):
            ket_qua = book_to_skill.extract_single_file(duong_dan, "text", "no")
    except book_to_skill.ExtractionError as e:
        # Ba phép kiểm đã qua, nên đây mới là bản hỏng thật. Chuỗi lỗi trả về cho
        # người đọc hiểu chuyện gì, KHÔNG để phân loại lỗi bằng cách so chuỗi —
        # chuỗi đó không phải hợp đồng ổn định giữa các phiên bản engine.
        emit("khong_rut_duoc_chu", 2, duong_dan=str(duong_dan), thong_diep=str(e))

    so_lieu = {k: ket_qua[k] for k in METRIC_KEYS if k in ket_qua}

    mau = so_lieu.get("chapter_headings_sample")
    if isinstance(mau, list) and len(mau) > SAMPLE_TITLE_COUNT:
        so_lieu["chapter_headings_sample"] = mau[:SAMPLE_TITLE_COUNT]
        so_lieu["chapter_headings_da_cat"] = len(mau) - SAMPLE_TITLE_COUNT

    emit("ok", 0, duong_dan=str(duong_dan), so_lieu=so_lieu)


if __name__ == "__main__":
    main()
