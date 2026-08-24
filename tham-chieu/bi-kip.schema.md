# Quy cách bí kíp

**schema: 1** · Đi kèm `../../docs/VAN-DAO-dac-ta-v1.0.md` · Vị trí trong plugin: `tham-chieu/bi-kip.schema.md`

Đây là **hợp đồng** giữa bên thu sách (Thủ khố, pha 2–3) và bên dạy (Thư linh, Giám khảo, nghiệm công). Mọi thứ khác trong hệ đứng lên file này.

`kiem-bi-kip.py` thực thi phần kiểm được bằng máy. Phần cần phán đoán ghi ở §7.

---

## 1 · Bố cục file

```
~/.vandao/bi-kip/<id>/
  manifest.yaml           cấp quyển
  chuong/
    01.yaml
    02.yaml
    ...
```

Tàn quyển **không có thư mục `chuong/`** — mọi trường sư phạm nằm thẳng trong `manifest.yaml`.

---

## 2 · Định danh

```yaml
id: kiem-thu-dac-ta
```

**Bất biến.** Khai một lần lúc thu, không đổi về sau.

Lý do không suy từ tên thư mục: `id` xuất hiện trong `ban-giao/nghiem-cong/<id>/`, `ban-giao/khao-thi/<id>.md`, `chi-diem.jsonl`, `bat-dong.jsonl`, `chu-giai/<id>/`. Đổi tên thư mục mà id suy từ đó thì **mọi bài nộp cũ mồ côi** — và bài nộp là nguồn duy nhất cho định vị cảnh giới.

Đổi tên hiển thị thì sửa `nguon.tieu_de`, không sửa `id`.

Quy cách: kebab-case, không dấu, không khoảng trắng.

---

## 3 · Cấp quyển — `manifest.yaml`

```yaml
schema: 1
id: kiem-thu-dac-ta
loai: bi-kip                    # bi-kip | tan-quyen
cau_truc: chuoi                 # chuoi | mang

nguon:
  tieu_de: "Kiểm thử dựa trên đặc tả"
  tac_gia: "Nguyễn Văn A"
  nam: 2018

nguon_file:
  duong_dan: "/home/hanh/sach/kiem-thu.pdf"
  van_tay: "sha256:3f2a…"       # để phát hiện gãy con trỏ (§6.8 đặc tả)

canh_gioi_vao: luyen-khi        # luyen-khi | truc-co | ket-dan | nguyen-anh | hoa-than
canh_gioi_ra: ket-dan

mach: [tu-duy, ky-thuat]
vai: [tester, ba]               # tuỳ chọn — tâm pháp thường không có

xuong_song: [1, 2, 4, 7]
chi_nhanh: [3, 5, 6]
phu_thuoc:
  4: [2]
  7: [4, 5]

lop_nhiem_vu:
  - chuong: [1, 2]
    do_phuc_tap: thap
    gian_giao: day
  - chuong: [4, 7]
    do_phuc_tap: cao
    gian_giao: mong

ha_son_sau: [2, 7]

khao_thi_quyen:
  khuon: "Một {he_thong} có {quy_mo}, đang gặp {van_de}. Ngươi được giao {nhiem_vu}."
  bo_tham_so:                     # MỖI PHẦN TỬ LÀ MỘT BỘ đã khớp sẵn, không phải ba danh sách rời
    - {he_thong: "form đăng ký", quy_mo: "12 trường",
       van_de: "test case phình theo số trường", nhiem_vu: "rút gọn bộ test"}
    - {he_thong: "API thanh toán", quy_mo: "8 tham số",
       van_de: "lỗi lọt ở biên giá trị", nhiem_vu: "thiết kế lại ca kiểm"}
  du_thua:
    - "một ràng buộc hiệu năng không liên quan"
  tieu_chi_dat:
    - id: kq1
      mo_ta: "chia được phân vùng cho ít nhất hai trường có nhiều miền giá trị"
```

### 3.1 `cau_truc` — chuỗi hay mạng

`lop_nhiem_vu` **luôn là nhóm chương**, ở cả hai cấu trúc. Khác nhau ở **cách chọn nhóm**:

