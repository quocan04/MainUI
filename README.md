# 📚 Library Management System

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![MySQL](https://img.shields.io/badge/MySQL-8.0+-orange.svg)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)

**Hệ thống quản lý thư viện với Python GUI - Module Quản lý Bạn đọc**

[Tính năng](#-tính-năng) • [Cài đặt](#-cài-đặt) • [Sử dụng](#-sử-dụng) • [Demo](#-demo) • [Đóng góp](#-đóng-góp)

</div>

---

## 📋 Mục lục

- [Giới thiệu](#-giới-thiệu)
- [Tính năng](#-tính-năng)
- [Công nghệ](#-công-nghệ-sử-dụng)
- [Yêu cầu hệ thống](#-yêu-cầu-hệ-thống)
- [Cài đặt](#-cài-đặt)
- [Cấu hình](#️-cấu-hình)
- [Sử dụng](#-sử-dụng)
- [Cấu trúc dự án](#-cấu-trúc-dự-án)
- [Database Schema](#-database-schema)
- [Screenshots](#-screenshots)
- [API Documentation](#-api-documentation)
- [Troubleshooting](#-troubleshooting)
- [Roadmap](#-roadmap)
- [Đóng góp](#-đóng-góp)
- [License](#-license)
- [Tác giả](#-tác-giả)

---

## 🎯 Giới thiệu

**Library Management System** là một ứng dụng desktop được phát triển bằng Python, sử dụng Tkinter cho giao diện đồ họa và MySQL làm cơ sở dữ liệu. Dự án hiện tại tập trung vào **module Quản lý Bạn đọc (Reader Management)** với đầy đủ các tính năng CRUD, tìm kiếm, lọc, thống kê và xuất dữ liệu.

### 🌟 Điểm nổi bật

- ✅ **Kiến trúc MVC** chuẩn, dễ mở rộng
- ✅ **OOP** đầy đủ, code sạch và có tổ chức
- ✅ **MySQL Connection Pooling** tối ưu hiệu suất
- ✅ **Validation** dữ liệu đầu vào chi tiết
- ✅ **Exception Handling** toàn diện
- ✅ **Logging** system hoàn chỉnh
- ✅ **Export** đa định dạng (JSON, CSV, Excel, PDF)
- ✅ **UI/UX** thân thiện, dễ sử dụng

---

## ✨ Tính năng

### 📌 Quản lý Bạn đọc (Hoàn thành 100%)

#### CRUD Operations
- ➕ **Thêm** bạn đọc mới với validation đầy đủ
- ✏️ **Sửa** thông tin bạn đọc
- 🗑️ **Xóa** bạn đọc (kiểm tra ràng buộc)
- 👁️ **Xem** chi tiết thông tin

#### Tìm kiếm & Lọc
- 🔍 **Tìm kiếm** theo nhiều tiêu chí: 
  - Họ tên
  - Số điện thoại
  - Email
  - Địa chỉ
  - Tất cả (tìm kiếm toàn văn)
- 🔎 **Lọc** theo:
  - Trạng thái (Active/Expired/Locked)
  - Điểm uy tín (từ X đến Y)
  - Thẻ sắp hết hạn (30 ngày)

#### Quản lý Trạng thái
- 🔒 **Khóa/Mở khóa** bạn đọc
- 📅 **Gia hạn thẻ** linh hoạt
- 🔄 **Auto-update** trạng thái hết hạn
- ⚠️ **Cảnh báo** thẻ sắp hết hạn

#### Thống kê & Báo cáo
- 📊 **Dashboard** tổng quan
- 📈 **Thống kê** theo:
  - Tổng số bạn đọc
  - Phân loại trạng thái
  - Điểm uy tín trung bình
  - Thẻ sắp hết hạn
- 📉 **Biểu đồ** trực quan

#### Xuất dữ liệu
- 📄 **JSON** - Dữ liệu có cấu trúc
- 📊 **CSV** - Import vào Excel
- 📗 **Excel (. xlsx)** - Báo cáo đẹp với định dạng
- 📕 **PDF** - In ấn và lưu trữ

#### UI/UX Features
- ⌨️ **Keyboard shortcuts** đầy đủ
- 🖱️ **Context menu** (chuột phải)
- 🔄 **Auto-refresh** thông minh
- 🎨 **Color coding** theo trạng thái
- 📱 **Responsive** layout
- ⚡ **Fast search** (debounced)

### 🚧 Modules khác (Đang phát triển)

- 📚 Quản lý Sách (Books)
- 📋 Mượn/Trả sách (Borrow/Return)
- 💰 Quản lý Phạt (Penalties)
- 👥 Quản lý Nhân viên (Staff)
- 📊 Báo cáo tổng hợp

---

## 🛠️ Công nghệ sử dụng

### Backend
- **Python** 3.8+
- **MySQL** 8.0+ (với Connection Pooling)
- **mysql-connector-python** 8.2.0

### Frontend
- **Tkinter** (GUI Framework)
- **ttk** (Themed widgets)

### Libraries
- **openpyxl** - Excel export
- **reportlab** - PDF export
- **python-dotenv** - Environment variables

### Architecture
- **MVC Pattern** (Model-View-Controller)
- **OOP** (Object-Oriented Programming)
- **Service Layer** pattern

### Database
- **MySQL** 8.0+
- **Connection Pooling**
- **Prepared Statements** (SQL Injection prevention)

---

## 💻 Yêu cầu hệ thống

### Phần mềm
- **Python** 3.8 hoặc cao hơn
- **MySQL** 8.0 hoặc cao hơn
- **pip** (Python package manager)

### Hệ điều hành
- ✅ Windows 10/11
- ✅ macOS 10.14+
- ✅ Linux (Ubuntu 20.04+, Fedora 35+)

### Phần cứng (khuyến nghị)
- **CPU:** 2 cores trở lên
- **RAM:** 4GB trở lên
- **Disk:** 100MB trống (cho ứng dụng + data)

---

## 🚀 Cài đặt

### Bước 1: Clone Repository

```bash
git clone https://github.com/NvkhoaDev54/library-management.git
cd library-management
```

### Bước 2: Tạo Virtual Environment

```bash
# Tạo virtual environment
python -m venv venv

# Kích hoạt virtual environment

# Windows (Command Prompt)
venv\Scripts\activate

# Windows (PowerShell)
venv\Scripts\Activate. ps1

# macOS/Linux
source venv/bin/activate
```

### Bước 3: Cài đặt Dependencies

```bash
pip install -r requirements.txt
```

**requirements.txt:**
```txt
mysql-connector-python==8.2.0
openpyxl==3.1.2
reportlab==4.0.7
python-dotenv==1.0.0
```

### Bước 4: Cài đặt MySQL

#### Windows
1. Download [MySQL Community Server](https://dev.mysql.com/downloads/mysql/)
2. Chạy installer và làm theo hướng dẫn
3. Ghi nhớ **root password**

#### macOS (Homebrew)
```bash
brew install mysql
brew services start mysql
mysql_secure_installation
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install mysql-server
sudo systemctl start mysql
sudo mysql_secure_installation
```

### Bước 5: Tạo Database

```bash
# Đăng nhập MySQL
mysql -u root -p

# Hoặc chạy file SQL trực tiếp
mysql -u root -p < library_management.sql
```

**Hoặc trong MySQL shell:**
```sql
source library_management.sql;
```

### Bước 6: Cấu hình Database

Tạo file `.env` trong thư mục gốc:

```bash
# Copy từ template
cp .env.example .env

# Chỉnh sửa file . env
nano .env  # hoặc notepad .env (Windows)
```

**Nội dung `.env`:**
```env
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password_here
DB_NAME=library_management

APP_NAME=Library Management System
APP_VERSION=1.0.0
DEBUG=True
```

> ⚠️ **Lưu ý:** Thay `your_password_here` bằng password MySQL của bạn

### Bước 7: Chạy ứng dụng

```bash
python main.py
```

---

## ⚙️ Cấu hình

### Cấu hình Database (config/settings.py)

```python
class DatabaseConfig:
    HOST = '127.0.0.1'
    PORT = 3306
    USER = 'root'
    PASSWORD = 'your_password'
    DATABASE = 'library_management'
    
    # Connection Pool
    POOL_SIZE = 10
    POOL_NAME = 'library_pool'
```

### Cấu hình Application

```python
class AppConfig:
    APP_NAME = 'Library Management System'
    VERSION = '1.0.0'
    DEBUG = True
    
    # Thư mục
    EXPORT_DIR = 'data/export'
    TEMP_DIR = 'data/temp'
    
    # Settings
    DEFAULT_CARD_VALIDITY_DAYS = 365
    MAX_SEARCH_RESULTS = 1000
```

---

## 📖 Sử dụng

### Khởi động

```bash
python main.py
```

### Giao diện chính

Sau khi khởi động, bạn sẽ thấy: 
- **Header:** Logo và thông tin phiên bản
- **Menu bar:** File, Quản lý, Báo cáo, Công cụ, Trợ giúp
- **Tabs:** Quản lý Bạn đọc, Sách, Mượn/Trả... 
- **Status bar:** Trạng thái kết nối, thời gian

### Quản lý Bạn đọc

#### Thêm mới
1. Click nút **"➕ Thêm mới"**
2. Điền thông tin: 
   - Họ tên (bắt buộc)
   - Số điện thoại
   - Email
   - Địa chỉ
   - Ngày cấp thẻ / Ngày hết hạn
   - Trạng thái
   - Điểm uy tín
3. Click **"💾 Lưu"**

#### Sửa
1. Double-click vào dòng cần sửa
2. Hoặc chọn dòng → Click **"✏️ Sửa"**
3. Chỉnh sửa thông tin
4. Click **"💾 Lưu"**

#### Xóa
1. Chọn dòng cần xóa
2. Nhấn **Delete** hoặc Click **"🗑️ Xóa"**
3. Xác nhận xóa

#### Tìm kiếm
1. Nhập từ khóa vào ô tìm kiếm
2. Chọn tiêu chí:  Tất cả / Họ tên / SĐT / Email / Địa chỉ
3. Nhấn **Enter** hoặc click **"🔍 Tìm"**

#### Lọc
1. Chọn trạng thái: Active / Expired / Locked
2. Đặt khoảng điểm uy tín:  Từ X đến Y
3. Check "Sắp hết hạn (30 ngày)" nếu cần
4. Click **"🔎 Lọc"**

#### Xuất dữ liệu
1. Click nút xuất:  **JSON / CSV / Excel / PDF**
2. File sẽ được lưu vào `data/export/`
3. Thông báo hiển thị đường dẫn file

### Phím tắt

| Phím | Chức năng |
|------|-----------|
| `F5` | Làm mới dữ liệu |
| `Ctrl+Q` | Thoát ứng dụng |
| `Ctrl+1` | Tab Bạn đọc |
| `Ctrl+2` | Tab Sách |
| `Ctrl+3` | Tab Mượn/Trả |
| `Delete` | Xóa dòng được chọn |
| `Enter` | Lưu (trong dialog) |
| `Esc` | Hủy (trong dialog) |

### Context Menu (Chuột phải)

- ✏️ Sửa
- 🗑️ Xóa
- 🔒 Khóa
- 🔓 Mở khóa
- 📅 Gia hạn thẻ
- ℹ️ Chi tiết

---

## 📂 Cấu trúc dự án

```
library_management/
│
├── main.py                     # Entry point
├── requirements.txt            # Dependencies
├── . env                        # Config (không commit)
├── .env.example                # Config template
├── . gitignore                  # Git ignore rules
├── README.md                   # Documentation
├── library_management.sql      # Database schema
│
├── config/                     # Configuration
│   ├── __init__.py
│   ├── database.py            # MySQL connection pool
│   └── settings.py            # App settings
│
├── models/                     # Data Models
│   ├── __init__.py
│   └── reader.py              # Reader model
│
├── controllers/                # Controllers
│   ├── __init__.py
│   └── reader_controller.py   # Reader controller
│
├── views/                      # GUI Views
│   ├── __init__.py
│   ├── main_window.py         # Main window
│   ├── reader_view.py         # Reader management view
│   └── reader_dialog.py       # Add/Edit dialog
│
├── services/                   # Business Logic
│   ├── __init__.py
│   └── reader_service.py      # Reader service
│
├── utils/                      # Utilities
│   ├── __init__.py
│   ├── validators.py          # Input validation
│   ├── messagebox_helper.py   # Message boxes
│   └── export_helper.py       # Export functions
│
├── data/                       # Data directory
│   ├── . gitkeep
│   ├── library. db             # SQLite (optional)
│   ├── export/                # Exported files
│   │   └── . gitkeep
│   └── temp/                  # Temporary files
│       └── .gitkeep
│
└── logs/                       # Log files
    ├── . gitkeep
    └── app.log                # Application log
```

---

## 🗄️ Database Schema

### Table: `readers`

```sql
CREATE TABLE readers (
    reader_id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(150) NOT NULL,
    address VARCHAR(255),
    phone VARCHAR(20),
    email VARCHAR(100),
    card_start DATE,
    card_end DATE,
    status ENUM('ACTIVE','EXPIRED','LOCKED') DEFAULT 'ACTIVE',
    reputation_score INT DEFAULT 100
);
```

### Ràng buộc & Indexes

```sql
-- Index cho tìm kiếm nhanh
CREATE INDEX idx_full_name ON readers(full_name);
CREATE INDEX idx_phone ON readers(phone);
CREATE INDEX idx_email ON readers(email);
CREATE INDEX idx_status ON readers(status);
CREATE INDEX idx_card_end ON readers(card_end);

-- Index composite
CREATE INDEX idx_status_card ON readers(status, card_end);
```

### Relationships

```
readers (1) ----< (N) borrow_slips
readers (1) ----< (N) penalties
```

---

## 📸 Screenshots

### Giao diện chính
![Main Window](screenshots/main_window.png)

### Quản lý Bạn đọc
![Reader Management](screenshots/reader_management. png)

### Dialog thêm/sửa
![Add/Edit Dialog](screenshots/dialog. png)

### Thống kê
![Statistics](screenshots/statistics.png)

### Xuất PDF
![PDF Export](screenshots/pdf_export.png)

> 💡 **Lưu ý:** Screenshots sẽ được thêm vào sau

---

## 📚 API Documentation

### ReaderService

#### `create_reader(reader:  Reader) -> Tuple[bool, Optional[str], Optional[int]]`
Thêm bạn đọc mới vào database. 

**Parameters:**
- `reader` (Reader): Object chứa thông tin bạn đọc

**Returns:**
- `Tuple[bool, Optional[str], Optional[int]]`: (success, error_message, reader_id)

**Example:**
```python
reader = Reader(
    full_name="Nguyễn Văn A",
    phone="0901234567",
    email="nguyenvana@example.com",
    card_start="2025-01-01",
    card_end="2026-01-01",
    status="ACTIVE",
    reputation_score=100
)

success, error, reader_id = service.create_reader(reader)
if success:
    print(f"Created reader with ID: {reader_id}")
```

#### `get_all_readers() -> List[Reader]`
Lấy danh sách tất cả bạn đọc.

**Returns:**
- `List[Reader]`: Danh sách bạn đọc

#### `search_readers(keyword: str, search_by: str) -> List[Reader]`
Tìm kiếm bạn đọc theo từ khóa.

**Parameters:**
- `keyword` (str): Từ khóa tìm kiếm
- `search_by` (str): Tiêu chí ('all', 'name', 'phone', 'email', 'address')

**Returns:**
- `List[Reader]`: Danh sách kết quả

---

## 🐛 Troubleshooting

### Lỗi kết nối MySQL

```
Error 1045 (28000): Access denied for user 'xxx'@'localhost'
```

**Giải pháp:**
1. Kiểm tra username/password trong `.env`
2. Tạo user và cấp quyền: 
```sql
CREATE USER 'username'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON library_management.* TO 'username'@'localhost';
FLUSH PRIVILEGES;
```

### Lỗi thiếu thư viện

```
ModuleNotFoundError: No module named 'mysql'
```

**Giải pháp:**
```bash
pip install -r requirements.txt
```

### Lỗi port MySQL

```
Error 2003 (HY000): Can't connect to MySQL server on '127.0.0.1:3306'
```

**Giải pháp:**
1. Kiểm tra MySQL đang chạy: 
```bash
# Windows
sc query MySQL80

# macOS/Linux
sudo systemctl status mysql
```

2. Kiểm tra port trong `.env` (3306 hoặc 3307)

### Lỗi encoding UTF-8

**Giải pháp:**
Đảm bảo tất cả file Python có encoding UTF-8:
```python
# -*- coding: utf-8 -*-
```

### Ứng dụng không mở

**Giải pháp:**
1. Kiểm tra log:  `logs/app.log`
2. Chạy với debug mode: 
```bash
python -u main.py
```

---

## 🗺️ Roadmap

### Version 1.1.0 (Q1 2025)
- [ ] Module Quản lý Sách
- [ ] Module Mượn/Trả sách
- [ ] Tích hợp Barcode scanner

### Version 1.2.0 (Q2 2025)
- [ ] Module Quản lý Nhân viên
- [ ] Hệ thống đăng nhập
- [ ] Phân quyền người dùng (Roles)

### Version 1.3.0 (Q3 2025)
- [ ] Module Phạt và Thanh toán
- [ ] In thẻ bạn đọc
- [ ] Email notifications

### Version 2.0.0 (Q4 2025)
- [ ] Web version (Flask/Django)
- [ ] Mobile app (React Native)
- [ ] REST API

---

## 🤝 Đóng góp

Mọi đóng góp đều được hoan nghênh!  Hãy làm theo các bước sau:

### Cách đóng góp

1. **Fork** repository
2. **Clone** về máy local: 
```bash
git clone https://github.com/your-username/library-management.git
```

3. **Tạo branch** mới: 
```bash
git checkout -b feature/amazing-feature
```

4. **Commit** changes:
```bash
git commit -m "Add some amazing feature"
```

5. **Push** lên branch:
```bash
git push origin feature/amazing-feature
```

6. Mở **Pull Request**

### Coding Standards

- Tuân thủ **PEP 8** Python style guide
- Viết **docstrings** cho functions/classes
- Thêm **type hints** khi có thể
- Viết **unit tests** cho code mới
- Cập nhật **README** nếu cần

### Bug Reports

Nếu phát hiện bug, hãy [tạo Issue](https://github.com/NvkhoaDev54/library-management/issues) với: 
- Mô tả chi tiết bug
- Các bước tái hiện
- Expected vs Actual behavior
- Screenshots (nếu có)
- Environment (OS, Python version, MySQL version)

---

## 📄 License

Dự án này được phân phối dưới giấy phép **MIT License**.

```
MIT License

Copyright (c) 2025 NvkhoaDev54

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software. 

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

Chi tiết:  [LICENSE](LICENSE)

---

## 👨‍💻 Tác giả

**NvkhoaDev54**

- GitHub: [@NvkhoaDev54](https://github.com/NvkhoaDev54)
- Email: nvkhoadev54@example.com
- LinkedIn: [Your LinkedIn](https://linkedin.com/in/yourprofile)

---

## 🙏 Cảm ơn

- [Python Software Foundation](https://www.python.org/)
- [MySQL](https://www.mysql.com/)
- [Tkinter Documentation](https://docs.python.org/3/library/tkinter. html)
- [ReportLab](https://www.reportlab.com/)
- [OpenPyXL](https://openpyxl.readthedocs.io/)

---

## 📞 Liên hệ & Hỗ trợ

Nếu bạn cần hỗ trợ hoặc có câu hỏi: 

- 📧 Email: nvkhoadev54@example.com
- 💬 Discord: [Join our server](https://discord.gg/yourserver)
- 🐛 Issues: [GitHub Issues](https://github.com/NvkhoaDev54/library-management/issues)
- 📖 Wiki: [Project Wiki](https://github.com/NvkhoaDev54/library-management/wiki)

---

## ⭐ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=NvkhoaDev54/library-management&type=Date)](https://star-history.com/#NvkhoaDev54/library-management&Date)

---

<div align="center">

**Nếu thấy project hữu ích, hãy cho một ⭐ nhé! **

Made with ❤️ by [NvkhoaDev54](https://github.com/NvkhoaDev54)

</div>