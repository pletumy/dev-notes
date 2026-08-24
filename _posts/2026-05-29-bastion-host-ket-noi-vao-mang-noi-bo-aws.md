---
title: "Bastion Host — Kết nối vào mạng nội bộ AWS"
date: 2026-05-29
categories: [javascript]
slug: bastion-host-ket-noi-vao-mang-noi-bo-aws
---

## Câu chuyện thực tế

Hôm đó mình cần kết nối vào RDS PostgreSQL đang chạy trong private subnet của VPC. RDS không có public endpoint. Nhưng tôi cần debug dữ liệu ngay lập tức.

Giải pháp: SSH vào một EC2 có public DNS, rồi **forward port** từ máy local xuống RDS thông qua con EC2 đó.

```bash
ssh -i myphan.pem \
    -L 5433:my-rds.cluster-xxx.ap-southeast-1.rds.amazonaws.com:5432 \
    ec2-user@ec2-xx-xx-xx-xx.ap-southeast-1.compute.amazonaws.com \
    -N
```

Sau đó kết nối bình thường:

```bash
psql -h localhost -p 5433 -U postgres -d mydb
```

Con EC2 đó chính là **Bastion Host**.

## Bastion Host là gì?

Bastion Host (hay Jump Server) là một server đặc biệt nằm ở vùng DMZ — có thể truy cập từ internet, nhưng đóng vai trò **cửa ngõ duy nhất** để vào hạ tầng nội bộ.

![ChatGPT Image May 29, 2026, 03_31_40 PM.png](f4510938-6f0f-4029-a984-ce7f57669371)


## Cách SSH Port Forwarding hoạt động

Khi chạy lệnh:

```bash
ssh -L 5433:rds-host:5432 user@bastion -N
```

Máy tính của bạn sẽ lắng nghe port `5432`. Mọi kết nối tới `localhost:5432` được SSH tunnel chuyển tiếp tới `rds-host:5432` — **thông qua** bastion, từ góc nhìn của mạng nội bộ AWS.

## Security Group cần cấu hình như thế nào?

**Bastion EC2 — Inbound:**

![Screenshot 2026-05-29 at 15.36.50.png](608033ee-d3cd-4b98-827d-e354ff0c72da)

**RDS — Inbound:**

| Type       | Port | Source                    |
|------------|------|---------------------------|
| PostgreSQL | 5432 | Security Group của Bastion |

Không bao giờ mở RDS ra `0.0.0.0/0`

---

## Câu lệnh hay dùng

**Kết nối có tunnel (chạy nền):**

```bash
ssh -i key.pem \
    -L 5433:rds-endpoint:5432 \
    ec2-user@bastion-ip \
    -fN
```

**Kết nối vào app server qua bastion (ProxyJump):**

```bash
ssh -i key.pem \
    -J ec2-user@bastion-ip \
    ec2-user@private-app-ip
```

**Cấu hình `~/.ssh/config` cho tiện:**

```
Host bastion
    HostName ec2-xx-xx.compute.amazonaws.com
    User ec2-user
    IdentityFile ~/.ssh/myphan.pem

Host rds-tunnel
    HostName localhost
    Port 5433
    LocalForward 5433 my-rds.xxx.rds.amazonaws.com:5432
    ProxyJump bastion
```

Sau đó chỉ cần `ssh rds-tunnel -N` là xong.

Bastion Host là pattern đơn giản nhưng hiệu quả. Hiểu rõ nó giúp bạn vừa debug nhanh khi cần, vừa duy trì kiến trúc bảo mật đúng đắn.
