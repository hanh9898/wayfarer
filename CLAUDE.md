# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

Plugin `van-dao`: biến sách PDF/EPUB người dùng đã có thành lộ trình học có người kèm.

Repo viết bằng tiếng Việt — định danh trong mã, tên file, tên trường YAML dùng tiếng Việt **không
dấu**; kebab-case cho file và `id`, snake_case cho trường YAML.

Đang ở đâu, làm gì tiếp: `docs/VAN-DAO-trang-thai-du-an.md` §10. Thiết kế: `docs/VAN-DAO-dac-ta-v1.0.md`
— 2.112 dòng, mở theo mục và bắt đầu ở §0 (bảng tra từ vựng), đừng nạp cả file.

## Lệnh

```bash
pip install -r requirements-dev.txt        # pyyaml + pytest

python -m pytest tests/ -v                 # toàn bộ test (đúng lệnh CI chạy)
python -m pytest tests/test_kiem_bi_kip.py::test_bo_tham_so_thieu_khoa_la_loi -v   # một test

python bin/kiem-bi-kip.py --kho tests/fixtures     # kiểm cả kho fixture — thoát 1 là ĐÚNG, sach-loi lỗi có chủ ý
python bin/kiem-bi-kip.py tests/fixtures/sach-loi  # kiểm một quyển
python bin/kiem-bi-kip.py <quyển> --json           # đầu ra cho skill; mã thoát 0 đạt · 1 có lỗi · 2 không chạy được

claude plugin validate . --strict          # sau mỗi lần đụng .claude-plugin/ hay thêm skill
```

CI chạy `pytest` trên Python 3.11, cả `ubuntu-latest` và `windows-latest`.

## Luật

- **IMPORTANT: không bao giờ commit nội dung sách hoặc hồ sơ người học.** Chúng ở `~/.vandao/` trên máy
  người dùng; `.gitignore` chặn `*.pdf` · `*.epub` · `.vandao/`. Đừng tạo file mẫu vi phạm việc này.
- Đặc tả là nguồn sự thật. Mã lệch đặc tả thì sửa đặc tả trước, sửa mã sau.
- Không thêm thành phần ngoài §13 đặc tả mà chưa hỏi.
- Không viết thêm design hay data contract trước khi có executable spec — viết just-in-time theo vòng.
  Căn cứ: `trang-thai-du-an` §4.2, bốn lần soát tài liệu bắt 0/11 defect, walkthrough chạy ca thật bắt 11/11.
- Mọi script trong `bin/` phải kèm luật tương đương bằng lời trong `tham-chieu/` (§12.3), và **không được
  phụ thuộc code page của máy chạy**: mở file khai `encoding="utf-8"`, ép `sys.stdout`/`sys.stderr` về UTF-8.
- Mọi SKILL.md phải có "Xong khi" và "Khi nào skill này không giúp được", theo nhịp trình → xác nhận →
  ghi → kiểm (§12.4). Không ghi đè im lặng.
- Mọi ví dụ trong đặc tả và `tham-chieu/` phải là ví dụ tổng hợp, không lấy từ bí kíp thật (R24).
- Yêu cầu ở đặc tả §8 gồm **32 mục**: `R1`–`R31` cộng `R13b`. Sửa hành vi thì trỏ đúng R nào.

## Chỗ dễ sai

- **Rỗng ≠ vắng** (R13). `chi_nhanh: []` hợp lệ; `sai_lam_pho_bien: []` chỉ là cảnh báo. Defect đầu tiên
  của dự án, đã có regression test khoá lại.
- `tham-chieu/bi-kip.schema.md` và `bin/kiem-bi-kip.py` là **một cặp**: §6 của schema là luật bằng lời
  của đúng những phép kiểm script thực thi, §7 là phần script không làm. Đổi một bên thì đổi bên kia
  trong cùng một thay đổi, kèm fixture và test.
- Validator có ba mức — `L()` lỗi chặn nhập kho · `C()` cảnh báo · `G()` ghi chú — và chỉ `loi` quyết
  định mã thoát. Chọn nhầm mức là cách âm thầm nhất làm hỏng luồng thu sách.
- Bí kíp có hai hình dạng rẽ ở `kiem_mot()`: `loai: bi-kip` có `chuong/` và đồ thị phụ thuộc;
  `loai: tan-quyen` không có `chuong/`, trường sư phạm nằm thẳng trong `manifest.yaml`.
- Ba đường truyền tin định nghĩa thiết kế bằng thứ **không** mang theo (§4.5): thư linh → nghiệm công
  không mang giáo án; giám khảo → phúc khảo không mang tiêu chí; trưởng môn → trưởng lão không mang
  `thu-linh/**`. Bốn vai chấm là subagent **tươi**, không bao giờ fork.
- `.pham-vi.json` thiếu → **không vai nào** đọc được, không phải mọi vai đọc được (R26). Fail an toàn.

## Test

`tests/test_kiem_bi_kip.py` gọi script qua `subprocess` và đọc `--json`, nên nó kiểm cả giao diện lệnh.
Ba fixture: `kiem-thu-dac-ta` sạch · `sach-loi` nhiều lỗi cố ý · `tan-quyen-mau` nhánh tàn quyển.

Thêm phép kiểm mới thì thêm ca lỗi vào `sach-loi` và assert theo **mã lỗi** (`ma`), không assert theo
thông điệp. Test phải phân biệt được: kiểm nó fail trên bản chưa sửa, không chỉ pass trên bản đã sửa.

Eval cho skill và agent nằm ở `.claude/rules/eval.md` — tự nạp khi làm việc trong `skills/` hoặc
`agents/`, không chiếm ngữ cảnh phiên khác.
