# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

Repo và toàn bộ tài liệu viết bằng **tiếng Việt** — định danh trong mã, tên file, tên trường YAML dùng
tiếng Việt **không dấu**, kebab-case cho file/id, snake_case cho trường YAML. Giữ nguyên quy ước này.

---

## Dự án này là gì

Plugin Claude Code (`van-dao`) biến sách PDF/EPUB người dùng **đã có** thành lộ trình học có người kèm.
Repo **không chứa quyển sách nào** — nội dung sách và hồ sơ người học nằm ở `~/.vandao/` trên máy người
dùng, và `.gitignore` chặn `*.pdf` · `*.epub` · `.vandao/`. Đừng commit hay tạo file mẫu vi phạm việc này.

**Trạng thái:** đặc tả đóng, một validator chạy được, **chưa có skill/agent/hook nào** (`skills/`,
`agents/`, `hooks/` chỉ có `.gitkeep`). Trước khi sửa gì, đọc `docs/VAN-DAO-trang-thai-du-an.md` §10
để biết việc tiếp theo.

## Lệnh

```bash
pip install -r requirements-dev.txt        # pyyaml + pytest

python -m pytest tests/ -v                 # toàn bộ test (đúng lệnh CI chạy)
python -m pytest tests/test_kiem_bi_kip.py::test_bo_tham_so_thieu_khoa_la_loi -v   # một test

python bin/kiem-bi-kip.py --kho tests/fixtures     # kiểm cả kho fixture — thoát 1 là ĐÚNG, sach-loi lỗi có chủ ý
python bin/kiem-bi-kip.py tests/fixtures/sach-loi  # kiểm một quyển
python bin/kiem-bi-kip.py <quyển> --json           # đầu ra cho skill; mã thoát 0 đạt · 1 có lỗi · 2 không chạy được

claude plugin validate . --strict          # bắt buộc sau mỗi lần đụng .claude-plugin/ hay thêm skill
```

CI (`.github/workflows/kiem.yml`) chạy `pytest` trên Python 3.11, **cả `ubuntu-latest` và
`windows-latest`** — người dựng dùng Windows, hook và script nhắm Linux, lệch giữa hai bên chỉ hiện
ra khi cả hai đều chạy.

## Luật khi làm việc trong repo này

- **Đặc tả là nguồn sự thật.** `docs/VAN-DAO-dac-ta-v1.0.md` (2.112 dòng). Mã lệch đặc tả thì sửa đặc
  tả trước, sửa mã sau. Đọc **theo mục**, không nạp cả file — §0 là bảng tra từ vựng, mở nó trước.
- **Không thêm thành phần ngoài §13 mà chưa hỏi.** Đặc tả đã khai 28 thành phần, 8 vai, 11 lệnh; rủi
  ro số một của dự án là đặc tả phình nhanh hơn thứ đã chạy.
- **Không viết thêm design cho tới khi có executable spec** (căn cứ: `trang-thai-du-an` §4.2 — bốn lần
  soát tài liệu bắt 0/11 defect, walkthrough chạy ca thật bắt 11/11).
- **Bảy data contract còn thiếu viết just-in-time theo vòng**, không viết trước cả bảy.
- **Mọi script trong `bin/` phải kèm luật tương đương bằng lời trong `tham-chieu/`** (đặc tả §12.3) —
  thiếu Python thì skill vẫn làm tay được, và phải **nói rõ đang làm tay**. Xem `bi-kip.schema.md` §6/§8.
- **Mọi SKILL.md phải có "Xong khi" và "Khi nào skill này không giúp được"**, và theo nhịp
  **trình → xác nhận → ghi → kiểm** (đặc tả §12.4). Không ghi đè im lặng.
- **Mọi ví dụ trong đặc tả và `tham-chieu/` phải là ví dụ tổng hợp** (R24) — lấy ví dụ từ bí kíp thật
  là rò rỉ instance qua đường tài liệu, phá tính cách ly của các vai chấm.
- Yêu cầu đánh số R1–R31 ở đặc tả §8. Sửa hành vi thì trỏ đúng R nào.
- **Chạy được trên cả Linux và Windows.** `.gitattributes` giữ LF ở cả hai phía. Script trong `bin/`
  **không được phụ thuộc code page của máy chạy** — mở file thì khai `encoding="utf-8"`, và ép
  `sys.stdout`/`sys.stderr` về UTF-8 ngay đầu file. Đầu ra tiếng Việt qua đường chuyển hướng trên
  Windows lấy cp1252/cp1258 và **chết giữa lúc in** thay vì báo lỗi bí kíp.

## Kiến trúc

### Hai vùng, đừng lẫn

| | Ở đâu | Ai đổi |
|---|---|---|
| **Plugin** (repo này) | `skills/ agents/ hooks/ bin/ tham-chieu/` | Theo nhịp phát hành |
| **Dữ liệu người học** | `~/.vandao/` — cây thư mục cố định ở đặc tả §15 | Lúc chạy, mỗi thư mục **đúng một vai** ghi |

### Tám vai và ba cạnh mang tải nặng nhất (đặc tả §4)

Phiên chính (được nói với người học): trưởng môn · tàng kinh trưởng lão · thư linh · giám khảo.
Subagent **tươi** (không bao giờ nói với người học, **không bao giờ fork**): nghiệm công · phúc khảo ·
trưởng lão mạch · chú giải.

