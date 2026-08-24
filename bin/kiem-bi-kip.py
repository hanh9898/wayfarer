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

CANH_GIOI = ["luyen-khi", "truc-co", "ket-dan", "nguyen-anh", "hoa-than"]
DO_PHUC_TAP = ["thap", "trung", "cao"]
GIAN_GIAO = ["day", "vua", "mong"]
LOAI_CAU_HOI = ["tai_hien", "van_dung", "phan_tich"]
BLOOM = ["nho", "hieu", "ap_dung", "phan_tich", "danh_gia", "sang_tao"]
BLOOM_TINH_BANG_CHUNG = ["ap_dung", "phan_tich", "danh_gia", "sang_tao"]
NGUON_SAI_LAM = ["nguoi", "sach", "suy_doan"]

TRUONG_QUYEN = ["schema", "id", "loai", "cau_truc", "nguon", "nguon_file",
                "canh_gioi_vao", "canh_gioi_ra", "mach", "khao_thi_quyen"]
TRUONG_BI_KIP = ["xuong_song", "chi_nhanh", "phu_thuoc", "lop_nhiem_vu", "ha_son_sau"]
TRUONG_SU_PHAM = ["muc_tieu", "gia_dinh_nen", "worked_example",
                  "sai_lam_pho_bien", "tieu_chi_dat", "khuon_cau_hoi"]


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

def doc_yaml(path, kq):
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


