---
title: "Rate Limiting trong FastAPI — Từ \"Không Có Gì\" Đến Production-Ready (Phần 1)"
date: 2026-05-23
categories: [python]
slug: rate-limiting-trong-fastapi-tu-khong-co-gi-en-production-ready-phan-1-2
---

Hôm nay mình sẽ chia sẻ về cách implement rate limiting cho blog cá nhân của mình — một thứ mà lúc đầu mình nghĩ "blog cá nhân cần gì rate limiting", nhưng sau khi chạy thử load test thì... ừ thôi implement đi cho chắc.

## Vấn đề bắt đầu từ đây

Trước khi có rate limiting, mình thử bắn 200 requests/giây từ 1 IP vào endpoint `GET /posts/` xem sao:

```bash
echo "GET https://api.test.com/api/v1/posts/" | vegeta attack -rate=200/s -duration=10s | vegeta report
```

Kết quả:

![Screenshot 2026-05-23 at 14.29.34.png](8f421b8c-aa0e-48d9-90b5-b4c4d131153a)

**p50 là 13.9 giây.** Tức là một nửa số requests mất gần 14 giây mới có response. Trộm vía app không crash, nhưng DB đang ăn 200 requests một cách vô nghĩa và phản hồi rất chậm.

## Kiến trúc: Hai lớp bảo vệ

Trước khi đi vào code, điều quan trọng là hiểu rate limiting không chỉ là một thứ — nó nên có nhiều lớp:

```
Client
  │
  ▼
Cloudflare Edge     ← Lớp 1: chặn tại network edge
  │
  ▼
FastAPI + SlowAPI   ← Lớp 2: chặn tại application
  │
  ▼
Redis               ← Shared counter cho tất cả instances
  │
  ▼
PostgreSQL
```

Hai lớp này bổ sung cho nhau:
- **Cloudflare** chặn sớm, không để request vào queue
- **SlowAPI + Redis** bảo vệ kể cả khi ai đó bypass Cloudflare và hit thẳng vào origin IP

## Tại sao Redis, không phải in-memory?

Câu hỏi hợp lý đầu tiên: "Lưu counter trong memory của app không được sao?"

Được, nhưng chỉ khi bạn chạy **đúng một instance**. Trên production với ECS hay Kubernetes, app thường scale ra nhiều instance:

```
# Nếu dùng in-memory counter

Instance A: counter = 40 req
Instance B: counter = 40 req  
Instance C: counter = 40 req

→ Thực tế đã có 120 requests, nhưng mỗi instance chỉ thấy 40
→ Rate limit 100/min vô nghĩa hoàn toàn
```

Redis giải quyết vấn đề này vì tất cả instances đều đọc/ghi vào **một counter duy nhất**:

```
Instance A ──┐
Instance B ──┼──→ Redis counter = 120 
Instance C ──┘
```

## Implementation

### 1. Thêm dependency

```
# requirements.txt
slowapi>=0.1.9
```

### 2. Tạo limiter

Tách ra file riêng để import từ bất kỳ router nào:

```python
# src/core/rate_limit.py
from slowapi import Limiter
from slowapi.util import get_remote_address
from src.core.config import settings

# ElastiCache dùng TLS với self-signed cert của AWS
# → cần tắt cert verification khi URL là rediss://
_storage_options = {"ssl_cert_reqs": "none"} if settings.REDIS_URL.startswith("rediss://") else {}

limiter = Limiter(
    key_func=get_remote_address,   # dùng IP client làm key
    storage_uri=settings.REDIS_URL,
    storage_options=_storage_options,
    default_limits=["300/minute"], # fallback cho mọi endpoint
)
```

Cái `_storage_options` ở đây xử lý một edge case thực tế: local dev dùng `redis://` bình thường, production dùng AWS ElastiCache với `rediss://` (TLS). Cert của ElastiCache là self-signed, không có trong trust store mặc định → nếu không tắt verify thì sẽ bị lỗi `SSL: CERTIFICATE_VERIFY_FAILED`.

### 3. Wire vào FastAPI app

```python
# main.py
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from src.core.rate_limit import limiter

app = FastAPI(...)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)
```

### 4. Decorate endpoints

```python
# src/api/post.py
from fastapi import APIRouter, Request
from src.core.rate_limit import limiter

@router.get("/", response_model=DefaultResponsePayload)
@limiter.limit("100/minute")
async def list_posts(request: Request, post_service: PostService = Depends(get_post_service)):
    res = await post_service.list()
    return DefaultResponsePayload(data=[post.to_dict() for post in res])
```
## Tại sao phải có `request: Request` dù không dùng?

Đây là câu hỏi mình cũng thắc mắc lúc đầu. `request: Request` không phải để business logic dùng mà SlowAPI cần đọc IP của client để build Redis key:

![Screenshot 2026-05-23 at 14.27.32.png](3794b725-5447-419c-af0f-f82a2fa56b88)

FastAPI inject `request` vào function, SlowAPI đọc IP từ đó, còn function body không cần đụng đến nó.

## Phân tầng limits theo loại endpoint

Không phải endpoint nào cũng nên có cùng một limit. Mình chia theo mức độ nhạy cảm:

```python
# Public read — thoải mái hơn
@router.get("/")
@limiter.limit("100/minute")
async def list_posts(request: Request, ...): ...

# Single resource
@router.get("/{id}")
@limiter.limit("200/minute")
async def get_post(request: Request, ...): ...

# Write operations — chặt hơn
@router.post("/")
@limiter.limit("20/minute")
async def create_post(request: Request, ...): ...

# Auth — quan trọng nhất, chặt nhất
@router.get("/auth/login")
@limiter.limit("20/minute")
async def oidc_login(request: Request): ...

# Tất cả endpoints còn lại → 300/minute (default)
```

Lý do auth endpoint cần limit thấp nhất: Hạn chế Brute force, credential stuffing.

## Kết quả sau khi implement

Chạy lại cùng test 200 req/s:

```bash
echo "GET https://api.test.com/api/v1/posts/" | vegeta attack -rate=200/s -duration=10s | vegeta report
```
![Screenshot 2026-05-23 at 14.29.27.png](b739d6b5-2347-42f7-a62e-f82afd6b3608)

**100 requests được phục vụ, 1857 bị chặn với 429.** Đúng bằng limit 100/minute.


Nhưng để ý: **p50 vẫn là 10.6s**. App trả 429 đúng rồi, nhưng response vẫn chậm. Lý do là Cloudflare đang để requests trong queue trước khi forward về ELB — app xử lý 429 chỉ ~1ms, nhưng request đã nằm chờ ~10s trong Cloudflare queue.

Bài tiếp theo sẽ cover phần còn lại: Cloudflare Rate Limiting Rule, tại sao p99 vẫn cao, và cách giảm xuống gần 0 với edge caching.
