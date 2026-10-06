---
title: "SSR vs CSR"
date: 2026-09-11
---

## 1. Định nghĩa cơ bản

- **CSR (Client-Side Rendering):** server trả về HTML gần như rỗng (chỉ có khung, ví dụ `<div id="root"></div>` + thẻ `<script>`). Trình duyệt tải JS về, JS tự gọi API lấy dữ liệu rồi dựng nội dung ngay trong trình duyệt.
- **SSR (Server-Side Rendering):** server tự chạy code, lấy dữ liệu, render sẵn ra HTML đã có đầy đủ nội dung, rồi mới gửi cho trình duyệt. Trình duyệt chỉ việc hiển thị.

## 2. HTML và JavaScript đóng vai trò gì

- **HTML** = cấu trúc/nội dung tĩnh, giống bộ xương của trang.
- **JavaScript** = làm trang "sống" — xử lý sự kiện (click, input), gọi API, sửa lại DOM. Giống cơ bắp + não bộ.

Trình tự trình duyệt tải một trang:

1. Gửi request → server trả về HTML (luôn tới trước).
2. Trình duyệt đọc HTML từ trên xuống, dựng dần cây DOM.
3. Gặp `<link>` (CSS) hay `<script>` (JS) thì tải về (script thường sẽ chặn parse HTML cho tới khi tải + chạy xong).
4. DOM + CSS dựng xong → trình duyệt vẽ (paint) lên màn hình.
5. JS chạy, có thể tiếp tục sửa DOM (thêm tương tác, load thêm dữ liệu...).

Khác biệt cốt lõi giữa SSR/CSR nằm ở bước 1: HTML đó đã có nội dung thật hay chỉ là cái vỏ rỗng.

## 3. Hydration là gì

Với SSR, sau khi HTML (đã có sẵn nội dung) hiển thị xong, React ở client vẫn cần chạy để so khớp (reconcile) cây ảo của nó với HTML tĩnh đó, rồi gắn event listener + khởi tạo state vào đúng chỗ — quá trình này gọi là **hydration**.

Trước khi hydrate xong, giao diện *nhìn* đầy đủ nhưng chưa hoạt động được — đây là lý do đôi khi bấm nút "Thêm vào giỏ hàng" ngay lúc trang vừa load xong lại chưa phản ứng gì trong chốc lát.

## 4. Build time vs Request time

- **Build time**: lúc chạy lệnh build (`next build`). Code được compile (TypeScript/JSX → JavaScript thuần) rồi bundle (gộp module, tree-shaking, code-splitting, minify).
- **SSG (Static Site Generation) / `'use cache'`**: hàm lấy dữ liệu + render được **chạy thật** ngay lúc build, HTML được lưu sẵn thành file tĩnh. Mọi người nhận cùng một bản HTML cho tới lần build lại hoặc revalidate tiếp theo.
- **SSR thật** (`getServerSideProps`, route đánh dấu dynamic): không chạy lúc build — đợi tới khi có request thật mới chạy. Luôn có dữ liệu mới nhất, nhưng tốn thời gian xử lý ở mỗi request.
- **CSR**: build chỉ tạo ra JS bundle + 1 HTML gần như rỗng. Không có bước render nào chạy trước — toàn bộ logic render chỉ thực thi trong trình duyệt của người dùng.

## 5. Cách nhận biết SSR vs CSR trên một trang bất kỳ

- ❌ Tab **Elements** (Inspect) trong F12 — không đáng tin, vì nó luôn hiện DOM *sau khi* JS đã chạy xong, dù trang là CSR hay SSR.
- ✅ **View Page Source** (Ctrl+U, hoặc chuột phải → View Page Source) — hiện đúng HTML thô server gửi, trước khi JS chạy. Có sẵn nội dung → SSR/SSG. Chỉ có div rỗng → CSR.
- ✅ Tab **Network** → request đầu tiên (loại Document) → xem tab Response.
- ✅ Tắt hẳn JavaScript của trình duyệt rồi tải lại trang.
- ✅ Gọi thẳng bằng `curl <url>` (không chạy JS).

