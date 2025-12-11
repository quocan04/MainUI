import tkinter as tk
from tkinter import ttk, messagebox
import sys
import logging

from config.database import db
from config.settings import AppConfig
from views.reader_view import ReaderView

logger = logging.getLogger(__name__)


class MainWindow(tk.Tk):
    """Cửa sổ chính của ứng dụng"""

    def __init__(self):
        super().__init__()

        self.title(f"{AppConfig.APP_NAME} v{AppConfig.VERSION}")
        self.geometry("1400x800")
        self.minsize(1200, 600)

        # Set icon (nếu có)
        # self.iconbitmap('icon.ico')

        # Test database connection
        if not self._test_database():
            messagebox.showerror(
                "❌ Lỗi kết nối Database",
                "Không thể kết nối đến MySQL database!\n\n"
                "Vui lòng kiểm tra:\n"
                "1. MySQL server đang chạy\n"
                "2. Database 'library_management' đã được tạo\n"
                "3. Thông tin kết nối trong file . env hoặc config/settings.py\n"
                "4. Tài khoản có quyền truy cập database",
                icon='error'
            )
            self.destroy()
            sys.exit(1)

        # Configure style
        self._configure_style()

        # Create widgets
        self._create_menu()
        self._create_widgets()

        # Center window
        self._center_window()

        # Bind close event
        self.protocol("WM_DELETE_WINDOW", self._on_closing)

    def _test_database(self) -> bool:
        """Test kết nối database"""
        try:
            return db.test_connection()
        except Exception as e:
            logger.error(f"Database connection failed: {e}")
            return False

    def _configure_style(self):
        """Cấu hình style cho ứng dụng"""
        style = ttk.Style()

        # Theme
        available_themes = style.theme_names()
        if 'clam' in available_themes:
            style.theme_use('clam')
        elif 'alt' in available_themes:
            style.theme_use('alt')

        # Custom colors
        style.configure('TLabel', font=('Arial', 10))
        style.configure('TButton', font=('Arial', 9))
        style.configure('Header.TLabel', font=('Arial', 12, 'bold'))

    def _create_menu(self):
        """Tạo menu bar"""
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="📁 File", menu=file_menu)
        file_menu.add_command(label="🔄 Làm mới", command=self._refresh_all, accelerator="F5")
        file_menu.add_separator()
        file_menu.add_command(label="🚪 Thoát", command=self._on_closing, accelerator="Ctrl+Q")

        # Quản lý menu
        manage_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="📚 Quản lý", menu=manage_menu)
        manage_menu.add_command(label="👥 Bạn đọc", command=lambda: self._show_tab(0), accelerator="Ctrl+1")
        manage_menu.add_separator()
        manage_menu.add_command(label="📚 Sách", state='disabled', accelerator="Ctrl+2")
        manage_menu.add_command(label="📋 Mượn/Trả", state='disabled', accelerator="Ctrl+3")
        manage_menu.add_command(label="💰 Phạt", state='disabled', accelerator="Ctrl+4")

        # Báo cáo menu
        report_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="📊 Báo cáo", menu=report_menu)
        report_menu.add_command(label="📈 Thống kê tổng quan", state='disabled')
        report_menu.add_command(label="📊 Báo cáo bạn đọc", state='disabled')
        report_menu.add_command(label="📊 Báo cáo mượn/trả", state='disabled')

        # Công cụ menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="🔧 Công cụ", menu=tools_menu)
        tools_menu.add_command(label="⚙️ Cài đặt", state='disabled')
        tools_menu.add_command(label="🗄️ Sao lưu dữ liệu", state='disabled')
        tools_menu.add_command(label="♻️ Khôi phục dữ liệu", state='disabled')

        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="❓ Trợ giúp", menu=help_menu)
        help_menu.add_command(label="📖 Hướng dẫn sử dụng", command=self._show_help)
        help_menu.add_separator()
        help_menu.add_command(label="ℹ️ Giới thiệu", command=self._show_about)

        # Keyboard shortcuts
        self.bind('<F5>', lambda e: self._refresh_all())
        self.bind('<Control-q>', lambda e: self._on_closing())
        self.bind('<Control-1>', lambda e: self._show_tab(0))

    def _create_widgets(self):
        """Tạo giao diện"""
        # Header
        header = ttk.Frame(self, relief='raised', borderwidth=2)
        header.pack(fill='x', side='top')

        header_content = ttk.Frame(header, padding=10)
        header_content.pack(fill='x')

        ttk.Label(
            header_content,
            text=f"📚 {AppConfig.APP_NAME}",
            font=('Arial', 18, 'bold'),
            foreground='#1976D2'
        ).pack(side='left')

        ttk.Label(
            header_content,
            text=f"v{AppConfig.VERSION}",
            font=('Arial', 10),
            foreground='#666'
        ).pack(side='left', padx=(10, 0))

        # Connection status
        status_indicator = ttk.Label(
            header_content,
            text="🟢 Connected to MySQL",
            font=('Arial', 9),
            foreground='#4CAF50'
        )
        status_indicator.pack(side='right')

        # Main container
        main_frame = ttk.Frame(self)
        main_frame.pack(fill='both', expand=True)

        # Notebook (tabs)
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill='both', expand=True, padx=5, pady=5)

        # Tab Bạn đọc
        reader_frame = ReaderView(self.notebook)
        self.notebook.add(reader_frame, text="👥 Quản lý Bạn đọc")

        # Placeholder tabs
        self._add_placeholder_tab("📚 Quản lý Sách")
        self._add_placeholder_tab("📋 Mượn/Trả sách")
        self._add_placeholder_tab("💰 Quản lý Phạt")
        self._add_placeholder_tab("📊 Thống kê & Báo cáo")

        # Status bar
        status_bar = ttk.Frame(self, relief='sunken', borderwidth=1)
        status_bar.pack(side='bottom', fill='x')

        self.status_label = ttk.Label(
            status_bar,
            text=f"  Sẵn sàng  |  {AppConfig.APP_NAME} v{AppConfig.VERSION}  |  MySQL Connected  ",
            font=('Arial', 9)
        )
        self.status_label.pack(side='left', fill='x', expand=True, pady=2)

        # Clock
        self.clock_label = ttk.Label(status_bar, font=('Arial', 9))
        self.clock_label.pack(side='right', padx=10)
        self._update_clock()

    def _add_placeholder_tab(self, title):
        """Thêm tab placeholder"""
        frame = ttk.Frame(self.notebook)

        content = ttk.Frame(frame)
        content.place(relx=0.5, rely=0.5, anchor='center')

        ttk.Label(
            content,
            text=f"🚧 {title}",
            font=('Arial', 20, 'bold'),
            foreground='#999'
        ).pack()

        ttk.Label(
            content,
            text="Chức năng đang được phát triển",
            font=('Arial', 12),
            foreground='#666'
        ).pack(pady=10)

        self.notebook.add(frame, text=title)

    def _show_tab(self, index: int):
        """Chuyển đến tab"""
        try:
            self.notebook.select(index)
        except:
            pass

    def _refresh_all(self):
        """Làm mới toàn bộ"""
        current_tab = self.notebook.select()
        current_widget = self.notebook.nametowidget(current_tab)

        if hasattr(current_widget, '_load_data'):
            current_widget._load_data()
            self.status_label.config(text="✅ Đã làm mới dữ liệu")

    def _update_clock(self):
        """Cập nhật đồng hồ"""
        from datetime import datetime
        now = datetime.now().strftime("%H:%M:%S - %d/%m/%Y")
        self.clock_label.config(text=f"🕐 {now}")
        self.after(1000, self._update_clock)

    def _center_window(self):
        """Center cửa sổ trên màn hình"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def _show_help(self):
        """Hiển thị trợ giúp"""
        help_text = """
