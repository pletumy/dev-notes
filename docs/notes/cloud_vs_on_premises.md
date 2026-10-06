---
title: "Cloud vs On-Premises"
date: 2026-10-04
---

![Dải lựa chọn tự làm vs thuê ngoài](./images/Screenshot%202026-10-04%20at%2023.52.16.png)

Đoạn này mở đầu một chủ đề mới: **tự làm hay thuê ngoài** (build or buy), áp dụng cho phần mềm và hạ tầng.

## Nguyên tắc chung: cái gì là lợi thế cốt lõi thì tự làm

Câu hỏi này thực chất là về ưu tiên kinh doanh. Quy tắc phổ biến: thứ gì là **năng lực cốt lõi** hoặc **lợi thế cạnh tranh** của công ty thì tự làm. Thứ gì là việc thông thường, ai cũng cần, không tạo khác biệt thì để nhà cung cấp lo.

Ví dụ cực đoan của tác giả: gần như không công ty phần mềm nào tự sản xuất chip CPU, vì mua của Intel hay AMD rẻ hơn nhiều. Chip quan trọng, nhưng không phải thứ giúp họ thắng đối thủ.

Ví dụ gần hơn: một công ty fintech nên tự viết logic chấm điểm tín dụng, vì đó là bí quyết kiếm tiền của họ. Nhưng hệ thống gửi email thì cứ dùng SendGrid hay Amazon SES, tự viết mail server chẳng giúp họ hơn ai.

## Hai câu hỏi: ai viết phần mềm, ai vận hành nó

Với phần mềm, có hai quyết định tách biệt: **ai viết code** và **ai chạy, bảo trì nó**. Hình 1-2 vẽ ba điểm trên một dải liên tục. Lấy Redis làm ví dụ cho dễ hình dung:

**Bên trái: tự viết, tự vận hành.** Ví dụ code ứng dụng FastAPI của bạn. Team bạn viết, team bạn deploy, sập thì team bạn sửa lúc 2 giờ sáng. Bạn có toàn quyền kiểm soát, nhưng tốn nhiều công sức nhất.

**Ở giữa: dùng phần mềm có sẵn, nhưng tự vận hành (self-host).** Ví dụ bạn lấy Redis (mã nguồn mở, không phải tự viết) rồi tự chạy trong Docker trên một máy EC2. Bạn không phải viết database, nhưng phải tự lo cài đặt, cấu hình, nâng cấp phiên bản, backup, theo dõi RAM đầy, và tự xử lý khi máy chết.

Máy đó có thể là server vật lý của công ty (gọi là *on-premises*, kể cả khi nó nằm trong datacenter thuê ngoài chứ không phải văn phòng công ty), hoặc một máy ảo trên cloud như EC2 (gọi là *IaaS*, hạ tầng như một dịch vụ). Dù là cái nào, việc vận hành phần mềm vẫn là của bạn.

**Bên phải: dùng phần mềm có sẵn, để nhà cung cấp vận hành (cloud service/SaaS).** Ví dụ dùng Amazon ElastiCache for Redis. Bạn chỉ nhận một địa chỉ để kết nối, còn AWS lo cài đặt, vá lỗi, backup, chuyển sang máy dự phòng khi máy chính hỏng. Ít việc nhất, nhưng cũng ít quyền kiểm soát nhất: bạn không chỉnh được mọi cấu hình, không chọn được thời điểm nâng cấp tùy ý, và phải chấp nhận giá của họ.

Mũi tên dưới hình tóm tắt sự đánh đổi: đi về bên trái thì **kiểm soát nhiều hơn nhưng tốn đầu tư hơn**, đi về bên phải thì **ít kiểm soát hơn nhưng đầu tư ít hơn**.

Ngoài ba điểm đó còn có nhiều điểm khác ở giữa, ví dụ lấy một phần mềm mã nguồn mở rồi sửa code cho hợp nhu cầu riêng và tự chạy bản đã sửa.

## Câu hỏi liên quan: deploy bằng cách nào

Đoạn cuối nhắc tới một câu hỏi khác: **triển khai ở đâu và bằng công cụ gì**, ví dụ chạy trên cloud hay server riêng, có dùng Kubernetes hay không. Bạn đang làm với ECS/EKS chính là đang ở trong câu hỏi này. Nhưng tác giả nói sách sẽ không đi sâu vào phần công cụ deploy, vì nó ít ảnh hưởng tới kiến trúc dữ liệu hơn những yếu tố khác.

## Tóm lại

Đoạn này đặt nền cho phần tiếp theo: mỗi lựa chọn trên dải từ "tự làm hết" tới "thuê hết" đều có đánh đổi giữa quyền kiểm soát và chi phí công sức, và nên chọn dựa trên việc thứ đó có phải là lợi thế cốt lõi của công ty hay không. Các trang sau trong sách sẽ phân tích kỹ ưu nhược điểm của cloud so với self-host.

## Downside của cloud services
Đoạn này là nửa còn lại của phần so sánh: sau khi nói về lợi ích, tác giả liệt kê **nhược điểm lớn nhất của cloud service: bạn không kiểm soát được nó**. Mình đi qua từng ý với ví dụ cụ thể.

## 1. Thiếu tính năng thì chỉ biết xin

