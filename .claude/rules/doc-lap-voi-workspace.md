---
paths:
  - "skills/**"
  - "agents/**"
  - "commands/**"
---

# Skill/agent phải tự đủ, không phụ thuộc workspace ngoài

Khi cài đặt thật, chỉ có nội dung bên trong `van-dao/` (thư mục này) được đóng gói và chuyển cho
người dùng — `docs/`, `_bmad/`, `_bmad-output/` ở workspace ngoài **không đi theo**. Một skill/agent
đọc đúng lúc viết, dựa vào ngữ cảnh đang có sẵn kiểu "như đã nêu ở FR32", "theo NFR8", "đặc tả §12.4
nói..." — nhưng người dùng thật chạy skill đó sẽ không có `docs/VAN-DAO-dac-ta-v1.0.md` hay PRD nào
để tra cứu. Khi đó, dòng chữ đó vô nghĩa hoặc gây hiểu lầm.

**Luật:** nội dung bên trong `skills/**`, `agents/**`, `commands/**` không được trích số hiệu
requirement (FR/NFR), số điều/số mục của đặc tả (§...), hay bất kỳ định danh nào chỉ tồn tại trong
tài liệu workspace ngoài. Thay vào đó, viết lại đúng nội dung cần thiết bằng lời tự nhiên, đủ để một
người/agent không có quyền truy cập workspace ngoài vẫn hiểu và làm đúng.

Nơi định danh đó (FR32, NFR8, §12.4...) vẫn nên xuất hiện — nhưng ở phía **workspace**: trong story
spec (`Spec Change Log`, `Design Notes`), trong commit message, trong `_bmad-output/`. Đó là nơi ghi
lại *tại sao* một quyết định được đưa ra; `van-dao/` chỉ cần ghi lại *quyết định đó là gì*.

**Ngoại lệ:** `van-dao/.claude/rules/*.md` (bao gồm chính file này) là công cụ phát triển, không đóng
gói theo plugin — được phép trỏ tới tài liệu workspace ngoài (`eval.md` trỏ
`../../../docs/VAN-DAO-setup-du-an.md` là hợp lệ).

Kiểm nhanh trước khi coi một skill là xong: đọc lại toàn bộ SKILL.md, tự hỏi "nếu tách riêng
`van-dao/` ra một máy khác, không còn workspace này, người đọc có hiểu và làm đúng được không?".
