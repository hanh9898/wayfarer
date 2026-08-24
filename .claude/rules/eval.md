---
paths:
  - "skills/**"
  - "agents/**"
---

# Eval cho skill và agent — dùng khung `skill-creator`, không tự dựng

Anthropic đã phát hành khung eval trong `skill-creator` (`run_eval.py` · `run_loop.py` ·
`improve_description.py` · `aggregate_benchmark.py`, ba agent chấm, eval viewer). Chi tiết:
`docs/VAN-DAO-setup-du-an.md` Phần 4.

Mỗi skill mới cần **cả hai loại**, chúng kiểm hai thứ khác nhau:

**Behavioral eval** — skill chạy có ra đúng thứ không. Đặt ở `skills/<tên>/evals/evals.json`.
Grader chấm từ transcript và mỗi expectation phải có `evidence` — trích đúng chỗ trong transcript
làm căn cứ. Luật này trùng R19 của đặc tả: bằng chứng trước khẳng định.

**Trigger eval** — skill có được gọi đúng lúc không. 20 câu, 8–10 nên kích hoạt và 8–10 không nên.
Hai luật viết ca:

- **Ca âm phải là near-miss** — chia từ khoá với skill nhưng thật ra cần thứ khác. *"đọc file PDF này
  rồi tóm tắt"* là ca âm tốt cho `thu-bi-kip`; *"viết hàm fibonacci"* không kiểm được gì.
- **Description nên hơi "đẩy"** — Claude có xu hướng dưới-kích-hoạt skill. Nói rõ *"dùng bất cứ khi nào
  người dùng nhắc tới X, kể cả khi họ không gọi tên nó ra"*.

Chạy mỗi câu **3 lần**, chia 60% train / 40% test, **chọn bản tốt nhất theo điểm test** chứ không theo
train.

## Chế độ hỏng âm thầm nhất

Claude chỉ tra skill cho việc nó không tự xử được dễ dàng. Câu *"dạy tôi chương 2 quyển này"* nghe rất
dễ, nên Claude có thể trả lời thẳng mà **không gọi `thu-linh`** — người học nhận một bài giảng bình
thường thay vì luồng F0→F2 có giáo án và nghiệm công. Không lỗi nào báo, chỉ là plugin không chạy.

Vì vậy `/vd:be-quan` giữ là **lệnh**, an toàn hơn để mặc tự kích hoạt. Trigger eval đo được điều này.

## Điểm áp thẳng sang bí kíp

Khái niệm **"assertion không phân biệt"** của khung eval áp đúng cho `tieu_chi_dat`: một tiêu chí mà
người **chưa đọc chương** cũng đạt được thì nó không đo gì cả. Hiệu chuẩn κ ở §10 đặc tả **không** bắt
được lỗi này — κ chỉ đo người và model có chấm khớp nhau không, và hai bên khớp hoàn hảo trên một tiêu
chí vô dụng vẫn là khớp.

Phép kiểm rẻ, làm một lần cho mỗi bí kíp mới ở pha 2: cho `nghiem-cong` chấm một bài viết bởi người
chưa đọc chương. Đạt → tiêu chí đó vứt đi, viết lại.
