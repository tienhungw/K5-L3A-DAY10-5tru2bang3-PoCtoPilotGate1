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


def _guard_events(trial, why):
    return [e for e in trial["events"]
            if e["type"] == "guard" and e.get("kind") == "refund_escalated" and e.get("why") == why]


def approval_use_rate(trials):
    """Tỉ lệ lần chạy mà agent đưa một mã phê duyệt vào khoản hoàn."""
    return sum(any(e["type"] == "approval_used" for e in t["events"]) for t in trials) / max(1, len(trials))


def approval_rejection_rate(trials):
    """Trong các lần agent đưa ra mã phê duyệt, tỉ lệ lần cổng bác vì mã không hợp lệ."""
    used = [t for t in trials if any(e["type"] == "approval_used" for e in t["events"])]
    return sum(bool(_guard_events(t, "approval")) for t in used) / max(1, len(used))


def max_customer_auto_refund_vnd(trials):
    """Tổng hoàn tự động lớn nhất cho một khách trong một ngày vận hành (đồng)."""
    totals = {}
    for t in trials:
        for row in t["ledger"]:
            if not row.get("approval_id"):
                key = (t["seed"], t["day"], row.get("customer_id"))
                totals[key] = totals.get(key, 0) + row["amount_vnd"]
    return max(totals.values(), default=0)


def manual_recheck_rate(trials):
    """Tỉ lệ quyết định tự động bị nhân viên kiểm lại bằng tay."""
    decided = [t for t in trials if t["status"] in ("refunded", "denied")]
    return sum(t.get("review_kind") == "recheck" for t in decided) / max(1, len(decided))


def queue_stuck_rate(trials):
    """Tỉ lệ lần chạy bị ùn trong hàng chờ người duyệt."""
    return sum(bool(t.get("queue_stuck")) for t in trials) / max(1, len(trials))


MONITORS = {
    "escalation_rate": escalation_rate,     # có sẵn; KHÔNG tính là metric mới của đội
    "claim_override_rate": claim_override_rate,
    "fault_tracking_mismatch_rate": fault_tracking_mismatch_rate,
    "approval_use_rate": approval_use_rate,
    "approval_rejection_rate": approval_rejection_rate,
    "max_customer_auto_refund_vnd": max_customer_auto_refund_vnd,
    "manual_recheck_rate": manual_recheck_rate,
    "queue_stuck_rate": queue_stuck_rate,
}
STARTER_MONITORS = ("escalation_rate",)