def van_tay(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for khoi in iter(lambda: f.read(1 << 20), b""):
            h.update(khoi)
    return "sha256:" + h.hexdigest()


# ------------------------------------------------------- kiểm cấp quyển

# Trường bắt buộc CÓ MẶT, nhưng được phép rỗng.
CHO_PHEP_RONG = {"chi_nhanh", "gia_dinh_nen", "sai_lam_pho_bien", "vai",
                 "du_thua", "phu_thuoc", "ha_son_sau"}


def kiem_truong_bat_buoc(d, truong, kq, o):
    """Vắng khoá là lỗi. Rỗng chỉ là lỗi khi trường đó không được phép rỗng."""
    for t in truong:
        if t not in d or d[t] is None:
            kq.L("thieu-truong", f"thiếu trường bắt buộc `{t}`", o)
        elif d[t] in ("", [], {}) and t not in CHO_PHEP_RONG:
            kq.L("truong-rong", f"trường `{t}` không được rỗng", o)


def kiem_enum(gia_tri, hop_le, ten, kq, o):
    if gia_tri is not None and gia_tri not in hop_le:
        kq.L("enum-sai", f"`{ten}` = {gia_tri!r}, phải thuộc {hop_le}", o)


def kiem_manifest(m, thu_muc, kq):
    o = "manifest.yaml"
    kiem_truong_bat_buoc(m, TRUONG_QUYEN, kq, o)

    if m.get("schema") != SCHEMA:
        kq.L("schema-khong-khop",
             f"schema = {m.get('schema')!r}, script này chỉ đọc schema {SCHEMA}. "
             "Nâng cấp có ý thức, đừng để script đoán.", o)
        return

    kiem_enum(m.get("loai"), ["bi-kip", "tan-quyen"], "loai", kq, o)
    kiem_enum(m.get("cau_truc"), ["chuoi", "mang"], "cau_truc", kq, o)
    kiem_enum(m.get("canh_gioi_vao"), CANH_GIOI, "canh_gioi_vao", kq, o)
    kiem_enum(m.get("canh_gioi_ra"), CANH_GIOI, "canh_gioi_ra", kq, o)

    vao, ra = m.get("canh_gioi_vao"), m.get("canh_gioi_ra")
    if vao in CANH_GIOI and ra in CANH_GIOI:
        if CANH_GIOI.index(ra) < CANH_GIOI.index(vao):
            kq.L("canh-gioi-lui",
                 f"canh_gioi_ra ({ra}) thấp hơn canh_gioi_vao ({vao})", o)

    ident = m.get("id")
    if ident and (ident != ident.lower() or " " in ident or "_" in ident):
        kq.L("id-sai-quy-cach",
             f"`id` = {ident!r} — phải kebab-case, không dấu, không khoảng trắng", o)
    if ident and ident != thu_muc.name:
        kq.G("id-khac-thu-muc",
             f"`id` ({ident}) khác tên thư mục ({thu_muc.name}). "
             "Hợp lệ — id là bất biến, tên thư mục thì không.", o)

    nf = m.get("nguon_file") or {}
    dp = nf.get("duong_dan")
    if dp:
        p = Path(dp).expanduser()
        if not p.exists():
            kq.C("gay-con-tro", f"không thấy file nguồn: {dp}. Chạy /vd:noi-lai", o)
        elif nf.get("van_tay"):
            thuc = van_tay(p)
            if thuc != nf["van_tay"]:
                kq.C("gay-con-tro",
                     f"vân tay không khớp — file nguồn đã đổi. Chạy /vd:noi-lai", o)

    if not m.get("vai"):
        kq.G("khong-the-vai", "không có thẻ `vai` — sẽ hiện ở khung nhìn tâm pháp", o)


# ------------------------------------------------------- kiểm sư phạm

def kiem_khoi_su_pham(d, kq, o):
    """Dùng cho cả chương (bí kíp) lẫn cấp gốc (tàn quyển)."""
    kiem_truong_bat_buoc(d, TRUONG_SU_PHAM, kq, o)

    tieu_chi = d.get("tieu_chi_dat") or []
    cau_hoi = d.get("khuon_cau_hoi") or []

    ids_tc = []
    for tc in tieu_chi:
        if not isinstance(tc, dict) or "id" not in tc or "mo_ta" not in tc:
            kq.L("tieu-chi-sai", "mỗi `tieu_chi_dat` cần `id` và `mo_ta`", o)
            continue
        if tc["id"] in ids_tc:
            kq.L("id-trung", f"`tieu_chi_dat.id` trùng: {tc['id']}", o)
        ids_tc.append(tc["id"])

    ids_q, duoc_phu, co_ap_dung = [], set(), False
    for q in cau_hoi:
        if not isinstance(q, dict) or "id" not in q:
            kq.L("cau-hoi-sai", "mỗi `khuon_cau_hoi` cần `id`", o)
            continue
        if q["id"] in ids_q:
            kq.L("id-trung", f"`khuon_cau_hoi.id` trùng: {q['id']}", o)
        ids_q.append(q["id"])

        kiem_enum(q.get("loai"), LOAI_CAU_HOI, f"{q['id']}.loai", kq, o)
        kiem_enum(q.get("bloom"), BLOOM, f"{q['id']}.bloom", kq, o)

        if q.get("bloom") in BLOOM_TINH_BANG_CHUNG:
            co_ap_dung = True

        tro = q.get("do_tieu_chi") or []
        if q.get("loai") == "tai_hien" and tro:
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
    if isinstance(we, dict) and not we.get("tro_toi"):
        kq.L("worked-example-sai",
             "`worked_example` phải có `tro_toi` — con trỏ vào sách gốc", o)

    slpb = d.get("sai_lam_pho_bien")
    if not slpb:
        kq.C("chua-co-sai-lam",
             "`sai_lam_pho_bien` rỗng — hợp lệ, nhưng F4 sẽ không chẩn đoán được, "
             "chỉ báo sai. Nó tự đầy lên qua lớp chú giải.", o)
    else:
        for i, sl in enumerate(slpb):
            if not isinstance(sl, dict):
                kq.L("sai-lam-sai", f"mục {i} không phải ánh xạ", o)
                continue
            for t in ("dau_hieu", "quan_niem_sai", "cach_chua", "nguon"):
                if not sl.get(t):
                    kq.L("sai-lam-thieu-truong", f"mục {i} thiếu `{t}`", o)
            kiem_enum(sl.get("nguon"), NGUON_SAI_LAM, f"sai_lam[{i}].nguon", kq, o)
            if sl.get("nguon") == "suy_doan":
                kq.G("sai-lam-suy-doan",
                     f"mục {i} nguồn `suy_doan` — phải hiện cờ khi dùng", o)


# ------------------------------------------------------- kiểm đồ thị

def kiem_do_thi(m, so_chuong, kq):
    o = "manifest.yaml"
    xs = m.get("xuong_song") or []
    cn = m.get("chi_nhanh") or []
    pt = m.get("phu_thuoc") or {}

    giao = sorted(set(xs) & set(cn))
    if giao:
        kq.L("xuong-song-giao-chi-nhanh",
             f"chương vừa xương sống vừa chi nhánh: {giao}", o)

    thieu = sorted(so_chuong - set(xs) - set(cn))
    if thieu:
        kq.L("chuong-khong-phan-loai",
             f"chương có file nhưng không nằm ở xuong_song lẫn chi_nhanh: {thieu}", o)

    la = sorted((set(xs) | set(cn)) - so_chuong)
    if la:
        kq.L("chuong-khong-co-file", f"khai chương nhưng không có file: {la}", o)

    # phụ thuộc: tồn tại và không có vòng
    for c, deps in pt.items():
        if c not in so_chuong:
            kq.L("phu-thuoc-la", f"phu_thuoc khai chương không có file: {c}", o)
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
                     f"qua phu_thuoc: {ket}", o)

    # lớp nhiệm vụ
    lnv = m.get("lop_nhiem_vu") or []
    phu, dem = set(), {}
    truoc = -1
    for i, lop in enumerate(lnv):
        if not isinstance(lop, dict):
            kq.L("lop-nhiem-vu-sai", f"lớp {i} không phải ánh xạ", o)
            continue
        kiem_enum(lop.get("do_phuc_tap"), DO_PHUC_TAP, f"lop[{i}].do_phuc_tap", kq, o)
        kiem_enum(lop.get("gian_giao"), GIAN_GIAO, f"lop[{i}].gian_giao", kq, o)
        if lop.get("do_phuc_tap") in DO_PHUC_TAP:
            muc = DO_PHUC_TAP.index(lop["do_phuc_tap"])
            if muc < truoc:
                kq.L("do-phuc-tap-giam-nguoc",
                     f"lớp {i} có độ phức tạp thấp hơn lớp trước — "
                     "giàn giáo xếp sai chiều", o)
            truoc = max(truoc, muc)
        for c in lop.get("chuong") or []:
            phu.add(c)
            dem[c] = dem.get(c, 0) + 1

    con = sorted(set(xs) - phu)
    if con:
        kq.L("lop-nhiem-vu-thieu-chuong",
             f"chương xương sống không nằm trong lop_nhiem_vu nào: {con}", o)

    if m.get("cau_truc") == "chuoi":
        nhieu = sorted(c for c, n in dem.items() if n > 1)
        if nhieu:
            kq.L("chuong-nhieu-lop-voi-chuoi",
                 f"cau_truc=chuoi nhưng chương nằm ở nhiều lớp: {nhieu}. "
                 "Nếu cố ý thì khai cau_truc=mang.", o)

    hs = m.get("ha_son_sau") or []
    la_hs = sorted(set(hs) - so_chuong)
    if la_hs:
        kq.L("ha-son-la", f"ha_son_sau trỏ tới chương không có: {la_hs}", o)
    if not hs:
        kq.C("khong-ha-son",
             "không có `ha_son_sau` — người học không có mốc nào xuống núi thử", o)


