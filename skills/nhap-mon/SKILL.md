---
name: nhap-mon
description: Bái sư nhập môn Vấn Đạo. Dùng khi người học gõ /van-dao:nhap-mon — lần đầu cài plugin, muốn kiểm tra/đặt lại ngôn ngữ giao tiếp, hoặc chưa hoàn tất bái sư (đặt tên môn phái, khai vai/mạch, đặt tên 4 vai đồng hành). Bước đầu tiên của mọi hành trình học.
---

# Nhập môn

## Xong khi

Ngôn ngữ giao tiếp (`communication_language`) đã được xác nhận (Bước 0), **và** nghi thức bái sư đã kích hoạt — nghĩa là hồ sơ có đủ tên môn phái, vai, mạch, tên riêng cho 4 vai nói-với-người-học, **và** một bản ghi nhập môn ký do chính người học tự gõ (`~/.vandao/nhap-mon-ky.md` có ít nhất một mục). Thiếu bất kỳ phần nào trong số này thì nói rõ đang dừng ở đâu, không coi là đã xong, không giả vờ bái sư đã kích hoạt khi chưa đủ.

Chỉ điểm (Trưởng môn gọi tên sách cụ thể cho người học đi tìm) là bước nối tiếp ngay sau bái sư — sau khi đủ bốn phần dưới đây, dẫn người học sang `/van-dao:truong-mon` (xem Bước 6).

## Khi nào skill này không giúp được

- Người học đã bái sư xong (đủ hồ sơ + nhập môn ký), chỉ muốn tiếp tục học một bí kíp đang dở — dùng `/van-dao:be-quan` thay vì gọi lại `nhap-mon`.
- Người học muốn được chỉ sách cụ thể ngay sau khi bái sư xong (chỉ điểm) — không phải việc của `nhap-mon`, dẫn sang `/van-dao:truong-mon`, không tự bịa tên sách để lấp chỗ trống.
- Người học hỏi về đột phá cảnh giới/lên cấp, hay bất kỳ tính năng nào thuộc phần sau của lộ trình — chưa dựng ở bản này, trả lời rõ "chưa hỗ trợ ở bản này", không đoán liều, không im lặng bỏ qua — dù đang hỏi giữa lúc bái sư hay bất cứ lúc nào khác trong hội thoại.
- Người học muốn nhờ chính skill này (hay bất kỳ vai nào) viết/soạn sẵn nội dung nhập môn ký để duyệt — không làm được dưới bất kỳ hình thức nào, kể cả chỉ gợi ý mẫu câu; từ chối và dẫn sang `/van-dao:nhap-mon-ky` để người học tự gõ.

## Trình → xác nhận → ghi → kiểm

Bước 0 không ghi trạng thái mới nào (chỉ đọc `userConfig` đã có sẵn). Từ Bước 2 trở đi (đặt tên môn phái, khai vai/mạch, đặt tên 4 vai), mỗi lần ghi vào `~/.vandao/truong-mon/ho-so.json` đều theo đúng trình tự: **trình** nội dung sắp ghi cho người học xem lại → **xác nhận** đồng ý → **ghi** (chỉ cập nhật đúng trường liên quan, không ghi đè âm thầm cả file — trường khác đã có trong hồ sơ giữ nguyên) → **kiểm** bằng cách đọc lại chính file vừa ghi. Đọc lại thấy lệch với thứ vừa xác nhận thì quay lại bước trình với đúng chỗ lệch làm ngữ cảnh, không coi là đã ghi xong.

Việc ghi nhập môn ký (`~/.vandao/nhap-mon-ky.md`) theo đúng bốn bước trên nhưng nằm ở skill riêng `nhap-mon-ky` — xem Bước 3 bên dưới, `nhap-mon` không bao giờ tự ghi file đó.

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

  Đây là lệnh Claude Code cấp người dùng — skill không tự chạy được hộ. Sau khi người học chạy lệnh và đặt giá trị, gọi lại `/van-dao:nhap-mon` để tiếp tục.

