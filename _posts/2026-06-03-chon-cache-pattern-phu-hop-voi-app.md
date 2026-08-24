---
title: "Chọn Cache Pattern Phù Hợp Với App ?"
description: "Chắc hẳn ai làm backend cũng từng gặp cảnh hệ thống đang chạy ngon lành, tự dưng traffic tăng một chút là database bắt đầu \"thở oxy\". Nhiều trường hợp, vấn đề không nằm ở DB hay server mà đơn giản là chưa tận dụng cache đúng cách.
"
date: 2026-06-03
categories: [python]
slug: chon-cache-pattern-phu-hop-voi-app
---

Chắc hẳn ai làm backend cũng từng gặp cảnh hệ thống đang chạy ngon lành, tự dưng traffic tăng một chút là DB bắt đầu "thở oxy". Nhiều trường hợp, vấn đề không nằm ở DB hay server mà đơn giản là chưa tận dụng cache đúng cách.

Nhưng cache không phải cứ thêm Redis vào là xong. Mỗi cách sử dụng cache sẽ phù hợp với một bài toán khác nhau. Chọn đúng thì hệ thống nhanh và ổn định hơn rất nhiều. Chọn sai thì lại phải đau đầu xử lý stale data, cache miss hàng loạt hoặc thậm chí mất dữ liệu.

Trong bài viết này, mình sẽ đi qua 4 cache pattern phổ biến nhất và những trường hợp thực tế mà chúng thường được sử dụng.

## 1. Cache Aside
![cache aside.png](3fd35428-83f5-42fc-804e-c7525042313c)


Đây có lẽ là pattern quen thuộc nhất với đa số developer.

Luồng hoạt động khá đơn giản:

1. App check trong cache trước.
2. Nếu cache có dữ liệu (cache hit) thì trả về ngay.
3. Nếu cache không có (cache miss) thì đọc từ DB.
4. Sau khi lấy được dữ liệu từ DB, ứng dụng lưu lại vào cache để dùng cho những lần sau.

Nói cách khác, backend chịu trách nhiệm hoàn toàn cho việc đọc và ghi cache.

### Ví dụ thực tế

Một ví dụ điển hình là trang hồ sơ người dùng trên mạng xã hội.

Thông tin như tên, avatar hay bio thường không thay đổi nhiều nhưng lại được đọc liên tục. Vì vậy mỗi lần có người truy cập profile, hệ thống sẽ kiểm tra Redis trước. Nếu không có mới query xuống DB rồi cache lại kết quả.

### Khi nào nên dùng?

* Dữ liệu được đọc nhiều hơn ghi.
* Muốn toàn quyền kiểm soát logic cache.
* Cache và dữ liệu trong DB không nhất thiết phải có cùng cấu trúc.
* Muốn hệ thống vẫn hoạt động nếu cache gặp sự cố.

### Điểm cần lưu ý

Vấn đề thường gặp nhất là dữ liệu bị cũ (stale data). Nếu dữ liệu trong DB đã thay đổi nhưng cache chưa được cập nhật, người dùng sẽ tiếp tục nhìn thấy data cũ. Vì vậy Cache Aside thường đi kèm với TTL hoặc cơ chế invalidate cache khi có thao tác ghi.
Với ví dụ trên, chẳng hạn user update lại thông tin cá nhân vào DB, nhưng cache vẫn  chưa cập nhật thì load trên UI vẫn là thông tin cũ.

## 2. Read Through

Read Through có cách hoạt động khá giống Cache Aside nhưng trách nhiệm được chuyển sang cache layer. Thay vì app tự query từ DB khi cache miss thì cache sẽ đi query, app chỉ giao tiếp với cache.

![read through.png](3ba072ef-31b0-404c-bbfe-36bb9dcce2b7)


Luồng xử lý sẽ là:

1. App yêu cầu dữ liệu từ cache.
2. Cache hit → trả về ngay.
3. Cache miss → cache query DB, lưu lại rồi trả kết quả cho app.

Từ góc nhìn của ứng dụng, DB gần như bị "ẩn đi".

### Ví dụ thực tế

Các hệ thống đọc nội dung như blog, tin tức hoặc tài liệu thường rất phù hợp với mô hình này. Nhiều framework hiện nay như Spring Cache hay Django Cache Framework hỗ trợ khá tốt. Developer chỉ cần đánh dấu hàm cần cache, phần còn lại framework sẽ xử lý.

### Khi nào nên dùng?