Nếu dịch vụ thiếu một tính năng bạn cần, bạn chỉ có thể gửi yêu cầu lịch sự cho nhà cung cấp và chờ. Bạn không tự thêm vào được.

Ví dụ: bạn dùng ElastiCache và cần một module Redis đặc biệt (như RedisJSON phiên bản mới). Tự host thì cài vào là xong. Trên dịch vụ quản lý sẵn, nếu AWS chưa hỗ trợ module đó thì bạn đành chịu.

## 2. Dịch vụ sập thì chỉ biết chờ

Khi AWS gặp sự cố ở một region, hàng nghìn công ty cùng sập theo, và việc duy nhất họ làm được là ngồi xem trang trạng thái của AWS. Tự host thì ít nhất bạn còn có thể tự lao vào sửa, còn ở đây bạn hoàn toàn bất lực.

## 3. Khó chẩn đoán khi có lỗi hoặc chậm

Khi tự chạy phần mềm, bạn xem được mọi thứ: CPU, RAM, ổ đĩa, log của server, thậm chí debug sâu vào hệ điều hành để hiểu tại sao nó chậm. Với dịch vụ do nhà cung cấp vận hành, bạn thường không được nhìn vào bên trong.

Ví dụ: database cloud của bạn đột nhiên chậm vào 3 giờ chiều mỗi ngày. Có thể do bạn dùng sai cách, có thể do máy chủ bên dưới đang chia sẻ với khách hàng khác, có thể do họ đang chạy bảo trì. Bạn chỉ thấy vài chỉ số họ cho phép xem, nên đoán mò rất mệt.

## 4. Bị phụ thuộc vào nhà cung cấp (vendor lock-in)

Nếu nhà cung cấp đóng cửa dịch vụ, tăng giá quá cao, hoặc thay đổi sản phẩm theo hướng bạn không thích, bạn hoàn toàn phụ thuộc vào họ. Bạn không thể tiếp tục chạy phiên bản cũ, mà buộc phải chuyển sang dịch vụ khác.

Ví dụ thật: năm 2022 Heroku bỏ gói miễn phí, rất nhiều dự án phải chuyển đi trong vài tháng.

Rủi ro này nhẹ hơn nếu có dịch vụ thay thế dùng **API tương thích**. Ví dụ Amazon Aurora tương thích Postgres: nếu muốn rời AWS, code của bạn vẫn chạy được trên Postgres ở nơi khác mà gần như không phải sửa. Nhưng nếu bạn xây cả hệ thống trên DynamoDB, vốn có API riêng của AWS, thì muốn chuyển đi là phải viết lại toàn bộ tầng truy cập dữ liệu. Chi phí chuyển đổi cao như vậy chính là "lock-in", bị khóa chặt vào một nhà cung cấp.

## 5. Rủi ro chính trị

Nếu nhà cung cấp ở nước khác và hai nước xảy ra xung đột, bạn có thể bị cắt dịch vụ do lệnh trừng phạt. Ví dụ năm 2019, GitHub từng hạn chế tài khoản của người dùng ở một số khu vực bị Mỹ cấm vận, dù họ không làm gì sai. Với một doanh nghiệp, mất quyền truy cập vào hạ tầng chỉ sau một quyết định chính trị là rủi ro rất lớn.

## 6. Phải tin tưởng nhà cung cấp về bảo mật

Dữ liệu của bạn nằm trên máy của họ, nên bạn phải tin họ giữ an toàn. Việc này làm phức tạp chuyện tuân thủ luật. Ví dụ một ngân hàng ở một số nước bị yêu cầu dữ liệu khách hàng phải nằm trong lãnh thổ quốc gia, và phải chứng minh được ai có quyền truy cập. Khi dữ liệu nằm trên cloud, họ phải xác minh nhà cung cấp đáp ứng được các yêu cầu đó, chứ không tự kiểm soát hoàn toàn.

## Kết luận của tác giả

Dù có những rủi ro trên, ngày càng nhiều công ty vẫn xây ứng dụng mới trên cloud, hoặc dùng cách **lai (hybrid)**: một phần chạy cloud, một phần tự host.

Nhưng cloud sẽ không thay thế hoàn toàn hệ thống tự host, vì hai lý do. Thứ nhất, nhiều hệ thống cũ ra đời trước cả khi có cloud và vẫn đang chạy tốt. Thứ hai, có những yêu cầu đặc biệt mà cloud không đáp ứng được. Ví dụ giao dịch chứng khoán tần suất cao (high-frequency trading): chậm vài micro giây là thua đối thủ, nên các công ty này cần kiểm soát hoàn toàn phần cứng, thậm chí đặt máy chủ ngay cạnh sàn giao dịch để rút ngắn đường truyền mạng. Trên cloud, bạn không chọn được máy chủ nằm ở đâu hay chạy chung với ai, nên không đạt được mức kiểm soát đó.

## Tóm lại

Đoạn trước nói cloud tiết kiệm công sức và linh hoạt. Đoạn này nói cái giá phải trả: mất quyền kiểm soát, gồm không tự thêm tính năng được, không tự sửa khi sập, khó debug, bị khóa vào nhà cung cấp, và phụ thuộc vào chính trị cũng như cam kết bảo mật của họ. Lựa chọn đúng là cân giữa hai mặt này cho từng hệ thống cụ thể.