# Sách thử — fixture chung để chạy eval thu bí kíp

Sách thật không bao giờ vào repo (`.gitignore` chặn `*.pdf` · `*.epub`, và đó là chủ ý —
xem Policy trong `AGENTS.md` của workspace). Nên thứ được version control ở đây là **công thức
lấy sách**, không phải sách.

Ai cần chạy lại eval thì lấy đúng cuốn này về, sẽ ra cùng một đầu vào.

## Cuốn đang dùng

| | |
|---|---|
| Tên | The Art of War |
| Tác giả | Sun Tzu (bản dịch Lionel Giles, 1910) |
| Nguồn | Project Gutenberg #132 — public domain |
| Định dạng | EPUB |
| Kích thước | ~226 KB |

Chọn cuốn này vì: public domain (tải lại được mãi, không vướng bản quyền), có 13 chương
tách bạch rõ (đủ cấu trúc để thử phân giải), và bản thân là sách dạy một kỹ năng — đúng
loại sách hệ này sinh ra để xử lý.

## Lấy về

Chạy từ gốc repo `van-dao`. Cả hai lệnh cho cùng một file.

**PowerShell (Windows):**

```powershell
New-Item -ItemType Directory -Force tests/fixtures/sach-thu | Out-Null
Invoke-WebRequest -Uri "https://www.gutenberg.org/cache/epub/132/pg132.epub" -OutFile "tests/fixtures/sach-thu/art-of-war.epub"
```

**bash (Linux/macOS/Git Bash):**

```bash
mkdir -p tests/fixtures/sach-thu
curl -sL -o tests/fixtures/sach-thu/art-of-war.epub "https://www.gutenberg.org/cache/epub/132/pg132.epub"
```

## Kiểm đã lấy đúng chưa

```bash
file tests/fixtures/sach-thu/art-of-war.epub   # phải in "EPUB document"
```

Không ghim checksum: Project Gutenberg thỉnh thoảng sinh lại file (đổi metadata, sửa lỗi
soát chính tả) nên hash đổi mà nội dung sách không đổi. Ghim hash sẽ làm eval gãy vì một
lý do không liên quan gì tới hành vi đang kiểm.

## Muốn thêm sách thử khác

Thêm một mục vào bảng trên kèm lệnh lấy về. Giữ nguyên nguyên tắc: **chỉ public domain**,
và không bao giờ commit chính file sách.
