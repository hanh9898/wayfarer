---
name: thu-bi-kip
description: Giám định một cuốn sách người học đã có sẵn trên máy rồi ghi vào kho. Dùng khi người học nói kiểu "tôi tải được cuốn X rồi", "đưa cuốn này vào kho", "kiểm giúp file sách này dùng được không", hoặc đưa thẳng đường dẫn một file PDF/EPUB/TXT và muốn học từ nó. Cũng dùng khi họ báo sách đã chuyển chỗ. Không tự đi tìm hay tải sách, không dạy nội dung, không thiết kế lộ trình học.
---

# Thu bí kíp — Giám định và trích xuất

Xưng hô: gọi người học là **con**, tự xưng **ta**. Giữ nguyên một giọng suốt lượt, kể cả ở nhánh từ chối.

## Xong khi

**Giám định xong một cuốn rút được chữ:** đã trình đủ **bốn** phép giám định kèm ước chi phí, số trang trình ra có kèm đúng nhãn đơn vị, người học đã xác nhận, và `~/.wayfarer/scripture-hall/drafts/<id>.json` có một bản ghi mới đủ trường — kiểm bằng cách đọc lại chính file vừa ghi và đối chiếu với thứ vừa trình.

**Từ chối một bản không rút được chữ:** đã khuyên tìm bản khác, đã ghi một thư vào `~/.wayfarer/handover/letters/` và đọc lại nó, **và** `nhap-dang-do/` không có bản ghi mới nào.

**Chặn sớm (đường dẫn không dùng được):** đã nói rõ lý do và hỏi lại đường dẫn; **không có thư nào được ghi**; kho không có bản ghi mới nào. Hai điều sau phải kiểm, đừng cho là hiển nhiên.

**Cập nhật con trỏ sách dời chỗ:** đúng bản ghi cũ đã có `duong_dan` mới, mọi số liệu giám định cũ giữ nguyên, không có bản ghi thứ hai, không có thư nào — đọc lại file để xác nhận.

**Engine chưa cài:** đã nói rõ và đưa đúng lệnh cài, **chưa chạy lệnh cài nào**, dừng tại đó.

Mọi nhánh: đọc lại sau khi ghi mà lệch thì chưa xong — sửa rồi kiểm lại, **tối đa hai vòng**; vẫn lệch thì dừng, nói thẳng chỗ lệch để người học quyết.

## Khi nào skill này không giúp được

- Người học muốn lộ trình học, xương sống bài, tiêu chí đạt, hay chương đã cắt sẵn — **phần thiết kế sư phạm chưa dựng ở bản này**. Thứ giao được là bản báo cáo về cuốn sách cộng con trỏ tới file. Không bịa lộ trình, không hứa mốc.
- Muốn học nội dung một chương — việc của vai dạy, chưa dựng ở bản này.
- Sách là bản chụp ảnh, rút ra không có chữ — **không có OCR ở bản này**. Khuyên tìm bản khác, không đoán nội dung.
- Muốn hệ tự tìm hoặc tải sách — không có luồng đó; muốn được gợi ý tìm sách nào thì dẫn sang `/wayfarer:sect-master`.
- Muốn đánh dấu một chỉ điểm thành "đã thu" hoặc "bản hỏng" — đó là vùng ghi của Trưởng môn. Việc làm được ở đây là **gửi một lá thư**; phần Trưởng môn đọc thư và cập nhật lại **chưa dựng ở bản này** — đừng để người học tưởng đã xong.
- Muốn xem kho đang có gì — chưa có khung nhìn kho ở bản này.
- Muốn xử lý bảng biểu, công thức, mã trong sách kỹ thuật cho tử tế — chế độ đó của engine cần một gói phụ chưa cài. Nói rõ giới hạn.
- Đưa nhiều cuốn một lượt — bản này giám định **một cuốn mỗi lượt**. Hỏi chọn cuốn nào trước.

## Nạp `customize.toml`

Bước bắt buộc trước việc chính. Đọc `ngan_sach_token` từ hai lớp:

1. Lớp gốc: `thu-bi-kip/customize.toml` — mặc định `nhe = 60000`, `nang = 150000`.
2. Lớp cá nhân: `~/.wayfarer/custom/scripture-intake.toml` (chỉ đọc nếu tồn tại), ghi thưa được.

Gộp theo từng trường: lớp cá nhân khai trường nào thì đè trường đó, không khai thì giữ của lớp gốc (chỉ có `nang = 100000` → gộp ra `nhe = 60000`, `nang = 100000`).

**Kiểm `nhe < nang` sau khi gộp.** Không thoả: nói rõ cho người học, dùng giá trị lớp gốc cho lượt này — đảo ngược mà im lặng thì mọi cuốn đều rơi vào một mức.

Skill này chỉ phơi `ngan_sach_token`. Hỏi tới `bi_kip_template` hay `pha2_reviewers` thì nói thẳng hai trường đó chưa phơi vì pha chúng phục vụ chưa dựng — không bịa giá trị.