| | Nhóm theo |
|---|---|
| `chuoi` | Thứ tự chương — chương đầu là lớp thấp |
| `mang` | Độ phức tạp tình huống áp dụng — chương nào dùng được ở ca đơn giản thì vào lớp thấp, bất kể số thứ tự |

Với BABOK: chương về Interface Analysis có thể ở lớp thấp khi áp vào một màn hình đơn, và cùng chương đó xuất hiện lại ở lớp cao khi áp vào hệ nhiều bên liên quan. **Chương nằm ở hai lớp là hợp lệ với `mang`, không hợp lệ với `chuoi`.**

`ha_son_sau` trỏ tới **số chương** ở cả hai cấu trúc — vẫn là mốc "học xong tới đây thì xuống núi thử".

### 3.2 Tàn quyển

`loai: tan-quyen` thì **bỏ hẳn** năm trường: `chuong/`, `xuong_song`, `chi_nhanh`, `phu_thuoc`, `lop_nhiem_vu`, `ha_son_sau`.

Các trường sư phạm ở §4 nằm **thẳng trong `manifest.yaml`**, cùng cấp với `id`.

`khao_thi_quyen` **vẫn bắt buộc** — tàn quyển tự đứng được, có khảo thí riêng.

---

## 4 · Cấp chương — `chuong/NN.yaml`

```yaml
schema: 1
chuong: 2
muc_tieu: "Chia được input thành phân vùng tương đương cho một form thật"

gia_dinh_nen:
  - "biết một test case gồm những gì"
  - "đã từng đọc một đặc tả chức năng"

worked_example:
  tro_toi: "chương 2, mục 2.3"     # CON TRỎ vào sách gốc, không chép nội dung

sai_lam_pho_bien:
  - dau_hieu: "chia phân vùng theo trường trên màn hình"
    quan_niem_sai: "tưởng mỗi ô nhập là một phân vùng"
    cach_chua: "đưa một ô có 3 miền giá trị hợp lệ khác nhau"
    nguon: nguoi                   # nguoi | sach | suy_doan

tieu_chi_dat:
  - id: tc1
    mo_ta: "nêu được ≥1 phân vùng mà ranh giới không trùng ranh giới trường nhập"

khuon_cau_hoi:
  - id: q0
    loai: tai_hien
    bloom: nho
    do_tieu_chi: []                # câu khởi động — KHÔNG tính bằng chứng
    khuon: "Phân vùng tương đương là gì?"
  - id: q1
    loai: van_dung
    bloom: ap_dung
    do_tieu_chi: [tc1]
    khuon: "Trong {tinh_huong}, trường nào có nhiều hơn một miền hợp lệ?"
  - id: q2
    loai: phan_tich
    bloom: phan_tich
    do_tieu_chi: [tc1]
    khuon: "Cách chia trong sách vướng gì ở {tinh_huong}?"

bai_luyen_lap: "…"
```

### 4.1 Ba loại câu hỏi

| `loai` | `bloom` | Tính là bằng chứng? | Dùng để |
|---|---|---|---|
| `tai_hien` | `nho` · `hieu` | **Không** | Khởi động đầu chương, F6 nhắc lại |
| `van_dung` | `ap_dung` | **Có** | Sàn tối thiểu |
| `phan_tich` | `phan_tich` · `danh_gia` · `sang_tao` | **Có** | Chạm tầng cao hơn |

Câu tái hiện **được phép tồn tại** — nó có ích để khởi động và để nhắc lại. Nó chỉ **không được trỏ tới tiêu chí nào** (`do_tieu_chi: []`), nên không bao giờ làm căn cứ cho việc đạt.

### 4.15 Mẹo viết `tieu_chi_dat`

**Tiêu chí đòi LOẠI TRỪ phân biệt tốt hơn tiêu chí đòi NÊU LÝ DO.**

Đọc lướt vẫn nêu được lý do — *"đây là công nghệ tiên tiến nhất, các công ty lớn đều dùng"* là ba lý do. Nhưng muốn nói **vì sao không dùng cách kia** thì phải biết cách kia dùng khi nào, và đọc lướt không cho thứ đó.

| Yếu | Mạnh |
|---|---|
| "nêu được lý do chọn cách tiếp cận" | "loại trừ được ≥1 cách tiếp cận, lý do dựa trên dữ liệu" |
| "giải thích được khái niệm X" | "chỉ ra được tình huống X **không** áp dụng được" |

