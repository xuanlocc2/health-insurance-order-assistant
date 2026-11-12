# Vì sao các ông lớn chưa làm, và vì sao mình làm được

> Giải thích bằng lời thường, cho người không chuyên business. Dựa trên [diem-nghen-his.md](diem-nghen-his.md), [doi-thu.md](doi-thu.md) và ghi chú trong `research_notes/`. Chỗ ghi *(suy luận)* là nhận định của nhóm, chưa có nguồn xác nhận. **Mọi ví dụ về bệnh nhân đều là ca giả để minh họa.**

## Trước hết: có 3 vai

| Vai | Làm gì | Hình dung như |
|---|---|---|
| **Bác sĩ** | Ra chỉ định, tích dòng nào BHYT trả | Cầu thủ |
| **BHXH** | Trả tiền, và chấm xem chỉ định có đúng không | Trọng tài |
| **Hãng phần mềm** (VNPT, Viettel, FPT) | Làm phần mềm cho bệnh viện | Người bán thiết bị cho đội bóng |

Câu hỏi: vì sao người bán thiết bị không làm một cái **"máy nhắc"** để cầu thủ biết trước trọng tài có thổi phạt không?

**Trả lời ngắn:** họ không thiếu tiền hay kỹ sư. Viettel còn từng làm hệ thống chấm cho chính BHXH. Cái khó không nằm ở công nghệ. Nó nằm ở **luật**, **trách nhiệm** và **quyền diễn giải luật**, và hãng phần mềm không nắm thứ nào trong ba thứ đó.

---

## Điểm nghẽn 1: Luật viết bằng lời, máy không tự kiểm được

**Hình dung.** Một quán bar có quy định: *"Được vào khu VIP nếu đáp ứng 2 trong 4 điều: mặc vest, đi cùng hội viên, đặt bàn trước, trên 25 tuổi."* Camera ở cửa không kiểm được luật này. Nó không biết anh này có đặt bàn không, có đi cùng hội viên không. Thông tin đó nằm trong đầu người khác, chưa ai nhập vào máy.

**BHYT y như vậy.**

> **Ví dụ.** Bé B, 3 tuổi, khám vì sốt 2 ngày. Bác sĩ chỉ định Công thức máu và CRP.
> - Luật (TT 39/2024, nhánh trẻ em): CRP chỉ được trả khi bé **nghi ngờ có ổ nhiễm trùng**, **và** nhiệt độ ≤ 36°C hoặc ≥ 38,3°C, **và** nhịp tim hoặc nhịp thở vượt giới hạn sinh lý theo tuổi. (Điều kiện "2 trong 4 tiêu chuẩn", có bạch cầu, là của người lớn.)
> - Lúc chỉ định, phần mềm chỉ thấy mã bệnh "sốt" và danh sách dịch vụ. Nhịp tim, nhịp thở ghi bằng chữ trong phiếu khám, nếu có ghi. "Nghi ngờ có ổ nhiễm trùng" là nhận định của bác sĩ, chỉ nằm trong câu chữ. Văn bản cũng không nói "giới hạn sinh lý theo tuổi" theo bảng nào.
> - Phần mềm không thể kết luận.

**Cái khó không phải là viết luật vào máy.** Chỉ có khoảng 56 dịch vụ kèm điều kiện kiểu này, ngồi vài ngày là viết xong. **Cái khó là máy thiếu thông tin để áp luật.** Chỉ có hai cách lấy thông tin, và cách nào cũng có giá:
1. Bắt bác sĩ tích thêm ô "Bé đủ điều kiện CRP". Bác sĩ chậm hơn, và dễ bấm cho xong.
2. Cho AI đọc phiếu khám. Kết quả chỉ là "có lẽ", không phải kết luận.

**Ở Mỹ thì sao?** Mỹ làm được vì cơ quan bảo hiểm (CMS) công bố sẵn luật *kèm danh sách mã bệnh hợp lệ*. Bác sĩ chỉ cần chọn đúng mã. Việt Nam thiếu đúng lớp dữ liệu đó.