Thiết kế nằm ở thứ **không** truyền đi, không ở thứ truyền đi:

- `thư linh → nghiệm công` **không** mang giáo án/ghi chép — người dạy không được là người cấp chứng nhận
- `giám khảo → phúc khảo` **không** mang tiêu chí — thấy tiêu chí thì hai người soát hết trực giao
- `trưởng môn → trưởng lão` mang `pham_vi_doc` **không** chứa `thu-linh/**` (R9)

Bốn ràng buộc không được vi phạm ở §4.5. Chúng là **đặc tính nhân vật**, viết thẳng vào SKILL.md, không
phải luật để nhớ lúc chạy.

### Kỹ thuật dựng chính: đổi ràng buộc từ lời dặn sang cấu trúc dữ liệu

Lặp ba lần trong dự án, mỗi lần làm ràng buộc kiểm được bằng script (`trang-thai-du-an` §9.1):
`do_tieu_chi` liên kết câu hỏi↔tiêu chí · `bo_tham_so` bộ khớp sẵn thay ba danh sách rời ·
`dau_hieu[]` tách khỏi `nhan_dinh` để không lộ nhãn bậc.

**Gặp một ràng buộc chỉ tồn tại dưới dạng lời dặn thì hỏi: có cấu trúc dữ liệu nào làm nó kiểm được không?**

Hai hệ quả liên quan:
- **Fail an toàn:** `.pham-vi.json` thiếu → **không vai nào đọc được**, không phải mọi vai đọc được (R26).
- **Yếu ở đâu là lỗi của bí kíp, không phải lỗi của hệ** — tiêu chí không phân biệt, đề không ép khẳng
  định đều sửa trong bí kíp, không sửa trong hệ. Nó giữ hệ khỏi phình mỗi lần một quyển viết kém.

### `bi-kip.schema.md` ↔ `kiem-bi-kip.py` là một cặp

`tham-chieu/bi-kip.schema.md` là hợp đồng giữa bên thu sách và bên dạy; §6 liệt kê **đúng** những phép
kiểm tất định mà script thực thi, §7 liệt kê phần cần người phán đoán (script **không** làm).
**Đổi một bên thì đổi bên kia trong cùng một thay đổi**, và thêm fixture + test.

Validator phân ba mức — `L()` lỗi chặn nhập kho · `C()` cảnh báo · `G()` ghi chú — và mức quyết định mã
thoát chỉ là `loi`. Chọn nhầm mức là cách âm thầm nhất làm hỏng luồng thu sách.

Bí kíp có hai hình dạng: `loai: bi-kip` (có `chuong/`, có đồ thị phụ thuộc) và `loai: tan-quyen` (không
có `chuong/`, trường sư phạm nằm thẳng trong `manifest.yaml`). Hai nhánh này rẽ ở `kiem_mot()`.

**Rỗng ≠ vắng** (R13). `chi_nhanh: []` hợp lệ, `sai_lam_pho_bien: []` chỉ là cảnh báo. Đây là defect
đầu tiên của dự án và đã có regression test khoá lại — đừng làm nó tái phát.

### Test

`tests/test_kiem_bi_kip.py` gọi script qua `subprocess` và đọc `--json`, nên nó kiểm cả **giao diện
lệnh** chứ không chỉ hàm bên trong. Ba fixture ở `tests/fixtures/`: `kiem-thu-dac-ta` (bí kíp sạch) ·
`sach-loi` (nhiều lỗi cố ý) · `tan-quyen-mau` (nhánh tàn quyển). Thêm phép kiểm mới thì thêm ca lỗi
vào `sach-loi` và assert theo **mã lỗi** (`ma`), không assert theo thông điệp.

## Thứ tự dựng đã chốt (đặc tả §16 · `trang-thai-du-an` §10)

`bi-kip.schema.md` → `kiem-bi-kip.py` → `giam-dinh.py` + `skills/thu-bi-kip` → **thu một quyển thật** →
`skills/thu-linh` → `nhap-mon`/`dao-tam` → **tự bế quan quyển đó bằng plugin**.

Hai bước in đậm là phép thử của bước ngay trước. Bước cuối là thứ duy nhất chạm được cột *giá trị*.

## Eval — dùng khung `skill-creator`, không tự dựng

Mỗi skill mới cần cả hai (`docs/VAN-DAO-setup-du-an.md` Phần 4):

- **Behavioral eval** — `skills/<tên>/evals/evals.json`, grader chấm từ transcript và bắt buộc có `evidence`.
- **Trigger eval** — 20 câu, 8–10 nên kích hoạt / 8–10 không nên. Ca âm phải là **near-miss** (chia từ
  khoá với skill nhưng thật ra cần thứ khác), chạy mỗi câu 3 lần, chọn bản tốt nhất theo điểm **test**.

Claude có xu hướng **dưới-kích-hoạt** skill, nên `description` phải hơi "đẩy". Chế độ hỏng âm thầm nhất:
câu nghe dễ ("dạy tôi chương 2") làm Claude trả lời thẳng mà không gọi `thu-linh` — không lỗi nào báo,
chỉ là plugin không chạy. Vì vậy giữ `/vd:be-quan` là **lệnh**, không để mặc tự kích hoạt.
