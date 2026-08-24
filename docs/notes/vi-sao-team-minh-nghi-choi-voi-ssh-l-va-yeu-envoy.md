---
title: "Từ ssh -L đến TCP Tunnel Manager — và vì sao Envoy là mảnh ghép còn thiếu"
description: "Tụi mình thay ssh -L bằng một con proxy dựa trên Envoy: quản lý tunnel qua UI web, thêm bớt thoải mái mà không cần restart — ai trong team cũng dùng được, kể cả người không rành terminal."
date: 2026-05-29
---

# Hành trình khai tử cái lệnh `ssh -L` trong team mình

> Hay là câu chuyện về việc tụi mình chán SSH tunnel như thế nào, rồi dựng một con proxy biết tự "thay áo" mà không cần khởi động lại.

---

## Mọi chuyện bắt đầu từ một tin nhắn lúc 11 giờ đêm

> *"Ê, cái lệnh connect vào con DB staging là gì ấy nhỉ? Mình quên rồi"*

Nếu bạn đã từng làm trong một team có hạ tầng AWS, chắc chắn bạn nhận ra tin nhắn này. Và đây là lần thứ... à thôi, mình không đếm nữa.

Câu chuyện luôn diễn ra theo đúng một kịch bản:

1. Database, Redis, mấy con internal service — tất cả nằm gọn trong **private subnet**, không có đường ra internet (đúng như nó nên thế, vì lý do bảo mật).
2. Developer cần chọc vào để debug, để chạy migration, để xem tại sao con query kia chậm.
3. Và thế là ai cũng thuộc lòng câu thần chú:

```bash
ssh -L 5432:db.internal.aws:5432 bastion-host
```

Trông thì gọn gàng đấy. Nhưng sống chung với nó một thời gian thì...

---

## Ba "đặc sản" của SSH tunnel

**Thứ nhất — Nó khá mong manh.**

Wifi giật một cái? Tunnel chết. Laptop ngủ đông? Tunnel chết. Đổi mạng từ nhà sang quán cà phê? Bạn đoán đúng rồi đấy — tunnel chết. Mỗi lần như vậy là một lần phải mở terminal, lục lại lệnh, gõ lại từ đầu.

**Thứ hai — Mạnh ai nấy làm.**

Mỗi người tự cấu hình theo kiểu của mình. Người thì map port 5432, người thì 5433 vì "5432 bị chiếm rồi". Người dùng `~/.ssh/config`, người gõ tay. Đến khi onboard người mới thì y như rằng phải copy-paste một đoạn hướng dẫn dài cả mét, kèm theo câu kinh điển: *"À mà chỗ đó hay lỗi, để mình gọi voice chỉ cho nhanh."*

**Thứ ba — Hoàn toàn mù mịt chuyện ai đang làm gì.**

Không log tập trung. Không ai biết hiện tại có bao nhiêu tunnel đang mở, ai đang nối vào con DB production. Khi cần audit cho security review thì chỉ biết... nhún vai.

**Và còn một điểm nữa, ít ai để ý:** không phải ai trong team cũng là dev rành terminal.

QA, tester, BA, hay mấy bạn mới vào nghề — họ cũng cần chọc vào database để kiểm tra dữ liệu sau khi test, cần connect vào Redis để xem cache, cần mở một con DB tool để query cho nhanh. Nhưng bảo họ tự dựng `ssh -L`, sửa `~/.ssh/config`, rồi xử lý mấy lỗi kiểu "permission denied (publickey)" thì hơi cực cho cả hai bên. Cứ vài hôm lại có một bạn nhắn dev: *"Anh ơi connect giúp em với, em làm hoài không được."* Thế là dev bị ngắt mạch công việc, còn bạn QA thì ngồi chờ — kẹt cả dây chuyền.

Tụi mình muốn một thứ mà **bất kỳ ai cũng dùng được**: mở trang web lên, nhìn thấy danh sách tunnel, lấy host và port, cắm vào con DB tool yêu thích là xong. Không SSH key, không dòng lệnh, không cần hiểu mạng nội bộ hoạt động ra sao.

Tụi mình nhìn nhau và nghĩ: *chắc chắn phải có cách hay hơn chứ.*

---

## Đi tìm lời giải: thử qua vài ngã rẽ

Trước khi đến đích, tụi mình cũng đi lạc vài hướng — kể ra đây để bạn khỏi mất công đi lại.

### Ngã rẽ 1: "Hay là dựng VPN?"

Nghe hợp lý. Nhưng VPN nghĩa là phải quản lý client cho mọi người, phải lo cấp/thu hồi cert, và mỗi lần ai đó kêu *"VPN của em không vào được"* là lại tốn nửa buổi. Hơi nặng so với nhu cầu thực sự của tụi mình: **chỉ là cho dev chọc vào vài cái port nội bộ thôi mà.**

### Ngã rẽ 2: "Vậy viết một con proxy đơn giản?"

Tụi mình thử dựng một proxy TCP tự viết. Nó chạy được! Cho đến khi cần **thêm một tunnel mới** — và phải sửa config rồi **restart cả con proxy**. Mà restart proxy nghĩa là cắt đứt toàn bộ kết nối đang chạy của mọi người. Bạn đang chạy dở một migration 20 phút? Xin chia buồn.

