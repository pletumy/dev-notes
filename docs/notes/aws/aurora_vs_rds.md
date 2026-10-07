# Lựa chọn PostgreSQL trên AWS: EC2 tự host vs RDS vs Aurora

Có ba cách chạy PostgreSQL trên AWS:

- **PostgreSQL tự cài trên EC2** — tự quản lý toàn bộ.
- **Amazon RDS** — dịch vụ database quản lý sẵn (managed), phù hợp cho tải nhỏ.
- **Amazon Aurora** (tương thích MySQL + PostgreSQL) — phù hợp cho app chịu tải nhiều, truy xuất nhiều.

RDS và Aurora đều là dịch vụ **fully-managed**: chỉ việc dùng, không cần tự cài đặt hay cập nhật thư viện/phiên bản — tiết kiệm thời gian vận hành so với tự host trên EC2.

## Tự host trên EC2

- **Ưu điểm**: toàn quyền kiểm soát (cấu hình, phiên bản, hệ điều hành...).
- **Nhược điểm**: tốn nhiều nhân lực hơn để bảo trì (cài đặt, vá lỗi, backup, theo dõi...).

![RDS vs Aurora overview](./images/Screenshot%202026-10-05%20at%2015.39.36.png)

## RDS

- Dịch vụ database quan hệ managed của AWS, hỗ trợ nhiều engine (PostgreSQL, MySQL...).
- Phù hợp cho các ứng dụng có tải vừa và nhỏ.

![RDS detail](./images/Screenshot%202026-10-05%20at%2016.02.25.png)

## Aurora vs RDS

- Aurora là engine database do AWS tự phát triển, tương thích API với MySQL và PostgreSQL, nhưng có kiến trúc lưu trữ riêng (tách compute và storage) giúp hiệu năng và khả năng mở rộng tốt hơn RDS thông thường.
- Nên chọn **RDS** khi tải nhỏ, ưu tiên chi phí thấp và đơn giản.
- Nên chọn **Aurora** khi ứng dụng cần chịu tải cao, đọc/ghi nhiều, cần khả năng mở rộng và độ sẵn sàng cao hơn.
