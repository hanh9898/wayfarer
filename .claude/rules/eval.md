---
paths:
  - "skills/**"
  - "agents/**"
---

# Eval cho skill và agent

Dùng khung eval của `skill-creator`, không tự dựng. Cơ chế, ví dụ `evals.json`, và phần còn lại:
`../../../docs/VAN-DAO-setup-du-an.md` Phần 4.

Mỗi skill mới cần **cả hai loại**, chúng kiểm hai thứ khác nhau:

- **Behavioral eval** — `skills/<tên>/evals/evals.json`. Skill chạy có ra đúng thứ không. Mỗi
  expectation phải có `evidence`: trích đúng chỗ trong transcript làm căn cứ — cùng luật với R19.
- **Trigger eval** — skill có được gọi đúng lúc không. 20 câu, 8–10 nên kích hoạt, 8–10 không nên.

Bốn quyết định không đoán được, áp mỗi lần:

- **Ca âm phải là near-miss** — chia từ khoá với skill nhưng thật ra cần thứ khác.
- **Description phải hơi "đẩy"** — Claude có xu hướng dưới-kích-hoạt skill.
- **Chạy mỗi câu 3 lần**, chia 60% train / 40% test, chọn bản tốt nhất theo điểm **test** để tránh overfit.
- **`/vd:be-quan` giữ là lệnh**, không để mặc tự kích hoạt: câu nghe dễ làm Claude trả lời thẳng mà
  không gọi `thu-linh` — không lỗi nào báo, chỉ là plugin không chạy.