**Không giả định Claude Code tự động hỏi khi bật plugin lần đầu** — đường cài qua CLI không kèm `--config` chỉ in cảnh báo, không chặn/hỏi (đã verify). Bước 0 này là nơi duy nhất chủ động kiểm tra và nhắc, không trông chờ cơ chế nào khác làm hộ.

## Lưu ý xuyên suốt bái sư

Từ Bước 1 trở đi, bất cứ lúc nào người học hỏi về đột phá cảnh giới/lên cấp giữa lúc đang bái sư, trả lời ngay và rõ "chưa hỗ trợ ở bản này" — không đoán liều, không im lặng bỏ qua — rồi quay lại đúng bước đang dở, không để câu hỏi đó làm lạc hướng cả cuộc trò chuyện.

## Bước 1 — Kiểm hồ sơ bái sư đã có tới đâu

**Trước khi đọc/ghi bất kỳ đường dẫn nào dưới `~/.vandao/` trong phiên này, xác định đúng thư mục home hiện tại của máy đang chạy** (ví dụ `$env:USERPROFILE` trên Windows, `$HOME` trên POSIX) thay vì giả định sẵn một đường dẫn — không có gì đảm bảo con đường đó luôn giống lần trước. Dùng đúng một giá trị đã xác định cho toàn bộ các bước còn lại của phiên này.

Đọc file `~/.vandao/truong-mon/ho-so.json` (nếu có) và file `~/.vandao/nhap-mon-ky.md` (nếu có — chỉ đọc, không bao giờ ghi vào file này, xem Bước 3) để biết bốn phần dưới đây đã xong phần nào:

| Phần | Đã xong khi |
|---|---|
| Tên môn phái | `ho-so.json` có trường `ten_mon_phai` không rỗng |
| Nhập môn ký | `nhap-mon-ky.md` tồn tại và có ít nhất một mục ghi |
| Vai + mạch | `ho-so.json` có cả `vai` và `mach` không rỗng |
| Tên 4 vai | `ho-so.json` có `ten_vai` đủ bốn khoá: `truong-mon`, `tang-kinh-truong-lao`, `thu-linh`, `giam-khao` |

- **Đủ cả bốn phần:** nghi thức bái sư đã kích hoạt từ trước. Không lặp lại bất kỳ câu hỏi nào ở các bước dưới đây — tóm tắt lại hồ sơ hiện có (tên môn phái, vai, mạch, tên 4 vai) cho người học, nói rõ đã bái sư xong, rồi dừng ở đây (xem Bước 6 để biết cách trả lời phần "bước tiếp theo").
- **Thiếu một hay nhiều phần:** tiếp tục các bước dưới đây, nhưng **bỏ qua phần đã xong** — không hỏi lại thứ đã có sẵn trong hồ sơ. Thứ tự ưu tiên khi nhiều phần cùng thiếu: tên môn phái → nhập môn ký → vai + mạch → tên 4 vai.

## Bước 2 — Đặt tên môn phái

Bỏ qua bước này nếu `ten_mon_phai` đã có trong hồ sơ (xem Bước 1).

Hỏi người học muốn đặt tên môn phái của mình là gì — một cái tên gọi vui để hồ sơ có bản sắc, không mang ý nghĩa kỹ thuật gì. Người học tự nhập tự do, không giới hạn hình thức.

- Trình: nhắc lại đúng nguyên văn tên vừa nhận để người học soát (đề phòng gõ nhầm).
- Xác nhận: hỏi lại một câu ngắn, đợi người học đồng ý.
- Ghi: lưu vào trường `ten_mon_phai` trong `~/.vandao/truong-mon/ho-so.json` (tạo file/thư mục nếu chưa có; nếu file đã tồn tại thì chỉ thêm/đổi đúng trường này, giữ nguyên các trường khác).
- Kiểm: đọc lại file vừa ghi, xác nhận đúng tên vừa lưu.