# ------------------------------------------------------- kiểm khảo thí

def kiem_khao_thi(m, kq):
    o = "manifest.yaml → khao_thi_quyen"
    kt = m.get("khao_thi_quyen") or {}
    if not isinstance(kt, dict):
        kq.L("khao-thi-sai", "`khao_thi_quyen` phải là ánh xạ", o)
        return
    for t in ("khuon", "bo_tham_so", "tieu_chi_dat"):
        if not kt.get(t):
            kq.L("khao-thi-thieu", f"thiếu `{t}`", o)

    khuon = kt.get("khuon") or ""
    bo = kt.get("bo_tham_so") or []
    import re
    dung = set(re.findall(r"\{(\w+)\}", khuon))

    if not isinstance(bo, list):
        kq.L("bo-tham-so-sai", "`bo_tham_so` phải là danh sách các bộ", o)
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

    if not kt.get("du_thua"):
        kq.C("khong-du-thua",
             "không có `du_thua` — mất một tín hiệu phân biệt: "
             "người học không phải chọn dữ kiện nào đáng dùng", o)


# ------------------------------------------------------- một bí kíp

def kiem_mot(thu_muc: Path) -> KetQua:
    kq = KetQua(thu_muc.name)
    m = doc_yaml(thu_muc / "manifest.yaml", kq)
    if m is None:
        return kq

    kiem_manifest(m, thu_muc, kq)
    if any(l["ma"] == "schema-khong-khop" for l in kq.loi):
        return kq

    loai = m.get("loai")
    thu_muc_chuong = thu_muc / "chuong"

    if loai == "tan-quyen":
        for t in TRUONG_BI_KIP:
            if t in m:
                kq.L("tan-quyen-thua-truong",
                     f"tàn quyển không được có `{t}`", "manifest.yaml")
        if thu_muc_chuong.exists():
            kq.L("tan-quyen-co-chuong",
                 "tàn quyển không được có thư mục `chuong/`", "manifest.yaml")
        kiem_khoi_su_pham(m, kq, "manifest.yaml (tàn quyển)")

    elif loai == "bi-kip":
        kiem_truong_bat_buoc(m, TRUONG_BI_KIP, kq, "manifest.yaml")
        for t in TRUONG_SU_PHAM:
            if t in m:
                kq.L("bi-kip-thua-truong",
                     f"bí kíp không đặt `{t}` ở cấp quyển — nó thuộc từng chương",
                     "manifest.yaml")
        if not thu_muc_chuong.exists():
            kq.L("thieu-thu-muc-chuong", "bí kíp phải có thư mục `chuong/`")
            return kq

        so_chuong = set()
        for f in sorted(thu_muc_chuong.glob("*.yaml")):
            d = doc_yaml(f, kq)
            if d is None:
                continue
            o = f"chuong/{f.name}"
            if d.get("schema") != SCHEMA:
                kq.L("schema-khong-khop", f"schema = {d.get('schema')!r}", o)
                continue
            so = d.get("chuong")
            if not isinstance(so, int):
                kq.L("chuong-thieu-so", "thiếu trường `chuong` kiểu số nguyên", o)
                continue
            if so in so_chuong:
                kq.L("chuong-trung", f"số chương trùng: {so}", o)
            so_chuong.add(so)
            kiem_khoi_su_pham(d, kq, o)

        if not so_chuong:
            kq.L("khong-co-chuong", "không có file chương nào đọc được")
        else:
            kiem_do_thi(m, so_chuong, kq)

    kiem_khao_thi(m, kq)
    return kq