* Hệ thống thiên về đọc dữ liệu.
* Muốn giảm lượng code liên quan đến cache.
* Muốn chuẩn hóa cách cache trong toàn bộ ứng dụng.

### Điểm cần lưu ý

Lần truy cập đầu tiên chắc chắn sẽ bị cache miss. Ngoài ra, Read Through thường hoạt động tốt nhất khi dữ liệu trong cache và dữ liệu trong DB có cùng cấu trúc. Nếu cần transform dữ liệu phức tạp trước khi cache thì Cache Aside sẽ linh hoạt hơn.

## 3. Write Back (Write Behind) – Ghi trước, đồng bộ sau

Nếu Cache Aside và Read Through chủ yếu tối ưu cho việc đọc thì Write Back lại tập trung vào tốc độ ghi.

![write back.png](02c939bf-1297-42cd-8570-415e9fe7882f)


Thay vì ghi xuống DB ngay lập tức, hệ thống:

1. Ghi vào cache trước.
2. Trả kết quả thành công cho người dùng.
3. Đồng bộ dữ liệu từ cache xuống DB theo lô hoặc theo lịch định kỳ.

Nhờ vậy độ trễ khi ghi giảm đáng kể.

### Ví dụ thực tế

Like, view hoặc reaction trên mạng xã hội là ví dụ kinh điển. Nếu mỗi lượt xem video đều ghi trực tiếp vào database thì hệ thống sẽ nhanh chóng trở thành một vấn đề nếu có ông nào spam click.
Cáchcách phổ biến là:
* Tăng counter trong Redis.
* Định kỳ vài giây hoặc vài nghìn lượt cập nhật thì ghi xuống database.

Game leaderboard thời gian thực cũng thường áp dụng cách tiếp cận tương tự.

### Khi nào nên dùng?

* Hệ thống có lượng ghi rất lớn.
* Cần giảm áp lực cho database.
* Chấp nhận eventual consistency.

### Điểm cần lưu ý

Trade-off lớn nhất là nguy cơ mất dữ liệu.

Nếu cache gặp sự cố trước khi dữ liệu được đồng bộ xuống DB, phần dữ liệu đó có thể biến mất hoàn toàn.
Vì vậy Write Back thường cần kết hợp với persistence hoặc replication để giảm rủi ro.

## 4. Write Around – Ghi thẳng vào DB, cache khi thực sự cần

![write around.png](3a504ca2-6921-4de5-8124-ad6d382daf59)


Write Around có triết lý khá đơn giản:

* Ghi trực tiếp vào database.
* Không đưa dữ liệu mới vào cache ngay.
* Chỉ cache khi có nhu cầu đọc thực sự.

Mục tiêu là tránh làm đầy cache bằng những dữ liệu có thể chẳng bao giờ được truy cập lại.

### Ví dụ thực tế

Log hệ thống là trường hợp rất điển hình. Hàng triệu bản ghi log có thể được tạo ra mỗi ngày, nhưng phần lớn sẽ không bao giờ được đọc lại. Nếu mỗi lần ghi log đều cache luôn thì chỉ đang lãng phí tài nguyên bộ nhớ.

### Khi nào nên dùng?

* Dữ liệu được ghi nhiều nhưng ít khi đọc lại ngay.
* Muốn hạn chế cache pollution.
* Muốn tối ưu dung lượng cache cho những dữ liệu thực sự quan trọng.

### Điểm cần lưu ý

Lần đọc đầu tiên thường chậm hơn vì phải truy vấn database.

Nếu cơ chế invalidate không tốt, hệ thống vẫn có thể gặp vấn đề stale data giống các pattern khác.

## So sánh nhanh

![Screenshot 2026-06-03 at 17.08.06.png](753222c5-1caa-4a12-b373-dc1822ca89cb)

## Kết luận

Không có cache pattern nào là "tốt nhất" cho mọi trường hợp.

Điều quan trọng là hiểu đặc điểm dữ liệu của hệ thống:

* Đọc nhiều hay ghi nhiều?
* Chấp nhận dữ liệu cũ trong bao lâu?
* Cache gặp sự cố thì điều gì sẽ xảy ra?
* Dữ liệu vừa ghi có cần được đọc lại ngay không?

Khi trả lời được những câu hỏi đó, việc chọn cache pattern sẽ trở nên dễ dàng hơn rất nhiều. Và trong đa số dự án thực tế, bài toán không phải là "có dùng cache hay không", mà là "dùng cache theo cách nào cho hợp lý".
