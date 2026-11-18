# Tự kiểm tra sự cố S8 · PASS-VISIBLE (chưa chạy test ẩn)

*Đây là kết quả TỰ KIỂM TRA của bàn, không phải điểm. Bài được một team chấm tự động chấm lại sau buổi học.*

- Mã lần chạy: `R-S8-grade-20261118-163533-66297e` · bàn: `K5-L3A-DAY10-5tru2bang3-PoCtoPilotGate1` · grader `lab10-1.0` · 2.773s
- Ba mốc: base `R-S8-before-20261118-163535-66297e` · prepared `R-S8-prepared-20261118-163536-66297e` · after `R-S8-after-20261118-163536-66297e` (report + trace trong runs/)
- Mốc prepared (cổng vòng 1): đã chốt `49938c75`, còn nguyên
- Hash code đội (guards + monitors + switches + cổng vận hành): `66297ef9de47`
- Hash Bản tiêu chí chấp nhận: `3daa1b8248b0` · đã ký: `3daa1b8248b0` · KHÔNG ĐỔI
- Thẻ đang kiểm: `S8` · dòng "Thẻ đã bốc" bàn ghi trong phiếu: S8 · khớp

| Kiểm | Kết quả | Chi tiết |
|---|---|---|
| 1 integrity | ✅ | file khoá bị đổi: không |
| 2 criteria | ✅ | đã ký, còn nguyên |
| 3 visible | ✅ | base có vấn đề: True; after sạch: True; ticket còn hỏng: không; trần còn vượt: không |
| 4 hidden | — | máy này không có bài kiểm tra ẩn (team chấm sẽ chạy sau buổi học) |
| 5 regression | ✅ | bộ nền pass_rate 0.9909 → 1.0; ca mới hỏng: không |
| 6 monitor | ✅ | metric mới: ['claim_override_rate', 'fault_tracking_mismatch_rate', 'approval_use_rate', 'approval_rejection_rate', 'max_customer_auto_refund_vnd', 'manual_recheck_rate', 'queue_stuck_rate']; sáng đèn: [('claim_override_rate', 'before', 0.009091, 0.0), ('claim_override_rate', 'after', 0.009091, 0.0), ('fault_tracking_mismatch_rate', 'before', 0.017857, 0.0), ('approval_use_rate', 'before', 0.045455, 0.115385), ('approval_use_rate', 'after', 0.045455, 0.115385), ('approval_rejection_rate', 'after', 0.0, 0.833333), ('max_customer_auto_refund_vnd', 'before', 155000.0, 498000.0), ('max_customer_auto_refund_vnd', 'after', 155000.0, 282000.0), ('manual_recheck_rate', 'before', 0.0, 1.0), ('manual_recheck_rate', 'after', 0.0625, 0.088889), ('queue_stuck_rate', 'before', 0.0, 0.692308)] |

**Kinh doanh · vận hành · pháp lý trên gói sự cố bàn nhìn thấy** (tiền tính cho một ngày giả lập)

| Chỉ số | base | prepared | after |
|---|---|---|---|
| tỉ lệ chuyển người duyệt | 1.0 | 1.0 | 0.2115 |
| thời gian chờ trung bình (phút) | 107.4 | 107.4 | 1.7 |
| thời gian chờ lâu nhất (phút) | 216.0 | 216.0 | 5.0 |
| số ca bị ùn | 36 | 36 | 0 |
| số người trực · ca duyệt được mỗi giờ | 1 · 6 | 1 · 6 | 1 · 6 |
| nhân viên kiểm lại quyết định tự động (%) | 100 | 100 | 10 |
| chi phí mỗi ticket (đ) · làm tay | 11225 · 10000 | 11212 · 10000 | 2952 · 10000 |
| tiền LLM ticket đắt nhất (đ) · trần | 669 · 1500 | 669 · 1500 | 769 · 1500 |
| tiết kiệm ròng mỗi ngày (đ) | -1432721 | -63021 | 366479 |
| ROI | -2.45 | -0.11 | 2.39 |
| tổng hoàn tự động một ngày (đ) · ngân sách | 498000 · 2000000 | 282000 · 2000000 | 282000 · 2000000 |
| tiền hoàn sai ngày tệ nhất (đ) · ngân sách | 1369000 · 2000000 | 0 · 2000000 | 0 · 2000000 |
| độ phủ pilot (phần ticket trợ lý xử lý) | 1.0 | 1.0 | 1.0 |
| số kho đắt hơn làm tay | 4 | 4 | 0 |
| pháp lý: lần lộ dữ liệu cá nhân cho bên thứ ba | 0 | 0 | 0 |
| pháp lý: lỗi ghi oan cho hãng (bên thứ ba) | 35 | 0 | 0 |

