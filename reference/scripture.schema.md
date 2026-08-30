# Quy cách bí kíp

**schema: 1** · Đi kèm `../../docs/VAN-DAO-dac-ta-v1.0.md` · Vị trí trong plugin: `reference/scripture.schema.md`

Đây là **hợp đồng** giữa bên thu sách (Thủ khố, pha 2–3) và bên dạy (Thư linh, Giám khảo, nghiệm công). Mọi thứ khác trong hệ đứng lên file này.

`validate-scripture.py` thực thi phần kiểm được bằng máy. Phần cần phán đoán ghi ở §7.

---

## 1 · Bố cục file

```
~/.wayfarer/scriptures/<id>/
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
id: spec-based-testing
```

**Bất biến.** Khai một lần lúc thu, không đổi về sau.

Lý do không suy từ tên thư mục: `id` xuất hiện trong `ban-giao/nghiem-cong/<id>/`, `ban-giao/khao-thi/<id>.md`, `counsel.jsonl`, `bat-dong.jsonl`, `chu-giai/<id>/`. Đổi tên thư mục mà id suy từ đó thì **mọi bài nộp cũ mồ côi** — và bài nộp là nguồn duy nhất cho định vị cảnh giới.

Đổi tên hiển thị thì sửa `nguon.tieu_de`, không sửa `id`.

Quy cách: kebab-case, không dấu, không khoảng trắng.

---

## 3 · Cấp quyển — `manifest.yaml`

```yaml
schema: 1
id: spec-based-testing
kind: scripture                    # bi-kip | tan-quyen
structure: chain                 # chuoi | mang

source:
  title: "Kiểm thử dựa trên đặc tả"
  author: "Nguyễn Văn A"
  year: 2018

source_file:
  path: "/home/hanh/sach/kiem-thu.pdf"
  fingerprint: "sha256:3f2a…"       # để phát hiện gãy con trỏ (§6.8 đặc tả)

realm_required: qi-refining        # luyen-khi | truc-co | ket-dan | nguyen-anh | hoa-than
realm_granted: core-formation

meridians: [tu-duy, ky-thuat]
roles: [tester, ba]               # tuỳ chọn — tâm pháp thường không có

spine: [1, 2, 4, 7]
branches: [3, 5, 6]
depends_on:
  4: [2]
  7: [4, 5]

task_class:
  - chapter: [1, 2]
    complexity: low
    scaffold: heavy
  - chapter: [4, 7]
    complexity: high
    scaffold: light

descend_after: [2, 7]

volume_ordeal:
  template: "Một {he_thong} có {quy_mo}, đang gặp {van_de}. Ngươi được giao {nhiem_vu}."
  parameter_set:                     # MỖI PHẦN TỬ LÀ MỘT BỘ đã khớp sẵn, không phải ba danh sách rời
    - {he_thong: "form đăng ký", quy_mo: "12 trường",
       van_de: "test case phình theo số trường", nhiem_vu: "rút gọn bộ test"}
    - {he_thong: "API thanh toán", quy_mo: "8 tham số",
       van_de: "lỗi lọt ở biên giá trị", nhiem_vu: "thiết kế lại ca kiểm"}
  redundant:
    - "một ràng buộc hiệu năng không liên quan"
  pass_criteria:
    - id: kq1
      description: "chia được phân vùng cho ít nhất hai trường có nhiều miền giá trị"
```

### 3.1 `structure` — chuỗi hay mạng

`task_class` **luôn là nhóm chương**, ở cả hai cấu trúc. Khác nhau ở **cách chọn nhóm**:

| | Nhóm theo |
|---|---|
| `chain` | Thứ tự chương — chương đầu là lớp thấp |
| `web` | Độ phức tạp tình huống áp dụng — chương nào dùng được ở ca đơn giản thì vào lớp thấp, bất kể số thứ tự |

