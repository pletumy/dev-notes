# Redis

Redis là một **in-memory database**, lưu trữ dữ liệu dưới dạng các object (JSON) theo cặp **key-value** — gần như mọi thứ trong Redis đều là key-value pair.

Các database khác thường lưu dữ liệu trên **disk**, trong khi Redis lưu trên **RAM**, nên tốc độ đọc/ghi nhanh hơn rất nhiều (khoảng 1000 lần).

**Nhược điểm**: nếu server sập, toàn bộ dữ liệu trong RAM sẽ bị mất (wiped out) vì không lưu persistent theo mặc định. Vì vậy Redis phù hợp nhất cho các loại dữ liệu mà người dùng truy cập thường xuyên nhưng ít bị thay đổi.

## Vì sao Redis nhanh?

- Lưu dữ liệu trên **RAM** thay vì disk.
- **Single-threaded** — kiến trúc đơn giản hơn so với các hệ cơ sở dữ liệu đa luồng.

### Vậy Redis xử lý nhiều request cùng lúc bằng cách nào nếu chỉ chạy đơn luồng?

Nhờ cơ chế **I/O multiplexing** kết hợp **event loop**: thay vì tạo thread riêng cho từng kết nối, Redis dùng một vòng lặp sự kiện để theo dõi nhiều kết nối I/O cùng lúc và xử lý tuần tự các sự kiện sẵn sàng, nên vẫn phục vụ được nhiều client đồng thời mà không cần đa luồng.
