# Database vs Data Lake vs Data Warehouse

## Database

- Theo mô hình **OLTP** (Online Transaction Processing).
- Dữ liệu được đọc/ghi và thay đổi theo thời gian thực.

## Data Lake

- Theo mô hình **OLAP** (Online Analytical Processing) — hỗ trợ việc viết các câu query phức tạp trên tập dữ liệu quá khứ.
- Dữ liệu lưu trong data lake về cơ bản giống dữ liệu gốc trong database (thường ở dạng thô, chưa qua xử lý nhiều).

## Data Warehouse

- Cũng theo mô hình **OLAP**.

### Data Mart

- Mỗi data warehouse có thể chứa nhiều **data mart** khác nhau — mỗi data mart phục vụ một nhóm nghiệp vụ/phòng ban cụ thể (ví dụ: marketing, tài chính...).

## Vai trò các nhân sự liên quan

- **Data Engineer**: xây dựng các **data pipeline** để ingest dữ liệu từ database sang data lake, và xử lý (process) dữ liệu từ data lake sang data warehouse.
- **Data Analyst**: xử lý số liệu ở data lake và data warehouse. Đây thường là người hiểu rõ nghiệp vụ (business) nhất, biết cần dùng số liệu nào để tạo ra báo cáo, có thể tự viết SQL để xử lý dữ liệu đơn giản. Với các trường hợp cần xử lý dữ liệu phức tạp hơn, họ sẽ phối hợp với Data Engineer — Data Engineer sẽ dựa theo nhu cầu của Data Analyst để xây dựng pipeline phù hợp.
- **Data Scientist**: sử dụng nhiều loại dữ liệu khác nhau, thử nghiệm để tìm ra dữ liệu phù hợp phục vụ việc xây dựng mô hình (model).