Với BABOK: chương về Interface Analysis có thể ở lớp thấp khi áp vào một màn hình đơn, và cùng chương đó xuất hiện lại ở lớp cao khi áp vào hệ nhiều bên liên quan. **Chương nằm ở hai lớp là hợp lệ với `web`, không hợp lệ với `chain`.**

`descend_after` trỏ tới **số chương** ở cả hai cấu trúc — vẫn là mốc "học xong tới đây thì xuống núi thử".

### 3.2 Tàn quyển

`loai: fragment` thì **bỏ hẳn** năm trường: `chuong/`, `spine`, `branches`, `depends_on`, `task_class`, `descend_after`.

Các trường sư phạm ở §4 nằm **thẳng trong `manifest.yaml`**, cùng cấp với `id`.

`volume_ordeal` **vẫn bắt buộc** — tàn quyển tự đứng được, có khảo thí riêng.

---

## 4 · Cấp chương — `chuong/NN.yaml`

```yaml
schema: 1
chapter: 2
objective: "Chia được input thành phân vùng tương đương cho một form thật"

baseline_assumption:
  - "biết một test case gồm những gì"
  - "đã từng đọc một đặc tả chức năng"

worked_example:
  points_to: "chương 2, mục 2.3"     # CON TRỎ vào sách gốc, không chép nội dung

common_mistakes:
  - signal: "chia phân vùng theo trường trên màn hình"
    misconception: "tưởng mỗi ô nhập là một phân vùng"
    remedy: "đưa một ô có 3 miền giá trị hợp lệ khác nhau"
    origin: person                   # nguoi | sach | suy_doan

pass_criteria:
  - id: tc1
    description: "nêu được ≥1 phân vùng mà ranh giới không trùng ranh giới trường nhập"

question_templates:
  - id: q0
    kind: recall
    bloom: remember
    covers_criteria: []                # câu khởi động — KHÔNG tính bằng chứng
    template: "Phân vùng tương đương là gì?"
  - id: q1
    kind: apply
    bloom: apply
    covers_criteria: [tc1]
    template: "Trong {tinh_huong}, trường nào có nhiều hơn một miền hợp lệ?"
  - id: q2
    kind: analyze
    bloom: analyze
    covers_criteria: [tc1]
    template: "Cách chia trong sách vướng gì ở {tinh_huong}?"

drill: "…"
```

### 4.1 Ba loại câu hỏi

| `kind` | `bloom` | Tính là bằng chứng? | Dùng để |
|---|---|---|---|
| `recall` | `remember` · `understand` | **Không** | Khởi động đầu chương, F6 nhắc lại |
| `apply` | `apply` | **Có** | Sàn tối thiểu |
| `analyze` | `analyze` · `evaluate` · `create` | **Có** | Chạm tầng cao hơn |

Câu tái hiện **được phép tồn tại** — nó có ích để khởi động và để nhắc lại. Nó chỉ **không được trỏ tới tiêu chí nào** (`do_tieu_chi: []`), nên không bao giờ làm căn cứ cho việc đạt.

### 4.15 Mẹo viết `pass_criteria`

**Tiêu chí đòi LOẠI TRỪ phân biệt tốt hơn tiêu chí đòi NÊU LÝ DO.**

Đọc lướt vẫn nêu được lý do — *"đây là công nghệ tiên tiến nhất, các công ty lớn đều dùng"* là ba lý do. Nhưng muốn nói **vì sao không dùng cách kia** thì phải biết cách kia dùng khi nào, và đọc lướt không cho thứ đó.

| Yếu | Mạnh |
|---|---|
| "nêu được lý do chọn cách tiếp cận" | "loại trừ được ≥1 cách tiếp cận, lý do dựa trên dữ liệu" |
| "giải thích được khái niệm X" | "chỉ ra được tình huống X **không** áp dụng được" |

Cùng một cách kiểm nhanh trước khi chốt tiêu chí: viết thử một bài trả lời kiểu đọc lướt, xem nó có đạt không. Đạt → tiêu chí không phân biệt, viết lại (§11.1 đặc tả).

