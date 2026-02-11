from scanner.fa_gate.store import FASnapshotStore, FAStatus
from scanner.fa_gate.loader import FALoader


# 1. Tạo store
store = FASnapshotStore()

# 2. Tạo loader (min thanh khoản = 100 tỷ)
loader = FALoader(store, min_avg_value_traded=100_000_000_000)

# 3. Dữ liệu FA giả lập (offline batch)
raw_fa_data = {
    "VCB": {
        "avg_value_traded": 150_000_000_000,
        "is_suspended": False,
        "is_delisting": False,
        "profit_positive": True,
    },
    "PENNY": {
        "avg_value_traded": 10_000_000_000,
        "is_suspended": False,
        "is_delisting": False,
        "profit_positive": True,
    },
    "RISKY": {
        "avg_value_traded": 200_000_000_000,
        "is_suspended": True,
        "is_delisting": False,
        "profit_positive": True,
    },
    "UNKNOWN": {
        # thiếu dữ liệu
    },
}

# 4. Load batch (offline)
loader.load_batch(raw_fa_data)

# 5. Freeze snapshot (giả lập vào phiên)
store.freeze()

# 6. Kiểm tra status
symbols = ["VCB", "PENNY", "RISKY", "UNKNOWN"]

for s in symbols:
    status = store.get_status(s)
    print(f"{s} -> {status.value}")
