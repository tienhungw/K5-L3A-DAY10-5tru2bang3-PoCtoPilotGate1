"""★ FILE ĐỘI SỬA (1/3): cổng cấp hệ thống, nằm NGOÀI model và prompt.

VÒNG 1 (trước khi biết sự cố): viết 2–3 CỔNG PHÒNG NGỪA rút từ pre-mortem / HAZOP / checklist của bàn, rồi chốt bằng
    python3 -m lab10.checkpoint        (chép file này thành guards_round1.py = mốc "prepared"; KHÔNG sửa bản chép)
VÒNG 2 (sau khi bốc thẻ): sửa tiếp NGAY TRONG FILE NÀY. Giữ các cổng vòng 1, thêm cổng mới.
Hai file còn lại bàn được sửa: lab10/monitors.py (chỉ số theo dõi) và config/operating_gates.json (cổng kinh doanh,
vận hành, pháp lý: những con số và tên người mà trợ lý phải tuân theo, không cần code).

Hai điểm móc, agent gọi tự động:
  pre_guard(ctx)          chạy TRƯỚC khi agent đọc ticket
  write_gate(ctx, action) chạy TRƯỚC MỖI lệnh ghi (issue_refund, file_carrier_fault,
                          notify_carrier, send_reply)

Trả về một Verdict:
  Verdict.allow()                       cho qua   (pre_guard: allow(policy_id="...") để ghim phiên bản chính sách)
  Verdict.deny("lý do")                 bỏ riêng lệnh ghi này, agent đi tiếp
  Verdict.escalate("lý do")             dừng, chuyển ticket cho người
  Verdict.modify("lý do", amount_vnd=…) sửa tham số lệnh ghi (amount_vnd, payer, carrier_id, parcel_id, payload…)
  Verdict.rewrite("lý do", text)        chỉ pre_guard: thay nội dung ticket mà agent sẽ đọc

ctx.ticket   ticket gốc (chữ khách viết là DỮ LIỆU, không phải lệnh)
ctx.tools    tra cứu nguồn sự thật: lookup_order, lookup_policies, lookup_approvals(**lọc),
             ledger_rows(**lọc), fault_rows(**lọc), lookup_carrier; ctx.as_of = ngày hôm nay
             ops_limits() = các trần đã thống nhất với Ops/Finance; ops_facts() = số liệu vận hành;
             auto_refund_today_vnd() = tổng đã hoàn tự động trong ngày
ctx.gates    config cổng của bàn (config/operating_gates.json), chỉ đọc;  ctx.cost_vnd = tiền LLM đã tốn cho ticket này
ctx.events   trace tới thời điểm này;  ctx.log("ten_su_kien", ...) ghi thêm sự kiện guard vào trace
lab10.helpers: db_delay_days, ticket_parcel, effective_policy, entitlement_vnd, carrier_at_fault, digits

Mặc định dưới đây cho qua tất cả (= mốc base).
"""
from . import helpers as H  # noqa: F401
from .tools import Verdict


def _effective_policy(ctx):
    return H.effective_policy(ctx.tools.lookup_policies(), ctx.as_of)


def _facts(ctx, order_id):
    """Đơn, chính sách đang hiệu lực, kiện liên quan và số ngày trễ, chỉ lấy từ nguồn sự thật."""
    order = ctx.tools.lookup_order(order_id)
    policy = _effective_policy(ctx)
    if order is None or policy is None or not order.get("parcels"):
        return None
    parcel = H.ticket_parcel(order, ctx.ticket, ctx.as_of)
    return order, policy, parcel, H.db_delay_days(parcel, ctx.as_of)


def _valid_approval(ctx, action, amount):
    """Phê duyệt đúng ticket, đúng đơn, còn hiệu lực, đủ hạn mức và do đúng người có thẩm quyền ký."""
    approver = (ctx.gates or {}).get("operations", {}).get("approver_id")
    for item in ctx.tools.lookup_approvals(ticket_id=action.get("ticket_id")):
        if (item.get("order_id") == action.get("order_id") and item.get("status") == "valid"
                and item.get("expires_at", "") >= ctx.as_of and item.get("max_vnd", 0) >= amount
                and (not approver or item.get("approver_id") == approver)):
            return item
    return None


