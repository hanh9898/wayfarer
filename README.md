# Vấn Đạo

Biến sách bạn **đã có** thành lộ trình học có người kèm.

Bạn đưa vào một quyển PDF hoặc EPUB. Vấn Đạo phân giải nó thành **lớp sư phạm** — mục tiêu từng chương, giả định nền, tiêu chí đạt, khuôn câu hỏi — rồi dẫn bạn học từng chương và ra đề khảo thí ở cuối quyển.

**Kho sách là của riêng bạn.** Repo này không chứa quyển nào; nội dung sách nằm trên máy bạn.

## Trạng thái

**Chưa dùng được.** Đặc tả xong, một validator chạy được, chưa có skill nào. Xem `../docs/VAN-DAO-trang-thai-du-an.md`.

## Thế giới quan

Bạn là **phàm nhân** bái sư gia nhập **tông môn**. Sách là **bí kíp**, kho sách là **tàng kinh các**. Tám vai hướng dẫn: trưởng môn chỉ đường, tàng kinh trưởng lão thu sách, thư linh dạy, giám khảo ra đề, trưởng lão mạch định cảnh giới, cùng ba vai soát.

Thế giới quan không phải lớp sơn — nó **đổi cách hệ hành xử**. Ví dụ: thư linh là linh hồn của **một quyển sách**, nên nó không được tuyên bố bạn đã đạt một **mạch** năng lực. Ràng buộc đó là đặc tính nhân vật, không phải luật phải nhớ.

## Cấu trúc

```
van-dao/
  .claude-plugin/     plugin.json · marketplace.json
  reference/         data contract
  bin/                script tất định
  tests/              pytest + fixture
  skills/ agents/ hooks/    chưa có gì
```

Đặc tả · trạng thái dự án · hướng dẫn dựng nằm ở `../docs/` (workspace BMAD ngoài repo này, không đi kèm khi phân phối/clone riêng `van-dao/`).

## Chạy validator

```bash
pip install pyyaml
python bin/validate-scripture.py --kho tests/fixtures
```

## Đọc theo thứ tự nào

| Muốn biết | Đọc |
|---|---|
| Đang ở đâu, làm gì tiếp | `../docs/VAN-DAO-trang-thai-du-an.md` |
| Hệ thiết kế thế nào và vì sao | `../docs/VAN-DAO-dac-ta-v1.0.md` — bắt đầu ở §0 bảng tra |
| Quy cách một bí kíp | `reference/scripture.schema.md` |
| Dựng môi trường | `../docs/VAN-DAO-setup-du-an.md` |

## Giấy phép

MIT. Không sao chép mã hay văn bản từ dự án nào khác — xem §19 đặc tả để truy vết những gì đã học hỏi.