## 6. Cache mặc định khi fetch data trong Next.js

Có 2 mô hình tùy có bật `cacheComponents` hay không (flag từ Next.js 16+, gộp lại từ 2 flag thử nghiệm cũ `dynamicIO` + `useCache`):

| | Mô hình cũ (mặc định) | `cacheComponents: true` |
|---|---|---|
| Mặc định | fetch() tự động **được cache** | fetch()/data **dynamic**, không cache |
| Muốn đổi hành vi mặc định | Tắt cache bằng `cache: 'no-store'` hoặc set `revalidate` | Bật cache bằng đánh dấu `'use cache'` (kèm `cacheLife`) |

## 7. Build error vs Runtime error

| | Build error | Runtime error (do logic phụ thuộc dữ liệu) |
|---|---|---|
| Là gì | Phát hiện chỉ bằng đọc code tĩnh: lỗi cú pháp, import sai, sai kiểu TypeScript | Chỉ lộ ra khi code thực sự chạy với dữ liệu cụ thể (vd: `product.name` khi `product` là `undefined`) |
| CRA (CSR thuần) | Có, bắt bình thường như mọi project JS/TS | Không bắt được lúc build (build không chạy component với data thật) — chỉ lộ khi người dùng thật gặp trong trình duyệt |
| Next.js SSG / `'use cache'` | Có, bắt bình thường | Có thể bắt **ngay lúc `next build`**, vì Next.js thực sự chạy render logic với dữ liệu thật để tạo HTML tĩnh |
| Next.js SSR thật / Client Component | Có, bắt bình thường | Vẫn chỉ lộ lúc có request thật (lỗi phía server) hoặc lúc chạy trong trình duyệt (lỗi phía client) |

## 8. Vì sao SEO hay được nhắc tới khi so sánh SSR/CSR

Bot của công cụ tìm kiếm (và bot lấy preview link) đọc HTML thô — về bản chất giống hệt thao tác "View Source" ở mục 5. Nhiều bot **không chạy được JavaScript**:

- CSR: HTML thô gần như rỗng → bot không thấy nội dung → khó index, ảnh hưởng SEO.
- SSR/SSG: nội dung có sẵn trong HTML thô → bot nào cũng đọc được ngay, không phụ thuộc JS có chạy được hay không.

Googlebot hiện đại có chạy được JS (dùng trình duyệt headless), nhưng việc này tốn tài nguyên hơn nên thường index CSR chậm hơn (index theo 2 đợt). SSR cũng thường hiển thị nội dung nhanh hơn (tốt cho Core Web Vitals), gián tiếp lợi thêm cho SEO.

## 9. Bảng tổng kết

| Tiêu chí | SSR / SSG | CSR |
|---|---|---|
| HTML ban đầu | Có sẵn nội dung | Gần như rỗng |
| Tốc độ thấy nội dung lần đầu | Nhanh | Chậm hơn (chờ JS tải + fetch data) |
| SEO | Tốt, mọi bot đọc được | Phụ thuộc bot có chạy JS hay không |
| Bắt lỗi runtime-logic sớm | SSG/`use cache`: có thể bắt lúc build | Không — chỉ lộ ở trình duyệt người dùng |
| Dữ liệu luôn mới nhất | SSR thật: có (render lại mỗi request); SSG: không (cache tới khi revalidate) | Có (fetch ngay lúc trang chạy) |
| Tải server mỗi request | SSR thật: cao hơn (phải render mỗi lần) | Thấp hơn (server chỉ trả file tĩnh + JS bundle) |

## Tham khảo

- [next.config.js: cacheComponents | Next.js](https://nextjs.org/docs/app/api-reference/config/next-config-js/cacheComponents)
- [Getting Started: Caching | Next.js](https://nextjs.org/docs/app/getting-started/caching)