### 4.16 Mẹo viết `template` khảo thí

**Đề phải ép ra một khẳng định, không cho phép liệt kê.**

Đề hỏi *"nên dùng cách tiếp cận nào"* thì trả lời *"có bốn lựa chọn, còn tuỳ đặc điểm dữ liệu"* vẫn **hợp lệ và không sai gì cả**. Người viết né đúng chỗ khó, và mọi thước đo im lặng — không vai nào có căn cứ nói chưa làm được.

| Yếu | Mạnh |
|---|---|
| "nên dùng cách tiếp cận nào" | "nêu **một** cách tiếp cận cụ thể và nói vì sao không chọn **hai cách gần nhất**" |
| "phân tích tình huống này" | "quyết định X hay Y, và nêu điều kiện nào sẽ làm ngươi đổi ý" |

Cách kiểm: viết thử một bài trả lời **an toàn** — đúng hết nhưng không kết luận gì. Nếu nó lọt thì đề chưa ép khẳng định.

**Đề yếu là lỗi của bí kíp, không phải lỗi của hệ** — cùng ranh giới với tiêu chí không phân biệt.

### 4.17 `redundant` là tín hiệu tầng thấp

Dữ kiện thừa bắt được người **chưa phân biệt nổi dữ kiện nào liên quan** — họ lấy nó làm luận cứ. Đó là dấu hiệu bậc rõ ràng, và rẻ.

Nhưng người ở bậc trên **bỏ qua nó không cần nghĩ**, nên `redundant` không phân biệt được trong nhóm trên. Nó là tín hiệu nhị phân ở đáy thang, không phải thước đo suốt thang.

**Hệ quả khi viết bí kíp:** quyển nhắm `realm_granted` cao thì đừng trông vào `redundant` để phân biệt — nó sẽ im lặng với mọi bài. Phân biệt ở tầng trên phải nằm trong `pass_criteria` và trong độ khó của đề.

### 4.2 `covers_criteria` — trường làm cho bao phủ kiểm được

Không có liên kết tường minh này thì câu hỏi *"khuôn câu hỏi có phủ hết tiêu chí không"* chỉ kiểm được bằng mắt, và sẽ không ai kiểm.

### 4.3 `source` của `common_mistakes`

| Giá trị | Nghĩa |
|---|---|
| `person` | Người thu sách nhập ở pha 2 — có nghề, biết chỗ người ta hay sai |
| `book` | Sách có mục cạm bẫy, hoặc chỗ nó phân biệt hai khái niệm gần nhau |
| `inference` | Model đoán — **phải hiện cờ khi dùng** |

Trường này **được phép rỗng lúc thu**. Nó tự đầy lên qua lớp chú giải.

---

## 5 · Enum

| Trường | Giá trị hợp lệ |
|---|---|
| `kind` | `scripture` · `fragment` |
| `structure` | `chain` · `web` |
| `realm_required` / `realm_granted` | `qi-refining` · `foundation` · `core-formation` · `nascent-soul` · `soul-transformation` |
| `complexity` | `low` · `medium` · `high` |
| `scaffold` | `heavy` · `medium` · `light` |
| `kind` (câu hỏi) | `recall` · `apply` · `analyze` |
| `bloom` | `remember` · `understand` · `apply` · `analyze` · `evaluate` · `create` |
| `source` | `person` · `book` · `inference` |

---

## 6 · `validate-scripture.py` kiểm gì — tất định

**Đủ trường.** Thiếu bất kỳ trường bắt buộc nào → fail, nêu **đúng tên trường thiếu**.

**Liên kết:**
- Mọi `covers_criteria` trỏ tới `tieu_chi_dat.id` có thật trong cùng chương
- Mỗi `pass_criteria` có **≥1** câu hỏi trỏ tới — trừ khi chương đó không có tiêu chí nào
- `id` câu hỏi và `id` tiêu chí duy nhất trong phạm vi chương