Đến đây tụi mình nhận ra cái mấu chốt thật sự nằm ở đâu:

> **Cái tụi mình cần không phải là một con proxy. Mà là một con proxy biết "thay áo giữa lúc đang chạy" — thêm bớt tunnel mà không bao giờ phải restart.**

### Ngã rẽ 3: Gặp được Envoy

Và rồi tụi mình tìm đến [Envoy](https://www.envoyproxy.io/) — một con proxy vốn sinh ra cho thế giới microservice. Điểm hay của nó là **xDS** (dynamic configuration): bạn có thể đẩy cấu hình mới vào cho Envoy trong lúc nó đang chạy, và nó tự cập nhật — không restart, không reload, không đứt kết nối.

Đúng là mảnh ghép tụi mình tìm mãi.

---

## Giải pháp: TCP Tunnel Manager

Ý tưởng cuối cùng gói gọn trong một câu: **dựng một con Envoy persistent trên bastion, rồi cho phép quản lý tunnel qua một cái UI web — không ai phải đụng đến terminal hay SSH nữa.**

Bức tranh toàn cảnh trông như thế này:

```
┌─────────────────────────────────────┐
│           Central Web UI            │
│  - list tunnels                     │
│  - create / delete                  │
└──────────────┬──────────────────────┘
               │ REST API
┌──────────────▼──────────────────────┐
│      Backend API (on bastion)       │
│  - tunnel registry (SQLite)         │
│  - acts as xDS control plane        │
│  - pushes config to Envoy via gRPC  │
└──────────────┬──────────────────────┘
               │ xDS gRPC
┌──────────────▼──────────────────────┐
│         Envoy (on bastion)          │
│  - dynamically updated              │
│  - no restarts/reloads ever         │
└──────────────┬──────────────────────┘
               │ TCP proxy
       ┌───────┴────────┐
       ▼                ▼
private-db.aws    private-redis.aws
```

Tất cả sống chung trên một con **bastion EC2** có public IP. Developer chỉ cần nối thẳng vào bastion, còn việc luồn lách vào private network thì để Envoy lo.

Và với developer, trải nghiệm thực ra khá "phẳng":

```
Dev machine                    Bastion (public EC2)         Private AWS
┌─────────────────┐           ┌────────────────────┐       ┌──────────────────┐
│                 │           │                    │       │                  │
│ psql -h bastion │──TCP─────►│ Envoy :15432       │──────►│ db.internal.aws  │
│ redis-cli       │──TCP─────►│ Envoy :16379       │──────►│ redis.internal   │
│ any TCP client  │──TCP─────►│ Envoy :1xxxx       │──────►│ any private host │
│                 │           │                    │       │                  │
└─────────────────┘           └────────────────────┘       └──────────────────┘
```

Bạn dùng `psql`, `redis-cli`, `mysql` y như bình thường — cứ tưởng tượng con database đang nằm ngay trên máy mình vậy. Không cần biết gì về cái mê cung mạng nội bộ bên trong.

---

## Bên trong nó có những gì?

Hệ thống được ghép từ ba mảnh, mỗi mảnh làm đúng một việc và làm cho tốt.

### Frontend — Cái UI để mọi người khỏi phải nhớ lệnh

Đây chính là thứ thay thế cho đoạn hướng dẫn dài cả mét ngày xưa. Một web app Next.js, nhẹ nhàng và sáng sủa:

- Liệt kê tất cả tunnel đang có, kèm trạng thái, port, target — nhìn phát biết ngay.
- Tạo tunnel mới chỉ bằng vài cú click.
- Bật/tắt tunnel mà không mất cấu hình (tiện cho lúc muốn "khoá tạm" một đường nào đó).
- Có cả dark mode cho hội cú đêm, và đăng nhập qua OIDC để biết ai là ai.

### Backend — Bộ não, kiêm "control plane"

Phần này là FastAPI, nấp kín bên trong, không thò ra internet. Nhiệm vụ của nó:

- Giữ sổ sách toàn bộ tunnel trong một file **SQLite** nhỏ gọn.
- Mỗi khi có tunnel được tạo/sửa/xoá, nó **viết lại file config YAML** cho Envoy.

Và đây là chỗ thú vị:

```
Có thay đổi tunnel (tạo / sửa / xoá)
        │
        ▼
Backend ghi lại file CDS + LDS YAML
        │
        ▼
Envoy phát hiện file đổi (qua inotify)
        │
        ▼
Envoy tự nạp lại config — không downtime, không ai bị đứt
```

Cái migration 20 phút của bạn? Cứ chạy tiếp, chẳng ai làm phiền đâu.

### Envoy — Người gác cổng

Nhân vật chính của cả câu chuyện. Envoy mở một loạt port trong dải `15000–17000`, mỗi tunnel một port riêng. Mỗi khi backend đẩy config mới vào, nó cập nhật mà không cần khởi động lại lần nào. Đúng tinh thần "thay áo giữa lúc đang chạy" mà tụi mình cần từ đầu.

#### Envoy là gì, và cái config YAML kia trông ra sao?

Nói ngắn gọn, **Envoy** là một con proxy mã nguồn mở do Lyft tạo ra, giờ thuộc CNCF — cùng nhà với Kubernetes. Nó vốn quen thuộc trong thế giới service mesh, nhưng điểm tụi mình quan tâm là khả năng cấu hình động qua **xDS** — viết tắt của "x Discovery Service", với "x" là một họ các API. Trong dự án này tụi mình dùng hai anh em quan trọng nhất:

- **CDS** (*Cluster Discovery Service*) — định nghĩa các **đích đến**, tức là "traffic sẽ được đẩy về đâu". Mỗi cluster ở đây chính là một con database hay service nội bộ.
- **LDS** (*Listener Discovery Service*) — định nghĩa các **cổng lắng nghe**, tức là "Envoy mở port nào để nhận kết nối".

Ghép lại thì một tunnel = một listener (port Envoy mở ra) trỏ tới một cluster (host nội bộ). Khi backend tạo một tunnel tên `postgres_tunnel`, nó chỉ việc viết ra hai mẩu YAML như sau:

```yaml
# lds.yaml — Envoy lắng nghe ở port 15432
resources:
- "@type": type.googleapis.com/envoy.config.listener.v3.Listener
  name: postgres_tunnel
  address:
    socket_address:
      address: 0.0.0.0
      port_value: 15432
  filter_chains:
  - filters:
    - name: envoy.filters.network.tcp_proxy
      typed_config:
        "@type": type.googleapis.com/envoy.extensions.filters.network.tcp_proxy.v3.TcpProxy
        stat_prefix: postgres_tunnel
        cluster: postgres_tunnel        # trỏ sang cluster cùng tên bên dưới
```

```yaml
# cds.yaml — và đẩy traffic về con DB nội bộ trên AWS
resources:
- "@type": type.googleapis.com/envoy.config.cluster.v3.Cluster
  name: postgres_tunnel
  type: LOGICAL_DNS
  dns_lookup_family: V4_ONLY
  connect_timeout: 10s
  load_assignment:
    cluster_name: postgres_tunnel
    endpoints:
    - lb_endpoints:
      - endpoint:
          address:
            socket_address:
              address: my-db.xxxxxxxx.ap-southeast-1.rds.amazonaws.com
              port_value: 5432
```

Hai file đều có chung dạng `resources` — một danh sách mà mỗi phần tử khai báo `@type` để Envoy biết đang đọc Listener hay Cluster. Listener và cluster được nối với nhau qua cái tên chung (`postgres_tunnel`): listener nói "ai gõ vào port `15432` thì đẩy sang cluster `postgres_tunnel`", còn cluster nói "cluster đó chính là con RDS ở `my-db...:5432`". Thêm một tunnel mới đơn giản là thêm một phần tử nữa vào hai danh sách này.

Đẹp ở chỗ: backend chỉ cần **ghi đè hai file rồi save**. Envoy thấy file đổi là tự đọc lại và áp dụng — không cần ai gõ lệnh reload, không cần SSH vào server, và quan trọng nhất là **không làm rớt kết nối nào đang chạy**.

---

## Còn chuyện "mất điện" thì sao?

Một nỗi lo chính đáng: lỡ container restart thì có mất hết không?

Câu trả lời là **không**. Toàn bộ trạng thái — cuốn sổ SQLite lẫn mấy file config của Envoy — đều nằm gọn trong thư mục `./data` được mount ra host:

```
./data/
├── tunnels.db      ← cuốn sổ ghi danh tunnel (SQLite)
├── cds.yaml        ← config cluster của Envoy
└── lds.yaml        ← config listener của Envoy
```

Container có restart thì mọi thứ vẫn còn nguyên. Ngủ ngon.

---

## Nhìn lại

Từ một tin nhắn lúc 11 giờ đêm hỏi "lệnh connect là gì ấy nhỉ", tụi mình đã đi một vòng: chán SSH tunnel → thử VPN (nặng quá) → thử proxy tự viết (restart đau quá) → và cuối cùng dừng lại ở Envoy với xDS.

Kết quả là không ai trong team còn phải nhớ một dòng `ssh -L` nào nữa. Cần tunnel? Mở UI, click một cái, xong. Cần audit xem ai đang nối vào đâu? Cũng chỉ một màn hình. Và quan trọng nhất: **không còn cảnh ai đó bị đứt kết nối chỉ vì người khác vừa thêm một tunnel mới.**

Mà phần tụi mình thích lại không nằm ở chỗ kỹ thuật: giờ một bạn QA hay tester cũng tự lấy được host/port rồi cắm vào DB tool để test, chẳng cần gõ một dòng lệnh hay phiền ai cả. Cái tool nhỏ này, hoá ra, gỡ kẹt cho cả những người không-phải-dev.

Đôi khi giải pháp tốt nhất không phải là viết thêm thật nhiều code, mà là tìm đúng công cụ đã giải quyết phần khó nhất giúp mình rồi.
