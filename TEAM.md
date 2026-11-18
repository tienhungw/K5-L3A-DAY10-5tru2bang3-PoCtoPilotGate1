# Team

## Thông tin nhóm

- Tên nhóm (`TenNhom`, không dấu, không khoảng trắng): `5tru2bang3`
- Lớp: `L3A`
- Repo của bàn: `K5-L3A-DAY10-5tru2bang3-PoCtoPilotGate1`
- Thẻ sự cố đã bốc (S1–S8): `S8`

## Thành viên

Họ tên đầy đủ và MSSV của **mọi** thành viên; thêm dòng nếu cần. Vai: Kỹ sư cổng · Sản phẩm và kinh doanh · Vận hành và pháp lý (README mục 3, phút 0–15).

| STT | Họ và tên        | MSSV        | Vai                    | Trưởng nhóm |
| --: | ---------------- | ----------- | ---------------------- | :---------: |
|   1 | Nguyễn Tiến Hưng | 2A202603365 | Kỹ sư cổng             |      ✓      |
|   2 | Dương Ngọc Tuyên | 2A202603511 | Sản phẩm và kinh doanh |             |
|   3 | Dương Minh Tân   | 2A202603464 | Vận hành và pháp lý    |             |

Ghi `members` trong `submission/submission.json` theo dạng `"HoVaTen-MSSV"`, khớp bảng trên.

## Cá nhân

Mỗi thành viên tự viết phần còn trống trong mục của mình.

## NguyenTienHung-2A202603365

### Phần việc phụ trách

Kỹ sư cổng, trưởng nhóm. Câu 1.3, 2.1, 2.2, 2.6, 2.7, 2.8, 3.1 (trace), 3.5 (code), 3.6. Phiếu A mục A2 (cột Offline); Phiếu B mục B0, B1, B2, B7.1–B7.3; Phiếu C mục C0, C2, C7 (dòng code), C8. File `lab10/guards.py`, `lab10/monitors.py`.

### Đóng góp cụ thể

- Thiết lập repo của bàn: điền thông tin nhóm, thêm `.gitattributes` để giữ nguyên byte của file khoá, gắn `upstream`, đặt danh tính Git.
- Câu 1.3: thước đo độ chính xác ghi lỗi hãng (Phiếu A mục A2, cột Offline).
- Ký Bản tiêu chí theo bản cuối của Tuyên và điền Phiếu A mục A5.
- Câu 2.1 và 2.2: chạy mốc base, so với tiêu chí đã ký, dò và phân loại lỗi `T-002@55` (Phiếu B mục B0, B1, B2).
- Câu 2.6: ba cổng trong `lab10/guards.py` cho khoản hoàn, lỗi hãng và thông báo gửi hãng (Phiếu B mục B7.1).
- Câu 2.7: hai bước tránh rò rỉ dữ liệu (Phiếu B mục B7.2).
- Câu 2.8: một tính chất và hai ticket hiểm (Phiếu B mục B7.3).
- Chốt cổng vòng 1, đo mốc `prepared`, thêm `claim_override_rate` và `fault_tracking_mismatch_rate` trong `lab10/monitors.py`.
- Dùng AI: Claude Code hỗ trợ đọc code của lab, thiết lập repo, thao tác Git, chạy lệnh đo, viết và kiểm thử cổng, chỉ số theo dõi, soạn các câu 1.3, 2.1, 2.2, 2.6, 2.7, 2.8.

### Bằng chứng

- Commit `c4dd721`: thiết lập repo.
- Commit `bf25b51`: câu 1.3 và câu 2.7.
- Commit `0ae93d0`: ký tiêu chí.
- Commit `8431651`: chốt cổng vòng 1, hash `49938c75`.
- Commit `6f75de2`: Phiếu A mục A5, Phiếu B mục B0–B2, B7.1, B7.3, chỉ số theo dõi.
- Mã lần chạy: `R-base-before-20261118-153928-7ff038`, `R-base-after-20261118-154122-7ff038`, `R-base-after-20261118-154124-8f4f45`, `R-base-prepared-20261118-154340-8f4f45`.

### Exit ticket

Một điều học được, một điều còn chưa chắc.

## DuongNgocTuyen-2A202603511

### Phần việc phụ trách

Sản phẩm và kinh doanh, người ký Bản tiêu chí. Câu 1.1, 1.6, 2.3, 2.9, 3.2, 3.5 (`business`), quyết định v1 và v2. Phiếu A mục A1 (câu 1.1), A4, A5; Phiếu B mục B3, B7.4, B8; Phiếu C mục C5 (câu 3.2), C7 (dòng `business`), C12. File `config/acceptance_criteria.json`, `config/operating_gates.json` mục `business`.

### Đóng góp cụ thể