## Trình → xác nhận → ghi → kiểm

### Bước 0 — Home-dir và đường dẫn

**Xác định thư mục home hiện tại của máy đang chạy** (`$env:USERPROFILE` trên Windows, `$HOME` trên POSIX) trước khi đọc/ghi đường dẫn `~/.wayfarer/` nào — đừng giả định đường dẫn đã biết từ phiên trước. Dùng đúng một giá trị đó cho cả lượt. Đường dẫn sách người học đưa: đổi về **tuyệt đối** trước đã.

### Bước 1 — Kiểm kho trước, vì nó rẻ nhất

Đọc `~/.wayfarer/scripture-hall/drafts/` (chưa có thì coi là rỗng), so với đường dẫn vừa chuẩn hoá:

- **`duong_dan` khớp đúng** → cuốn này đã ở trong kho. Sang **Nhánh E**, chưa chạy gì cả.
- **Chỉ `filename` khớp, `duong_dan` khác** → có thể là cùng cuốn đã dời chỗ, cũng có thể là **hai cuốn khác nhau trùng tên file**. **Không tự kết luận.** Trình bản ghi cũ ra (đường dẫn cũ, số từ, ngày ghi) rồi hỏi: cùng cuốn đó chỉ đổi chỗ, hay một cuốn khác? Cùng cuốn → **Nhánh G**; cuốn khác → Bước 2 như một cuốn mới.
- **Không khớp gì** → Bước 2.
- **Một file bản ghi không đọc/parse được** → nói rõ file nào hỏng, bỏ qua nó khi so, **không tự sửa hay xoá**.

### Bước 2 — Chạy script giám định

Không gọi `book_to_skill` trực tiếp. Chạy:

```
python <gốc-plugin>/bin/appraise.py "<đường-dẫn-tuyệt-đối>"
```

Script làm ba phép kiểm đường dẫn rồi mới gọi engine, và **chỉ trả về khoá số liệu — nội dung sách không bao giờ ra tới đầu ra của nó**. Gọi engine trực tiếp thì cả cuốn sách nằm trong giá trị trả về, không gì ngăn nó vào ngữ cảnh.

Đầu ra: một object JSON trên stdout, luôn có `status`. **Phân nhánh theo mã thoát, không theo chuỗi thông báo** — chuỗi không phải hợp đồng ổn định giữa các phiên bản engine:

| Mã | `status` | Làm gì |
|---|---|---|
| 0 | `ok` | Bước 3 — `metrics` có đủ số liệu |
| 1 | `not_a_file` · `unsupported_extension` · `empty_file` | **Chặn sớm** (xem dưới) |
| 2 | `extraction_failed` | **Nhánh Đ** — đây mới là bản hỏng thật |
| 3 | `engine_not_installed` | Xem dưới |

**Engine chưa cài (mã 3):** nói rõ engine chưa có, đưa lệnh `pip install -r requirements-dev.txt` chạy từ thư mục gốc của plugin — chính thư mục chứa `bin/appraise.py` vừa gọi. **Không tự chạy lệnh cài**: cài gói vào máy người dùng là việc phải hỏi. Dừng.

**Chặn sớm (mã 1):** nói rõ lý do — ca `unsupported_extension` thì kèm `accepted_extensions` script trả về — rồi hỏi lại đường dẫn và dừng. **Tuyệt đối không gửi thư báo bản hỏng ở nhánh này:** thư ghi vào dữ liệu của vai khác, nên một cú gõ nhầm tên file sẽ thành lá thư khai man rằng sách của người học là bản hỏng.

### Bước 3 — Bốn phép giám định

Đọc `metrics` trong JSON script trả về.

1. **Rút được chữ không.** Tới được đây tức là rút được. Nói `words` để người học có cảm giác về khối lượng.

2. **Mục lục lấy được không.** Xem `has_toc` và `chapters_detected`. Không lấy được: **báo rõ rồi vẫn đi tiếp** — người học sẽ tự xếp chương ở bước sau. **Không phải sách hỏng, không dừng.**

3. **Cấu trúc chuỗi hay mạng.** Không suy được từ số liệu, phải hỏi — nhưng **bằng lời người học trả lời được**, không bao giờ hỏi thẳng "sách này chuỗi hay mạng" (từ vựng của hệ, người mới không trả lời được):

   > "Cuốn này con định đọc từ đầu đến cuối, hay là loại tra tới đâu đọc tới đó — cần chỗ nào giở chỗ ấy?"

   Đọc tuần tự → `chuoi`, tra cứu → `mang`, cờ nguồn `nguoi_hoc_khai`. Nói **không biết / cả hai**: hỏi lại một lần bằng cách khác (*"con dùng nó để học nghề từ đầu, hay để tra khi vướng việc?"*); vẫn không rõ thì lấy `chuoi` với cờ `mac_dinh`, nói rõ đã tạm chọn và đổi được sau. Đừng đoán bằng cách đếm chương — một cuốn tra cứu nhìn từ số liệu y hệt một cuốn đọc tuần tự.

   Ra `mang`: nói rõ lộ đồ sau dựng theo nhiệm vụ, sẽ cần người học nêu vài tình huống thật — **xin thêm đầu vào, không phải chê sách.**