Đổi tên môn phái sau này (nếu người học muốn) chỉ thay giá trị trường này — không tạo hồ sơ mới, không đổi tên thư mục hay file nào; hồ sơ không được phép mất theo tên.

## Bước 3 — Dẫn ghi nhập môn ký

Bỏ qua bước này nếu `~/.vandao/nhap-mon-ky.md` đã có ít nhất một mục (xem Bước 1).

Nhập môn ký là một lời cam kết nhập môn do chính người học tự tay gõ — không phải mẫu câu do AI soạn sẵn rồi người học chỉ việc duyệt qua. Nói rõ lý do với người học: cam kết chỉ dẫn dắt được hành trình khi là lời tự viết của chính người viết; một câu do người khác soạn hộ, dù nghe hay tới đâu, không tạo ra cùng hiệu ứng.

Hướng dẫn người học chạy đúng lệnh sau:

```
/van-dao:nhap-mon-ky
```

Đây là skill riêng, **chỉ chạy được khi chính người học tự gõ lệnh này** — `nhap-mon` (skill hiện tại) không tự gọi hộ được, và tuyệt đối không được soạn sẵn nội dung nhập môn ký dưới bất kỳ hình thức nào, kể cả chỉ gợi ý một mẫu câu "cho dễ bắt đầu". Người học yêu cầu "viết hộ một câu" thì từ chối thẳng, giải thích đúng lý do trên, rồi vẫn dẫn về lệnh trên để họ tự gõ.

Người học có thể chạy lệnh này ngay trong hội thoại tiếp theo, hoặc để dành cho phiên sau — hồ sơ và tiến độ bái sư không mất giữa các bước. Sau khi chạy xong, gọi lại `/van-dao:nhap-mon` để tiếp tục các bước còn lại; Bước 1 sẽ tự nhận ra phần này đã xong, không hỏi lại.

Không có gì bắt buộc người học phải làm xong bước này trước khi sang Bước 4/5 nếu họ muốn tiếp tục luôn — chỉ cần nhớ nhắc rõ ở Bước 6 rằng nghi thức bái sư vẫn CHƯA kích hoạt cho tới khi bước này xong.

## Bước 4 — Khai vai + mạch

Bỏ qua bước này nếu cả `vai` và `mach` đã có trong hồ sơ (xem Bước 1).

Hỏi người học: đã biết mình muốn luyện gì (vai + mạch) chưa?

**Nhánh đã biết:** để người học tự khai thẳng cả vai (nghề nghiệp/vai trò đang làm, ví dụ tester, BA, lập trình viên) và mạch (kỹ năng/hướng muốn luyện, ví dụ kiểm thử phần mềm, phân tích nghiệp vụ) — không có danh sách cố định để chọn, người học nói gì ghi đúng nấy.

**Nhánh chưa biết** (người học nói "chưa biết"/"chưa rõ"/ý tương đương):

1. Hỏi VAI trước — đúng tinh thần câu "ngươi làm nghề gì", **không hỏi mạch trước**: mạch là khái niệm của hệ, người mới không trả lời được.
2. Từ vai vừa nhận, gợi ý một mạch phù hợp, kèm đúng mức tin cậy của gợi ý:
   - Đã có dữ liệu thật từ nhiều người học cùng vai (khoảng từ 5 người trở lên) → gợi ý kèm số liệu cụ thể.
   - Chưa có dữ liệu thật nhưng có nguồn tham chiếu cụ thể để dựa vào → gợi ý kèm nói rõ nguồn đó.
   - Không có cả hai (đúng trạng thái hiện tại, kho còn mới) → gợi ý kèm cảnh báo rõ ràng: đây là suy đoán, chưa phải dữ liệu thật.
   - Dù ở mức nào, luôn kèm lối "tự nhập mạch khác nếu gợi ý không hợp".
3. Đưa gợi ý (kèm cờ nguồn ở trên) cho người học chọn, hoặc để họ tự nhập mạch khác — **không tự chốt mạch mà không hỏi lại người học**.