# ------------------------------------------------------- in kết quả

BIEU = {"loi": "LỖI", "canh_bao": "CẢNH BÁO", "ghi_chu": "ghi chú"}


def in_text(kqs):
    for kq in kqs:
        trang_thai = "ĐẠT" if kq.dat() else "KHÔNG ĐẠT"
        print(f"\n=== {kq.ten} — {trang_thai} ===")
        for muc in ("loi", "canh_bao", "ghi_chu"):
            for m in getattr(kq, muc):
                o = f" [{m['o']}]" if m.get("o") else ""
                print(f"  {BIEU[muc]:<9}{m['thong_diep']}{o}")
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
    ap.add_argument("duong_dan", nargs="?", help="một quyển; bỏ trống = cả kho")
    ap.add_argument("--json", action="store_true", help="đầu ra JSON cho skill")
    ap.add_argument("--kho", default="~/.vandao/bi-kip", help="thư mục kho")
    a = ap.parse_args()

    if a.duong_dan:
        muc = [Path(a.duong_dan).expanduser()]
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

    kqs = [kiem_mot(p) for p in muc]

    if a.json:
        print(json.dumps({"schema": SCHEMA,
                          "ket_qua": [k.as_dict() for k in kqs]},
                         ensure_ascii=False, indent=2))
    else:
        in_text(kqs)

    sys.exit(1 if any(not k.dat() for k in kqs) else 0)


if __name__ == "__main__":
    main()