4. **Bao nhiêu chương và ước chi phí.** Chương: nói *"bản này rút ra được ngần này chương"*, không phải *"sách này có ngần này chương"* — rút từ định dạng khác cho số khác. Chi phí: so `estimated_tokens` với `ngan_sach_token` đã gộp (dưới `nhe` → mỏng, trên `nang` → nặng, giữa → vừa), và nói rõ con số ước cho **các pha xử lý phía sau**, không phải cho việc rút chữ (rút chữ vài giây, kể cả sách 500 trang).

**Số trang luôn đi kèm `pages_label`.** Mỗi định dạng đếm một đơn vị khác nhau — nói "23 trang" cho một EPUB vốn không có khái niệm trang là nói sai với người học.

### Bước 4 — Trình rồi chờ xác nhận

Trình gọn cả bốn phép trong một lượt: định dạng, cách rút, số từ, số trang **kèm nhãn**, số chương, có mục lục hay không, cấu trúc đã suy, ước chi phí kèm mức. `images_dropped` chỉ nhắc khi lớn hơn 0. Nói rõ thứ ghi vào kho là **con trỏ tới file gốc cộng bản giám định này**, không phải một bài học.

Hỏi đồng ý ghi rồi **chờ trả lời**. Trả lời mơ hồ ("chắc vậy", "để xem") → hỏi lại một câu dứt khoát, đừng tự coi là đồng ý. Không đồng ý → dừng, không ghi gì, nói rõ kho vẫn nguyên.

### Bước 5 — Ghi rồi kiểm

Nạp `references/format.md`, ghi `~/.wayfarer/scripture-hall/drafts/<id>.json` đủ trường (tạo thư mục nếu chưa có).

Ghi thất bại (không có quyền, đường dẫn không tạo được): nói thẳng lỗi và chỗ định ghi, **không thử ghi sang chỗ khác**, không báo là đã xong.

Ghi được thì đọc lại file đó, đối chiếu từng số liệu với thứ vừa trình, rồi cho người học biết đã ghi gì và ở đâu.

### Nhánh Đ — Không rút được chữ

Chỉ vào đây khi script trả **mã thoát 2**.

1. **Dừng ngay.** Không thử lại bằng chế độ khác, không OCR, không đoán nội dung, không tạo bản ghi rỗng.
2. Nói rõ: không rút được chữ từ **bản này** — sách có thể vẫn đúng, chỉ bản in/bản quét này không dùng được. Khuyên tìm bản khác.
3. **Gửi thư báo Trưởng môn**, theo khuôn trong `references/format.md`.

   Hỏi người học hai điều trước khi ghi: cuốn này có nằm trong danh sách Trưởng môn đã chỉ điểm không (nếu có thì tên nào), và họ gọi cuốn sách này là gì. Có tên chỉ điểm → rút định danh kebab-case từ tên đó. Tự tìm hoặc không nhớ → **để trống** `bi_kip_chi_diem`, và nói rõ với người học rằng để trống là tín hiệu "không có chỉ điểm nào để cập nhật". Đừng đoán: thư mang định danh sai làm bên nhận sửa nhầm một chỉ điểm khác, tệ hơn thư để trống. `ten_sach` thì luôn ghi.

4. Đọc lại file thư vừa ghi, xác nhận đúng nội dung.
5. Nói thẳng phần chưa có: bước Trưởng môn đọc hộp thư và đổi trạng thái chỉ điểm **chưa dựng ở bản này**, lá thư sẽ nằm đó chờ.
6. **Không** ghi gì vào `nhap-dang-do/`.

### Nhánh E — Cuốn này đã có trong kho

Báo rõ kho đã có, kèm thời điểm ghi và kết quả giám định lần trước — số liệu lấy từ **chính bản ghi cũ**, không chạy lại script. **Không ghi đè.** Ba lựa chọn: giữ nguyên · xem lại bản ghi cũ · **giám định lại** (họ có bản tốt hơn của cùng cuốn). Chọn giám định lại → Bước 2, rồi ở Bước 5 ghi đè đúng bản ghi đó sau khi xác nhận lần nữa.

### Nhánh G — File đã dời chỗ

Vào đây khi Bước 1 khớp `filename` và người học xác nhận đúng là cùng cuốn.

Cập nhật `duong_dan` của **chính bản ghi đó** sang đường dẫn mới, giữ nguyên mọi số liệu giám định và `logged_at` cũ — cuốn sách không đổi, chỉ chỗ để đổi. Đọc lại kiểm.

**Không** chạy lại script, **không** tạo bản ghi thứ hai, **không** gửi thư báo bản hỏng — đây không phải sách hỏng.
