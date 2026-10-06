# Network Cache (DNS Cache)

Khái niệm cache xuất hiện ở rất nhiều nơi, không chỉ ở server mà còn ở browser và DNS.

## DNS Cache

> Tham khảo: [video giải thích DNS](https://www.youtube.com/watch?v=PI9-kQST_BM)

DNS cache hỗ trợ việc tra cứu nhanh địa chỉ IP của một server/domain, được lưu ở nhiều lớp khác nhau: browser, hệ điều hành, router, và ISP.

Thứ tự tra cứu khi nhập một URL và nhấn Enter:

1. Tìm trong **DNS cache của trình duyệt (browser)**.
2. Nếu không có, tìm tiếp trong **cache của hệ điều hành (OS)**.
3. Nếu không có, tìm tiếp trong **cache của router**.
4. Nếu không có, tìm tiếp trong **cache của ISP** (ví dụ VNPT, Viettel — kiểm tra xem đã từng có request tới domain này trước đó chưa).
5. Nếu ISP cũng không có, ISP sẽ gửi truy vấn tới các **DNS server** để tìm domain này đang khớp với địa chỉ IP nào, rồi trả kết quả ngược về qua từng lớp cache ở trên.
