---
name: nhap-mon
description: Bái sư nhập môn Vấn Đạo. Dùng khi người học gõ /vd:nhap-mon — lần đầu cài plugin, hoặc muốn kiểm tra/đặt lại ngôn ngữ giao tiếp. Bước đầu tiên của mọi hành trình học.
---

# Nhập môn

## Xong khi

Ngôn ngữ giao tiếp (`communication_language`) đã được xác nhận — hoặc đã có giá trị và được dùng ngay, hoặc chưa có và người học đã được hướng dẫn rõ cách đặt. Bản này (Story 1.1) dừng lại ở đây; bái sư (đặt tên môn phái, khai vai/mạch, đặt tên 4 vai) là phần nối tiếp của một story sau, chưa có trong bản này.

## Khi nào skill này không giúp được

- Người học đã bái sư xong (đã có hồ sơ), chỉ muốn tiếp tục học một bí kíp đang dở — dùng `/vd:be-quan` thay vì gọi lại `nhap-mon`.
- Người học hỏi về đột phá cảnh giới hay các tính năng thuộc Vòng 3/4 — chưa dựng ở bản này, trả lời rõ "chưa hỗ trợ ở bản này", không đoán liều.

## Trình → xác nhận → ghi → kiểm

Bước 0 dưới đây không ghi trạng thái mới nào (chỉ đọc `userConfig` đã có sẵn) — trình tự "trình → xác nhận → ghi → kiểm" đầy đủ (khai vai/mạch, ghi nhập môn ký) áp dụng từ bước bái sư của story sau, không áp dụng cho bước 0 này.

## Nạp `customize.toml`

Skill này chưa phơi field nào trong `customize.toml` — không có tuỳ biến ở phạm vi bản này.

## Bước 0 — Kiểm ngôn ngữ giao tiếp

Giá trị `communication_language` người học đã cấu hình (Claude Code tự thế chỗ vào đây lúc nạp skill,
không phải giá trị tĩnh khai trong `plugin.json`):

```
${user_config.communication_language}
```

**Không đọc trực tiếp `.claude-plugin/plugin.json` để lấy giá trị này** — file đó chỉ khai *schema*
(kiểu, tiêu đề, `default` gợi ý), không phải giá trị người học thật sự đã đặt; giá trị thật nằm ở
`pluginConfigs["van-dao@van-dao"].options` trong `settings.json` của Claude Code, và cách đọc đúng
là qua chỗ thế chỗ `${user_config.communication_language}` ở trên — đã verify chạy thật: đọc
thẳng `plugin.json` luôn thấy `default: "Vietnamese"` bất kể người học đã cấu hình gì, nên không phân
biệt được "chưa đặt" với "đã đặt đúng bằng giá trị mặc định".

- **Dòng thế chỗ ở trên hiện ra một giá trị ngôn ngữ cụ thể** (vd. `Vietnamese`, `English` — khác
  với chuỗi placeholder `${user_config.communication_language}` y hệt bên trên): đó là giá trị đã
  cấu hình — dùng ngay cho mọi phản hồi tiếp theo trong phiên này. Không hỏi lại người học — kể cả
  ở phiên sau, vì đây là cấu hình plugin bền, Claude Code tự nạp lại.
- **Dòng thế chỗ ở trên trống, hoặc vẫn còn nguyên văn placeholder `${user_config.communication_language}`
  chưa được thế** (cả hai đều nghĩa là chưa có giá trị nào được cấu hình — cơ chế thế chỗ có thể để
  trống hoặc giữ nguyên cú pháp khi field chưa set, không giả định cố định là dạng nào): nói rõ với
  người học là chưa đặt ngôn ngữ giao tiếp, và hướng dẫn chạy:

  ```
  /plugin configure van-dao@van-dao
  ```

  Đây là lệnh Claude Code cấp người dùng — skill không tự chạy được hộ. Sau khi người học chạy lệnh và đặt giá trị, gọi lại `/vd:nhap-mon` để tiếp tục.

**Không giả định Claude Code tự động hỏi khi bật plugin lần đầu** — đường cài qua CLI không kèm `--config` chỉ in cảnh báo, không chặn/hỏi (đã verify). Bước 0 này là nơi duy nhất chủ động kiểm tra và nhắc, không trông chờ cơ chế nào khác làm hộ.