---

## Điểm nghẽn 2: Không có đáp án, và barem chấm bị giữ kín

**Hình dung.** Một kỳ thi tự luận mà Bộ không công bố đáp án, còn giám khảo chấm theo barem riêng và không cho thí sinh xem.

### "Không có đáp án": không có bảng "mã bệnh này thì được làm xét nghiệm nào"

Lý do là y khoa không ghép một-một được.

> **Ví dụ.** Hai bé cùng mã bệnh R10.4 "đau bụng":
> - Bé C: đau quanh rốn, bụng mềm, không sốt → bác sĩ không cho siêu âm.
> - Bé D: đau hố chậu phải, ấn đau, sốt nhẹ → siêu âm là hợp lý (nghi ruột thừa).
>
> Cùng một mã bệnh nhưng quyết định ngược nhau. Bảng "đau bụng → được siêu âm" sai với bé C. Bảng "đau bụng → không được siêu âm" sai với bé D.

Vì vậy Bộ Y tế không ra bảng cứng *(suy luận)*. Bảng cứng sẽ sai với nhiều ca, Bộ bị trách là can thiệp chuyên môn, và bệnh viện sẽ khiếu nại liên tục. Căn cứ thật mà giám định viên dùng là các hướng dẫn điều trị dài hàng nghìn trang, và không ai muốn gánh việc "dịch" chúng thành bảng.

### "Barem giữ kín": BHXH không công khai quy tắc chấm

Lý do là công khai thì bị "học tủ" *(suy luận)*.

> **Ví dụ.** Giả sử BHXH công bố: "Siêu âm lặp lại trong 7 ngày sẽ bị cắt". Bệnh viện có thể chỉ cần hẹn bệnh nhân quay lại vào ngày thứ 8, chứ không thật sự chỉ định đúng hơn.

Giữ kín cũng cho BHXH quyền linh hoạt khi cần siết chi. Một điểm đáng chú ý: Viettel làm hệ thống chấm cho BHXH nhưng không đưa logic đó vào phần mềm bệnh viện của mình. Nhiều khả năng là do hợp đồng và xung đột lợi ích, vì không thể vừa làm trọng tài vừa bán bí kíp cho cầu thủ *(suy luận)*.

→ Ai muốn làm "máy nhắc" thì phải **tự đoán barem**. Đoán sai thì bị trách.

---

## Điểm nghẽn 3: Phần lớn là chấm tay, mà chấm tay thì có lúc khác nhau

Khoảng **83% số tiền bị cắt** là do giám định viên đọc hồ sơ rồi tự đánh giá, không phải do máy tự bắt (số liệu 2018–2022).

**Hình dung.** Chấm bài văn. Cùng một bài, người này cho 7 điểm, người kia cho 6. Nhưng không phải lúc nào cũng ngẫu nhiên:

| Loại | Nghĩa là | Ví dụ | Làm gì được |
|---|---|---|---|
| **Có quy luật** | Cùng người chấm, cùng tỉnh thường cắt cùng kiểu | Giám định viên tỉnh X hay cắt CRP và PCT làm cùng ngày ở ca sốt nhẹ ngoại trú | **Học được** từ lịch sử xuất toán của chính viện |
| **Thật sự chủ quan** | Khác người, khác đợt | Cùng kiểu ca siêu âm "đau bụng", quý này được trả, quý sau bị cắt vì đổi người chấm | **Không đoán trước được**, chỉ chống đỡ bằng hồ sơ giải trình |

→ **Không ai có thể biết trước chắc chắn một chỉ định có bị cắt không**, kể cả công ty lớn. Đây không phải chuyện thiếu tiền hay thiếu công nghệ.

---

## Vậy vì sao các ông lớn không làm?

Ba lý do rất đời thường:

