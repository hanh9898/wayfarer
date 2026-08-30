# Định dạng file — `thu-bi-kip`

Nạp file này khi tới bước ghi (Bước 5 hoặc Nhánh Đ), không cần đọc trước đó.

## `~/.vandao/tang-kinh/nhap-dang-do/<id>.json`

Vùng ghi riêng của vai này. Mỗi cuốn một file.

```json
{
  "schema": 1,
  "id": "art-of-war",
  "duong_dan": "C:/Users/an/Sach/art-of-war.epub",
  "filename": "art-of-war.epub",
  "pha": "da_giam_dinh",
  "giam_dinh": {
    "format": "epub",
    "extraction_method": "ebooklib",
    "words": 58389,
    "chars": 335990,
    "estimated_tokens": 77852,
    "muc_chi_phi": "vua",
    "pages": 23,
    "pages_label": "spine_items",
    "chapters_detected": 13,
    "chapters_method": "numeric",
    "has_toc": true,
    "images_dropped": 1,
    "cau_truc": "chuoi",
    "cau_truc_nguon": "nguoi_hoc_khai"
  },
  "ghi_luc": "2026-08-28T18:55:37+07:00"
}
```

| Trường | Ghi gì |
|---|---|
| `id` | kebab-case rút từ tên sách (bỏ dấu, khoảng trắng thành gạch nối, chữ thường). Trùng `id` đã có thì thêm hậu tố `-2`, `-3`… |
| `duong_dan` | đường dẫn **tuyệt đối** tới file gốc — con trỏ, không phải bản sao |
| `pha` | luôn `da_giam_dinh` ở bản này. Pha sau đọc trường này để biết bản ghi mới dừng ở giám định, chưa có lớp sư phạm |
| `giam_dinh` | chép nguyên từ `so_lieu` script trả về, cộng ba trường skill tự suy: `muc_chi_phi`, `cau_truc`, `cau_truc_nguon` |
| `muc_chi_phi` | `nhe` · `vua` · `nang` — suy từ `estimated_tokens` so với `ngan_sach_token` đã gộp |
| `cau_truc` | `chuoi` · `mang` |
| `cau_truc_nguon` | `nguoi_hoc_khai` khi người học trả lời rõ · `mac_dinh` khi họ nói không biết. Không có giá trị nào khác ở bản này |
| `ghi_luc` | ISO 8601 kèm offset múi giờ, hoặc `Z` nếu UTC |

**Không bao giờ ghi khoá `text` vào file này** — script không trả nó ra, nên nó không có đường tới đây; đừng tự thêm bằng cách khác.

## `~/.vandao/ban-giao/thu/<id>.json`

Hộp thư chung — mọi vai gửi, mọi vai đọc. Mỗi thư một file.

```json
{
  "schema": 1,
  "tu": "tang-kinh",
  "toi": "truong-mon",
  "hoi": "bao_ban_hong",
  "bi_kip_chi_diem": "art-of-war",
  "ten_sach": "The Art of War",
  "ly_do": "EPUB đổi đuôi thành .pdf; engine không rút được chữ sau khi đã qua kiểm đường dẫn, đuôi và kích thước",
  "trang_thai": "cho"
}
```

| Trường | Ghi gì |
|---|---|
| `id` file | kebab-case từ `ten_sach`, **kèm hậu tố thời gian** (`<ten>-<YYYYMMDDHHmm>.json`). Không có hậu tố thì gửi lại cùng cuốn lần thứ hai sẽ ghi đè thư cũ, mà hộp thư chỉ được ghi thêm |
| `bi_kip_chi_diem` | định danh kebab-case của chỉ điểm cuốn sách đến từ đó. **Chuỗi rỗng khi sách không đến từ chỉ điểm nào** — không đoán |
| `ten_sach` | tên sách đúng như người học gọi, **luôn ghi**. Đường khớp dự phòng khi định danh sinh lại không tra ra dòng nào bên Trưởng môn |
| `ly_do` | sự thật quan sát được: định dạng gì, hỏng ở khâu nào. Không chép chuỗi lỗi thô của engine |
| `trang_thai` | `cho` khi vừa gửi. Vai này không đổi giá trị đó — xử lý thư là việc của bên nhận |

Vai này **không** đọc, không ghi `truong-mon/chi-diem.jsonl` hay `chi-diem-hong.jsonl` dưới bất kỳ hình thức nào.
