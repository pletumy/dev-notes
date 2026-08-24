---
title: "JWT, OAuth2, IdP, Access Token — Phân biệt các khái niệm trong Authentication & Authorization"
description: "Mỗi lần làm tính năng login là lại gặp một đống thuật ngữ: OAuth2, JWT, IdP, access token, refresh token, SSO... "
date: 2026-05-31
---

Mỗi lần làm tính năng login là lại gặp một đống thuật ngữ: OAuth2, JWT, IdP, access token, refresh token, SSO... Bài này mình sẽ phân biệt từng khái niệm, vẽ ra luồng thực tế, và chỉ rõ chúng liên quan với nhau như thế nào.

## IdP — Identity Provider

**IdP** là hệ thống xác minh danh tính người dùng và phát token. Google, GitHub, Facebook, Okta, Auth0, Keycloak, Authentik... đều là IdP.

> ⚠️ Ảnh thiếu: **Screenshot 2026-05-31 at 23.14.15.png** (không có trong dữ liệu export, cần upload lại thủ công)

**① Click "Login with Google"**
Bạn bấm nút. App nói: "tao không tự xác minh mày, tao gửi mày sang Google."

**② App redirect về Google**
App tạo một URL dạng `google.com/auth?client_id=...&scope=openid` rồi bảo trình duyệt gửi request đến đó. App xong việc, ngồi chờ response từ Google.

**③ Trình duyệt đến Google**
Trình duyệt thực sự chạy sang Google — giống như bạn gõ địa chỉ mới vào thanh URL. 

**④ Google hiện form đăng nhập**
Form này là của Google, App không quản lý.

**⑤ Bạn nhập email + password**
Password đi thẳng vào server Google. App không handle/ ko lưu password của user — đây là điểm mấu chốt của toàn bộ hệ thống.

**⑥ Google trả về Authorization Code**
Google xác minh xong, nhưng **không trả token ngay**. Thay vào đó Google redirect trình duyệt về App kèm một cái code ngắn, kiểu: `yourapp.com/callback?code=4/0AX4...`. Code này sống khoảng 10 giây, dùng 1 lần.

**⑦ Trình duyệt forward code về App**

**⑧ App gọi thẳng Google để đổi code**
Đây là bước quan trọng nhất. App gọi API Google từ **server của mình** — không qua trình duyệt — kèm theo `code` vừa nhận và `client_secret` của backend. 

**⑨ Google trả token thật**
Google xác nhận code hợp lệ + secret đúng → trả về `access_token` (để gọi API), `id_token` (JWT chứa tên, email, user ID của bạn), `refresh_token`. Token đi qua kênh server-to-server, không qua trình duyệt.

**⑩ App tạo session, đăng nhập xong**
App dựa `id_token` ra biết bạn là ai, tạo session, trả cookie về trình duyệt. Từ giờ bạn đã logged in. App có thể định danh được user mà ko cần lưu credentials

## OAuth2 — Giao thức ủy quyền

**OAuth2** là một *giao thức* định nghĩa cách một ứng dụng xin quyền truy cập tài nguyên thay mặt người dùng. Giao diện thường thấy của Google OAuth2:

> ⚠️ Ảnh thiếu: **authz-single-consent.png** (không có trong dữ liệu export, cần upload lại thủ công)

Ví dụ thực tế: App muốn truy cập Google Calendar của bạn, nó sẽ redirect sang UI của Google, Google confirm viuws user như ảnh: "App X muốn đọc calendar của bạn, đồng ý không?" Nếu user đồng ý, Google cấp token cho app và app dùng token đó để gọi Google Calendar API

**Quan trọng:** OAuth2 ban đầu là về *authorization* (ủy quyền truy cập resource), không phải authentication. Nhưng nó thường bị dùng cho cả login — đó là lý do OpenID Connect ra đời.

## OpenID Connect (OIDC)

**OIDC** là một lớp identity xây trên OAuth2. Nếu OAuth2 sẽ quản lý authorization, thì OIDC sẽ quản phẩn authentication

OIDC thêm vào OAuth2:
- **ID Token** — chứa thông tin về user (name, email, sub)
- **UserInfo endpoint** — lấy thêm thông tin user
- **Standardized scopes** — `openid`, `profile`, `email`

Khi bạn dùng "Login with Google", thực ra bạn đang dùng OAuth2 + OIDC.

## JWT — JSON Web Token

**JWT** là *format* của token — không phải giao thức, không phải hệ thống.

Cấu trúc JWT gồm 3 phần, ngăn cách bằng dấu `.`:

```
eyJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJ1c2VyMTIzIiwibmFtZSI6IlR1IE15IiwiZXhwIjoxNzE2MDAwMDAwfQ.signature
      Header                              Payload                                    Signature
```

**Header** — thuật toán ký (RS256, HS256...)  
**Payload** — claims: thông tin user, thời gian hết hạn, issuer...  
**Signature** — chữ ký để verify tính toàn vẹn

Decode payload ra:

```json
{
  "sub": "67......2b1b412285",
  "email": "ple.tumy@gmail.com",
  "jti": "1bac......15f0eecd",
  "exp": 1780271782,
  "iat": 1780242982
}
```


## Access Token

**Access Token** là token dùng để truy cập API/resource trên server. 

Đặc điểm:
- **Short-lived** — thường 15 phút đến 1 giờ
- Gửi kèm trong `Authorization: Bearer <token>` header

```
Client → GET /api/posts
         Authorization: Bearer eyJhbGci...
         
Server → verify token → trả data
```

## Refresh Token

**Refresh Token** giải quyết vấn đề access token ngắn hạn.

Khi access token hết hạn, thay vì bắt user login lại:

```
Client → POST /auth/token
         grant_type=refresh_token
         refresh_token=<refresh_token>
         
Auth Server → access_token mới + refresh_token mới
```

Đặc điểm:
- **Long-lived** — thường 7-30 ngày
- Được lưu an toàn (httpOnly cookie, secure storage)
- Chỉ gửi đến auth server, không đến resource server
- Có thể bị revoke — khi user logout, đổi password

## SSO — Single Sign-On

**SSO** là trải nghiệm "đăng nhập một lần, dùng nhiều app". Kỹ thuật bên dưới thường là OAuth2/OIDC với shared IdP.

```
User login vào Google một lần
→ Mở Gmail    → Google confirm session → vào thẳng
→ Mở Drive    → Google confirm session → vào thẳng
→ Mở YouTube  → Google confirm session → vào thẳng
```

Trong enterprise: Okta/Azure AD là IdP trung tâm, tất cả app (Slack, GitHub, Jira...) đều delegate identity về đó.

## Tóm tắt quan hệ giữa các khái niệm
> ⚠️ Ảnh thiếu: **Screenshot 2026-05-31 at 23.37.56.png** (không có trong dữ liệu export, cần upload lại thủ công)


OAuth2          → Giao thức ủy quyền
  └── OIDC     → Thêm lớp identity lên OAuth2

IdP             → Hệ thống thực thi OAuth2/OIDC (Google, Auth0...)

JWT             → Format của token (dùng trong access token, id token)

Access Token    → Token ngắn hạn để gọi API
Refresh Token   → Token dài hạn để lấy access token mới
ID Token        → JWT chứa thông tin user (từ OIDC)

SSO             → Trải nghiệm người dùng, implement bằng OAuth2/OIDC