Cùng một cách kiểm nhanh trước khi chốt tiêu chí: viết thử một bài trả lời kiểu đọc lướt, xem nó có đạt không. Đạt → tiêu chí không phân biệt, viết lại (§11.1 đặc tả).

### 4.16 Mẹo viết `khuon` khảo thí

**Đề phải ép ra một khẳng định, không cho phép liệt kê.**

Đề hỏi *"nên dùng cách tiếp cận nào"* thì trả lời *"có bốn lựa chọn, còn tuỳ đặc điểm dữ liệu"* vẫn **hợp lệ và không sai gì cả**. Người viết né đúng chỗ khó, và mọi thước đo im lặng — không vai nào có căn cứ nói chưa làm được.

| Yếu | Mạnh |
|---|---|
| "nên dùng cách tiếp cận nào" | "nêu **một** cách tiếp cận cụ thể và nói vì sao không chọn **hai cách gần nhất**" |
| "phân tích tình huống này" | "quyết định X hay Y, và nêu điều kiện nào sẽ làm ngươi đổi ý" |

Cách kiểm: viết thử một bài trả lời **an toàn** — đúng hết nhưng không kết luận gì. Nếu nó lọt thì đề chưa ép khẳng định.

**Đề yếu là lỗi của bí kíp, không phải lỗi của hệ** — cùng ranh giới với tiêu chí không phân biệt.

### 4.17 `du_thua` là tín hiệu tầng thấp

Dữ kiện thừa bắt được người **chưa phân biệt nổi dữ kiện nào liên quan** — họ lấy nó làm luận cứ. Đó là dấu hiệu bậc rõ ràng, và rẻ.

Nhưng người ở bậc trên **bỏ qua nó không cần nghĩ**, nên `du_thua` không phân biệt được trong nhóm trên. Nó là tín hiệu nhị phân ở đáy thang, không phải thước đo suốt thang.

**Hệ quả khi viết bí kíp:** quyển nhắm `canh_gioi_ra` cao thì đừng trông vào `du_thua` để phân biệt — nó sẽ im lặng với mọi bài. Phân biệt ở tầng trên phải nằm trong `tieu_chi_dat` và trong độ khó của đề.

### 4.2 `do_tieu_chi` — trường làm cho bao phủ kiểm được

Không có liên kết tường minh này thì câu hỏi *"khuôn câu hỏi có phủ hết tiêu chí không"* chỉ kiểm được bằng mắt, và sẽ không ai kiểm.

### 4.3 `nguon` của `sai_lam_pho_bien`

| Giá trị | Nghĩa |
|---|---|
| `nguoi` | Người thu sách nhập ở pha 2 — có nghề, biết chỗ người ta hay sai |
| `sach` | Sách có mục cạm bẫy, hoặc chỗ nó phân biệt hai khái niệm gần nhau |
| `suy_doan` | Model đoán — **phải hiện cờ khi dùng** |

Trường này **được phép rỗng lúc thu**. Nó tự đầy lên qua lớp chú giải.

---

## 5 · Enum

| Trường | Giá trị hợp lệ |
|---|---|
| `loai` | `bi-kip` · `tan-quyen` |
| `cau_truc` | `chuoi` · `mang` |
| `canh_gioi_vao` / `canh_gioi_ra` | `luyen-khi` · `truc-co` · `ket-dan` · `nguyen-anh` · `hoa-than` |
| `do_phuc_tap` | `thap` · `trung` · `cao` |
| `gian_giao` | `day` · `vua` · `mong` |
| `loai` (câu hỏi) | `tai_hien` · `van_dung` · `phan_tich` |
| `bloom` | `nho` · `hieu` · `ap_dung` · `phan_tich` · `danh_gia` · `sang_tao` |
| `nguon` | `nguoi` · `sach` · `suy_doan` |

---

## 6 · `kiem-bi-kip.py` kiểm gì — tất định

**Đủ trường.** Thiếu bất kỳ trường bắt buộc nào → fail, nêu **đúng tên trường thiếu**.

**Liên kết:**
- Mọi `do_tieu_chi` trỏ tới `tieu_chi_dat.id` có thật trong cùng chương
- Mỗi `tieu_chi_dat` có **≥1** câu hỏi trỏ tới — trừ khi chương đó không có tiêu chí nào
- `id` câu hỏi và `id` tiêu chí duy nhất trong phạm vi chương

