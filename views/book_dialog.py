import tkinter as tk
from tkinter import ttk
from datetime import datetime
from typing import Optional, List

from models.book import Book, Author, Category, Publisher
from controllers.book_controller import BookController


class BookDialog(tk.Toplevel):
    """Dialog thêm/sửa sách"""

    def __init__(self, parent, title="Sách", book: Optional[Book] = None):
        super().__init__(parent)
        self.title(title)
        self.geometry("700x800")
        self.resizable(False, False)

        self.controller = BookController()
        self.book = book
        self.result: Optional[Book] = None
        self.is_edit_mode = book is not None

        # Load data
        self.authors = self.controller.get_all_authors()
        self.categories = self.controller.get_all_categories()
        self.publishers = self.controller.get_all_publishers()

        # Style configuration
        self.configure(bg='#f0f0f0')

        self._create_widgets()

        if self.is_edit_mode:
            self._fill_data()

        # Center window
        self.transient(parent)
        self.grab_set()
        self._center_window()

    def _center_window(self):
        """Center dialog on parent"""
        self.update_idletasks()
        x = self.winfo_x() + (self.master.winfo_width() // 2) - (self.winfo_width() // 2)
        y = self.winfo_y() + (self.master.winfo_height() // 2) - (self.winfo_height() // 2)
        self.geometry(f"+{x}+{y}")

    def _create_widgets(self):
        """Tạo giao diện form"""
        # Main container with padding
        main_frame = ttk.Frame(self, padding=20)
        main_frame.pack(fill='both', expand=True)

        # Title
        title_frame = ttk.Frame(main_frame)
        title_frame.pack(fill='x', pady=(0, 20))

        icon = "✏️" if self.is_edit_mode else "➕"
        title_text = f"{icon} {'CẬP NHẬT' if self.is_edit_mode else 'THÊM MỚI'} SÁCH"

        ttk.Label(
            title_frame,
            text=title_text,
            font=('Arial', 16, 'bold'),
            foreground='#1976D2'
        ).pack()

        # Scrollable form frame
        canvas = tk.Canvas(main_frame, highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient='vertical', command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)

        row = 0

        # ========== THÔNG TIN CƠ BẢN ==========
        ttk.Label(
            scrollable_frame,
            text="📚 THÔNG TIN CƠ BẢN",
            font=('Arial', 11, 'bold'),
            foreground='#1976D2'
        ).grid(row=row, column=0, columnspan=2, sticky='w', pady=(0, 10))
        row += 1

        # Tựa sách *
        self._create_field_label(scrollable_frame, row, "Tựa sách:", required=True)
        self.title_var = tk.StringVar()
        self.title_entry = ttk.Entry(
            scrollable_frame,
            textvariable=self.title_var,
            width=50,
            font=('Arial', 10)
        )
        self.title_entry.grid(row=row, column=1, sticky='w', pady=8, padx=(0, 10))
        self.title_entry.focus()
        row += 1

        # Tác giả
        self._create_field_label(scrollable_frame, row, "Tác giả:")
        author_frame = ttk.Frame(scrollable_frame)
        author_frame.grid(row=row, column=1, sticky='w', pady=8)

        self.author_var = tk.StringVar()
        author_combo = ttk.Combobox(
            author_frame,
            textvariable=self.author_var,
            values=[a.author_name for a in self.authors],
            width=35,
            font=('Arial', 10)
        )
        author_combo.pack(side='left', padx=(0, 5))

        ttk.Button(
            author_frame,
            text="➕",
            command=self._add_author,
            width=3
        ).pack(side='left')
        row += 1

        # Thể loại
        self._create_field_label(scrollable_frame, row, "Thể loại:")
        category_frame = ttk.Frame(scrollable_frame)
        category_frame.grid(row=row, column=1, sticky='w', pady=8)

        self.category_var = tk.StringVar()
        category_combo = ttk.Combobox(
            category_frame,
            textvariable=self.category_var,
            values=[c.category_name for c in self.categories],
            width=35,
            font=('Arial', 10)
        )
        category_combo.pack(side='left', padx=(0, 5))

        ttk.Button(
            category_frame,
            text="➕",
            command=self._add_category,
            width=3
        ).pack(side='left')
        row += 1

        # Nhà xuất bản
        self._create_field_label(scrollable_frame, row, "Nhà xuất bản:")
        publisher_frame = ttk.Frame(scrollable_frame)
        publisher_frame.grid(row=row, column=1, sticky='w', pady=8)

        self.publisher_var = tk.StringVar()
        publisher_combo = ttk.Combobox(
            publisher_frame,
            textvariable=self.publisher_var,
            values=[p.publisher_name for p in self.publishers],
            width=35,
            font=('Arial', 10)
        )
        publisher_combo.pack(side='left', padx=(0, 5))

        ttk.Button(
            publisher_frame,
            text="➕",
            command=self._add_publisher,
            width=3
        ).pack(side='left')
        row += 1

        # Năm xuất bản
        self._create_field_label(scrollable_frame, row, "Năm xuất bản:")
        self.year_var = tk.IntVar(value=datetime.now().year)
        ttk.Spinbox(
            scrollable_frame,
            from_=1900,
            to=datetime.now().year + 5,
            textvariable=self.year_var,
            width=15,
            font=('Arial', 10)
        ).grid(row=row, column=1, sticky='w', pady=8)
        row += 1

        # Separator
        ttk.Separator(scrollable_frame, orient='horizontal').grid(
            row=row, column=0, columnspan=2, sticky='ew', pady=15
        )
        row += 1

        # ========== MÃ & GIÁ ==========
        ttk.Label(
            scrollable_frame,
            text="🏷️ MÃ & GIÁ",
            font=('Arial', 11, 'bold'),
            foreground='#1976D2'
        ).grid(row=row, column=0, columnspan=2, sticky='w', pady=(0, 10))
        row += 1

        # ISBN
        self._create_field_label(scrollable_frame, row, "ISBN:")
        self.isbn_var = tk.StringVar()
        ttk.Entry(
            scrollable_frame,
            textvariable=self.isbn_var,
            width=50,
            font=('Arial', 10)
        ).grid(row=row, column=1, sticky='w', pady=8)
        row += 1

        # Mã vạch (Barcode)
        self._create_field_label(scrollable_frame, row, "Mã vạch:")
        self.barcode_var = tk.StringVar()
        ttk.Entry(
            scrollable_frame,
            textvariable=self.barcode_var,
            width=50,
            font=('Arial', 10)
        ).grid(row=row, column=1, sticky='w', pady=8)
        row += 1

        # Giá
        self._create_field_label(scrollable_frame, row, "Giá (VNĐ):")
        self.price_var = tk.DoubleVar(value=0.0)
        price_frame = ttk.Frame(scrollable_frame)
        price_frame.grid(row=row, column=1, sticky='w', pady=8)

        ttk.Entry(
            price_frame,
            textvariable=self.price_var,
            width=20,
            font=('Arial', 10)
        ).pack(side='left', padx=(0, 5))

        ttk.Label(
            price_frame,
            text="VNĐ",
            font=('Arial', 10)
        ).pack(side='left')
        row += 1

        # Separator
        ttk.Separator(scrollable_frame, orient='horizontal').grid(
            row=row, column=0, columnspan=2, sticky='ew', pady=15
        )
        row += 1

        # ========== MÔ TẢ ==========
        ttk.Label(
            scrollable_frame,
            text="📝 MÔ TẢ",
            font=('Arial', 11, 'bold'),
            foreground='#1976D2'
        ).grid(row=row, column=0, columnspan=2, sticky='w', pady=(0, 10))
        row += 1

        self._create_field_label(scrollable_frame, row, "Mô tả:")
        self.description_text = tk.Text(
            scrollable_frame,
            width=50,
            height=5,
            font=('Arial', 10),
            wrap='word'
        )
        self.description_text.grid(row=row, column=1, sticky='w', pady=8)
        row += 1

        # Pack canvas and scrollbar
        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        # ========== BUTTONS ==========
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=(20, 0))

        ttk.Button(
            button_frame,
            text="💾 Lưu",
            command=self._save,
            width=20
        ).pack(side='left', padx=5)

        ttk.Button(
            button_frame,
            text="❌ Hủy",
            command=self.destroy,
            width=20
        ).pack(side='left', padx=5)

        # Bind Enter key
        self.bind('<Return>', lambda e: self._save())
        self.bind('<Escape>', lambda e: self.destroy())

    def _create_field_label(self, parent, row, text, required=False):
        """Tạo label cho field"""
        label_text = f"{text} {'*' if required else ''}"
        ttk.Label(
            parent,
            text=label_text,
            font=('Arial', 10, 'bold' if required else 'normal'),
            foreground='#d32f2f' if required else 'black'
        ).grid(row=row, column=0, sticky='w', pady=8, padx=(0, 10))

    def _add_author(self):
        """Thêm tác giả mới"""
        dialog = tk.Toplevel(self)
        dialog.title("➕ Thêm tác giả")
        dialog.geometry("400x150")
        dialog.resizable(False, False)
        dialog.transient(self)
        dialog.grab_set()

        ttk.Label(dialog, text="Tên tác giả:", font=('Arial', 10)).pack(pady=10)
        name_var = tk.StringVar()
        ttk.Entry(dialog, textvariable=name_var, width=40).pack(pady=5)

        def save():
            name = name_var.get().strip()
            if name:
                author_id = self.controller.add_author(name, parent=dialog)
                if author_id:
                    # Refresh authors list
                    self.authors = self.controller.get_all_authors()
                    self.author_var.set(name)
                    dialog.destroy()

        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Lưu", command=save, width=10).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Hủy", command=dialog.destroy, width=10).pack(side='left', padx=5)

    def _add_category(self):
        """Thêm thể loại mới"""
        dialog = tk.Toplevel(self)
        dialog.title("➕ Thêm thể loại")
        dialog.geometry("400x150")
        dialog.resizable(False, False)
        dialog.transient(self)
        dialog.grab_set()

        ttk.Label(dialog, text="Tên thể loại:", font=('Arial', 10)).pack(pady=10)
        name_var = tk.StringVar()
        ttk.Entry(dialog, textvariable=name_var, width=40).pack(pady=5)

        def save():
            name = name_var.get().strip()
            if name:
                category_id = self.controller.add_category(name, parent=dialog)
                if category_id:
                    self.categories = self.controller.get_all_categories()
                    self.category_var.set(name)
                    dialog.destroy()

        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Lưu", command=save, width=10).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Hủy", command=dialog.destroy, width=10).pack(side='left', padx=5)

    def _add_publisher(self):
        """Thêm nhà xuất bản mới"""
        dialog = tk.Toplevel(self)
        dialog.title("➕ Thêm nhà xuất bản")
        dialog.geometry("450x250")
        dialog.resizable(False, False)
        dialog.transient(self)
        dialog.grab_set()

        frame = ttk.Frame(dialog, padding=20)
        frame.pack(fill='both', expand=True)

        ttk.Label(frame, text="Tên NXB:", font=('Arial', 10)).grid(row=0, column=0, sticky='w', pady=5)
        name_var = tk.StringVar()
        ttk.Entry(frame, textvariable=name_var, width=35).grid(row=0, column=1, sticky='w', pady=5)

        ttk.Label(frame, text="Địa chỉ:", font=('Arial', 10)).grid(row=1, column=0, sticky='w', pady=5)
        address_var = tk.StringVar()
        ttk.Entry(frame, textvariable=address_var, width=35).grid(row=1, column=1, sticky='w', pady=5)

        ttk.Label(frame, text="Điện thoại:", font=('Arial', 10)).grid(row=2, column=0, sticky='w', pady=5)
        phone_var = tk.StringVar()
        ttk.Entry(frame, textvariable=phone_var, width=35).grid(row=2, column=1, sticky='w', pady=5)

        def save():
            name = name_var.get().strip()
            if name:
                publisher = Publisher(
                    publisher_name=name,
                    address=address_var.get().strip() or None,
                    phone=phone_var.get().strip() or None
                )
                publisher_id = self.controller.add_publisher(publisher, parent=dialog)
                if publisher_id:
                    self.publishers = self.controller.get_all_publishers()
                    self.publisher_var.set(name)
                    dialog.destroy()

        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=20)
        ttk.Button(btn_frame, text="Lưu", command=save, width=10).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Hủy", command=dialog.destroy, width=10).pack(side='left', padx=5)

    def _fill_data(self):
        """Điền dữ liệu khi sửa"""
        if not self.book:
            return

        self.title_var.set(self.book.title or '')
        self.author_var.set(self.book.author_name or '')
        self.category_var.set(self.book.category_name or '')
        self.publisher_var.set(self.book.publisher_name or '')
        self.year_var.set(self.book.publish_year or datetime.now().year)
        self.isbn_var.set(self.book.isbn or '')
        self.barcode_var.set(self.book.barcode or '')
        self.price_var.set(self.book.price or 0.0)

        if self.book.description:
            self.description_text.delete('1.0', 'end')
            self.description_text.insert('1.0', self.book.description)

    def _save(self):
        """Lưu dữ liệu"""
        # Lấy dữ liệu từ form
        title = self.title_var.get().strip()
        author_name = self.author_var.get().strip()
        category_name = self.category_var.get().strip()
        publisher_name = self.publisher_var.get().strip()
        publish_year = self.year_var.get()
        isbn = self.isbn_var.get().strip()
        barcode = self.barcode_var.get().strip()
        price = self.price_var.get()
        description = self.description_text.get('1.0', 'end').strip()

        # Validate cơ bản
        if not title:
            from utils.messagebox_helper import MessageBoxHelper
            MessageBoxHelper.show_error("Lỗi", "Vui lòng nhập tựa sách", parent=self)
            self.title_entry.focus()
            return

        # Tìm ID của author, category, publisher
        author_id = None
        if author_name:
            author = next((a for a in self.authors if a.author_name == author_name), None)
            author_id = author.author_id if author else None

        category_id = None
        if category_name:
            category = next((c for c in self.categories if c.category_name == category_name), None)
            category_id = category.category_id if category else None

        publisher_id = None
        if publisher_name:
            publisher = next((p for p in self.publishers if p.publisher_name == publisher_name), None)
            publisher_id = publisher.publisher_id if publisher else None

        # Tạo Book object
        book = Book(
            title=title,
            author_id=author_id,
            category_id=category_id,
            publisher_id=publisher_id,
            publish_year=publish_year if publish_year else None,
            isbn=isbn if isbn else None,
            barcode=barcode if barcode else None,
            price=price if price else None,
            description=description if description else None
        )

        # Nếu là edit mode, giữ lại ID
        if self.is_edit_mode and self.book:
            book.book_id = self.book.book_id

        self.result = book
        self.destroy()