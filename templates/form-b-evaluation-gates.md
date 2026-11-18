# Phiếu B · Đo, rủi ro, cổng vòng 1 và quyết định v1 · Khối 2A + 2B + chốt (phút 65–115)

**Bàn:** K5-L3A-DAY10-5tru2bang3-PoCtoPilotGate1

Tiêu chí đã ký ở Phiếu A. Từ phút 65 bàn mới được chạy trợ lý. Khối 2A (65–85) chưa sửa code hay config. Khối 2B (85–105) sửa
`lab10/guards.py` và `config/operating_gates.json`. Phút 105–115 chốt cổng vòng 1 rồi viết quyết định v1. Sau phút 115 không sửa phiếu này
(trừ khi Phiếu C bảo "mở lại" một ô và ghi bằng bút khác màu).

**Mục lục**
- [B0 · Nhật ký lần chạy vòng 1 (suốt khối)](#b0)
- [B1 · Câu 2.1 · Lần chạy đầu tiên, cổng tự chặn hay người duyệt · phút 65–71](#b1)
- [B2 · Câu 2.2 · Bảng soát lỗi `T-002@55` · phút 71–75](#b2)
- [B3 · Câu 2.3 · Bản đồ dữ liệu và ví dụ drift · phút 65–75](#b3)
- [B4 · Câu 2.4 · HAZOP vòng 1 · phút 65–75](#b4)
- [B5 · Câu 2.4 · Checklist 9 nhóm việc, lần 1 · phút 70–75](#b5)
- [B6 · Câu 2.5 · Pre-mortem bốn lăng kính → cổng phòng ngừa · phút 75–85](#b6)
- [B7 · Câu 2.6–2.10 · Cổng phòng ngừa, runbook phần 1–3, giờ cao điểm · phút 85–105](#b7)
- [B8 · Chốt cổng vòng 1 và quyết định Gate 1 · v1 · phút 105–115](#b8)

---

<a id="b0"></a>

## B0 · Nhật ký lần chạy vòng 1

*Yêu cầu: ít nhất 3 lần chạy, mỗi lần đổi một thứ, có mã lần chạy và khoảng tin cậy.* Mỗi lệnh `lab10.eval` và `lab10.grade` tự ghi
một dòng vào `runs/journal.jsonl`. Việc của bàn là điền cột "Đổi MỘT thứ gì" (tham số `--note`) và cột "Kết luận".
Mọi con số trong quyết định Gate 1 phải trỏ về một dòng ở đây hoặc ở Phiếu C mục C0.

| # | Mã lần chạy | Bộ ticket · mốc | Đổi MỘT thứ gì so với lần trước | pass_rate (khoảng tin cậy 95%) | pass_k | Hoàn sai (đ) · lỗi hãng oan · lộ dữ liệu | Tỉ lệ chuyển người | Kết luận (một câu) |
|---|---|---|---|---|---|---|---|---|
| 1 | | base · base | (baseline, chưa có cổng) | | | | | |
| 2 | | base · after | (cổng vòng 1, thử trước khi chốt) | | | | | |
| 3 | | base · prepared | (cổng vòng 1 đã chốt) | | | | | |
| 4 | | | | | | | | |

---

<a id="b1"></a>

## B1 · Câu 2.1 · Lần chạy đánh giá đầu tiên

```bash
python3 -m lab10.eval --suite base --stage base --note "baseline"
python3 -m lab10.gate --run runs/<mã lần chạy>/report.json
```

- Mã lần chạy: `__________` (ghi cả vào B0 dòng 1)
- Ngưỡng đã ký nào `[CHƯA]` đạt: …
- Khối "kinh doanh và vận hành" ở cuối output: dòng nào đáng lo? …
- Khối "theo kho và hãng": kho hoặc hãng nào có số xấu nhất? …

**Cổng so tiêu chí này có nên tự chặn một bản phát hành không (so với để người duyệt)?**

| Lý lẽ ủng hộ tự chặn | Lý lẽ phản đối |
|---|---|
| | |

Khuyến nghị (khoanh một): **tự chặn · người duyệt · kết hợp**. Vì: …

---

<a id="b2"></a>

## B2 · Câu 2.2 · Bảng soát lỗi cho `T-002@55`

```bash
python3 -m lab10.trace --suite base --ticket T-002 --seed 55
```

**Cách làm, giữ nguyên ba phần:** (1) ghi lại từng lỗi bằng **cái người ta thực sự thấy**, ai gặp, mức hệ trọng,
và xếp vào một trong ba **loại lỗi**; (2) đưa lỗi qua bộ câu hỏi để tìm **nguồn**; (3) viết **hướng xử lý**: vì sao người ta coi
đó là lỗi, người ta đi tiếp bằng đường nào, hệ thống học được gì.

Ba loại lỗi:
- **Giới hạn của hệ thống**: hệ thống không thể trả lời đúng, hoặc không trả lời được, vì giới hạn vốn có.
- **Lỗi ngữ cảnh**: hệ thống "chạy đúng thiết kế" nhưng người dùng thấy sai, vì hành động không được giải thích, trái với hình dung của họ, hoặc dựa trên giả định kém.
- **Lỗi chìm**: hệ thống chạy sai mà **cả người dùng lẫn hệ thống đều không nhận ra**. Với một trợ lý có quyền ghi sổ, đây là loại nguy hiểm nhất: người chịu hại thường là bên thứ ba.

### Phần 1 · Ghi lỗi (bằng chứng là mã ticket@seed và dòng trace, không tả chung chung)

| # | Lỗi: người ta thấy gì (dán dòng trace / sổ cái) | Ai gặp, ai chịu | Hệ trọng (thấp / cao) | Loại lỗi (giới hạn hệ thống / ngữ cảnh / chìm) |
|---|---|---|---|---|
| 1 | | | | |
| 2 | | | | |

### Phần 2 · Tìm nguồn (đánh dấu câu nào đúng với từng lỗi)

| Câu hỏi | Lỗi 1 | Lỗi 2 |
|---|---|---|
| **Đầu vào:** hệ thống có tự diễn giải / sửa đầu vào của người dùng theo cách họ không lường? Có đặt sai trọng số cho một lời nói hay tín hiệu của người dùng? | | |
| **Độ liên quan:** hệ thống có thiếu dữ liệu cần để quyết đúng? Dữ liệu vào có nhiễu, thiếu ổn định? | | |
| **Thứ bậc hệ thống:** có hai hệ thống cùng ghi / cùng theo dõi một thứ mà không rõ bên nào là chủ (ví dụ CSKH hoàn tay và trợ lý cùng ghi sổ)? | | |
| **Trạng thái hỏng:** nhiều lỗi cộng lại có làm tính năng không dùng được (ví dụ LLM lỗi liên tiếp)? | | |

### Phần 3 · Hướng xử lý (mỗi lỗi một ô)

| | Lỗi 1 | Lỗi 2 |
|---|---|---|
| Vì sao người gặp coi đây là lỗi | | |
| Kiểu giải pháp: phản hồi cho người dùng / trao quyền kiểm soát cho người / khác | | |
| Đường đi của người sau khi có giải pháp (ví dụ: ticket chuyển sang người duyệt → duyệt → khách được trả lời) | | |
| Hệ thống học được gì (tín hiệu ghi lại để theo dõi: tên metric trong `monitors.py`) | | |

**Ví dụ (bộ nền, đừng chép):** `T-002@55` · sổ cái có dòng hoàn 20.000đ, hãng VNX nhận một lỗi, trong khi tracking ghi trễ 2 ngày ·
khách không thấy gì sai, hãng chịu · cao · **lỗi chìm**. Nguồn: đầu vào (đặt sai trọng số cho con số khách tự khai). Xử lý:
hãng coi là lỗi vì sổ giao của họ ghi 2 ngày; kiểu giải pháp: trao quyền cho người (số khai khác tracking thì chuyển người duyệt);
tín hiệu: đếm sự kiện `model_override` mỗi ngày.

---

<a id="b3"></a>

## B3 · Câu 2.3 · Bản đồ dữ liệu của trợ lý và ví dụ drift

**Cách làm:** đi từ người dùng và việc họ cần làm, tới đầu ra của hệ thống, rồi mới hỏi hệ thống cần dữ liệu
gì, định dạng ra sao, và **thế giới thật làm dữ liệu đó lệch đi thế nào**; cuối cùng tóm lại trong vài câu.
Trợ lý LogiX không huấn luyện gì trong lab này, nên ta hỏi về "dữ liệu trợ lý đọc lúc chạy / trường then chốt / nguồn sự thật".
Gợi ý: mở `data/world.json` phần `policies`, `orders[].parcels`, `ops_limits`, `ops_facts`.

| Mục | Điền cho trợ lý hoàn tiền |
|---|---|
| Người dùng | |
| Việc người dùng cần làm xong | |
| Đầu ra của hệ thống (kể cả các lệnh ghi) | |
| Dữ liệu trợ lý đọc lúc chạy (bảng nào trong `data/world.json`) | |
| Trường then chốt quyết định tiền và lỗi hãng | |
| Với mỗi trường then chốt: **nguồn sự thật** hay **bản sao** (ai cập nhật, khi nào)? | |
| Định dạng cần để ý (ngày, trường được phép trống, đơn nhiều kiện) | |
| Thế giới thật làm dữ liệu lệch ở đâu (theo mùa, đổi chính sách, giờ cao điểm, người nhập tay)? | |
| Câu người ngoài sẽ hỏi về nguồn dữ liệu ("sao hệ thống biết đơn trễ mấy ngày?") | |

**Tóm lại (điền vào chỗ trống):**
Trợ lý dùng `__________`, `__________`, `__________` để giúp `__________` làm được `__________`.
Trường mà nếu sai thì tiền hoặc lỗi hãng sai theo: `__________`, `__________`.
Chúng tôi biết thế giới thật sẽ làm dữ liệu lệch ở: `__________`. Dấu hiệu nhìn thấy sớm nhất: `__________`.

**Ví dụ drift trong 3 tháng tới** (lấy từ dòng "thế giới thật làm dữ liệu lệch"): cái gì đổi `____` · đổi ngày nào `____` ·
trường nào cho thấy `____` · con số nào của Bản tiêu chí bị ảnh hưởng `____`.
Đây là đầu vào đổi hay quan hệ vào–ra đổi? Chỉ số nào sẽ phát hiện? `__________`

**Ví dụ một dòng (đừng chép):** trường then chốt `parcels[].delivered_date` · bản ghi do máy quét ở điểm phát tạo ra, là nguồn
sự thật về ngày giao · lệch khi điểm phát quét sót hoặc nhập bù bằng tay.

---

<a id="b4"></a>

## B4 · Câu 2.4 · HAZOP vòng 1 trên tool của agent

*Chỉ làm MỘT vòng, trên MỘT tool. Đây là HAZOP vòng 1; HAZOP của thẻ sự cố viết riêng ở Phiếu C mục C4, không ghi đè bảng này.*

**Khung tư duy.** HAZOP không hỏi "cái gì có thể hỏng" một cách chung chung. Nó cầm từng **từ gợi ý** áp vào từng **dòng dữ
liệu đi vào một hành động** và hỏi: nếu dòng này lệch theo kiểu đó thì hậu quả là gì, ai chịu. Mục tiêu là tìm ra những nhánh
mà cả bàn chưa nghĩ tới, không phải tả lại nhánh đã biết.

| Guideword | Nghĩa khi áp vào một tool của agent |
|---|---|
| **WRONG** | Giá trị đưa vào có đủ, hợp lệ về hình thức, nhưng sai sự thật |
| **INVALID** | Giá trị không còn hiệu lực: hết hạn, sai phiên bản, sai đối tượng |
| **INCOMPLETE** | Thiếu một phần thông tin cần có để quyết định |
| **PERTURBED** | Đầu vào bị ai đó cố ý hoặc vô tình làm lệch (cài câu lệnh, gửi lặp) |
| **INCAPABLE** | Thành phần không trả lời được: quá tải, lỗi, hết quota |

**Câu hỏi dẫn dắt:** tool nào tạo ra hậu quả không đảo ngược? Mỗi tham số của tool đó lấy từ đâu (ticket, DB, model tự suy)?
Với mỗi guideword: hậu quả cho ai, hiện có gì ngăn, cần thêm gate ở tầng nào (phát hiện / chặn / giới hạn thiệt hại)?

Tool chọn phân tích: `notify_carrier` (gửi thông báo cho hãng sau khi ghi lỗi hãng; đây là chỗ dữ liệu rời hệ thống LogiX, `lab10/agent.py` dòng 200–205)

| Tham số / dòng dữ liệu | Guideword | Lệch cụ thể (viết bằng dữ kiện của lab) | Hậu quả, cho ai | Hiện có gì ngăn? | Gate đề xuất + tầng |
|---|---|---|---|---|---|
| `carrier_id` (lấy từ `parcels[0]`) | WRONG | Đơn nhiều kiện (ví dụ `O-1013` của `T-013`): code lấy hãng của kiện đầu tiên, trong khi kiện trễ có thể do hãng khác chở. Thông báo và lỗi đi nhầm hãng. **Nhánh bàn chưa thấy trên trace.** | Hãng không có lỗi bị báo lỗi, có thể bị phạt (GHSH 150.000đ/lỗi); hãng có lỗi thật không biết | Không có | `write_gate` so `carrier_id` với kiện có `delay_cause` thuộc lỗi hãng; lệch thì chặn (chặn) |
| `payload.recipient_contact` (tên, SĐT người nhận đơn quà) | INCOMPLETE | Đơn `is_gift`: trợ lý gửi tên và SĐT người nhận cho hãng mà không có sự đồng ý của người nhận | Người nhận quà bị lộ dữ liệu; LogiX chịu trách nhiệm pháp lý về dữ liệu cá nhân | Không có (bản phát `pii_fields_blocked_to_third_party` = `[]`) | `legal.pii_fields_blocked_to_third_party` có `recipient_contact` (chặn) |
| `payload.customer_note` (chữ khách tự gõ) | PERTURBED | Khách gõ tên, SĐT, địa chỉ của người khác hoặc câu lệnh vào ticket; nội dung được chép nguyên văn sang hãng | Người thứ ba bị lộ dữ liệu; hãng nhận nội dung không kiểm soát | Không có | Chặn `customer_note` trong `legal.pii_fields_blocked_to_third_party` (chặn) |
| `delay_days` | WRONG | Số ngày trễ lấy theo lời khách thay vì tracking DB, hãng nhận số sai | Hãng tranh chấp, chị Oanh phải sửa sổ khi đối soát | Chưa có | `write_gate` so với độ trễ từ `helpers` (chặn) |
| Kênh gửi hãng | INCAPABLE | Hệ thống của hãng không nhận thông báo, hoặc gửi lặp khi thử lại | Hãng nhận trùng thông báo, hiểu là nhiều lỗi | Không có | Theo dõi số thông báo mỗi hãng mỗi ngày (phát hiện) |

Không bắt buộc điền đủ năm dòng. Bắt buộc: **ít nhất ba dòng, trong đó một dòng là nhánh bàn chưa thấy trên trace**.

**Mở rộng ra ngoài kỹ thuật (thêm ít nhất hai dòng):** "thành phần" không chỉ là model và tool. Áp cùng năm từ gợi ý vào:

| Thành phần ngoài code | Ví dụ câu hỏi |
|---|---|
| **Người duyệt** (vận hành) | INCAPABLE: chỉ một người trực mà 14 ca tới trong một giờ thì ca cuối chờ bao lâu? |
| **Ngân sách** (kinh doanh) | WRONG: tổng hoàn tự động trong ngày vượt mức Finance cho phép mà không ai được báo thì sao? |
| **Phạm vi pilot** (kinh doanh) | INVALID: có nhóm ticket nào trợ lý luôn phải chuyển người, tức là tự động hoá vô nghĩa? |
| **Dữ liệu gửi bên thứ ba** (pháp lý) | PERTURBED: chữ khách tự gõ có tên, số điện thoại người khác bị chép sang hãng thì ai chịu? |

| Thành phần | Guideword | Lệch cụ thể | Hậu quả, cho ai | Cổng đề xuất: code hay con số nào trong `config/operating_gates.json` |
|---|---|---|---|---|
| Người duyệt (vận hành) | INCAPABLE | Chỉ 1 người trực (`default_reviewers_on_shift` = 1), duyệt 6 ca/giờ; giờ cao điểm tới 14 ca/giờ thì ca cuối chờ hơn 60 phút (`review_sla_minutes`) | Khách chờ lâu, chị Hạnh quá tải, ca bị ùn | `operations.reviewers_on_shift`, `operations.max_queue_wait_minutes` = 60; runbook Giờ cao điểm gọi thêm người |
| Ngân sách (kinh doanh) | WRONG | Tổng hoàn tự động trong ngày vượt 2.000.000đ (`daily_auto_refund_budget_vnd`) mà không ai được báo | LogiX mất tiền ngoài mức Finance duyệt; chị Oanh phát hiện muộn khi đối soát | `business.daily_refund_cap_vnd`; điều kiện dừng trong `operations.stop_conditions` |
| Dữ liệu gửi bên thứ ba (pháp lý) | PERTURBED | Chữ khách tự gõ có tên, SĐT người khác bị chép sang hãng | Người thứ ba lộ dữ liệu, LogiX chịu trách nhiệm | `legal.pii_fields_blocked_to_third_party` = `["recipient_contact", "customer_note"]` |
| Ghi lỗi cho hãng (pháp lý, hãng nhỏ) | INCOMPLETE | Tracking chưa ghi `delay_cause` (trễ do thời tiết, do khách) mà trợ lý vẫn ghi lỗi cho hãng | Hãng nhỏ GHSH, DNB bị đình chỉ sau 3 lỗi trong 7 ngày | `legal.carrier_fault_requires_recorded_cause` = `true` |

**Ví dụ mẫu (`issue_refund`, đừng chép):** tham số `amount_vnd` · WRONG · số tiền tính từ số ngày khách tự khai · LogiX mất
tiền, hãng bị kéo theo một lỗi · hiện chỉ có trần "không vượt tổng tiền đơn" · cổng ghi so với quyền lợi tính từ DB (chặn).

---

<a id="b5"></a>

## B5 · Câu 2.4 · Checklist go-live 9 nhóm việc, lần 1

Checklist chín nhóm việc phải xong trước khi chạy thử thật. Bàn điền lần đầu ở đây, rồi cập nhật sau sự cố ở Phiếu C mục C11.
Cột "Bằng chứng lấy từ đâu" trỏ tới mục bàn đã điền ở bước khác; không điền thêm phiếu nào chỉ để lấp cột này.

Trạng thái: **Xong** (có bằng chứng) · **Chưa** · **Không áp dụng** (ghi lý do). Bằng chứng là **mã lần chạy**, tên file / mục phiếu, hoặc số trong report.
**Cột PIC bắt buộc:** mỗi dòng một người có tên (không ghi "cả bàn"). Dòng nào chưa có PIC thì coi như Chưa.

| # | Nhóm việc | Bằng chứng lấy từ đâu (đã có sẵn trong lab) | Mục cần kiểm tra | Trạng thái | Bằng chứng | PIC |
|---|---|---|---|---|---|---|
| 1 | Chất lượng | Report `lab10.eval` (mã lần chạy) + bảng soát lỗi (Phiếu B mục B2) | pass_rate, pass^k đạt ngưỡng đã ký; `T-002@55` đã xếp loại lỗi | Chưa | (mã lần chạy base: chờ chạy câu 2.1) | Nguyễn Tiến Hưng |
| 2 | Dữ liệu | Bản đồ dữ liệu (Phiếu B mục B3, câu 2.3): trường nào là nguồn sự thật, trường nào là bản sao | Độ trễ và `delay_cause` lấy từ tracking DB, không lấy lời khách; có một ví dụ drift | Chưa | Phiếu B mục B3 (chờ điền) | Dương Ngọc Tuyên |
| 3 | Bảo mật | Một vòng HAZOP với guideword PERTURBED (Phiếu B mục B4): chữ nào đi vào model mà không do LogiX viết | `customer_note` do khách gõ, được chép sang hãng | Xong | Phiếu B mục B4, dòng PERTURBED; `legal.pii_fields_blocked_to_third_party` | Nguyễn Tiến Hưng |
| 4 | Quyền hạn | `config/switches.json` + guard trước lệnh ghi; thẻ S2, S8 có thêm mục mức kiểm soát (Phiếu C mục C3) | Có `write_gate` trước `issue_refund`, `file_carrier_fault`; người giữ công tắc là NV-TUNG | Chưa | `lab10/guards.py` (chờ câu 2.6) | Nguyễn Tiến Hưng |
| 5 | Hiệu năng, hạ tầng | Đội tự ước tính; HAZOP guideword INCAPABLE: LLM không trả lời thì sao; số người duyệt và số ca mỗi giờ | 1 người × 6 ca/giờ có đủ cho lượng ca chuyển người không; LLM lỗi thì ticket về làm tay | Chưa | Phiếu B mục B4 dòng INCAPABLE; số ca ùn trong report (chờ chạy) | Nguyễn Tiến Hưng |
| 6 | Chi phí | Khối "kinh doanh và vận hành" của report: chi phí mỗi ticket so với làm tay, ROI, tiền LLM ticket đắt nhất; `config/operating_gates.json` mục `business` | Chi phí mỗi ticket < 10.000đ làm tay; tiền LLM ≤ 1.500đ/ticket | Chưa | Mục `business` (chờ câu 2.9); report (chờ chạy) | Dương Ngọc Tuyên |
| 7 | Vận hành | Runbook (Phiếu B mục B7.5–B7.6) + `config/operating_gates.json` mục `operations` (PIC, người duyệt, số người trực, điều kiện dừng, kênh báo tin) + metric trong `monitors.py` | PIC, người duyệt, điều kiện dừng, kênh báo tin đã đặt; runbook 1–3 khớp số | Xong | `config/operating_gates.json` mục `operations`; Phiếu B mục B7.5, B7.6 | Dương Minh Tân |
| 8 | Con người, pháp lý | Bên thứ ba (hãng, tài xế, shop, người nhận quà, người đứng tên duyệt); `config/operating_gates.json` mục `legal`; thẻ S6, S7, S8 có mục riêng ở Phiếu C mục C3 | Không gửi SĐT người nhận quà và chữ khách tự gõ cho hãng; chỉ ghi lỗi hãng khi tracking có nguyên nhân | Xong | `config/operating_gates.json` mục `legal`; Phiếu B mục B4 | Dương Minh Tân |
| 9 | Quyết định | Câu tiêu chí (Phiếu A mục A4) + hash Bản tiêu chí đã ký + quyết định Gate 1 (Phiếu B mục B8, Phiếu C mục C12) | Tiêu chí đã ký và push trước lần chạy đầu; v1 khớp `decision_rule` | Chưa | Phiếu A mục A5 (chờ ký) | Dương Ngọc Tuyên |

Ô "Chưa" có rủi ro cao → chuyển thành một dòng Risk register (Phiếu C mục C10).

---

<a id="b6"></a>

## B6 · Câu 2.5 · Pre-mortem bốn lăng kính → cổng phòng ngừa (khoảng 8–10 phút, cả bàn)

*Mọi bàn làm pre-mortem ở vòng 1, TRƯỚC khi biết sự cố, để chọn 2–3 cổng phòng ngừa sẽ dựng. Ở vòng 2 bàn mở lại phần này ở
Phiếu C mục C1 (bút khác màu).*

**Khung tư duy.** Hỏi "có rủi ro gì không" thì ai cũng dè dặt. Nói "nó đã hỏng rồi, vì sao" thì mọi người được phép nói ra
điều mình vẫn lo. Làm im lặng trước, đọc sau, để ý kiến của người nói to không lấn át.

**Đề bài (đọc to):** *"Ba tháng sau pilot, LogiX phải tắt trợ lý hoàn tiền ở cả hai depot. Chuyện gì đã xảy ra?"*

1. **2 phút, im lặng:** mỗi người viết 2 lý do, mỗi lý do một dòng.
2. **2 phút:** đọc vòng tròn, mỗi lượt một lý do, không bình luận. Gộp lý do trùng.
3. **2 phút:** xếp từng lý do vào một **lăng kính**. Lăng kính nào còn trống thì cả bàn viết thêm ít nhất một lý do cho nó.
4. **2 phút:** chọn 2–3 lý do sẽ biến thành **cổng phòng ngừa** ngay hôm nay (code trong `guards.py` hoặc con số trong
   `config/operating_gates.json`). Lý do còn lại → Risk register.

Bốn lăng kính (bắt buộc đủ cả bốn; dự án AI hay chết ở ba lăng kính sau hơn là ở lăng kính đầu):

| Lăng kính | Câu hỏi gợi ý trên LogiX |
|---|---|
| **Kỹ thuật** | Model tin nhầm cái gì? Dữ liệu nào thiếu, cũ, lệch? Lệnh ghi nào không đảo ngược được? |
| **Kinh doanh** | Mỗi ticket tốn bao nhiêu so với làm tay? Một ngày hoàn tối đa bao nhiêu? Nhóm ticket nào không thể có lời? |
| **Con người và vận hành** | Ai duyệt, mấy người, mỗi giờ được mấy ca? Lượng việc tăng gấp ba thì sao? Nhân viên có tin trợ lý không? |
| **Pháp lý** | Dữ liệu cá nhân của ai rời hệ thống? Bên thứ ba nào bị ghi lỗi, bị trừ tiền mà không được hỏi? |

| Lý do thất bại (viết ở thì quá khứ) | Lăng kính | Kiểm được hôm nay? (trace / data / config nào) | Thành cổng phòng ngừa nào (code hay config) / hay vào risk register |
|---|---|---|---|
| | Kỹ thuật | | |
| | Kinh doanh | | |
| | Con người và vận hành | | |
| | Pháp lý | | |
| | | | |

---

<a id="b7"></a>

## B7 · Khối 2B · Cổng phòng ngừa (phút 85–105)

### B7.1 · Câu 2.6 · 2–3 cổng phòng ngừa trong `lab10/guards.py`

Mỗi cổng ứng với một dòng pre-mortem (B6) hoặc một dòng HAZOP (B4). Viết trong `pre_guard(ctx)` (trước khi trợ lý đọc ticket)
hoặc `write_gate(ctx, action)` (trước mỗi lệnh ghi). Thử bằng:

```bash
python3 -m lab10.eval --suite base --stage after --note "cổng vòng 1: ..."
python3 -m unittest discover -s tests
```

| # | Cổng (hàm và nhánh, ví dụ `write_gate` khi `tool == "issue_refund"`) | Ứng với dòng nào ở B6 / B4 | Chặn điều gì, dựa vào nguồn sự thật nào | Mã lần chạy `base · after` | Ca đang đúng nào bị hỏng? (phải là "không") |
|---|---|---|---|---|---|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |

### B7.2 · Câu 2.7 · Hai bước tránh rò rỉ dữ liệu

Bàn đang chỉnh cổng tới khi 22 ticket bộ nền xanh hết. Nêu 2 bước cụ thể để không "chỉnh trên chính bộ dùng để chấm"
(gắn với bộ nền, gói sự cố, bài kiểm tra ẩn):

1. **Không để cổng nhìn đáp án hoặc nhận ra bộ nền.** Agent đưa nguyên dòng ticket vào `ctx.ticket` (`lab10/agent.py`, dòng 40), nên cổng đọc được cả `label`, `kind`, `scenario`, là những trường production không có. Cổng của bàn chỉ dùng dữ liệu của yêu cầu và nguồn sự thật qua `ctx.tools`, `lab10.helpers`; không rẽ nhánh theo mã ticket, mã đơn, mã khách hay câu chữ của bộ nền. Trước `lab10.checkpoint`, chạy lệnh sau và kết quả phải trống: `git grep -nE "label|kind|scenario|T-[0-9]{3}|O-[0-9]{4}|C-[0-9]{2}|S[1-8]-[0-9]{2}" -- lab10/guards.py`.
2. **Giữ phần dữ liệu chưa dùng để chỉnh cổng.** Bộ nền chỉ dùng để phát hiện ca mới hỏng; 22 ticket xanh không chứng minh cổng đúng ở nơi khác. Cổng vòng 1 được chốt bằng `lab10.checkpoint` trước khi nhận thẻ, nên lần đầu chạy `lab10.grade --incident Sx` khi chưa sửa là số đo trên gói sự cố mà cổng chưa từng được chỉnh theo. Từ lúc sửa ở vòng 2, gói sự cố nhìn thấy đã thành dữ liệu để chỉnh, nên bài kiểm tra ẩn mới là phép đo độc lập; bàn không suy ra kết quả ẩn từ việc gói nhìn thấy đã xanh.

### B7.3 · Câu 2.8 · Một behavioral test

- Tính chất (một câu): …

```bash
python3 -m lab10.trace --suite base --stage after --adhoc "..." --order O-10xx --customer C-xx
```

| Ticket hiểm | Nội dung ticket (`--adhoc`) | `--order` · `--customer` | Kết quả (dán dòng `SỔ CÁI` / `LỖI HÃNG` / `GỬI HÃNG`) | Tính chất giữ được? |
|---|---|---|---|---|
| 1 | | | | |
| 2 | | | | |

Giữ hai ticket này cho phần demo.

### B7.4 · Câu 2.9 · Cổng kinh doanh (`config/operating_gates.json` mục `business`)

Mỗi con số kèm một câu lý do, lấy từ `data/world.json` → `ops_limits`, `ops_facts`.

| Khoá | Giá trị bàn đặt | Lý do (một câu, có số) |
|---|---|---|
| `business.daily_refund_cap_vnd` | | |
| `business.cost_budget_per_ticket_vnd` | | |
| `business.pilot_scope` (all / warehouse / percent) | | |
| `business.roi_min` | | |

### B7.5 · Câu 2.10 · Cổng con người, vận hành, pháp lý + Runbook phần 1–3

Điền `config/operating_gates.json` mục `operations` và `legal` (PIC, người duyệt, số người trực mỗi ca, công suất duyệt mỗi giờ,
thời gian chờ tối đa, điều kiện dừng, kênh báo tin; trường dữ liệu cá nhân không gửi cho bên thứ ba; ghi lỗi cho hãng phải có
nguyên nhân trong tracking). Rồi viết runbook dưới đây **khớp với các con số đó**.

*Runbook là tờ giấy người trực ca cầm lúc 23h khi có chuyện. Nó trả lời: nhìn con số nào, ngưỡng nào thì làm gì, ai được quyết.
Phần 1–3 và mục Giờ cao điểm viết ở vòng 1. Phần 4–5 viết ở vòng 2 (Phiếu C mục C11). Mọi con số phải khớp `config/operating_gates.json` và report.*
*Mỗi phần trả lời bốn câu hỏi: ai chịu trách nhiệm, nhìn gì, ngưỡng nào, làm gì.* **Người viết (vai Vận hành và pháp lý):** Dương Minh Tân

#### Runbook 1 · Ai chịu trách nhiệm

| Vai | Tên / mã nhân viên (lấy từ `data/world.json` → `staff`) | Được quyền làm gì | Liên lạc qua kênh nào |
|---|---|---|---|
| PIC của trợ lý (một người) | Lê Thanh Tùng · `NV-TUNG` (`operations.pic`) | Chịu trách nhiệm chung; quyết dừng một phần hoặc dừng hẳn; ký bật lại | `#logix-refund-pilot`, gọi điện khi tín hiệu đỏ |
| Người duyệt đứng tên các khoản vượt hạn mức | Trần Thị Hạnh · `NV-HANH` (`operations.approver_id`) | Duyệt hoặc từ chối ca trợ lý chuyển sang; đề nghị gọi thêm người trực | `#logix-refund-pilot` |
| Người giữ công tắc tắt từng thao tác ghi | Lê Thanh Tùng · `NV-TUNG` | Tắt `issue_refund`, `file_carrier_fault`, `notify_carrier`, `send_reply` trong `config/switches.json` | `#logix-refund-pilot` |
| Người nhận khiếu nại của bên thứ ba (hãng, shop, người nhận quà) | Phạm Kiều Oanh · `NV-OANH` | Ghi nhận khiếu nại, huỷ hoặc điều chỉnh dòng lỗi hãng và sổ cái khi đối soát; báo PIC | `#logix-refund-pilot`, email đối soát với hãng và shop |

Số người trực duyệt mỗi ca: **1** (`operations.reviewers_on_shift`) · Mỗi giờ duyệt được: **6** ca (`review_capacity_per_hour` = `null` → 1 × 6, theo `ops_facts`) · Phạm vi pilot: theo `business.pilot_scope` do vai Sản phẩm và kinh doanh đặt (câu 2.9)

#### Runbook 2 · Nhìn con số nào, ngưỡng nào thì làm gì

Mỗi dòng một tín hiệu. Cột "Lấy ở đâu" phải là một dòng trong report của `lab10.eval` / `lab10.grade` hoặc một chỉ số trong `lab10/monitors.py`.

| Tín hiệu | Lấy ở đâu | Bình thường | Ngưỡng VÀNG → việc làm | Ngưỡng ĐỎ → việc làm | Ai quyết |
|---|---|---|---|---|---|
| Thời gian chờ người duyệt lâu nhất | Report, khối "kinh doanh và vận hành": thời gian chờ | < 30 phút | ≥ 45 phút → chị Hạnh gọi thêm 1 người trực | > 60 phút (`max_queue_wait_minutes`) → thu hẹp `pilot_scope` | Hạnh (vàng), Tùng (đỏ) |
| Số ca bị ùn | Report: số ca bị ùn | 0 | 1 ca → gọi thêm người, báo vào kênh | > 2 ca trong một ca làm việc → tắt `issue_refund`, ticket về làm tay | Tùng |
| Chi phí mỗi ticket so với làm tay | Report: chi phí mỗi ticket, ROI | < 10.000đ (làm tay, `ops_facts`) và ≤ `business.cost_budget_per_ticket_vnd` | Chạm ngân sách mỗi ticket → báo vai Sản phẩm và kinh doanh | ≥ 10.000đ hoặc ROI dưới `business.roi_min` → đề xuất Thu hẹp | Tùng, cùng vai Sản phẩm và kinh doanh |
| Tổng tiền hoàn tự động trong ngày so với trần | Report: tổng tiền hoàn so với trần | < 80% trần ngày | ≥ 80% trần → báo chị Oanh, chị Hạnh chuẩn bị nhận ca | Chạm 2.000.000đ (`daily_auto_refund_budget_vnd`) → mọi khoản hoàn còn lại chuyển người duyệt | Tùng |
| Tiền hoàn sai | Report: `wrongful_refund_vnd` | 0đ | (không có vàng) | > 0đ → tắt `issue_refund`, chị Oanh rà sổ cái trong ngày | Tùng |
| Lỗi ghi oan cho hãng / lộ dữ liệu cá nhân (pháp lý) | Report: lỗi oan cho hãng, lộ dữ liệu cá nhân | 0 | (không có vàng) | ≥ 1 lỗi oan → tắt `file_carrier_fault` và `notify_carrier`; ≥ 1 lần lộ dữ liệu → tắt `notify_carrier` | Tùng |
| Tỉ lệ chuyển người duyệt | Report: tỉ lệ chuyển người duyệt | ≤ `escalation_rate_max` đã ký | Vượt ngưỡng đã ký → kiểm hàng chờ, gọi thêm người | Hàng chờ cùng lúc vượt 60 phút → thu hẹp phạm vi | Hạnh, Tùng |

#### Runbook 3 · Điều kiện dừng và cách dừng

- Dừng một phần (tắt một thao tác ghi, thu hẹp phạm vi) khi: có 1 lỗi ghi oan cho hãng (tắt `file_carrier_fault`, `notify_carrier`); có 1 lần lộ dữ liệu cá nhân sang hãng (tắt `notify_carrier`); tổng hoàn tự động trong ngày chạm 2.000.000đ (hoàn còn lại chuyển người duyệt); có ca chờ quá 60 phút (thu hẹp `business.pilot_scope`). Khớp `operations.stop_conditions`.
- Dừng hẳn khi: có tiền hoàn sai > 0đ lặp lại sau khi đã tắt và sửa một lần; hoặc hai điều kiện dừng một phần xảy ra trong cùng một ngày; hoặc điều kiện dừng trong `stop_condition` của tiêu chí đã ký bị chạm.
- Cách dừng, từng bước: (1) Tùng đặt công tắc tương ứng trong `config/switches.json` về tắt (dừng hẳn: cả bốn `issue_refund`, `file_carrier_fault`, `notify_carrier`, `send_reply`); (2) nếu là thu hẹp, đổi `business.pilot_scope` trong `config/operating_gates.json`; (3) báo vào `#logix-refund-pilot` lý do, giờ tắt, mã ticket gây tín hiệu; (4) chị Oanh khoá các dòng lỗi hãng và khoản hoàn của ngày để rà.
- Từ tín hiệu đỏ đến lúc dừng xong tối đa **15** phút; người bấm: **Lê Thanh Tùng (`NV-TUNG`)**; vắng thì chị Hạnh (`NV-HANH`) bấm và báo lại.
- Khi đã dừng, ticket đang chờ đi đâu, ai xử lý: mọi ticket mới và ticket đang chờ chuyển về hàng làm tay của CSKH; chị Hạnh phân ca; các khoản đã hoàn hoặc lỗi đã ghi trong ngày được chị Oanh rà lại.
- Điều kiện để bật lại, ai ký: đã tìm ra nguyên nhân, có cổng sửa (code hoặc con số), chạy lại `lab10.eval` trên bộ nền không có ca mới hỏng và chỉ số an toàn về 0; Tùng ký bật lại, chị Oanh xác nhận sổ đã khớp.

### B7.6 · Giờ cao điểm (bắt buộc với thẻ S4; các thẻ khác nên có)

Lượng ticket có thể dồn gấp ba trong một giờ (ngày sale, sau bão). Viết trước, khi chưa biết sự cố.

| Câu hỏi | Trả lời (có số, có tên) |
|---|---|
| Giờ cao điểm là khi nào, bao nhiêu ticket mỗi giờ (dựa vào `ops_facts`)? | Ngày sale và sau bão, lượng ticket gấp 3 trong một giờ. Một người duyệt chỉ được 6 ca/giờ (`review_capacity_per_reviewer_per_hour`). Nếu giờ cao điểm có 14 ca chuyển người duyệt thì 1 người chỉ xử lý được 6, còn 8 ca dồn sang giờ sau và chờ quá 60 phút (`review_sla_minutes`). |
| Ai trực giờ cao điểm, mấy người (khớp `operations.reviewers_on_shift`)? | Ngày thường: 1 người (`reviewers_on_shift` = 1), chị Hạnh (`NV-HANH`). Ngày sale đã biết trước: tăng `reviewers_on_shift` lên 3 (18 ca/giờ ≥ 14 ca/giờ), chị Hạnh cùng 2 nhân viên CSKH, Tùng (`NV-TUNG`) trực công tắc. |
| Ngưỡng nào thì **gọi thêm người** (hàng chờ bao nhiêu ca, chờ lâu nhất bao nhiêu phút)? Ai gọi? | Hàng chờ > 6 ca (quá sức 1 giờ của 1 người), hoặc có ca chờ ≥ 45 phút. Chị Hạnh gọi, báo vào `#logix-refund-pilot`. |
| Ngưỡng nào thì **thu hẹp** phạm vi (khoá `business.pilot_scope`) hoặc **tắt** một thao tác ghi (`config/switches.json`)? Ai quyết? | Có ca chờ > 60 phút (`max_queue_wait_minutes`) dù đã thêm người → thu hẹp `pilot_scope` về 1 kho hoặc giảm phần trăm. Hơn 2 ca bị ùn trong một ca làm việc → tắt `issue_refund`, ticket về làm tay. Tùng quyết. |
| Thêm người thì chi phí mỗi ticket và ROI thay đổi thế nào (đọc report)? | Mỗi người trực thêm tốn 30.000đ phí giữ chỗ mỗi ca (`reviewer_standby_fee_vnd`), nên chi phí mỗi ticket tăng và ROI giảm. Thêm 2 người là thêm 60.000đ/ca. Số cụ thể: đọc lại report sau khi đổi `reviewers_on_shift` (điền sau khi chạy). |

---

<a id="b8"></a>

## B8 · Chốt cổng vòng 1 và quyết định Gate 1 · v1 (phút 105–115)

Làm đúng thứ tự:

```bash
python3 -m lab10.checkpoint
python3 -m lab10.eval --suite base --stage prepared
python3 -m lab10.gate --run runs/<mã lần chạy>/report.json
```

**Khung tư duy.** Gate 1 "đạt" khi **quyết định khớp bằng chứng và khớp tiêu chí đã ký trước**. Tiếp tục, Thu hẹp, Cải tiến
thêm, Dừng đều có thể là quyết định đạt. Quyết định không đạt là quyết định mà con số trong report không đỡ được.
Chỉ chọn Tiếp tục khi mọi chỉ số bắt buộc đều đạt.

Ba câu tự vấn trước khi viết: (1) Rủi ro còn lại có chấp nhận được như hiện trạng không? (2) Cần thêm biện pháp nào, tốn
bao nhiêu thời gian? (3) Có phần nào của dự án không nên làm tiếp?

| | **v1** (phút 105–115, TRƯỚC khi nhận thẻ sự cố) |
|---|---|
| Commit ký tiêu chí (message `Sign acceptance criteria`; hash commit, tuỳ chọn) | |
| Hash chốt cổng vòng 1 (8 ký tự lệnh `lab10.checkpoint` in ra, tuỳ chọn) | |
| Mã lần chạy dùng làm bằng chứng | bộ nền, mốc base: ________ · bộ nền với cổng vòng 1 (prepared): ________ |
| Còn dòng "vượt trần" nào trong report? (hàng chờ, chi phí, ROI, trần tiền, pháp lý) | |
| Kho hoặc hãng có số xấu nhất: ____. Nếu chỉ nhìn phân khúc này, quyết định có đổi không? *(Đọc khối "theo kho và hãng" ở cuối output `lab10.eval` / `lab10.grade`, hoặc mục `by_segment` trong `report.json`.)* | |
| Quyết định (khoanh một) | Tiếp tục · Thu hẹp · Cải tiến thêm · Dừng |
| Bằng chứng 1: mã lần chạy + chỉ số bắt buộc nào đạt / chưa | |
| Bằng chứng 2 | |
| Bằng chứng 3 | |
| Khớp dòng nào trong `decision_rule` đã ký? | |
| Nếu Thu hẹp: cắt phần nào, vì sao | |
| Nếu Cải tiến thêm: giả thuyết cụ thể + hạn | |
| Nếu Dừng: bài học ghi lại | |
| Một bằng chứng còn thiếu (thứ bộ nền chưa đo được) | |
| Ngày quyết định lại (trừ khi Dừng) | |
| PIC ký | |

Xong v1 thì lưu và đẩy một bản (sau mốc này không sửa cột v1):

```bash
git add lab10/guards.py lab10/guards_round1.py config/operating_gates.json config/operating_gates.round1.json config/round1.lock templates/form-b-evaluation-gates.md
git commit -m "LAB 10: chốt cổng vòng 1, quyết định v1"
git push -u origin main
```
