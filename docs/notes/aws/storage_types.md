# Các loại Storage trên AWS: S3 vs EBS vs EFS

## S3 (Simple Storage Service)

- Lưu trữ theo đơn vị **object** (file được upload lên).
- Tối đa **5TB/file**, dung lượng tổng thể gần như không giới hạn.
- Mỗi bucket có tên **unique** trên toàn cầu.

### Storage Classes của S3

- **Standard**: dễ dàng upload và truy xuất, phù hợp dữ liệu truy cập thường xuyên.
- **Intelligent-Tiering**: tự động chuyển dữ liệu giữa các tier dựa trên tần suất truy cập, tính thêm phí quản lý.
- **Standard-IA** (Infrequent Access): dành cho dữ liệu ít truy cập, tính phí theo lượt truy xuất (retrieval fee).
- **One Zone-IA**: giống Standard-IA nhưng chỉ lưu trên **1 Availability Zone** — rẻ hơn nhưng có nguy cơ mất dữ liệu nếu AZ đó gặp sự cố.
- **Glacier**: dành cho dữ liệu lưu trữ (archive), ít truy cập, chi phí thấp.
- **Glacier Deep Archive**: lưu trữ dài hạn (long-term archive), ví dụ dữ liệu khách hàng cần giữ 10 năm — tương tự việc trước đây lưu vào băng từ (tape), chi phí thấp nhất nhưng thời gian truy xuất lâu nhất.

## EBS (Elastic Block Storage)

- Là loại **network-attached storage**, chỉ dùng cho EC2.
- Mỗi volume EBS chỉ được gắn (attach) vào **1 EC2 tại một thời điểm**.
- Bị giới hạn trong **1 Availability Zone** — EBS ở AZ1 chỉ kết nối được với EC2 cũng nằm ở AZ1.
- Có hai loại chính: **gp** (general purpose) và **io** (dành cho input/output tốc độ cao).
- Khi tạo một EC2 mới, mặc định sẽ tạo kèm một EBS volume (root volume).

## EFS (Elastic File System)

- Có thể được **mount vào nhiều EC2 cùng lúc**.
- Nhiều EC2 có thể cùng **ghi (write)** vào chung một EFS — phù hợp cho các workload cần chia sẻ file giữa nhiều instance.

## Tổng quan so sánh

![So sánh S3, EBS, EFS](./images/Screenshot%202026-10-05%20at%2017.52.24.png)

| | S3 | EBS | EFS |
|---|---|---|---|
| Đơn vị lưu trữ | Object | Block | File |
| Gắn với | Truy cập qua API/HTTP, không gắn trực tiếp vào EC2 | 1 EC2 tại 1 thời điểm | Nhiều EC2 cùng lúc |
| Phạm vi AZ | Toàn vùng (region) | 1 AZ | Nhiều AZ |
