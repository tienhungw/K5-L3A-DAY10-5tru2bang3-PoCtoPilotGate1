"""★ FILE ĐỘI SỬA (2/3): chỉ số theo dõi (monitor). Thêm ÍT NHẤT MỘT chỉ số bắt được sự cố của bàn.

Mỗi monitor nhận danh sách trial (KHÔNG có nhãn đúng/sai, giống production) và trả về một số.
Một trial = {"ticket_id", "seed", "day", "status", "amount_vnd", "ticket", "events", "ledger", "faults", "outbound",
             "arrive_min", "warehouse", "cost_vnd", "review_kind", "queue_wait_min", "queue_stuck"}
  "day"            một ngày vận hành giả lập: các ticket cùng "day" và cùng "seed" chạy nối nhau trên cùng một sổ cái
  "arrive_min"     phút ticket tới trong ca (0..480)          "warehouse"   kho của đơn
  "cost_vnd"       tiền LLM + nền tảng đã tốn cho ticket      "review_kind" None / "escalated" (trợ lý chuyển người) /
  "queue_wait_min" số phút chờ người duyệt (None nếu không vào hàng chờ)     "recheck" (nhân viên tự kiểm lại)
Chỉ số có thể là kỹ thuật (tỉ lệ model đè số trong ticket lên DB), vận hành (số ca cần người trong giờ đông nhất),
hay kinh doanh (tỉ lệ ticket trợ lý đọc xong vẫn phải chuyển người).

lab10.grade kiểm: monitor chạy không lỗi, và giá trị trên gói sự cố khác giá trị trên bộ nền,
tức là monitor "sáng đèn" khi sự cố xảy ra.
"""


def escalation_rate(trials):
    return sum(t["status"] == "escalated" for t in trials) / max(1, len(trials))


def claim_override_rate(trials):
    """Tỉ lệ lần chạy mà model dùng số ngày khách khai khác số ngày trong tracking."""
    hits = sum(any(e["type"] == "model_override" and e.get("ticket") != e.get("db") for e in t["events"])
               for t in trials)
    return hits / max(1, len(trials))


def fault_tracking_mismatch_rate(trials):
    """Tỉ lệ dòng lỗi hãng có kiện hoặc số ngày trễ không khớp tracking của lần chạy đó."""
    total = wrong = 0
    for t in trials:
        tracking = next((e for e in t["events"] if e["type"] == "tracking"), {})
        delays = {p["parcel_id"]: p["delay"] for p in tracking.get("parcels", [])}
        for row in t["faults"]:
            total += 1
            wrong += delays.get(row.get("parcel_id")) != row.get("delay_days")
    return wrong / max(1, total)


MONITORS = {
    "escalation_rate": escalation_rate,     # có sẵn; KHÔNG tính là metric mới của đội
    "claim_override_rate": claim_override_rate,
    "fault_tracking_mismatch_rate": fault_tracking_mismatch_rate,
}
STARTER_MONITORS = ("escalation_rate",)
