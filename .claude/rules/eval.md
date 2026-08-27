---
paths:
  - "skills/**"
  - "agents/**"
---

# Eval cho skill và agent

Dùng khung eval của `skill-creator`, không tự dựng. Cơ chế, ví dụ `evals.json`, và phần còn lại:
`../../../docs/VAN-DAO-setup-du-an.md` Phần 4.

**Thời điểm: khi viết skill đó, không dồn sang sau.** Đặc tả §16 ("ba thứ dựng xuyên suốt, không
có bước riêng") đã nói rõ — `evals/` đi cùng từng skill lúc skill đó được viết, không phải một giai
đoạn hình thức hoá riêng dựng sau khi đã có nhiều skill/vertical slice. Bắt đầu **nhẹ** là đủ để
coi một skill "xong nháp": vài kịch bản (2-3) khớp I/O matrix của chính story đó, chưa cần đạt độ
nghiêm ở dưới ngay. Nâng lên mức đầy đủ (20 câu trigger, 60/40 train/test) có thể dời tới một mốc cụ
thể — ví dụ trước khi chia sẻ/phát hành plugin — không dời vô thời hạn. Căn cứ: nghiên cứu
`_bmad-output/planning-artifacts/research/technical-quy-trinh-eval-khi-viet-skill-claude-ski-2026-08-27/research.md`
(quy trình chính thức `skill-creator` của Anthropic tự thực hiện đúng nhịp "viết nháp → vài eval
nhỏ ngay → lặp lại", không có tiền lệ nào ủng hộ hoãn eval tới vertical slice).

Mỗi skill mới cần **cả hai loại** (mức nhẹ ngay lúc viết, nâng dần lên mức đầy đủ theo đúng nhịp ở
trên), chúng kiểm hai thứ khác nhau:

- **Behavioral eval** — `skills/<tên>/evals/evals.json`. Skill chạy có ra đúng thứ không. Mỗi
  expectation phải có `evidence`: trích đúng chỗ trong transcript làm căn cứ — cùng luật với R19.
- **Trigger eval** — skill có được gọi đúng lúc không. 20 câu, 8–10 nên kích hoạt, 8–10 không nên.

Bốn quyết định không đoán được, áp mỗi lần:

- **Ca âm phải là near-miss** — chia từ khoá với skill nhưng thật ra cần thứ khác.
- **Description phải hơi "đẩy"** — Claude có xu hướng dưới-kích-hoạt skill.
- **Chạy mỗi câu 3 lần**, chia 60% train / 40% test, chọn bản tốt nhất theo điểm **test** để tránh overfit.
- **`/vd:be-quan` giữ là lệnh**, không để mặc tự kích hoạt: câu nghe dễ làm Claude trả lời thẳng mà
  không gọi `thu-linh` — không lỗi nào báo, chỉ là plugin không chạy.
