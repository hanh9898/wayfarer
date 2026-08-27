---
name: nhap-mon-ky
description: Ghi nhập môn ký — lời cam kết nhập môn do chính người học tự tay gõ, một phần của nghi thức bái sư. Chỉ chạy khi người học tự gõ lệnh /van-dao:nhap-mon-ky; không skill hay vai nào khác gọi được hộ, không soạn sẵn nội dung để duyệt.
disable-model-invocation: true
---

# Nhập môn ký

## Xong khi

Đã ghi được ít nhất một mục vào `~/.vandao/nhap-mon-ky.md`, nguyên văn đúng những gì người học tự gõ trong chính lượt hội thoại này — không thêm, không bớt, không "viết lại cho hay hơn", không sửa cả lỗi chính tả. Người học có thể gọi lại skill này nhiều lần để thêm mục mới ở phiên sau; mỗi lần là một mục ghi mới, không sửa mục cũ.

## Khi nào skill này không giúp được

- Người học muốn AI viết hộ, gợi ý mẫu câu, hay "chỉnh câu cho mượt" rồi ghi — từ chối thẳng: cam kết chỉ có giá trị khi là lời của chính người học; một câu do người khác (kể cả AI) soạn sẵn để duyệt không còn là cam kết của người học đó nữa. Chờ người học tự gõ lại bằng lời của chính mình, không tự đề xuất nội dung thay.
- Người học chưa gõ gì, chỉ hỏi "nhập môn ký là gì" — trả lời ngắn gọn ý nghĩa (lời cam kết nhập môn tự tay viết), rồi chờ người học tự gõ, không tự đưa ra nội dung mẫu.
- Người học muốn sửa hoặc xoá một mục đã ghi trước đó — skill này chỉ thêm mục mới (ghi nối thêm), không sửa hay xoá mục cũ; nói rõ giới hạn này nếu được hỏi.
- Người học hỏi về các phần khác của bái sư (tên môn phái, vai/mạch, tên 4 vai) — không thuộc phạm vi skill này, dẫn về `/van-dao:nhap-mon`.

## Trình → xác nhận → ghi → kiểm

**Trước khi đọc/ghi `~/.vandao/nhap-mon-ky.md`, xác định đúng thư mục home hiện tại của máy đang chạy** (ví dụ `$env:USERPROFILE` trên Windows, `$HOME` trên POSIX) thay vì giả định sẵn một đường dẫn.

1. **Trình:** yêu cầu người học tự gõ nguyên văn lời cam kết nhập môn của họ ngay trong lượt trả lời tiếp theo — nói rõ đây phải là lời của chính họ, không phải câu AI gợi ý. Sau khi nhận được, lặp lại đúng nguyên văn (không sửa một chữ nào, kể cả lỗi chính tả) để người học soát lại.
2. **Xác nhận:** hỏi đúng một câu ngắn (ví dụ "ghi đúng như trên chứ?"), chờ người học đồng ý. Người học muốn sửa thì quay lại bước 1 với đúng bản họ tự gõ lại — không phải bản AI sửa hộ.
3. **Ghi:** thêm một mục mới vào cuối `~/.vandao/nhap-mon-ky.md` (tạo file nếu chưa có), theo khuôn:

   ```
   ## <thời điểm ghi, ISO 8601 kèm offset múi giờ — vd. 2026-08-27T12:31:57+07:00 hoặc ...Z nếu UTC>

   <nguyên văn lời người học>
   ```

   Chỉ nối thêm — không ghi đè hay xoá các mục đã có.
4. **Kiểm:** đọc lại chính mục vừa ghi từ file, in ra cho người học thấy đúng những gì vừa được lưu. Lệch dù chỉ một chữ so với bản đã xác nhận ở bước 2 thì coi là chưa xong — sửa lại và ghi lại, không để sai lệch tồn tại.

Sau khi ghi xong, nếu người học chưa hoàn tất các phần khác của bái sư (tên môn phái, vai/mạch, tên 4 vai), nhắc một câu ngắn để họ quay lại `/van-dao:nhap-mon` tiếp tục — không bắt buộc, chỉ nhắc.

**Không vai hay skill nào khác được ghi vào `~/.vandao/nhap-mon-ky.md`** — kể cả `nhap-mon`, dù nó là nơi dẫn người học tới đây. `nhap-mon` chỉ được đọc file này để biết đã có mục nào chưa (phục vụ việc kiểm điều kiện kích hoạt bái sư), không bao giờ ghi.

## Nạp `customize.toml`

Skill này chưa phơi field nào trong `customize.toml` — không có tuỳ biến ở phạm vi bản này.

## Vì sao phải tự tay gõ, và khoá ở tầng nào

Một cam kết tự viết trước khi bắt tay vào việc giúp người viết dễ theo đuổi việc đó hơn — hiệu ứng này đến từ chính hành động tự đặt bút, không đến từ nội dung câu chữ. Một câu do người khác soạn sẵn rồi chỉ việc duyệt qua, dù nghe hay tới đâu, không tạo ra cùng hiệu ứng, vì người duyệt không phải người đã tự cam kết.

Vì lý do đó, `disable-model-invocation` được bật ở đúng skill này (không bật ở `nhap-mon`): thuộc tính này áp cho toàn bộ skill, nên phải tách riêng khỏi `nhap-mon` — nếu gộp chung một file, cả phần kiểm ngôn ngữ giao tiếp ở Bước 0 của `nhap-mon` cũng bị khoá theo, trong khi phần đó vẫn cần tự kích hoạt bình thường khi người học gõ `/van-dao:nhap-mon`. Tách skill là cách duy nhất khoá đúng một hành vi (tự ghi nhập môn ký) mà không khoá nhầm hành vi khác.

`disable-model-invocation` khoá đúng một việc, ở đúng tầng cơ chế: skill này không tự nạp được qua khớp `description` — chỉ chạy khi người học tự gõ nguyên văn `/van-dao:nhap-mon-ky`. Đây là cơ chế Claude Code thật, không phải quy ước, nên `nhap-mon` — hay bất kỳ vai/skill nào khác — không tự *kích hoạt* được skill này hộ người học.

Việc còn lại — không soạn sẵn nội dung để người học duyệt qua, không tự ghi thẳng vào `~/.vandao/nhap-mon-ky.md` bằng đường khác — không có cơ chế nền tảng nào chặn; đây là quy ước, giữ bằng chính hướng dẫn trong file này và dòng cấm ghi ở `nhap-mon/SKILL.md`. Một vai AI đọc sai hoặc cố tình bỏ qua hướng dẫn đó — tự ý ghi thẳng file bằng công cụ khác, hoặc tự đề xuất câu cam kết ngay trong lượt trả lời của `nhap-mon` mà không bao giờ gọi tới skill này — vẫn qua mặt được, vì không có gì ở tầng nền tảng ngăn lại. Hai tầng khác nhau: khoá *invocation* là cơ chế đã xác minh; khoá *nội dung* là quy ước, chỉ mạnh bằng việc các skill khác có đọc và tuân theo hướng dẫn hay không.
