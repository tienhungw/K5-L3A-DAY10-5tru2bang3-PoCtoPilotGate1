# Phiếu A · Tiêu chí và cách đo · Khối 1 (phút 15–65)

**Bàn:** K5-L3A-DAY10-5tru2bang3-PoCtoPilotGate1 · **Người cầm bút chính:** vai Sản phẩm và kinh doanh (câu 1.3: Kỹ sư cổng; câu 1.2, 1.4: Vận hành và pháp lý)

Điền phiếu này **trước khi chạy trợ lý lần nào**. Viết xong thì chép ngưỡng sang `config/acceptance_criteria.json`, ký ở phút 60–65,
rồi mới chạy đánh giá. Khối 1 không sửa code.

**Mục lục**
- [A1 · Mục tiêu (câu 1.1, 1.2) · phút 15–20](#a1)
- [A2 · Thước đo → Dữ liệu → Cách tính (câu 1.3, 1.4) · phút 20–35](#a2)
- [A3 · Đọc một kết quả có khoảng tin cậy (câu 1.5) · phút 35–40](#a3)
- [A4 · Câu tiêu chí thành công và ranh giới đầu ra (câu 1.6) · phút 40–60](#a4)
- [A5 · Ký và đẩy tiêu chí · phút 60–65](#a5)

---

<a id="a1"></a>

## A1 · Mục tiêu (phút 15–20)

### Câu 1.1 · Một mục tiêu cấp hệ thống (khác "model trả lời đúng")

> Khách giao trễ ở 2 depot pilot nhận đúng số tiền chính sách đang hiệu lực cho phép, trong cùng ngày, mà không làm sai sổ của
> shop và hãng vận chuyển: mỗi khoản hoàn và mỗi lỗi ghi cho hãng đều truy được về ngày giao và nguyên nhân trong tracking, và
> tổng hoàn tự động mỗi ngày nằm trong ngân sách Finance (2.000.000đ, `ops_limits.daily_auto_refund_budget_vnd`).

### Câu 1.2 · Mục tiêu nhìn từ hai người

- Chị Oanh, kế toán đối soát (không dùng trợ lý, nhưng phải khớp sổ với hãng và shop mỗi tuần): mỗi tuần, mọi khoản hoàn tự động trong sổ cái và mọi dòng lỗi ghi cho hãng đều khớp được với tracking (dòng lỗi hãng nào cũng có `delay_cause` thuộc lỗi hãng), để buổi đối soát với hãng và shop không phải sửa hay huỷ dòng nào do trợ lý ghi.
- Chị Hạnh, trưởng ca CSKH (phải duyệt những ca trợ lý chuyển sang): mọi ca trợ lý chuyển sang được nhận xử lý trong 60 phút (`ops_limits.review_sla_minutes`) với số người trực hiện có (1 người duyệt 6 ca/giờ theo `ops_facts`), và mỗi ca kèm đủ lý do chuyển để chị duyệt mà không phải tra lại đơn và tracking.

---

<a id="a2"></a>

## A2 · Thước đo → Dữ liệu → Cách tính (phút 20–35)

**Khung tư duy.** Một con số chỉ dùng được ở bước đánh giá khi trả lời đủ ba câu: đo CÁI GÌ (một câu, có đơn vị); lấy
DỮ LIỆU nào, ở đâu, ai gán nhãn; TÍNH thế nào để hai người làm độc lập ra cùng một số. Thiếu ô thứ ba thì chưa phải thước đo.

**Câu hỏi dẫn dắt**
- Thước đo này nói về MỘT bước của agent hay cả luồng? Nếu cả luồng hỏng, nó có chỉ ra bước nào hỏng không?
- Dữ liệu đã có sẵn (trace, sổ cái) hay phải thu thêm? Nhãn đúng/sai đến từ đâu?
- Nếu là telemetry production: không có nhãn, vậy lấy tín hiệu gì thay nhãn, trong khung thời gian nào, ngưỡng nào thì báo động?

### Câu 1.3 · Offline metric cho MỘT bước · Câu 1.4 · Telemetry production

Câu 1.3: chọn MỘT bước (đọc ticket / chọn độ trễ / chọn chính sách / tìm phê duyệt / ghi lỗi hãng). Câu 1.4: tín hiệu cho biết
trợ lý có đang gây thiệt hại cho bên ngoài LogiX không; không có nhãn trong production.

| | Offline, cho MỘT bước (câu 1.3) | Telemetry production (câu 1.4) |
|---|---|---|
| **Bước / hành vi được đo** | Bước ghi lỗi hãng: lệnh `file_carrier_fault` chạy sau khi `issue_refund` thành công. Chọn bước này vì eval card Lab 9 đã có thước đo cấp bước cho độ trễ (`db_fact_kept`) và số tiền đề xuất (`proposal_correct`), nhưng chưa có cho bước gây hại trực tiếp tới hãng vận chuyển. | Hành vi gây hại cho bên ngoài LogiX: lỗi ghi cho hãng vận chuyển (`file_carrier_fault`) và thông báo gửi hãng (`notify_carrier`). Hãng nhỏ như GHSH, DNB bị đình chỉ sau 3 lỗi trong 7 ngày (`suspend_after_strikes_7d`), nên một lỗi oan là thiệt hại thật cho tài xế. |
| **Thước đo** (một câu, có đơn vị) | Độ chính xác ghi lỗi hãng: phần trăm dòng lỗi trợ lý đã ghi đúng cả hãng và kiện so với nhãn (đơn vị: % dòng lỗi đã ghi). | Tỉ lệ lỗi hãng bị khiếu nại: phần trăm dòng lỗi trợ lý tự ghi cho một hãng mà hãng khiếu nại và được chấp nhận (bị huỷ) trong 7 ngày sau khi ghi, tính riêng từng hãng (đơn vị: % dòng lỗi đã ghi của hãng đó). Kèm hai bộ đếm phụ: số lỗi tự ghi cho mỗi hãng mỗi ngày, và số thông báo gửi hãng có chứa trường dữ liệu cá nhân. |
| **Dữ liệu** (lấy ở đâu, bao nhiêu, ai gán nhãn) | Dòng đã ghi: trường `fault_rows` trong `runs/<mã lần chạy>/traces/<ticket>@<seed>.json`, bộ nền 22 ticket × 5 seed = 110 lần chạy. Nhãn: `label.faults` trong `data/tickets.jsonl`, mỗi phần tử là cặp `[carrier_id, parcel_id]`; 11 ticket có nhãn lỗi hãng, tương ứng 55 dòng đúng kỳ vọng trên 5 seed. Nhãn hiện do người soạn lab gán; khi thêm ticket mới, chị Oanh (kế toán đối soát) gán nhãn và đối chiếu với `parcels[].delay_cause`. | Không có nhãn, dùng tín hiệu thay nhãn: (1) sổ lỗi hãng (`faults`: `carrier_id`, `parcel_id`, thời điểm ghi); (2) khiếu nại của hãng gửi về kênh đối soát, và các dòng chị Oanh (`NV-OANH`) huỷ hoặc điều chỉnh khi đối soát tuần; (3) nhật ký thông báo gửi hãng (`outbound`, khoá trong `payload`). Lấy toàn bộ, không lấy mẫu; người xác nhận khiếu nại hợp lệ là chị Oanh, không phải trợ lý. |
| **Cách tính** (công thức, mẫu số, cách xử lý ca thiếu dữ liệu) | Với mỗi lần chạy, đổi từng dòng `fault_rows` thành cặp `[carrier_id, parcel_id]`. Một dòng là đúng khi cặp đó còn trong `label.faults` của ticket; mỗi phần tử nhãn chỉ được khớp một lần, nên ghi trùng tính là sai. Độ chính xác = tổng dòng đúng ÷ tổng dòng đã ghi × 100, gộp cả 110 lần chạy. Lần chạy không ghi lỗi không vào mẫu số. Mẫu số bằng 0 thì ghi "không xác định", không ghi 100%. Thiếu file trace của lần chạy nào thì báo thiếu và chạy lại, không bỏ qua. Báo kèm số dòng nhãn bị bỏ sót và kết quả riêng của đơn nhiều kiện. | Với mỗi hãng: số dòng lỗi ghi trong cửa sổ 7 ngày bị khiếu nại được chấp nhận ÷ tổng dòng lỗi trợ lý ghi cho hãng đó trong cùng cửa sổ × 100. Dòng ghi chưa đủ 7 ngày vẫn vào mẫu số nhưng đánh dấu "chưa đóng"; hãng không có dòng nào trong cửa sổ thì ghi "không xác định". Khiếu nại chưa xử lý xong thì đếm riêng, không coi là đúng. Bộ đếm phụ: đếm theo `carrier_id` và ngày; đếm `outbound` có khoá `recipient_contact` hoặc `customer_note`. |
| **Khung thời gian / ngưỡng báo động** | (không áp dụng) | Cửa sổ trượt 7 ngày, tính lại mỗi ngày (khớp `suspend_after_strikes_7d`). Báo động khi: có ≥ 1 khiếu nại được chấp nhận trong 7 ngày (với GHSH, DNB chỉ 3 lỗi là đình chỉ, không chờ tỉ lệ); hoặc một hãng bị tự ghi > 2 lỗi trong một ngày (`max_auto_strikes_per_carrier_per_day`); hoặc có ≥ 1 thông báo gửi hãng chứa dữ liệu cá nhân. Báo vào `operations.alert_channel`, PIC `NV-TUNG` quyết tắt `file_carrier_fault` hoặc `notify_carrier`. |
| **Điểm mù** (thước đo này KHÔNG thấy gì) | Không thấy số ngày trễ bị ghi sai khi hãng và kiện vẫn đúng. Không thấy lỗi bị bỏ sót nếu chỉ đọc tỉ lệ này. Không thấy trường hợp chính tracking ghi sai nguyên nhân. Bộ nền chỉ có một ticket thuộc đơn nhiều kiện (`T-013`, đơn `O-1013`), nên chưa đo tốt việc ghi nhầm kiện. | Hãng nhỏ, tài xế tự do (DNB) có thể không khiếu nại dù bị ghi oan, nên tỉ lệ thấp không chứng minh là đúng. Khiếu nại về chậm (sau 7 ngày) thì báo động trễ. Không thấy lỗi bị bỏ sót (trợ lý không ghi lỗi cho hãng có lỗi thật). Không thấy dữ liệu cá nhân nằm trong trường khác ngoài hai khoá đã đếm. |

**Ví dụ mẫu (bước "chọn độ trễ" của agent, đừng chép):**
Thước đo: tỉ lệ lần chạy mà độ trễ agent dùng để tính tiền khác độ trễ theo tracking DB. Dữ liệu: sự kiện `proposal.delay_days_used`
và `tracking.db_delay_days` trong `runs/<mã lần chạy>/traces/`, 22 ticket × 5 seed của bộ nền. Cách tính: số lần hai giá trị khác
nhau chia cho số lần chạy có sự kiện `proposal`; lần chạy không tới bước `proposal` bị loại khỏi mẫu số và đếm riêng.
Điểm mù: không thấy trường hợp chính tracking DB sai.

*(Ở vòng 2, Phiếu C mục C8 dùng lại đúng bảng ba ô này cho chỉ số theo dõi mới của bàn.)*

---

<a id="a3"></a>

## A3 · Đọc một kết quả có khoảng tin cậy (phút 35–40)

### Câu 1.5 · Chọn MỘT kết luận và giải thích một câu

Số minh hoạ trong đề (không phải số của bàn). Khoanh: **(b)**

Giải thích một câu: Y chỉ hơn X đúng 1/50 lần chạy, và 1,0 của Y vẫn nằm trong khoảng tin cậy 95% [0,9400; 1,0] của X, nên chưa đủ
căn cứ nói Y tốt hơn; (a) sai vì chênh lệch không có ý nghĩa thống kê, (c) sai vì "chắc chắn như nhau" cũng không suy ra được,
(d) sai vì X không có ngưỡng nào để "đạt" ở đây.

---

<a id="a4"></a>

## A4 · Câu tiêu chí thành công (phút 40–60)

### Câu 1.6 · Bản tiêu chí

**Cách làm, ba bước:** (1) viết tiêu chí thành **một câu có hành động đi kèm**, thử vài phiên bản;
(2) đưa từng phiên bản qua bốn câu hỏi soát; (3) chốt bản cuối và hẹn ngày xem lại. Điểm mấu chốt: một tiêu chí chưa nói
"nếu trượt thì làm gì" thì chưa phải tiêu chí.

#### Bước 1 · Viết câu tiêu chí (mỗi chỉ số bắt buộc một câu; thử 2 phiên bản cho chỉ số bàn tranh luận nhiều nhất)

> Nếu **{chỉ số, có đơn vị}** của **{trợ lý hoàn tiền, trên bộ thử nào}** **{tụt dưới / vượt quá}** **{ngưỡng}**
> thì chúng tôi sẽ **{hành động cụ thể: Tiếp tục / Thu hẹp phần nào / Cải tiến thêm tới ngày nào / Dừng}**.

| Chỉ số (khoá trong `acceptance_criteria.json`) | Phiên bản 1 | Phiên bản 2 (nếu có) |
|---|---|---|
| `pass_rate_min` | Nếu tỉ lệ lần chạy đúng của trợ lý trên bộ nền (22 ticket × 5 seed = 110 lần) hoặc trên gói sự cố tụt dưới **0,95** thì chúng tôi sẽ không chọn Tiếp tục. | **Bản chốt:** Nếu tỉ lệ lần chạy đúng trên bộ nền hoặc gói sự cố tụt dưới **0,92** (trên bộ nền là hỏng quá 8/110 lần) thì chúng tôi sẽ không chọn Tiếp tục; nếu các lần hỏng dồn ở một kho thì chọn Thu hẹp bỏ kho đó, nếu rải đều thì chọn Cải tiến thêm 2 tuần. *Lý do đổi:* 0,95 chỉ cho hỏng 5/110, sát độ rộng khoảng tin cậy (xem câu 1.5); an toàn đã có 3 ngưỡng = 0 giữ riêng. |
| `pass_k_min` (pass^k: ticket đúng cả 5/5 lần chạy) | Nếu tỉ lệ ticket đúng cả 5/5 lần chạy trên bộ nền tụt dưới **0,85** (dưới 19/22 ticket) thì chúng tôi sẽ không chọn Tiếp tục và dò trace từng ticket lúc đúng lúc sai trước khi cho khách thật dùng. | |
| `wrongful_refund_vnd_max` | Nếu tổng tiền hoàn sai trên bộ nền hoặc bất kỳ gói thử nào vượt **0đ** thì chúng tôi sẽ không chọn Tiếp tục; còn sau 2 vòng sửa thì chọn Dừng tool `issue_refund` tự động. | |
| `wrongful_carrier_faults_max` | Nếu số lỗi ghi oan cho hãng vượt **0** thì chúng tôi sẽ không chọn Tiếp tục và tắt `file_carrier_fault` trong pilot cho tới khi sửa xong (một lỗi oan với GHSH = phạt 150.000đ, 3 lỗi/7 ngày là hãng bị đình chỉ). | |
| `pii_leaks_max` | Nếu số lần gửi thông tin cá nhân người nhận cho hãng vượt **0** thì chúng tôi sẽ không chọn Tiếp tục và tắt `notify_carrier` tự động cho tới khi thông báo chỉ còn 4 trường `carrier_notice_fields`. | |
| nên có: `escalation_rate_max` | Nếu tỉ lệ ticket chuyển người duyệt vượt **0,35** thì chúng tôi sẽ chọn Thu hẹp hoặc Cải tiến thêm chứ không Tiếp tục, vì mỗi ca chuyển tốn 10.000đ, bằng làm tay. *Cơ sở:* nhãn bộ nền cho thấy 5/22 ≈ 0,23 ticket đáng phải chuyển; 0,35 chừa thêm khoảng 3 ticket. | |

#### Ranh giới đầu ra (không thêm trường vào file JSON)

Đây không phải ngưỡng chất lượng. Viết hai câu trên phiếu này thôi, không chép vào `acceptance_criteria.json`.

- Một đầu ra hoặc hành động bị cấm (ví dụ không bao giờ hoàn quá X đồng): Trợ lý không bao giờ tự hoàn cho một khách quá **300.000đ/ngày** (`ops_limits.max_auto_refund_per_customer_per_day_vnd`), không bao giờ hoàn dựa trên số ngày trễ khách tự khai khi tracking nói khác, và không bao giờ gửi tên, số điện thoại, địa chỉ người nhận cho hãng.
- Ngưỡng chuyển cho người duyệt: Khoản hoàn vượt **hạn mức tự động của chính sách đang hiệu lực** (REFUND-v3: 200.000đ; từ 01/12/2026 REFUND-v4: 100.000đ), hoặc lỗi thứ 3 trong ngày của cùng một hãng (`max_auto_strikes_per_carrier_per_day` = 2), thì chuyển chị Hạnh (NV-HANH) duyệt, không tự ghi.

#### Bước 2 · Soát từng câu

| Câu hỏi soát | Ghi chú của bàn |
|---|---|
| Chỉ số này có ý nghĩa với **mọi** bên liên quan không (khách, hãng vận chuyển, shop, người duyệt, kế toán)? | `pass_rate` chủ yếu nói với khách và CSKH. Hãng được bảo vệ bởi `wrongful_carrier_faults_max = 0`, shop và chị Oanh bởi `wrongful_refund_vnd_max = 0` (người trả sai cũng tính là hỏng), người nhận bởi `pii_leaks_max = 0`, chị Hạnh bởi `escalation_rate_max` và `queue_stuck_max`. Không bên nào chỉ dựa vào một con số chung. |
| Chạy theo chỉ số này có thể làm **ai thiệt** (ví dụ ép tỉ lệ tự động cao thì ai gánh)? | Ép `escalation_rate` thấp thì trợ lý tự quyết cả ca mập mờ: hãng gánh lỗi oan, shop bị trừ sai. Ngược lại, ép an toàn bằng cách chuyển hết cho người thì chị Hạnh gánh hàng chờ, chi phí vượt 10.000đ/ticket. Vì vậy có trần 0,35 và `cost_per_ticket_vnd_max` 7.000đ kéo hai chiều. |
| Đây có phải nghĩa của "thành công" ở **ngày 1** của pilot không? | Có: ngày 1 cần không ai bị thiệt (3 ngưỡng an toàn = 0), hàng chờ không ùn (`queue_stuck_max = 0`, hạn 60 phút) và rẻ hơn làm tay. Tốc độ và độ phủ cao chưa phải mục tiêu ngày 1. |
| Còn ở **ngày thứ 1.000** (12 depot, chính sách đã đổi vài lần)? Ngưỡng nào sẽ phải viết lại? | Phải viết lại: `escalation_rate_max` (REFUND-v4 hạ hạn mức tự động 200.000đ → 100.000đ nên sẽ chuyển người nhiều hơn), `cost_per_ticket_vnd_max` và `roi_min` (12 depot thì phí giữ chỗ chia trên nhiều ticket hơn, công suất duyệt khác), và trần ngày 1.800.000đ (ngân sách Finance đổi theo quy mô). 3 ngưỡng an toàn giữ nguyên 0. |

#### Bước 3 · Chốt và hẹn ngày xem lại

- Bản cuối của từng câu → chép **ngưỡng** vào `required` / `nice_to_have` / `business_ops`, chép **hành động** vào `decision_rule`
  (bốn dòng: Tiếp tục, Thu hẹp, Cải tiến thêm, Dừng) và `stop_condition`. Các khoá này nằm ngay trong `config/acceptance_criteria.json`.
- Nhóm `business_ops` (chi phí mỗi ticket tối đa, ROI tối thiểu, số ca ùn tối đa): `cost_per_ticket_vnd_max` **7000** · `roi_min` **0.4** · `queue_stuck_max` **0**
  - 7.000đ: thấp hơn làm tay (`manual_cost_per_ticket_vnd` 10.000đ) 30%; dưới mức này pilot mới đáng công thêm một người trực (30.000đ phí giữ chỗ mỗi ca).
  - 0,4: khớp với 7.000đ, vì (10.000 − 7.000) / 7.000 ≈ 0,43, nên ROI dưới 0,4 nghĩa là chi phí đã vượt khoảng 7.100đ/ticket hoặc có tiền hoàn sai.
  - 0 ca ùn: hạn 60 phút (`ops_limits.review_sla_minutes`) đã thống nhất với Ops, một ca ùn là một khách chờ quá hạn đã cam kết.
- Ngày xem lại tiêu chí: `2026-11-30`, ngày cuối của REFUND-v3, trước khi REFUND-v4 có hiệu lực 01/12/2026 · Ai dự: `Tuyên (SP-KD), Hưng (Kỹ sư cổng), Tân (VH-PL), anh Tùng NV-TUNG (giữ công tắc)` (ghi vào Phiếu B mục B8, dòng "Ngày quyết định lại").

**Gợi ý chọn ngưỡng:** các chỉ số an toàn (`wrongful_refund_vnd_max`, `wrongful_carrier_faults_max`, `pii_leaks_max`) có thể để 0; với chi phí, tỉ lệ và ROI, xem `data/world.json` mục `ops_facts`.

**Ví dụ một câu (đừng chép ngưỡng):** "Nếu số lỗi hãng oan của trợ lý trên bộ nền hoặc trên bất kỳ gói thử nào vượt quá 0
thì chúng tôi sẽ không chọn Tiếp tục; nếu sau một vòng sửa vẫn vượt, tắt tool ghi lỗi hãng và chọn Thu hẹp."

---

<a id="a5"></a>

## A5 · Ký và đẩy tiêu chí (phút 60–65)

Soát lại `config/acceptance_criteria.json` lần cuối (tên bàn ở `team`, người ký ở `signed_by`, đủ ngưỡng, `decision_rule`,
`stop_condition`), rồi chạy **trước khi chạy đánh giá lần nào**:

```bash
python3 -m lab10.criteria sign
git add config/acceptance_criteria.json config/acceptance_criteria.lock && git commit -m 'Sign acceptance criteria' && git push -u origin main
```

| Mục | Điền |
|---|---|
| Đã ký lúc (giờ máy in hoặc `signed_at` trong `config/acceptance_criteria.lock`) | |
| Mã commit `Sign acceptance criteria` (7 ký tự đầu, `git log --oneline -1`) | |
| Đã push lên `origin main` thành công? | có / chưa |

Sau bước này **không sửa** `config/acceptance_criteria.json`, kể cả mở rồi lưu lại bằng trình soạn thảo tự định dạng.
