# DỰ ÁN MÔ PHỎNG BIẾN ĐỘNG GIÁ CỔ PHIẾU ABC
## 1. Giới thiệu dự án
Dự án xây dựng chương trình mô phỏng và phân tích biến động giá cổ phiếu ABC bằng ngôn ngữ Python.
Dự án sử dụng dữ liệu giá cổ phiếu để thực hiện thống kê, trực quan hóa và mô phỏng diễn biến giá theo thời gian.
## 2. Cấu trúc thư mục
- `data/`: Chứa dữ liệu đầu vào phục vụ mô phỏng.
- `out/`: Chứa video mô phỏng `abc.mp4` và các hình ảnh kết quả.
- `report/`: Chứa các tài liệu báo cáo liên quan.
- `animate.py`: Xây dựng hoạt ảnh mô phỏng biến động giá.
- `charts.py`: Xây dựng các biểu đồ trực quan hóa.
- `chay.py`: Chứa chương trình chạy các chức năng.
- `data_service.py`: Xử lý dữ liệu đầu vào.
- `latex_export.py`: Hỗ trợ xuất nội dung sang LaTeX.
- `main.py`: Chương trình chính.
- `thu.py`: Chứa các chức năng thử nghiệm.
- `index.html`: Giao diện trang web.
- `requirements.txt`: Danh sách thư viện Python cần thiết.
## 3. Công nghệ sử dụng
- Python
- NumPy
- Pandas
- Matplotlib
- FastAPI
- Uvicorn
- Jinja2
## 4. Cài đặt thư viện
Mở Terminal tại thư mục dự án và chạy:

```bash
pip install -r requirements.txt
```

## 5. Sản phẩm đầu ra
- Video mô phỏng biến động giá cổ phiếu ABC: `out/abc.mp4`.
- Các hình ảnh biểu đồ và kết quả phân tích.
- Báo cáo phân tích dữ liệu.
## 6. Hướng dẫn sử dụng
Mở dự án bằng Visual Studio Code, cài đặt các thư viện cần thiết và chạy chương trình theo hướng dẫn trong mã nguồn.
## 7. Kết luận
Dự án giúp minh họa quá trình phân tích và mô phỏng biến động giá cổ phiếu bằng Python, đồng thời ứng dụng các kỹ thuật xử lý dữ liệu và trực quan hóa dữ liệu.