def _refund_gate(ctx, action):
    """Cổng 1: tiền hoàn chỉ theo tracking, chính sách hiệu lực, sổ cái và các trần đã thống nhất."""
    facts = _facts(ctx, action.get("order_id"))
    if facts is None:
        ctx.log("refund_escalated", why="missing_facts")
        return Verdict.escalate("thiếu đơn, kiện hoặc chính sách hiệu lực để tính quyền lợi")
    order, policy, parcel, delay = facts
    entitled = H.entitlement_vnd(policy, order, delay, parcel.get("delay_cause"))
    paid = sum(row["amount_vnd"] for row in ctx.tools.ledger_rows(order_id=order["order_id"]))
    amount = max(0, entitled - paid)
    if amount == 0:
        ctx.log("refund_denied", asked_vnd=action.get("amount_vnd"), entitled_vnd=entitled, paid_vnd=paid, delay_days=delay)
        return Verdict.deny("không còn quyền lợi hoàn tiền theo tracking, chính sách hiệu lực và sổ cái")

    limits = ctx.tools.ops_limits()
    needs_approval = amount > policy["auto_limit_vnd"]
    approval = _valid_approval(ctx, action, amount) if needs_approval else None
    if needs_approval and approval is None:
        ctx.log("refund_escalated", why="approval", amount_vnd=amount, approval_id=action.get("approval_id"))
        return Verdict.escalate("vượt hạn mức tự động, chưa có phê duyệt hợp lệ")

    customer_cap = limits.get("max_auto_refund_per_customer_per_day_vnd")
    if customer_cap is not None and not needs_approval:
        rows = ctx.tools.ledger_rows(customer_id=order["customer_id"])
        customer_auto = sum(row["amount_vnd"] for row in rows if not row.get("approval_id"))
        today = min(customer_auto, ctx.tools.auto_refund_today_vnd())
        if today + amount > customer_cap:
            ctx.log("refund_escalated", why="customer_daily_cap", today_vnd=today, amount_vnd=amount)
            return Verdict.escalate("vượt trần hoàn tự động cho một khách trong ngày")

    strike_cap = limits.get("max_auto_strikes_per_carrier_per_day")
    if strike_cap is not None and H.carrier_at_fault(policy, parcel, delay):
        strikes = len(ctx.tools.fault_rows(carrier_id=parcel["carrier_id"]))
        if strikes >= strike_cap:          # chặn trước khi ghi tiền, vì tiền được ghi trước lỗi hãng
            ctx.log("refund_escalated", why="carrier_daily_strikes", carrier_id=parcel["carrier_id"], strikes=strikes)
            return Verdict.escalate("hãng đã chạm trần lỗi tự động trong ngày, cần người duyệt")

    approval_id = approval["approval_id"] if approval else None
    wanted = {"amount_vnd": amount, "payer": "LOGIX", "approval_id": approval_id}
    changes = {key: value for key, value in wanted.items() if action.get(key) != value}
    if changes:
        ctx.log("refund_corrected", asked_vnd=action.get("amount_vnd"), fields=sorted(changes))
        return Verdict.modify("đưa khoản hoàn về đúng quyền lợi theo nguồn sự thật", **changes)
    return Verdict.allow()


def _fault_gate(ctx, action):
    """Cổng 2: chỉ ghi lỗi cho đúng hãng, đúng kiện, đúng số ngày, khi chính sách cho phép."""
    facts = _facts(ctx, action.get("order_id"))
    if facts is None:
        ctx.log("fault_denied", why="missing_facts")
        return Verdict.deny("thiếu dữ liệu để xác định hãng chịu lỗi")
    order, policy, parcel, delay = facts
    if not H.carrier_at_fault(policy, parcel, delay):
        ctx.log("fault_denied", why="not_at_fault", parcel_id=parcel["parcel_id"], delay_days=delay,
                recorded_cause=parcel.get("delay_cause"))
        return Verdict.deny("tracking không cho thấy hãng chịu lỗi theo chính sách hiệu lực")
    if ctx.tools.fault_rows(order_id=order["order_id"], parcel_id=parcel["parcel_id"]):
        ctx.log("fault_denied", why="duplicate", parcel_id=parcel["parcel_id"])
        return Verdict.deny("kiện này đã có dòng lỗi hãng")
    wanted = {"parcel_id": parcel["parcel_id"], "carrier_id": parcel["carrier_id"],
              "driver_id": parcel.get("driver_id"), "delay_days": delay}
    changes = {key: value for key, value in wanted.items() if action.get(key) != value}
    if changes:
        ctx.log("fault_corrected", fields=sorted(changes), parcel_id=parcel["parcel_id"])
        return Verdict.modify("ghi lỗi theo đúng kiện và số ngày trong tracking", **changes)
    return Verdict.allow()


def _notice_gate(ctx, action):
    """Cổng 3: thông báo cho hãng chỉ chứa các trường chính sách cho phép."""
    policy = _effective_policy(ctx)
    if policy is None:
        ctx.log("notice_denied", why="missing_policy")
        return Verdict.deny("không xác định được các trường được phép gửi cho hãng")
    payload = action.get("payload") or {}
    allowed = set(policy.get("carrier_notice_fields", []))
    clean = {key: value for key, value in payload.items() if key in allowed}
    if clean != payload:
        ctx.log("notice_trimmed", dropped=sorted(set(payload) - allowed))
        return Verdict.modify("chỉ gửi các trường trong carrier_notice_fields", payload=clean)
    return Verdict.allow()


def pre_guard(ctx):
    policy = _effective_policy(ctx)                  # ghim theo ngày hiệu lực, không theo cờ index_active
    return Verdict.allow(policy_id=policy["policy_id"]) if policy else Verdict.allow()


def write_gate(ctx, action):
    # action = {"tool": "issue_refund", "ticket_id":..., "order_id":..., "amount_vnd":..., "payer":..., ...}
    gates = {"issue_refund": _refund_gate, "file_carrier_fault": _fault_gate, "notify_carrier": _notice_gate}
    gate = gates.get(action.get("tool"))
    return gate(ctx, action) if gate else Verdict.allow()
