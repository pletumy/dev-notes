---
title: "Giải thích dễ hiểu về TCP vs UDP"
description: "Lấy cảm hứng từ bài viết hay ho của Naman Sisodia trên Medium :v"
date: 2026-06-06
---

> **Bài viết này lấy cảm hứng từ bài viết hay ho của Naman Sisodia trên Medium:** [Understanding TCP, UDP, HTTP, And WebSocket Concepts PART - 1](https://any-one-can-code.medium.com/understanding-tcp-udp-http-and-websocket-concepts-part-1-499f9f751c54). Mình đọc bài này và thấy cách giải thích khá là rõ ràng, dễ hiểu, ko bị quá ngộp các thuật ngữ technical, nên quyết định viết lại bằng tiếng Việt, mở rộng thêm phần HTTP và WebSocket để cho trọn bộ. Mọi công nhận xứng đáng đều thuộc về tác giả gốc!
> ⚠️ Ảnh thiếu: **1_GEUhDCOVJVC1dGGBmFcg1Q (1).jpg** (không có trong dữ liệu export, cần upload lại thủ công)


## 1. UDP 

### UDP là gì?

UDP (User Datagram Protocol) là giao thức truyền dữ liệu theo cơ chế không cần kết nối và không đảm bảo (connectionless và unreliable). Nó sẽ cứ thế spam data tới đích mà không cần biết người nhận có đang sẵn sàng, có nhận được hay không, và cũng không yêu cầu phản hồi từ phía nhận.

### Câu chuyện của Server và Client với UDP

Ví dụ Server muốn nhắn cho Client câu: *"Mày ổn không?"* Server chuyển câu đó thành các **gói tin (packets)** — mỗi gói tin chứa một mảnh dữ liệu nhỏ — rồi gửi thẳng tới client, không biết là client có sẵn sàng nhận kết nối hay không.

**Happy case:** Client nhận đủ tất cả các gói tin, đọc được câu hoàn chỉnh. 
> ⚠️ Ảnh thiếu: **udp-happy.png** (không có trong dữ liệu export, cần upload lại thủ công)

**Unhappy case 1 — Mất gói tin:** 
> ⚠️ Ảnh thiếu: **udp-sad1.png** (không có trong dữ liệu export, cần upload lại thủ công)


**Unhappy case 2 — Nhận lung tung thứ tự:** 
> ⚠️ Ảnh thiếu: **udp-sad2.png** (không có trong dữ liệu export, cần upload lại thủ công)

Và Server? Server không hề biết Client nhận được gì. **Server đã gửi xong và quên luôn.**

### Vậy thì UDP có ích gì?

Nghe có vẻ ko ổn lắm nhưng UDP lại cực kỳ hữu ích vì một lý do đơn giản: **tốc độ**. Vì không phải lo lắng về việc xác nhận, kết nối, hay thứ tự gói tin — UDP truyền data rất nhanh. UDP = nhanh + không đảm bảo. Dùng khi bạn *có thể chấp nhận mất dữ liệu*.

UDP được dùng ở đâu?

- Game online/multiplayer
- Video streaming / YouTube
- VoIP (gọi điện qua internet)
- DNS

## 2. TCP 

### TCP là gì?

TCP (Transmission Control Protocol) là giao thức **hướng kết nối** (connection-oriented). Trước khi truyền data, Server và Client phải kết nối với nhau đã. Sau đó mọi gói tin đều được đánh số, xác nhận, và nếu mất thì gửi lại.

### Three-Way Handshake
> ⚠️ Ảnh thiếu: **Screenshot 2026-06-06 at 18.56.13.png** (không có trong dữ liệu export, cần upload lại thủ công)

Đây là bước khởi động bắt buộc của TCP. Nghe phức tạp nhưng thực ra rất đơn giản:

**Bước 1 — SYN:** Client nhắn Server: *"Ê Server, tao muốn nói chuyện. Số của tao là 100 nha."*

**Bước 2 — SYN-ACK:** Server trả lời: *"Tao nhận được rồi (100+1=101). Và số của tao là 500 nha."*

**Bước 3 — ACK:** Client xác nhận: *"Tao nhận được số của mày rồi (500+1=501). Bắt đầu thôi!"*

Cả hai bây giờ đã **xác nhận lẫn nhau** — ai cũng biết đối phương đang online và sẵn sàng kết nối.

### Nhược điểm của TCP?

- **Chậm hơn UDP** vì phải làm nhiều thứ hơn.
- **Không phù hợp để broadcast** — Nếu Server muốn gửi data cho 1 triệu người, phải tạo 1 triệu kết nối riêng. 

### TCP dùng ở đâu?

- Web (HTTP/HTTPS)
- WebSocket
- Email (SMTP, IMAP)
- Truyền file (FTP)
- SSH
Không cần dùng tool gì cho cái này — đây là đoạn dịch:

**UDP hay TCP — cái nào tốt hơn?**

Thực ra không có cái nào tốt hơn giữa UDP và TCP cả. Cả hai đều phù hợp với những use case khác nhau. Không có giao thức hoàn hảo nào tồn tại — hay sẽ tồn tại — mà không có giới hạn. UDP phù hợp với các ứng dụng real-time, hạn chế độ trễ, và việc mất hoặc xáo trộn thông tin vẫn có thể chấp nhận được. TCP thì ngược lại — nó đảm bảo dữ liệu được truyền đi chính xác, nên người dùng không cần lo lắng gì về dữ liệu. Bonus cho quả meme:

> ⚠️ Ảnh thiếu: **1_vjQxkIN0ncEIFKngYiaDPA.jpg** (không có trong dữ liệu export, cần upload lại thủ công)