1. **Không ai đặt hàng.** Bệnh viện mua phần mềm qua đấu thầu, và hồ sơ thầu chỉ đòi phần thu viện phí và gửi dữ liệu cho BHXH. Bác sĩ là người khổ nhưng không phải người cầm tiền mua phần mềm. Hãng làm theo những gì người mua yêu cầu.
2. **Làm thì bị trách cả hai chiều.**

   | Phần mềm báo | Chuyện xảy ra | Ai bị trách |
   |---|---|---|
   | "Được trả" nhưng vẫn bị cắt | Bác sĩ, viện vẫn mất tiền | Hãng: "phần mềm báo sai" |
   | "Không được trả" | Bác sĩ ngại chỉ định, bệnh nhân thiệt | Hãng: "phần mềm cản trở khám chữa bệnh". Với doanh nghiệp nhà nước, đây là rủi ro chính trị |

3. **Mỗi viện một kiểu, phải làm tay từng nơi.** Tên dịch vụ, danh mục và cách hiểu luật ở mỗi viện mỗi khác. Phần mềm thì cho thuê giá rẻ, không bù nổi chi phí ngồi làm tay cho hàng nghìn cơ sở.

---

## Vì sao mình làm được: các lợi thế thật, ở cấp viện

Mục tiêu của project là **cấp viện**, tức toàn bộ Vinmec Times City, không chỉ một khoa. Những lợi thế dưới đây vẫn đúng ở cấp đó:

| Ông lớn vướng | Mình né được vì |
|---|---|
| **Không ai đặt hàng** (người khổ ≠ người mua) | Đây là dự án **nội bộ của viện**. Người được lợi (bác sĩ phải bù tiền, viện bị xuất toán) cũng chính là người đặt ra yêu cầu |
| **Phải tự đoán barem, đoán sai bị trách** | Dùng **luật của chính viện**: viện đã có sẵn file Excel điều kiện BHYT, tức cách viện tự hiểu luật. Trách nhiệm nội dung thuộc về viện, có bác sĩ và lãnh đạo khoa duyệt |
| **Phải làm cho hàng nghìn cơ sở** | Chỉ cần **một bộ quy tắc cho một viện**. Vẫn là việc tay, nhưng là việc làm một lần và cập nhật định kỳ, không phải nhân lên hàng nghìn lần |
| **Không đoán được người chấm** | **Đổi mục tiêu:** không đoán trọng tài, mà (1) bắt các lỗi rõ ràng như sai danh mục, thẻ hết hạn, làm trùng, và (2) **lưu căn cứ để giải trình** khi bị cắt |
| **Lỗi chủ quan nhưng có quy luật** | Lịch sử xuất toán cũ của viện, kể cả qua lời kể, chính là **"barem ngầm" của người chấm địa phương**. Đây là dữ liệu hãng phần mềm không bao giờ có |

**Riêng cho MVP**, mình có thêm một lợi thế tạm thời: phạm vi hẹp (Nhi ngoại trú, 30–50 dịch vụ) nên làm tay nhanh để chứng minh tính khả thi. Đây **không phải** lý do chính để trả lời câu "sao ông lớn không làm mà mình làm được". Khi mở rộng ra toàn viện, khối lượng việc tay sẽ tăng, nhưng vẫn là một bộ quy tắc của một viện.

### Thông điệp nên dùng

- ✅ "Giúp bác sĩ **tránh lỗi rõ ràng** và **có hồ sơ để giải trình** khi bị xuất toán."
- ❌ Tránh nói "biết trước BHXH có trả hay không", vì không ai làm được điều đó.
- Vì vậy nhãn trạng thái tốt nhất là **"Phù hợp quy tắc BHYT"**, không phải "Được chi trả".

> **Ví dụ: vì sao lịch sử là giá trị cốt lõi.** Ba tháng sau, khoa nhận thông báo xuất toán ca siêu âm ổ bụng của bé D. Tra lịch sử thấy: lúc tích, trợ lý báo "Cần xem lại", trích phiếu khám "đau hố chậu phải, ấn đau, sốt nhẹ", bác sĩ xác nhận lúc 09:42. Bác sĩ dùng đúng đoạn trích này để làm hồ sơ giải trình, không phải lục lại bệnh án sau 3–6 tháng khi đã quên ca bệnh.

---