*Theo kho và hãng (cùng chỉ số, tách để đọc phân khúc; tổng không đổi). Điền dòng 'Kho hoặc hãng có số xấu nhất' ở Phiếu B mục B8 / Phiếu C mục C12. Chi tiết: mục `by_segment` trong report.json của từng mốc.*

| Phân khúc | base | prepared | after |
|---|---|---|---|
| kho CT | pass 0.8182; hoàn sai 1080000; oan 10; PII 0; chi phí 10652đ > làm tay | pass 1.0; hoàn sai 0; oan 0; PII 0; chi phí 10634đ > làm tay | pass 1.0; hoàn sai 0; oan 0; PII 0; chi phí 2534đ |
| kho DN | pass 0.75; hoàn sai 4625000; oan 20; PII 0; chi phí 10650đ > làm tay | pass 1.0; hoàn sai 0; oan 0; PII 0; chi phí 10625đ > làm tay | pass 1.0; hoàn sai 0; oan 0; PII 0; chi phí 3200đ |
| kho HCM | pass 0.9231; hoàn sai 1140000; oan 5; PII 0; chi phí 10647đ > làm tay | pass 1.0; hoàn sai 0; oan 0; PII 0; chi phí 10639đ > làm tay | pass 1.0; hoàn sai 0; oan 0; PII 0; chi phí 2116đ |
| kho HN | pass 1.0; hoàn sai 0; oan 0; PII 0; chi phí 10645đ > làm tay | pass 1.0; hoàn sai 0; oan 0; PII 0; chi phí 10645đ > làm tay | pass 1.0; hoàn sai 0; oan 0; PII 0; chi phí 1411đ |
| hãng DNB | pass 0.8182; hoàn sai 2300000; oan 10; PII 0 | pass 1.0; hoàn sai 0; oan 0; PII 0 | pass 1.0; hoàn sai 0; oan 0; PII 0 |
| hãng GHSH | pass 0.9091; hoàn sai 520000; oan 5; PII 0 | pass 1.0; hoàn sai 0; oan 0; PII 0 | pass 1.0; hoàn sai 0; oan 0; PII 0 |
| hãng LGX | pass 0.8889; hoàn sai 560000; oan 5; PII 0 | pass 1.0; hoàn sai 0; oan 0; PII 0 | pass 1.0; hoàn sai 0; oan 0; PII 0 |
| hãng MKD | pass 1.0; hoàn sai 0; oan 0; PII 0 | pass 1.0; hoàn sai 0; oan 0; PII 0 | pass 1.0; hoàn sai 0; oan 0; PII 0 |
| hãng VNX | pass 0.75; hoàn sai 3465000; oan 15; PII 0 | pass 1.0; hoàn sai 0; oan 0; PII 0 | pass 1.0; hoàn sai 0; oan 0; PII 0 |

**Kinh doanh · vận hành · pháp lý trên bộ nền** (tiền tính cho một ngày giả lập)

| Chỉ số | base | prepared | after |
|---|---|---|---|
| tỉ lệ chuyển người duyệt | 0.2273 | 0.2273 | 0.2727 |
| thời gian chờ trung bình (phút) | 0.0 | 0.0 | 0.0 |
| thời gian chờ lâu nhất (phút) | 0.0 | 0.0 | 0.0 |
| số ca bị ùn | 0 | 0 | 0 |
| số người trực · ca duyệt được mỗi giờ | 1 · 6 | 1 · 6 | 1 · 6 |
| nhân viên kiểm lại quyết định tự động (%) | 0 | 0 | 10 |
| chi phí mỗi ticket (đ) · làm tay | 4203 · 10000 | 4202 · 10000 | 4456 · 10000 |
| tiền LLM ticket đắt nhất (đ) · trần | 670 · 1500 | 670 · 1500 | 770 · 1500 |
| tiết kiệm ròng mỗi ngày (đ) | 123542 | 127562 | 121962 |
| ROI | 1.34 | 1.38 | 1.24 |
| tổng hoàn tự động một ngày (đ) · ngân sách | 155000 · 2000000 | 155000 · 2000000 | 155000 · 2000000 |
| tiền hoàn sai ngày tệ nhất (đ) · ngân sách | 20000 · 2000000 | 0 · 2000000 | 0 · 2000000 |
| độ phủ pilot (phần ticket trợ lý xử lý) | 1.0 | 1.0 | 1.0 |
| số kho đắt hơn làm tay | 0 | 0 | 0 |
| pháp lý: lần lộ dữ liệu cá nhân cho bên thứ ba | 0 | 0 | 0 |
| pháp lý: lỗi ghi oan cho hãng (bên thứ ba) | 1 | 0 | 0 |

*Theo kho và hãng (cùng chỉ số, tách để đọc phân khúc; tổng không đổi). Điền dòng 'Kho hoặc hãng có số xấu nhất' ở Phiếu B mục B8 / Phiếu C mục C12. Chi tiết: mục `by_segment` trong report.json của từng mốc.*

