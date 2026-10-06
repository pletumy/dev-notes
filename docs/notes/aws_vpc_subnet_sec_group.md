# VPC, Subnet, NACL và Security Group trên AWS

## VPC

- Mỗi tài khoản AWS có thể tạo nhiều VPC (Virtual Private Cloud) — mỗi VPC là một mạng ảo riêng biệt.

## Internet Gateway

- Mỗi VPC muốn kết nối ra Internet cần gắn một **Internet Gateway**.

## Subnet

![Subnet](./images/Screenshot%202026-10-05%20at%2022.03.08.png)

- Subnet nằm trong VPC — một VPC có thể chứa nhiều subnet.
- Có 2 loại: **public subnet** và **private subnet**, bản chất giống nhau, chỉ khác route table:
  - Route table của public subnet có đường đi ra Internet qua Internet Gateway.
  - Route table của private subnet thì không.
- **Public IP** được gắn cho các server nằm trong public subnet (thường là frontend).
- **Private subnet** chứa database và backend — không expose trực tiếp ra Internet.

## Network Access Control List (NACL)

![NACL](./images/Screenshot%202026-10-05%20at%2022.12.18.png)

- NACL là bộ rule áp dụng vào subnet, quy định traffic nào được đi vào/đi ra.
- **Stateless**: phải định nghĩa rule theo cả hai chiều (IN/OUT) riêng biệt. Ví dụ: nếu chỉ định nghĩa rule cho phép IN ở port 80 mà không định nghĩa OUT cho port 80, request đi vào được nhưng response không đi ra lại được cho client — vì vậy phải định nghĩa cả hai chiều.
- Mỗi subnet chỉ được gắn với **1 NACL** tại một thời điểm.
- Rule có thể là **allow** hoặc **deny** (defined/allowed).

### Inbound rule cho NACL

![Inbound rule NACL](./images/Screenshot%202026-10-05%20at%2022.13.35.png)

## Security Group

![Security Group bảo vệ EC2](./images/Screenshot%202026-10-05%20at%2022.44.35.png)

- Đóng vai trò **firewall** bảo vệ các component nằm trong subnet (ví dụ: đang bảo vệ một EC2).
- **Stateful** — ngược lại với NACL: chỉ cần định nghĩa request chiều vào (IN) là đủ, response tự động được cho phép đi ra mà không cần định nghĩa thêm.
- Chỉ có **allow**, không có **deny** như NACL.
- Không có khái niệm **order** (thứ tự rule) như NACL.

### Ví dụ luồng traffic

![Ví dụ inbound/outbound Security Group](./images/Screenshot%202026-10-05%20at%2022.47.35.png)

- **Inbound** đi vào: ví dụ người dùng gửi request đến cổng 80 → vào được cổng 80 → response tự động ra lại được cổng 80, không cần cấu hình gì thêm.
- **Outbound**: request từ EC2 đi ra — có thể gọi đến bất kỳ port nào, bất kỳ protocol nào (mặc định mở toàn bộ chiều ra).
- Tóm lại: chiều ra (outbound) mặc định mở toang, còn chiều vào (inbound) thì bị giới hạn theo đúng port/source đã khai báo.

## CIDR

- CIDR (Classless Inter-Domain Routing) dùng để định nghĩa dải địa chỉ IP cho VPC/subnet (ví dụ `10.0.0.0/16`), quyết định số lượng địa chỉ IP khả dụng trong mạng.

## Ví dụ: Set up Virtual Network

![Thiết lập Virtual Network mẫu](./images/Screenshot%202026-10-05%20at%2022.55.01.png)

Một thiết kế mạng mẫu gồm:

- 1 public subnet (chứa frontend, có public IP, route ra Internet qua Internet Gateway).
- 2 private subnet (chứa backend/database, không có đường ra Internet trực tiếp).
