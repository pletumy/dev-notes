# Semantic Versioning (SemVer)

> Tham khảo: [video giải thích Semantic Versioning](https://www.youtube.com/watch?v=33CwoRO6-GE&list=PLoaAbmGPgTSPSuyBWGJ9PfatrBvUTeMPL&index=5)

Một version theo chuẩn SemVer có dạng `MAJOR.MINOR.PATCH`, ví dụ `4.17.1`:

![Ví dụ version patch/minor/major](./images/Screenshot%202026-09-27%20at%2018.28.43.png)

- **Patch** (`4.17.1` → `4.17.2`): tăng lên mỗi lần release sau khi fix được bug, không thêm tính năng mới.
- **Minor** (`4.17.x` → `4.18.0`): release feature mới nhưng **không** thay đổi API hiện tại, không phá vỡ (break) functionality đang có.
- **Major** (`4.x.x` → thay đổi version đầu): release feature mới làm thay đổi cả API lẫn functionality của app. Ví dụ: thay đổi trên endpoint (bổ sung thêm tham số bắt buộc...) khiến các app phụ thuộc vào nó phải cập nhật code nhiều hơn khi nâng cấp lên version này.

## Ký hiệu range trong package.json

![Ký hiệu ^ và ~](./images/Screenshot%202026-09-27%20at%2018.41.57.png)

- **`^` (caret)**: giữ nguyên MAJOR, cho phép tự động cập nhật lên MINOR + PATCH cao nhất/mới nhất.
- **`~` (tilde)**: chỉ cho phép tự động cập nhật PATCH.

## Nên dùng cách nào?

- Nếu app đã chạy ổn định, nên **fix cứng version** (không dùng `^`/`~`) để tránh rủi ro.
- Nếu để tự động cập nhật minor/patch, có thể vô tình kéo theo bug mới từ các bản release sau — cần cân nhắc đánh đổi giữa việc tự động nhận bản vá và rủi ro phát sinh lỗi không lường trước.