- Câu 1.6, Bản tiêu chí (`config/acceptance_criteria.json`): 5 ngưỡng bắt buộc (`pass_rate_min` 0,92 · `pass_k_min` 0,85 · ba chỉ số an toàn = 0), `escalation_rate_max` 0,35, `business_ops` (7.000đ/ticket · ROI 0,4 · 0 ca ùn), `stop_condition` và 4 dòng `decision_rule` không chồng nhau. Mỗi ngưỡng có lý do từ `data/world.json` và nhãn bộ nền (5/22 ticket vốn phải chuyển người; tổng hoàn đúng 683.000đ/ngày).
- Câu 1.6 trên Phiếu A mục A4: câu "Nếu … thì chúng tôi sẽ …" cho từng chỉ số (2 phiên bản cho `pass_rate_min`), hai câu ranh giới đầu ra, bốn câu soát, ngày xem lại 2026-11-30 (trước REFUND-v4).
- Câu 1.1 (Phiếu A mục A1) và ghi kết luận câu 1.5 của cả bàn: chọn (b) (Phiếu A mục A3).
- Câu 2.3 (Phiếu B mục B3): bản đồ dữ liệu và ví dụ drift REFUND-v3 → REFUND-v4 ngày 2026-12-01 (cờ `index_active` không tự đổi theo ngày hiệu lực).
- Câu 2.9 (Phiếu B mục B7.4): mục `business` của `config/operating_gates.json`: trần hoàn ngày 1.800.000đ, ngân sách 1.500đ/ticket, phạm vi `all`, ROI 0,4, mỗi số một câu lý do.
- Quyết định Gate 1 v1 (Phiếu B mục B8): **Tiếp tục**, khớp dòng "Tiếp tục" của `decision_rule` trên bộ nền (5/5 ngưỡng bắt buộc, `business_ops` đạt, không vượt trần); ghi rõ vế "gói sự cố" để v2 đo lại.
- Dùng AI: Claude Code hỗ trợ đọc đề và code của lab, tính tổng tiền hoàn từ nhãn bộ nền, soạn nháp các câu trên và cột v1 ở B8. Mọi ngưỡng và con số do tôi duyệt và chịu trách nhiệm giải thích.

### Bằng chứng

- Commit `cc8abc8` (nhánh `tuyen`): bản nháp tiêu chí, mục `business`, Phiếu A (câu 1.1, 1.5, A4), Phiếu B (B3, B7.4).
- Commit `16c66a5` (nhánh `tuyen`): bản cuối tiêu chí, sửa `decision_rule` (Thu hẹp thêm `escalation_rate` và "report còn dòng vượt trần"; Dừng: "cao hơn mức làm tay 10.000 đ").
- Commit `0ae93d0` `Sign acceptance criteria`: Bản tiêu chí của tôi được ký nguyên văn (Hưng chạy lệnh ký trên máy đo).
- Quyết định v1 (Phiếu B mục B8) dựa trên `R-base-before-20261118-153928-7ff038` (base) và `R-base-prepared-20261118-154340-8f4f45` (prepared, bản chốt `49938c75`).
- Quyết định v2 (Phiếu C mục C12) và câu 3.2: bổ sung sau khi nhận thẻ sự cố.

### Exit ticket

- Học được: ngưỡng phải viết và ký trước khi xem số, và mỗi ngưỡng cần một hành động "thì chúng tôi sẽ …"; `decision_rule` phải phủ hết mọi trường hợp report có thể ra, nếu không sẽ có kết quả không khớp dòng nào.
- Còn chưa chắc: ngưỡng chi phí 7.000đ/ticket và ROI 0,4 mới ước tính tay từ `ops_facts` (khoảng 4.700đ/ticket); chưa biết số base thật có sát không.

## DuongMinhTan-2A202603464

### Phần việc phụ trách

Vận hành và pháp lý. Câu 1.2, 1.4, 2.4, 2.10, 3.1 (phần riêng theo thẻ), 3.3, 3.5 (`operations`, `legal`), 3.7. Phiếu A mục A1 (câu 1.2), A2 (cột Telemetry production); Phiếu B mục B4, B5, B7.5, B7.6; Phiếu C mục C3, C4, C5 (câu 3.3), C7 (dòng `operations`, `legal`), C9, C10, C11. File `config/operating_gates.json` mục `operations` và `legal`, `submission/submission.json`.

### Đóng góp cụ thể

- Câu 1.2: mục tiêu nhìn từ chị Oanh (kế toán đối soát) và chị Hạnh (trưởng ca CSKH) (Phiếu A mục A1).
- Câu 1.4: telemetry production "tỉ lệ lỗi hãng bị khiếu nại" theo từng hãng, cửa sổ 7 ngày, ngưỡng báo động và điểm mù (Phiếu A mục A2, cột Telemetry production).
- Câu 2.4: HAZOP vòng 1 trên `notify_carrier` (5 dòng kỹ thuật, trong đó nhánh chưa thấy trên trace là đơn nhiều kiện lấy hãng của `parcels[0]`; 4 dòng ngoài kỹ thuật) (Phiếu B mục B4); checklist 9 nhóm việc lần 1, mỗi dòng một PIC (B5).
- Câu 2.10: điền `config/operating_gates.json` mục `operations` (PIC `NV-TUNG`, người duyệt `NV-HANH`, chờ tối đa 60 phút, 4 điều kiện dừng, kênh báo tin) và `legal` (chặn `recipient_contact`, `customer_note` khi gửi hãng; ghi lỗi hãng phải có nguyên nhân trong tracking); runbook phần 1–3 (B7.5) và Giờ cao điểm (B7.6).
- Đối chiếu runbook và điều kiện dừng với số của Bản tiêu chí (trần 1.800.000đ/ngày, `queue_stuck_max` = 0, chi phí 7.000đ/ticket) để các con số khớp nhau.
- Dùng AI: Claude Code hỗ trợ đọc đề, phiếu và code của lab, soạn nháp câu 1.2, 1.4, 2.4, 2.10, đối chiếu số với nhánh của Tuyên và thao tác Git.

### Bằng chứng

- Commit `372b3f7`: câu 1.2, 1.4, 2.4, 2.10 và mục `operations`, `legal`.
- Commit `0bc8b2e`: runbook và điều kiện dừng khớp số của Bản tiêu chí.
- Mã lần chạy (`runs/<mã>`): bổ sung sau khi ký tiêu chí và chạy đánh giá.

### Exit ticket

Một điều học được, một điều còn chưa chắc.