**Đồ thị** (chỉ `loai: scripture`):
- `depends_on` **không có vòng**
- Mọi chương trong `spine` **tới được** từ chương đầu qua `depends_on`
- `spine` và `branches` **không giao nhau**, hợp lại phủ hết chương có file
- `task_class` phủ hết chương trong `spine`
- `cau_truc: chain` → một chương chỉ nằm ở **một** lớp; `cau_truc: web` → được nằm nhiều lớp
- `complexity` không giảm ngược theo thứ tự lớp
- `descend_after` trỏ tới chương có thật

**Tầng nhận thức:**
- Mỗi chương xương sống có **≥1** câu ở `apply` trở lên
- Câu `recall` có `covers_criteria` **rỗng** — trỏ tới tiêu chí là lỗi

**Cảnh giới:**
- `realm_granted` **không thấp hơn** `realm_required`

**Khảo thí quyển:**
- `volume_ordeal` là ánh xạ và có đủ `template` · `parameter_set` · `pass_criteria`
- `parameter_set` là **danh sách các bộ**, mỗi bộ một ánh xạ đã khớp sẵn — không phải ba danh sách rời (đặc tả §5.1)
- Mỗi bộ khai **đủ mọi khoá `{…}` mà `template` dùng** → thiếu là **lỗi**, vì đề sinh ra sẽ hở chỗ trống; khoá thừa chỉ **cảnh báo**
- Chỉ có **một** bộ → **ghi chú**: đề không đổi khi làm lại. Đủ dùng nếu chỉ thi một lần
- Không có `redundant` → **cảnh báo**: mất một tín hiệu phân biệt (§4.17)

**Tàn quyển:** năm trường ở §3.2 **vắng mặt**; trường sư phạm có ở cấp gốc.

**Con trỏ:** `nguon_file.duong_dan` tồn tại và `fingerprint` khớp — không khớp thì báo **gãy con trỏ**, không báo lỗi lược đồ.

---

## 7 · Cổng nhất quán chéo — cần phán đoán

Chạy cuối pha 3, model đề xuất, **người duyệt**. Không chặn việc thu; hỏng thì **báo và bắt xác nhận**.

| Câu hỏi | Vì sao script không làm được |
|---|---|
| `pass_criteria` có đo đúng `objective` không? | So sánh ngữ nghĩa |
| `worked_example` có minh hoạ đúng `objective` không? | Như trên |
| `remedy` có dựa vào thứ chương này dạy không? | Cần đọc nội dung sách |
| **Hợp các `pass_criteria` của chương xương sống có đủ để qua `volume_ordeal` không?** | Câu quan trọng nhất |

Dòng cuối là chỗ bí kíp gãy âm thầm nhất: khảo thí quyển đòi một thứ **không chương nào dạy**. Người học học đủ, thi trượt, không ai biết vì sao.

Không chặn vì có quyển cố ý đòi tổng hợp vượt tổng các phần — nhưng phải là **quyết định có ý thức**, không phải sơ suất.

---

## 8 · Luật tương đương bằng lời

Theo §12.2 đặc tả: mọi script phải kèm luật viết bằng lời để khi thiếu Python thì làm tay được.

Toàn bộ §6 là luật đó. Khi `validate-scripture.py` không chạy được, Thủ khố kiểm theo §6 bằng tay và **nói rõ đang kiểm tay**, không im lặng bỏ qua.

---

## 9 · Nâng cấp lược đồ

Mọi file mang `schema: 1`.

Khi lược đồ đổi, `validate-scripture.py` gặp `schema` không khớp thì **báo phiên bản không khớp** kèm hướng dẫn, không cố đọc và đoán.

Bí kíp đã thu **không tự nâng cấp** — người học chạy lệnh nâng cấp có ý thức, vì nâng cấp có thể đòi thêm trường mà chỉ người có sách mới điền được.