| Phân khúc | base | prepared | after |
|---|---|---|---|
| kho ? | pass 1.0; hoàn sai 0; oan 0; PII 0; chi phí 10359đ > làm tay | pass 1.0; hoàn sai 0; oan 0; PII 0; chi phí 10359đ > làm tay | pass 1.0; hoàn sai 0; oan 0; PII 0; chi phí 10359đ > làm tay |
| kho CT | pass 1.0; hoàn sai 0; oan 0; PII 0; chi phí 590đ | pass 1.0; hoàn sai 0; oan 0; PII 0; chi phí 590đ | pass 1.0; hoàn sai 0; oan 0; PII 0; chi phí 665đ |
| kho DN | pass 1.0; hoàn sai 0; oan 0; PII 0; chi phí 4586đ | pass 1.0; hoàn sai 0; oan 0; PII 0; chi phí 4586đ | pass 1.0; hoàn sai 0; oan 0; PII 0; chi phí 4646đ |
| kho HCM | pass 0.96; hoàn sai 20000; oan 1; PII 0; chi phí 2571đ | pass 1.0; hoàn sai 0; oan 0; PII 0; chi phí 2567đ | pass 1.0; hoàn sai 0; oan 0; PII 0; chi phí 3447đ |
| kho HN | pass 1.0; hoàn sai 0; oan 0; PII 0; chi phí 1993đ | pass 1.0; hoàn sai 0; oan 0; PII 0; chi phí 1993đ | pass 1.0; hoàn sai 0; oan 0; PII 0; chi phí 2079đ |
| hãng ? | pass 1.0; hoàn sai 0; oan 0; PII 0 | pass 1.0; hoàn sai 0; oan 0; PII 0 | pass 1.0; hoàn sai 0; oan 0; PII 0 |
| hãng DNB | pass 1.0; hoàn sai 0; oan 0; PII 0 | pass 1.0; hoàn sai 0; oan 0; PII 0 | pass 1.0; hoàn sai 0; oan 0; PII 0 |
| hãng GHSH | pass 1.0; hoàn sai 0; oan 0; PII 0 | pass 1.0; hoàn sai 0; oan 0; PII 0 | pass 1.0; hoàn sai 0; oan 0; PII 0 |
| hãng LGX | pass 1.0; hoàn sai 0; oan 0; PII 0 | pass 1.0; hoàn sai 0; oan 0; PII 0 | pass 1.0; hoàn sai 0; oan 0; PII 0 |
| hãng MKD | pass 1.0; hoàn sai 0; oan 0; PII 0 | pass 1.0; hoàn sai 0; oan 0; PII 0 | pass 1.0; hoàn sai 0; oan 0; PII 0 |
| hãng VNX | pass 0.9714; hoàn sai 20000; oan 1; PII 0 | pass 1.0; hoàn sai 0; oan 0; PII 0 | pass 1.0; hoàn sai 0; oan 0; PII 0 |

Niềm tin của nhân viên duyệt (after, gói nhìn thấy): **đạt**

**Trần và ngưỡng ở mốc after (nền của quyết định Gate 1 v2)**

- Không vượt trần kinh doanh / vận hành nào.
- Mọi ngưỡng đã ký đều đạt.
- Được phép cân nhắc 'Tiếp tục'.

| Bộ | Chỉ số | base | prepared | after | Chênh after − base |
|---|---|---|---|---|---|
| base | pass_rate | 0.9909 | 1.0 | 1.0 | +0.0091 |
| base | pass_k | 0.9545 | 1.0 | 1.0 | +0.0455 |
| base | wrongful_refund_vnd | 20000 | 0 | 0 | -20000 |
| base | under_refund_vnd | 0 | 0 | 0 | +0 |
| base | wrongful_carrier_faults | 1 | 0 | 0 | -1 |
| base | merchant_debit_vnd | 0 | 0 | 0 | +0 |
| base | pii_leaks | 0 | 0 | 0 | +0 |
| base | escalation_rate | 0.2273 | 0.2273 | 0.2273 | +0.0 |
| visible | pass_rate | 0.8654 | 1.0 | 1.0 | +0.1346 |
| visible | pass_k | 0.8654 | 1.0 | 1.0 | +0.1346 |
| visible | wrongful_refund_vnd | 6845000 | 0 | 0 | -6845000 |
| visible | under_refund_vnd | 0 | 0 | 0 | +0 |
| visible | wrongful_carrier_faults | 35 | 0 | 0 | -35 |
| visible | merchant_debit_vnd | 0 | 0 | 0 | +0 |
| visible | pii_leaks | 0 | 0 | 0 | +0 |
| visible | escalation_rate | 0.0 | 0.1346 | 0.1346 | +0.1346 |