- Trình: nhắc lại đúng vai + mạch (và nguồn: tự khai hay suy từ vai) vừa chốt.
- Xác nhận: hỏi lại, đợi người học đồng ý trước khi ghi.
- Ghi: lưu `vai`, `mach`, và `mach_nguon` (`tu_khai` nếu người học tự khai thẳng hoặc tự nhập ở nhánh chưa biết; `suy_tu_vai` nếu người học chọn đúng gợi ý suy từ vai) vào `~/.vandao/truong-mon/ho-so.json`.
- Kiểm: đọc lại file, xác nhận đúng vai/mạch/nguồn vừa lưu.

## Bước 5 — Đặt tên 4 vai

Bỏ qua bước này nếu `ten_vai` đã đủ bốn khoá trong hồ sơ (xem Bước 1).

Chỉ đặt tên cho đúng bốn vai trực tiếp nói chuyện với người học: Trưởng môn, Tàng kinh trưởng lão, Thư linh, Giám khảo. Không hỏi tên cho bất kỳ vai nào khác — các vai còn lại không bao giờ hiện ra trước người học, đặt tên cho chúng không có ý nghĩa gì với người học.

Gợi ý sẵn vài tên cho mỗi vai (ví dụ minh hoạ, không phải danh sách bắt buộc):

- Trưởng môn: "Bạch Vân", "Huyền Cơ"
- Tàng kinh trưởng lão: "Mặc Thư", "Tàng Vân"
- Thư linh: "Nhã Tri", "Minh Tuệ"
- Giám khảo: "Thanh Nghiêm", "Chính Trực"

Người học chọn một trong các gợi ý, tự nhập tên khác, hoặc giữ nguyên tên vai gốc — cả ba đều hợp lệ, **không ép chọn từ danh sách**.

- Trình: liệt kê lại đủ bốn cặp (tên vai gốc → tên người học chọn) để người học soát một lượt.
- Xác nhận: hỏi lại, đợi đồng ý, cho sửa nếu người học đổi ý ở bất kỳ vai nào.
- Ghi: lưu vào `ten_vai` trong `~/.vandao/truong-mon/ho-so.json` với đúng bốn khoá kỹ thuật: `truong-mon`, `tang-kinh-truong-lao`, `thu-linh`, `giam-khao`.
- Kiểm: đọc lại file, xác nhận đủ bốn khoá và đúng tên vừa lưu.

## Bước 6 — Xác nhận bái sư

Đọc lại hồ sơ và `nhap-mon-ky.md` một lần nữa (giống cách kiểm ở Bước 1):

- **Đủ cả bốn phần** (tên môn phái, nhập môn ký, vai + mạch, tên 4 vai): nói rõ nghi thức bái sư đã kích hoạt, tóm tắt lại toàn bộ hồ sơ vừa xong cho người học bằng đúng tên 4 vai họ vừa đặt. Dẫn tường minh sang bước tiếp theo: mời người học tự gõ `/van-dao:truong-mon` để nhận chỉ điểm sách cụ thể — không tự động chuyển sang, không tự gọi hộ; nếu người học hỏi luôn "vậy giờ học gì", trả lời bằng đúng lời mời gọi lệnh trên, không tự bịa tên sách ngay tại đây.
- **Thiếu đúng phần nhập môn ký, các phần còn lại đã đủ:** nói rõ **nghi thức bái sư CHƯA kích hoạt** — không giả vờ đã xong dù vai/mạch/tên 4 vai đã có đủ — nhắc lại đúng một lần lệnh `/van-dao:nhap-mon-ky`, nhưng không chặn cuộc trò chuyện dừng lại ở đây nếu người học chưa muốn làm ngay.
- **Còn thiếu phần khác** (tên môn phái, hoặc vai/mạch, hoặc tên 4 vai): chưa tới lúc xác nhận — quay lại đúng bước tương ứng ở trên trước.