🔹 HƯỚNG DẪN SỬ DỤNG

📋 Quản lý Bạn đọc:
• Thêm mới:  Click nút "➕ Thêm mới" hoặc Ctrl+N
• Sửa:  Double-click vào dòng hoặc click "✏️ Sửa"
• Xóa:  Chọn dòng và nhấn Delete hoặc click "🗑️ Xóa"
• Tìm kiếm: Gõ từ khóa vào ô tìm kiếm
• Lọc: Sử dụng các bộ lọc theo trạng thái, điểm uy tín

📤 Xuất dữ liệu: 
• JSON: Dữ liệu có cấu trúc
• CSV: Import vào Excel
• Excel:  Báo cáo đẹp với định dạng
• PDF: In ấn và lưu trữ

⌨️ Phím tắt:
• F5: Làm mới
• Ctrl+Q: Thoát
• Ctrl+1/2/3: Chuyển tab
• Delete: Xóa dòng được chọn
        """

        dialog = tk.Toplevel(self)
        dialog.title("📖 Hướng dẫn sử dụng")
        dialog.geometry("600x500")
        dialog.resizable(False, False)
        dialog.transient(self)

        text = tk.Text(dialog, wrap='word', font=('Arial', 10), padx=20, pady=20)
        text.pack(fill='both', expand=True)
        text.insert('1.0', help_text)
        text.config(state='disabled')

        ttk.Button(dialog, text="Đóng", command=dialog.destroy, width=15).pack(pady=10)

    def _show_about(self):
        """Hiển thị thông tin ứng dụng"""
        about_text = f"""
{AppConfig.APP_NAME}
Phiên bản: {AppConfig.VERSION}

📚 Hệ thống quản lý thư viện với Python GUI

🔧 Công nghệ:
• GUI:  Tkinter
• Database: MySQL
• Architecture: MVC Pattern

✨ Tính năng:
• Quản lý bạn đọc (CRUD đầy đủ)
• Tìm kiếm & lọc mạnh mẽ
• Xuất dữ liệu (JSON, CSV, Excel, PDF)
• Thống kê & báo cáo
• Validation dữ liệu
• Exception handling

👨‍💻 Phát triển bởi:  NvkhoaDev54
📅 Năm:  2025
📧 Email: support@library. com

© 2025 - Library Management System
All rights reserved. 
        """

        messagebox.showinfo(
            "ℹ️ Giới thiệu",
            about_text
        )

    def _on_closing(self):
        """Xử lý khi đóng ứng dụng"""
        if messagebox.askokcancel(
                "Xác nhận thoát",
                "Bạn có chắc chắn muốn thoát khỏi ứng dụng?"
        ):
            try:
                # Cleanup
                db.close_pool()
                logger.info("Application closed successfully")
            except Exception as e:
                logger.error(f"Error during cleanup: {e}")
            finally:
                self.destroy()