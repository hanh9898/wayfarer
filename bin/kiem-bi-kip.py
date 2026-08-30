#!/usr/bin/env python3
"""kiem-bi-kip.py — kiểm bí kíp theo tham-chieu/bi-kip.schema.md (schema 1).

Thực thi phần TẤT ĐỊNH của quy cách. Phần cần phán đoán (§7 quy cách) không
thuộc script này — nó chạy cuối pha 3 và do người duyệt.

Dùng:
    kiem-bi-kip.py                      kiểm cả kho ~/.vandao/bi-kip/
    kiem-bi-kip.py <đường-dẫn>          kiểm một quyển
    kiem-bi-kip.py <đường-dẫn> --json   đầu ra JSON cho skill

Mã thoát:
    0  không có lỗi (cảnh báo và ghi chú vẫn có thể có)
    1  có ít nhất một lỗi
    2  không chạy được (thiếu PyYAML, đường dẫn sai)

Phụ thuộc: PyYAML.  pip install pyyaml
Thiếu nó thì kiểm tay theo §6 quy cách và NÓI RÕ đang kiểm tay.
"""

import argparse
import hashlib
import json
import sys
from pathlib import Path


# Đầu ra luôn UTF-8, không phụ thuộc code page của máy chạy.
#
# Trên Windows, khi stdout bị chuyển hướng — đúng cách skill gọi script rồi bắt
# đầu ra, và cách CI ghi log — Python lấy code page hệ thống. cp1252/cp1258
# không mã hoá nổi tiếng Việt, nên script CHẾT giữa lúc in kết quả thay vì báo
# lỗi bí kíp. Chế độ hỏng tệ: người dùng thấy traceback Python, không thấy quyển
# sách của mình sai chỗ nào.
for _luong in (sys.stdout, sys.stderr):
    if hasattr(_luong, "reconfigure"):
        _luong.reconfigure(encoding="utf-8")

try:
    import yaml
except ImportError:
    sys.stderr.write(
        "Thiếu PyYAML. Cài bằng:  pip install pyyaml\n"
        "Chưa cài được thì kiểm tay theo §6 của tham-chieu/bi-kip.schema.md,\n"
        "và nói rõ với người dùng là đang kiểm tay.\n"
    )
    sys.exit(2)

SCHEMA = 1

REALMS = ["qi-refining", "foundation", "core-formation", "nascent-soul", "soul-transformation"]
COMPLEXITY = ["low", "medium", "high"]
SCAFFOLD = ["heavy", "medium", "light"]
QUESTION_KINDS = ["recall", "apply", "analyze"]
BLOOM = ["remember", "understand", "apply", "analyze", "evaluate", "create"]
BLOOM_COUNTS_AS_EVIDENCE = ["apply", "analyze", "evaluate", "create"]
MISTAKE_ORIGINS = ["person", "book", "inference"]

VOLUME_FIELDS = ["schema", "id", "kind", "structure", "source", "source_file",
                "realm_required", "realm_granted", "meridians", "volume_ordeal"]
SCRIPTURE_FIELDS = ["spine", "branches", "depends_on", "task_class", "descend_after"]
PEDAGOGY_FIELDS = ["objective", "baseline_assumption", "worked_example",
                  "common_mistakes", "pass_criteria", "question_templates"]


class KetQua:
    """Ba mức: lỗi chặn nhập kho, cảnh báo nên sửa, ghi chú chỉ để biết."""

    def __init__(self, ten):
        self.ten = ten
        self.loi = []
        self.canh_bao = []
        self.ghi_chu = []

    def L(self, ma, thong_diep, o=None):
        self.loi.append({"ma": ma, "thong_diep": thong_diep, "o": o})

    def C(self, ma, thong_diep, o=None):
        self.canh_bao.append({"ma": ma, "thong_diep": thong_diep, "o": o})

    def G(self, ma, thong_diep, o=None):
        self.ghi_chu.append({"ma": ma, "thong_diep": thong_diep, "o": o})

    def dat(self):
        return not self.loi

    def as_dict(self):
        return {"bi_kip": self.ten, "dat": self.dat(), "loi": self.loi,
                "canh_bao": self.canh_bao, "ghi_chu": self.ghi_chu}