**Đồ thị** (chỉ `loai: bi-kip`):
- `phu_thuoc` **không có vòng**
- Mọi chương trong `xuong_song` **tới được** từ chương đầu qua `phu_thuoc`
- `xuong_song` và `chi_nhanh` **không giao nhau**, hợp lại phủ hết chương có file
- `lop_nhiem_vu` phủ hết chương trong `xuong_song`
- `cau_truc: chuoi` → một chương chỉ nằm ở **một** lớp; `cau_truc: mang` → được nằm nhiều lớp
- `do_phuc_tap` không giảm ngược theo thứ tự lớp
- `ha_son_sau` trỏ tới chương có thật

**Tầng nhận thức:**
- Mỗi chương xương sống có **≥1** câu ở `ap_dung` trở lên
- Câu `tai_hien` có `do_tieu_chi` **rỗng** — trỏ tới tiêu chí là lỗi

**Cảnh giới:**
- `canh_gioi_ra` **không thấp hơn** `canh_gioi_vao`

**Khảo thí quyển:**
- `khao_thi_quyen` là ánh xạ và có đủ `khuon` · `bo_tham_so` · `tieu_chi_dat`
- `bo_tham_so` là **danh sách các bộ**, mỗi bộ một ánh xạ đã khớp sẵn — không phải ba danh sách rời (đặc tả §5.1)
- Mỗi bộ khai **đủ mọi khoá `{…}` mà `khuon` dùng** → thiếu là **lỗi**, vì đề sinh ra sẽ hở chỗ trống; khoá thừa chỉ **cảnh báo**
- Chỉ có **một** bộ → **ghi chú**: đề không đổi khi làm lại. Đủ dùng nếu chỉ thi một lần
- Không có `du_thua` → **cảnh báo**: mất một tín hiệu phân biệt (§4.17)

**Tàn quyển:** năm trường ở §3.2 **vắng mặt**; trường sư phạm có ở cấp gốc.

**Con trỏ:** `nguon_file.duong_dan` tồn tại và `van_tay` khớp — không khớp thì báo **gãy con trỏ**, không báo lỗi lược đồ.

---

## 7 · Cổng nhất quán chéo — cần phán đoán

Chạy cuối pha 3, model đề xuất, **người duyệt**. Không chặn việc thu; hỏng thì **báo và bắt xác nhận**.

| Câu hỏi | Vì sao script không làm được |
|---|---|
| `tieu_chi_dat` có đo đúng `muc_tieu` không? | So sánh ngữ nghĩa |
| `worked_example` có minh hoạ đúng `muc_tieu` không? | Như trên |
| `cach_chua` có dựa vào thứ chương này dạy không? | Cần đọc nội dung sách |
| **Hợp các `tieu_chi_dat` của chương xương sống có đủ để qua `khao_thi_quyen` không?** | Câu quan trọng nhất |

Dòng cuối là chỗ bí kíp gãy âm thầm nhất: khảo thí quyển đòi một thứ **không chương nào dạy**. Người học học đủ, thi trượt, không ai biết vì sao.

Không chặn vì có quyển cố ý đòi tổng hợp vượt tổng các phần — nhưng phải là **quyết định có ý thức**, không phải sơ suất.

---

## 8 · Luật tương đương bằng lời

Theo §12.2 đặc tả: mọi script phải kèm luật viết bằng lời để khi thiếu Python thì làm tay được.

Toàn bộ §6 là luật đó. Khi `kiem-bi-kip.py` không chạy được, Thủ khố kiểm theo §6 bằng tay và **nói rõ đang kiểm tay**, không im lặng bỏ qua.

---

## 9 · Nâng cấp lược đồ

Mọi file mang `schema: 1`.

Khi lược đồ đổi, `kiem-bi-kip.py` gặp `schema` không khớp thì **báo phiên bản không khớp** kèm hướng dẫn, không cố đọc và đoán.

Bí kíp đã thu **không tự nâng cấp** — người học chạy lệnh nâng cấp có ý thức, vì nâng cấp có thể đòi thêm trường mà chỉ người có sách mới điền được.