## Hướng phát triển: có mở rộng ra nhiều viện được không? *(không thuộc thiết kế hiện tại)*

**Câu hỏi:** mỗi viện có bảng tra BHYT riêng, vậy hệ thống chỉ dùng được trong một viện, hay có cách tự thích ứng theo từng viện?

**Trả lời: mở rộng được, nếu tách đúng phần chung và phần riêng.** "Mỗi viện một bảng" thật ra gồm 4 loại khác biệt, và chỉ một loại là riêng thật sự:

| Khác biệt giữa các viện | Bản chất | Cách xử lý |
|---|---|---|
| (a) Tên, mã dịch vụ nội bộ | Chỉ khác tên gọi | Đổi về **mã kỹ thuật chuẩn quốc gia**. Từ 01/7/2026 (TT 23/2024) các viện đã buộc phải làm việc này. AI có thể gợi ý ghép mã để nhập nhanh |
| (b) Danh mục viện đã đăng ký | Chỉ là cấu hình | Khai báo theo hợp đồng BHYT của viện |
| (c) Giá, hạng, tuyến | Chỉ là cấu hình | Khai báo |
| (d) Cách viện hiểu luật, thói quen người chấm địa phương | **Riêng thật sự** | Lớp riêng của từng viện, lấy từ file Excel và lịch sử xuất toán, có người duyệt |

> **Ví dụ.** Viện A gọi "XN CTM 18 chỉ số", viện B gọi "Tổng phân tích máu laser". Cả hai đổi về cùng một mã chuẩn. Luật "không lặp trong N ngày" chỉ viết một lần theo mã chuẩn và dùng chung cho cả hai viện. Chỉ những điều như "người chấm ở tỉnh của viện B hay cắt CTM lặp sau 3 ngày" mới nằm trong lớp riêng của viện B.

**Hình dung như 3 tầng:**

```
Tầng 1. Luật chung toàn quốc (một đội trung tâm cập nhật khi quy định đổi)
        danh mục và điều kiện của Bộ, mã kỹ thuật chuẩn, luật thẻ và mức hưởng
           ▲ luật viết theo mã chuẩn
Tầng 2. Cấu hình từng viện (khai báo một lần khi thêm viện, gần như cơ học)
        ghép mã nội bộ → mã chuẩn, danh mục đã đăng ký, giá, hạng, tuyến
           ▲
Tầng 3. Ghi đè riêng từng viện (có người của viện duyệt)
        file Excel của viện, quy luật học từ xuất toán cũ, ngoại lệ chuyên khoa
```

**Để mở rộng được thì cần:**
- **Luật là dữ liệu, không phải code.** Mỗi luật là một dòng trong bảng (mã chuẩn, điều kiện, căn cứ, ngày hiệu lực). Thêm viện là thêm cấu hình, không phải viết lại phần mềm.
- **Một đội trung tâm cập nhật tầng 1** khi quy định đổi (khoảng 15 văn bản trong 3 năm). Optum và Experian ở Mỹ làm theo kiểu này: thư viện luật trung tâm, mỗi khách hàng có cấu hình riêng.
- **Về lâu dài:** gom lịch sử xuất toán (ẩn danh) của nhiều viện cùng tỉnh sẽ học được thói quen người chấm địa phương tốt hơn từng viện tự học. Đây là lợi thế khó sao chép nhất, nhưng cũng nhạy cảm nhất về dữ liệu.

**Điều không thay đổi khi mở rộng:** quyền diễn giải luật (điểm nghẽn 2) và tính chủ quan của người chấm (điểm nghẽn 3) vẫn còn nguyên. Mở rộng chỉ làm phần cơ học rẻ hơn, còn phần diễn giải vẫn cần người của từng viện duyệt.

**Cho MVP hiện tại:** chưa cần làm 3 tầng, chỉ cần **viết mỗi luật theo mã kỹ thuật chuẩn, kèm cột căn cứ và ngày hiệu lực** ngay từ đầu. Việc này gần như không tốn thêm công, mà giữ được đường mở rộng sau này.