# ---------------------------------------------------------------- đọc file

def read_yaml(path, kq):
    try:
        with open(path, encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except FileNotFoundError:
        kq.L("thieu-file", f"không tìm thấy {path}")
        return None
    except yaml.YAMLError as e:
        kq.L("yaml-hong", f"{path.name} không đọc được: {e}")
        return None
    if not isinstance(data, dict):
        kq.L("yaml-hong", f"{path.name} phải là một ánh xạ ở cấp gốc")
        return None
    return data


def fingerprint(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for khoi in iter(lambda: f.read(1 << 20), b""):
            h.update(khoi)
    return "sha256:" + h.hexdigest()


# ------------------------------------------------------- kiểm cấp quyển

# Trường bắt buộc CÓ MẶT, nhưng được phép rỗng.
MAY_BE_EMPTY = {"branches", "baseline_assumption", "common_mistakes", "roles",
                 "redundant", "depends_on", "descend_after"}


def check_required_fields(d, truong, kq, o):
    """Vắng khoá là lỗi. Rỗng chỉ là lỗi khi trường đó không được phép rỗng."""
    for t in truong:
        if t not in d or d[t] is None:
            kq.L("thieu-truong", f"thiếu trường bắt buộc `{t}`", o)
        elif d[t] in ("", [], {}) and t not in MAY_BE_EMPTY:
            kq.L("truong-rong", f"trường `{t}` không được rỗng", o)


def check_enum(gia_tri, hop_le, ten, kq, o):
    if gia_tri is not None and gia_tri not in hop_le:
        kq.L("enum-sai", f"`{ten}` = {gia_tri!r}, phải thuộc {hop_le}", o)


def check_manifest(m, thu_muc, kq):
    o = "manifest.yaml"
    check_required_fields(m, VOLUME_FIELDS, kq, o)

    if m.get("schema") != SCHEMA:
        kq.L("schema-khong-khop",
             f"schema = {m.get('schema')!r}, script này chỉ đọc schema {SCHEMA}. "
             "Nâng cấp có ý thức, đừng để script đoán.", o)
        return

    check_enum(m.get("kind"), ["scripture", "fragment"], "kind", kq, o)
    check_enum(m.get("structure"), ["chain", "web"], "structure", kq, o)
    check_enum(m.get("realm_required"), REALMS, "realm_required", kq, o)
    check_enum(m.get("realm_granted"), REALMS, "realm_granted", kq, o)

    vao, ra = m.get("realm_required"), m.get("realm_granted")
    if vao in REALMS and ra in REALMS:
        if REALMS.index(ra) < REALMS.index(vao):
            kq.L("canh-gioi-lui",
                 f"realm_granted ({ra}) thấp hơn realm_required ({vao})", o)

    ident = m.get("id")
    if ident and (ident != ident.lower() or " " in ident or "_" in ident):
        kq.L("id-sai-quy-cach",
             f"`id` = {ident!r} — phải kebab-case, không dấu, không khoảng trắng", o)
    if ident and ident != thu_muc.name:
        kq.G("id-khac-thu-muc",
             f"`id` ({ident}) khác tên thư mục ({thu_muc.name}). "
             "Hợp lệ — id là bất biến, tên thư mục thì không.", o)

    nf = m.get("source_file") or {}
    dp = nf.get("path")
    if dp:
        p = Path(dp).expanduser()
        if not p.exists():
            kq.C("gay-con-tro", f"không thấy file nguồn: {dp}. Chạy /vd:noi-lai", o)
        elif nf.get("fingerprint"):
            thuc = fingerprint(p)
            if thuc != nf["fingerprint"]:
                kq.C("gay-con-tro",
                     f"vân tay không khớp — file nguồn đã đổi. Chạy /vd:noi-lai", o)

    if not m.get("roles"):
        kq.G("khong-the-vai", "không có thẻ `vai` — sẽ hiện ở khung nhìn tâm pháp", o)


# ------------------------------------------------------- kiểm sư phạm

def check_pedagogy_block(d, kq, o):
    """Dùng cho cả chương (bí kíp) lẫn cấp gốc (tàn quyển)."""
    check_required_fields(d, PEDAGOGY_FIELDS, kq, o)

    tieu_chi = d.get("pass_criteria") or []
    cau_hoi = d.get("question_templates") or []

    ids_tc = []
    for tc in tieu_chi:
        if not isinstance(tc, dict) or "id" not in tc or "description" not in tc:
            kq.L("tieu-chi-sai", "mỗi `pass_criteria` cần `id` và `description`", o)
            continue
        if tc["id"] in ids_tc:
            kq.L("id-trung", f"`pass_criteria.id` trùng: {tc['id']}", o)
        ids_tc.append(tc["id"])

    ids_q, duoc_phu, co_ap_dung = [], set(), False
    for q in cau_hoi:
        if not isinstance(q, dict) or "id" not in q:
            kq.L("cau-hoi-sai", "mỗi `question_templates` cần `id`", o)
            continue
        if q["id"] in ids_q:
            kq.L("id-trung", f"`question_templates.id` trùng: {q['id']}", o)
        ids_q.append(q["id"])

        check_enum(q.get("kind"), QUESTION_KINDS, f"{q['id']}.loai", kq, o)
        check_enum(q.get("bloom"), BLOOM, f"{q['id']}.bloom", kq, o)

        if q.get("bloom") in BLOOM_COUNTS_AS_EVIDENCE:
            co_ap_dung = True

        tro = q.get("covers_criteria") or []
        if q.get("kind") == "recall" and tro:
            kq.L("tai-hien-tro-tieu-chi",
                 f"câu `{q['id']}` loại tai_hien không được trỏ tới tiêu chí "
                 "— nó không tính là bằng chứng", o)
        for t in tro:
            if t not in ids_tc:
                kq.L("lien-ket-chet",
                     f"câu `{q['id']}` trỏ tới tiêu chí không có thật: {t}", o)
            else:
                duoc_phu.add(t)

    for t in ids_tc:
        if t not in duoc_phu:
            kq.L("thieu-bao-phu",
                 f"tiêu chí `{t}` không có câu hỏi nào trỏ tới — "
                 "không có cách nào lộ ra nó", o)

    if ids_tc and not co_ap_dung:
        kq.L("thieu-tang-ap-dung",
             "không có câu nào ở tầng Áp dụng trở lên — chương chỉ đo tầng Nhớ", o)

    we = d.get("worked_example") or {}
    if isinstance(we, dict) and not we.get("points_to"):
        kq.L("worked-example-sai",
             "`worked_example` phải có `points_to` — con trỏ vào sách gốc", o)

    slpb = d.get("common_mistakes")
    if not slpb:
        kq.C("chua-co-sai-lam",
             "`common_mistakes` rỗng — hợp lệ, nhưng F4 sẽ không chẩn đoán được, "
             "chỉ báo sai. Nó tự đầy lên qua lớp chú giải.", o)
    else:
        for i, sl in enumerate(slpb):
            if not isinstance(sl, dict):
                kq.L("sai-lam-sai", f"mục {i} không phải ánh xạ", o)
                continue
            for t in ("signal", "misconception", "remedy", "origin"):
                if not sl.get(t):
                    kq.L("sai-lam-thieu-truong", f"mục {i} thiếu `{t}`", o)
            check_enum(sl.get("origin"), MISTAKE_ORIGINS, f"common_mistakes[{i}].origin", kq, o)
            if sl.get("source") == "inference":
                kq.G("sai-lam-suy-doan",
                     f"mục {i} nguồn `suy_doan` — phải hiện cờ khi dùng", o)


# ------------------------------------------------------- kiểm đồ thị

def check_graph(m, so_chuong, kq):
    o = "manifest.yaml"
    xs = m.get("spine") or []
    cn = m.get("branches") or []
    pt = m.get("depends_on") or {}

    giao = sorted(set(xs) & set(cn))
    if giao:
        kq.L("xuong-song-giao-chi-nhanh",
             f"chương vừa xương sống vừa chi nhánh: {giao}", o)

    thieu = sorted(so_chuong - set(xs) - set(cn))
    if thieu:
        kq.L("chuong-khong-phan-loai",
             f"chương có file nhưng không nằm ở spine lẫn branches: {thieu}", o)

    la = sorted((set(xs) | set(cn)) - so_chuong)
    if la:
        kq.L("chuong-khong-co-file", f"khai chương nhưng không có file: {la}", o)

    # phụ thuộc: tồn tại và không có vòng
    for c, deps in pt.items():
        if c not in so_chuong:
            kq.L("phu-thuoc-la", f"depends_on khai chương không có file: {c}", o)
        for d in deps or []:
            if d not in so_chuong:
                kq.L("phu-thuoc-la", f"chương {c} phụ thuộc chương không có: {d}", o)

    mau = {}

    def co_vong(n, duong):
        mau[n] = 1
        for k in pt.get(n, []) or []:
            if mau.get(k) == 1:
                kq.L("do-thi-co-vong",
                     f"đồ thị phụ thuộc có vòng: {' → '.join(map(str, duong + [n, k]))}", o)
                return True
            if mau.get(k, 0) == 0 and co_vong(k, duong + [n]):
                return True
        mau[n] = 2
        return False

    for c in sorted(so_chuong):
        if mau.get(c, 0) == 0:
            co_vong(c, [])

    # mọi chương xương sống tới được từ chương đầu
    if xs:
        dau = min(so_chuong) if so_chuong else None
        toi_duoc = set()

        def lan(n):
            if n in toi_duoc:
                return
            toi_duoc.add(n)
            for k, deps in pt.items():
                if n in (deps or []):
                    lan(k)

        if dau is not None:
            lan(dau)
            ket = sorted(set(xs) - toi_duoc)
            if ket:
                kq.L("xuong-song-khong-toi-duoc",
                     f"chương xương sống không tới được từ chương {dau} "
                     f"qua depends_on: {ket}", o)

    # lớp nhiệm vụ
    lnv = m.get("task_class") or []
    phu, dem = set(), {}
    truoc = -1
    for i, lop in enumerate(lnv):
        if not isinstance(lop, dict):
            kq.L("lop-nhiem-vu-sai", f"lớp {i} không phải ánh xạ", o)
            continue
        check_enum(lop.get("complexity"), COMPLEXITY, f"task_class[{i}].complexity", kq, o)
        check_enum(lop.get("scaffold"), SCAFFOLD, f"task_class[{i}].scaffold", kq, o)
        if lop.get("complexity") in COMPLEXITY:
            muc = COMPLEXITY.index(lop["complexity"])
            if muc < truoc:
                kq.L("do-phuc-tap-giam-nguoc",
                     f"lớp {i} có độ phức tạp thấp hơn lớp trước — "
                     "giàn giáo xếp sai chiều", o)
            truoc = max(truoc, muc)
        for c in lop.get("chapters") or []:
            phu.add(c)
            dem[c] = dem.get(c, 0) + 1

    con = sorted(set(xs) - phu)
    if con:
        kq.L("lop-nhiem-vu-thieu-chuong",
             f"chương xương sống không nằm trong task_class nào: {con}", o)

    if m.get("structure") == "chain":
        nhieu = sorted(c for c, n in dem.items() if n > 1)
        if nhieu:
            kq.L("chuong-nhieu-lop-voi-chuoi",
                 f"cau_truc=chuoi nhưng chương nằm ở nhiều lớp: {nhieu}. "
                 "Nếu cố ý thì khai cau_truc=mang.", o)

    hs = m.get("descend_after") or []
    la_hs = sorted(set(hs) - so_chuong)
    if la_hs:
        kq.L("ha-son-la", f"descend_after trỏ tới chương không có: {la_hs}", o)
    if not hs:
        kq.C("khong-ha-son",
             "không có `descend_after` — người học không có mốc nào xuống núi thử", o)


# ------------------------------------------------------- kiểm khảo thí

def check_ordeal(m, kq):
    o = "manifest.yaml → volume_ordeal"
    kt = m.get("volume_ordeal") or {}
    if not isinstance(kt, dict):
        kq.L("khao-thi-sai", "`volume_ordeal` phải là ánh xạ", o)
        return
    for t in ("template", "parameter_set", "pass_criteria"):
        if not kt.get(t):
            kq.L("khao-thi-thieu", f"thiếu `{t}`", o)

    khuon = kt.get("template") or ""
    bo = kt.get("parameter_set") or []
    import re
    dung = set(re.findall(r"\{(\w+)\}", khuon))

    if not isinstance(bo, list):
        kq.L("bo-tham-so-sai", "`parameter_set` phải là danh sách các bộ", o)
        return
    for i, b in enumerate(bo):
        if not isinstance(b, dict):
            kq.L("bo-tham-so-sai", f"bộ {i} không phải ánh xạ", o)
            continue
        khai = set(b.keys())
        thieu = sorted(dung - khai)
        thua = sorted(khai - dung)
        if thieu:
            kq.L("bo-thieu-khoa",
                 f"bộ {i} thiếu khoá {thieu} mà khuôn dùng — đề sinh ra sẽ hở chỗ trống", o)
        if thua:
            kq.C("bo-thua-khoa", f"bộ {i} khai {thua} nhưng khuôn không dùng", o)
    if len(bo) == 1:
        kq.G("mot-bo-tham-so",
             "chỉ có 1 bộ — đề không đổi khi làm lại. Đủ dùng nếu chỉ thi một lần", o)

    if not kt.get("redundant"):
        kq.C("khong-du-thua",
             "không có `redundant` — mất một tín hiệu phân biệt: "
             "người học không phải chọn dữ kiện nào đáng dùng", o)


# ------------------------------------------------------- một bí kíp

def check_one(thu_muc: Path) -> KetQua:
    kq = KetQua(thu_muc.name)
    m = read_yaml(thu_muc / "manifest.yaml", kq)
    if m is None:
        return kq

    check_manifest(m, thu_muc, kq)
    if any(l["ma"] == "schema-khong-khop" for l in kq.loi):
        return kq

    loai = m.get("kind")
    thu_muc_chuong = thu_muc / "chapters"

    if loai == "fragment":
        for t in SCRIPTURE_FIELDS:
            if t in m:
                kq.L("tan-quyen-thua-truong",
                     f"tàn quyển không được có `{t}`", "manifest.yaml")
        if thu_muc_chuong.exists():
            kq.L("tan-quyen-co-chuong",
                 "tàn quyển không được có thư mục `chapters/`", "manifest.yaml")
        check_pedagogy_block(m, kq, "manifest.yaml (tàn quyển)")

    elif loai == "scripture":
        check_required_fields(m, SCRIPTURE_FIELDS, kq, "manifest.yaml")
        for t in PEDAGOGY_FIELDS:
            if t in m:
                kq.L("bi-kip-thua-truong",
                     f"bí kíp không đặt `{t}` ở cấp quyển — nó thuộc từng chương",
                     "manifest.yaml")
        if not thu_muc_chuong.exists():
            kq.L("thieu-thu-muc-chuong", "bí kíp phải có thư mục `chapters/`")
            return kq

        so_chuong = set()
        for f in sorted(thu_muc_chuong.glob("*.yaml")):
            d = read_yaml(f, kq)
            if d is None:
                continue
            o = f"chapters/{f.name}"
            if d.get("schema") != SCHEMA:
                kq.L("schema-khong-khop", f"schema = {d.get('schema')!r}", o)
                continue
            so = d.get("chapter")
            if not isinstance(so, int):
                kq.L("chuong-thieu-so", "thiếu trường `chapter` kiểu số nguyên", o)
                continue
            if so in so_chuong:
                kq.L("chuong-trung", f"số chương trùng: {so}", o)
            so_chuong.add(so)
            check_pedagogy_block(d, kq, o)

        if not so_chuong:
            kq.L("khong-co-chuong", "không có file chương nào đọc được")
        else:
            check_graph(m, so_chuong, kq)

    check_ordeal(m, kq)
    return kq


# ------------------------------------------------------- in kết quả

LABELS = {"loi": "LỖI", "canh_bao": "CẢNH BÁO", "ghi_chu": "ghi chú"}


def print_report(kqs):
    for kq in kqs:
        trang_thai = "ĐẠT" if kq.dat() else "KHÔNG ĐẠT"
        print(f"\n=== {kq.ten} — {trang_thai} ===")
        for muc in ("loi", "canh_bao", "ghi_chu"):
            for m in getattr(kq, muc):
                o = f" [{m['o']}]" if m.get("o") else ""
                print(f"  {LABELS[muc]:<9}{m['thong_diep']}{o}")
        if kq.dat() and not kq.canh_bao and not kq.ghi_chu:
            print("  không có gì để nói")

    tong_loi = sum(len(k.loi) for k in kqs)
    tong_cb = sum(len(k.canh_bao) for k in kqs)
    print(f"\n{len(kqs)} bí kíp · {tong_loi} lỗi · {tong_cb} cảnh báo")
    if tong_loi:
        print("Lỗi chặn nhập kho. Cảnh báo thì không — nhưng nên đọc.")
    print("\nPhần cần phán đoán (§7 quy cách) KHÔNG do script này kiểm:")
    print("  tiêu chí có đo đúng mục tiêu · ví dụ có minh hoạ đúng mục tiêu")
    print("  cách chữa có dựa vào chương này · hợp các tiêu chí có đủ qua khảo thí")


def main():
    ap = argparse.ArgumentParser(description="Kiểm bí kíp theo schema 1")
    ap.add_argument("path", nargs="?", help="một quyển; bỏ trống = cả kho")
    ap.add_argument("--json", action="store_true", help="đầu ra JSON cho skill")
    ap.add_argument("--kho", default="~/.vandao/bi-kip", help="thư mục kho")
    a = ap.parse_args()

    if a.path:
        muc = [Path(a.path).expanduser()]
        if not muc[0].is_dir():
            sys.stderr.write(f"không phải thư mục: {muc[0]}\n")
            sys.exit(2)
    else:
        kho = Path(a.kho).expanduser()
        if not kho.is_dir():
            sys.stderr.write(f"chưa có kho: {kho}\n")
            sys.exit(2)
        muc = sorted(p for p in kho.iterdir() if p.is_dir())
        if not muc:
            sys.stderr.write(f"kho rỗng: {kho}\n")
            sys.exit(2)

    kqs = [check_one(p) for p in muc]

    if a.json:
        print(json.dumps({"schema": SCHEMA,
                          "ket_qua": [k.as_dict() for k in kqs]},
                         ensure_ascii=False, indent=2))
    else:
        print_report(kqs)

    sys.exit(1 if any(not k.dat() for k in kqs) else 0)


if __name__ == "__main__":
    main()
