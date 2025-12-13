import tkinter as tk
from tkinter import ttk
from typing import Optional, List
import logging

from models.book import Book
from controllers.book_controller import BookController
from views.book_dialog import BookDialog
from utils.messagebox_helper import MessageBoxHelper

logger = logging.getLogger(__name__)


class BookView(ttk.Frame):
    """Giao diện quản lý sách"""

    def __init__(self, parent):
        super().__init__(parent)
        self.controller = BookController()
        self.msg_helper = MessageBoxHelper()
        self.current_books: List[Book] = []
        self.selected_book: Optional[Book] = None

        self._create_widgets()
        self._load_data()

    def _create_widgets(self):
        """Tạo giao diện"""
        # ========== TOOLBAR ==========
        toolbar = ttk.Frame(self, relief='raised', borderwidth=1)
        toolbar.pack(fill='x', padx=5, pady=5)

        # Left buttons
        left_frame = ttk.Frame(toolbar)
        left_frame.pack(side='left')

        ttk.Button(
            left_frame,
            text="➕ Thêm mới",
            command=self._show_add_dialog,
            width=12
        ).pack(side='left', padx=2, pady=3)

        ttk.Button(
            left_frame,
            text="✏️ Sửa",
            command=self._show_edit_dialog,
            width=12
        ).pack(side='left', padx=2, pady=3)

        ttk.Button(
            left_frame,
            text="🗑️ Xóa",
            command=self._delete_book,
            width=12
        ).pack(side='left', padx=2, pady=3)

        ttk.Separator(left_frame, orient='vertical').pack(side='left', fill='y', padx=5)

        ttk.Button(
            left_frame,
            text="📦 Tồn kho",
            command=self._show_inventory_dialog,
            width=12
        ).pack(side='left', padx=2, pady=3)

        ttk.Button(
            left_frame,
            text="🔄 Làm mới",
            command=self._load_data,
            width=12
        ).pack(side='left', padx=2, pady=3)

        ttk.Button(
            left_frame,
            text="📊 Thống kê",
            command=self._show_statistics,
            width=12
        ).pack(side='left', padx=2, pady=3)

        # Right buttons - Export
        right_frame = ttk.Frame(toolbar)
        right_frame.pack(side='right')

        ttk.Label(right_frame, text="Xuất:", font=('Arial', 9)).pack(side='left', padx=5)

        ttk.Button(
            right_frame,
            text="📄 JSON",
            command=self._export_json,
            width=10
        ).pack(side='left', padx=2, pady=3)

        ttk.Button(
            right_frame,
            text="📊 CSV",
            command=self._export_csv,
            width=10
        ).pack(side='left', padx=2, pady=3)

        ttk.Button(
            right_frame,
            text="📗 Excel",
            command=self._export_excel,
            width=10
        ).pack(side='left', padx=2, pady=3)

        ttk.Button(
            right_frame,
            text="📕 PDF",
            command=self._export_pdf,
            width=10
        ).pack(side='left', padx=2, pady=3)

        # ========== SEARCH FRAME ==========
        search_frame = ttk.LabelFrame(self, text="🔍 Tìm kiếm", padding=10)
        search_frame.pack(fill='x', padx=5, pady=5)

        ttk.Label(search_frame, text="Từ khóa:", font=('Arial', 9)).pack(side='left', padx=(0, 5))

        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=35, font=('Arial', 9))
        search_entry.pack(side='left', padx=(0, 5))
        search_entry.bind('<Return>', lambda e: self._search())
        search_entry.bind('<KeyRelease>', self._on_search_key_release)

        ttk.Label(search_frame, text="Tìm theo:", font=('Arial', 9)).pack(side='left', padx=(15, 5))

        self.search_by_var = tk.StringVar(value="all")
        ttk.Combobox(
            search_frame,
            textvariable=self.search_by_var,
            values=["all", "title", "author", "isbn", "barcode", "category"],
            state='readonly',
            width=15,
            font=('Arial', 9)
        ).pack(side='left', padx=(0, 5))

        ttk.Button(
            search_frame,
            text="🔍 Tìm",
            command=self._search,
            width=10
        ).pack(side='left', padx=5)

        ttk.Button(
            search_frame,
            text="↺ Reset",
            command=self._reset_search,
            width=10
        ).pack(side='left', padx=2)

        # ========== TABLE FRAME ==========
        table_frame = ttk.Frame(self)
        table_frame.pack(fill='both', expand=True, padx=5, pady=5)

        # Treeview
        columns = (
            'ID', 'Tựa sách', 'Tác giả', 'Thể loại', 'NXB',
            'Năm XB', 'ISBN', 'Barcode', 'Giá', 'Tổng SL', 'Còn', 'Trạng thái'
        )

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show='headings',
            selectmode='browse',
            height=15
        )

        # Cấu hình độ rộng cột
        self.tree.column('ID', width=50, anchor='center')
        self.tree.column('Tựa sách', width=250, anchor='w')
        self.tree.column('Tác giả', width=150, anchor='w')
        self.tree.column('Thể loại', width=120, anchor='w')
        self.tree.column('NXB', width=150, anchor='w')
        self.tree.column('Năm XB', width=80, anchor='center')
        self.tree.column('ISBN', width=120, anchor='center')
        self.tree.column('Barcode', width=120, anchor='center')
        self.tree.column('Giá', width=100, anchor='e')
        self.tree.column('Tổng SL', width=80, anchor='center')
        self.tree.column('Còn', width=80, anchor='center')
        self.tree.column('Trạng thái', width=120, anchor='center')

        # Định nghĩa columns headers
        for col in columns:
            self.tree.heading(col, text=col)

        # Scrollbars
        vsb = ttk.Scrollbar(table_frame, orient='vertical', command=self.tree.yview)
        hsb = ttk.Scrollbar(table_frame, orient='horizontal', command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        # Grid layout
        self.tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')

        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        # Context menu
        self.context_menu = tk.Menu(self.tree, tearoff=0)
        self.context_menu.add_command(label="✏️ Sửa", command=self._show_edit_dialog)
        self.context_menu.add_command(label="🗑️ Xóa", command=self._delete_book)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="📦 Cập nhật tồn kho", command=self._show_inventory_dialog)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="ℹ️ Chi tiết", command=self._show_detail)

        # Bind events
        self.tree.bind('<<TreeviewSelect>>', self._on_select)
        self.tree.bind('<Double-1>', lambda e: self._show_edit_dialog())
        self.tree.bind('<Button-3>', self._show_context_menu)
        self.tree.bind('<Delete>', lambda e: self._delete_book())

        # ========== DETAIL FRAME ==========
        detail_frame = ttk.LabelFrame(self, text="ℹ️ Chi tiết sách", padding=10)
        detail_frame.pack(fill='x', padx=5, pady=5)

        self.detail_text = tk.Text(
            detail_frame,
            height=3,
            wrap='word',
            font=('Arial', 9),
            state='disabled',
            background='#f5f5f5'
        )
        self.detail_text.pack(fill='x')

        # ========== STATUS BAR ==========
        status_bar = ttk.Frame(self, relief='sunken', borderwidth=1)
        status_bar.pack(fill='x', padx=5, pady=2)

        self.status_label = ttk.Label(
            status_bar,
            text="Sẵn sàng",
            font=('Arial', 9)
        )
        self.status_label.pack(side='left', padx=5)

        self.count_label = ttk.Label(
            status_bar,
            text="Tổng: 0 sách",
            font=('Arial', 9, 'bold')
        )
        self.count_label.pack(side='right', padx=5)

    def _load_data(self):
        """Load dữ liệu từ database"""
        try:
            self.current_books = self.controller.get_all_books()
            self._populate_tree(self.current_books)
            self.status_label.config(text="✅ Đã tải dữ liệu thành công")
            logger.info(f"Loaded {len(self.current_books)} books")
        except Exception as e:
            self.msg_helper.show_error("Lỗi", f"Không thể tải dữ liệu: {str(e)}")
            logger.error(f"Error loading data: {e}")

    def _populate_tree(self, books: List[Book]):
        """Hiển thị dữ liệu lên Treeview"""
        # Xóa dữ liệu cũ
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Thêm dữ liệu mới
        for book in books:
            # Format giá
            price_str = f"{book.price:,.0f}" if book.price else "0"

            values = (
                book.book_id,
                (book.title or '')[:40] + '...' if book.title and len(book.title) > 40 else (book.title or ''),
                book.author_name or '',
                book.category_name or '',
                book.publisher_name or '',
                book.publish_year or '',
                book.isbn or '',
                book.barcode or '',
                price_str,
                book.total_quantity,
                book.available_quantity,
                book.get_stock_status()
            )

            # Thêm tag màu theo trạng thái tồn kho
            tags = []
            if book.available_quantity == 0:
                tags.append('out_of_stock')
            elif book.available_quantity < 5:
                tags.append('low_stock')
            else:
                tags.append('in_stock')

            self.tree.insert('', 'end', values=values, tags=tuple(tags))

        # Cấu hình màu tag
        self.tree.tag_configure('out_of_stock', foreground='#F44336')
        self.tree.tag_configure('low_stock', foreground='#FF9800')
        self.tree.tag_configure('in_stock', foreground='#4CAF50')

        # Cập nhật count
        self.count_label.config(text=f"Tổng: {len(books)} sách")

    def _on_select(self, event):
        """Xử lý khi chọn 1 dòng"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            book_id = item['values'][0]
            self.selected_book = self.controller.get_book_by_id(book_id)
            self._update_detail_panel()

    def _update_detail_panel(self):
        """Cập nhật panel chi tiết"""
        self.detail_text.config(state='normal')
        self.detail_text.delete('1.0', 'end')

        if self.selected_book:
            price_str = f"{self.selected_book.price:,.0f} VNĐ" if self.selected_book.price else "N/A"
            detail = f"""📚 {self.selected_book.title} | 👤 {self.selected_book.author_name or 'N/A'} | 🏷️ {self.selected_book.category_name or 'N/A'}
📖 ISBN: {self.selected_book.isbn or 'N/A'} | 🏭 {self.selected_book.publisher_name or 'N/A'} | 💰 {price_str}
📦 Tồn kho: {self.selected_book.available_quantity}/{self.selected_book.total_quantity} | {self.selected_book.get_stock_status()}"""
            self.detail_text.insert('1.0', detail)

        self.detail_text.config(state='disabled')

    def _show_context_menu(self, event):
        """Hiển thị context menu"""
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)

    def _on_search_key_release(self, event):
        """Auto search khi gõ (debounced)"""
        if hasattr(self, '_search_after_id'):
            self.after_cancel(self._search_after_id)
        self._search_after_id = self.after(500, self._search)

    def _search(self):
        """Tìm kiếm"""
        keyword = self.search_var.get().strip()
        search_by = self.search_by_var.get()

        if not keyword:
            self._load_data()
            return

        try:
            books = self.controller.search_books(keyword, search_by)
            self._populate_tree(books)
            self.status_label.config(text=f"🔍 Tìm thấy {len(books)} kết quả")
        except Exception as e:
            self.msg_helper.show_error("Lỗi tìm kiếm", str(e))

    def _reset_search(self):
        """Reset tìm kiếm"""
        self.search_var.set("")
        self.search_by_var.set("all")
        self._load_data()

    def _show_add_dialog(self):
        """Hiển thị dialog thêm mới"""
        dialog = BookDialog(self, title="➕ Thêm sách mới")
        self.wait_window(dialog)

        if dialog.result:
            if self.controller.add_book(dialog.result, parent=self):
                self._load_data()

    def _show_edit_dialog(self):
        """Hiển thị dialog sửa"""
        if not self.selected_book:
            self.msg_helper.show_warning("Chưa chọn", "Vui lòng chọn sách cần sửa", parent=self)
            return

        dialog = BookDialog(
            self,
            title="✏️ Cập nhật thông tin sách",
            book=self.selected_book
        )
        self.wait_window(dialog)

        if dialog.result:
            if self.controller.update_book(dialog.result, parent=self):
                self._load_data()

    def _delete_book(self):
        """Xóa sách"""
        if not self.selected_book:
            self.msg_helper.show_warning("Chưa chọn", "Vui lòng chọn sách cần xóa", parent=self)
            return

        if self.controller.delete_book(
                self.selected_book.book_id,
                self.selected_book.title,
                parent=self
        ):
            self.selected_book = None
            self._load_data()

    def _show_inventory_dialog(self):
        """Hiển thị dialog cập nhật tồn kho"""
        if not self.selected_book:
            self.msg_helper.show_warning("Chưa chọn", "Vui lòng chọn sách", parent=self)
            return

        dialog = tk.Toplevel(self)
        dialog.title("📦 Cập nhật tồn kho")
        dialog.geometry("500x350")
        dialog.resizable(False, False)
        dialog.transient(self)
        dialog.grab_set()

        frame = ttk.Frame(dialog, padding=30)
        frame.pack(fill='both', expand=True)

        title_label = ttk.Label(
            frame,
            text="📦 CẬP NHẬT TỒN KHO",
            font=('Arial', 14, 'bold'),
            foreground='#1976D2'
        )
        title_label.pack(pady=(0, 15))

        book_title = self.selected_book.title
        if len(book_title) > 40:
            book_title = book_title[:40] + "..."

        book_label = ttk.Label(
            frame,
            text=book_title,
            font=('Arial', 11),
            foreground='#333',
            wraplength=400
        )
        book_label.pack(pady=(0, 20))

        ttk.Separator(frame, orient='horizontal').pack(fill='x', pady=(0, 20))

        # Tổng số lượng
        total_frame = ttk.Frame(frame)
        total_frame.pack(fill='x', pady=10)

        ttk.Label(
            total_frame,
            text="📊 Tổng số lượng:",
            font=('Arial', 10, 'bold')
        ).pack(side='left', padx=(0, 10))

        total_var = tk.IntVar(value=self.selected_book.total_quantity)
        total_spinbox = ttk.Spinbox(
            total_frame,
            from_=0,
            to=9999,
            textvariable=total_var,
            width=15,
            font=('Arial', 11)
        )
        total_spinbox.pack(side='left')

        # Số lượng còn
        available_frame = ttk.Frame(frame)
        available_frame.pack(fill='x', pady=10)

        ttk.Label(
            available_frame,
            text="✅ Số lượng còn:",
            font=('Arial', 10, 'bold')
        ).pack(side='left', padx=(0, 10))

        available_var = tk.IntVar(value=self.selected_book.available_quantity)
        available_spinbox = ttk.Spinbox(
            available_frame,
            from_=0,
            to=9999,
            textvariable=available_var,
            width=15,
            font=('Arial', 11)
        )
        available_spinbox.pack(side='left')

        ttk.Separator(frame, orient='horizontal').pack(fill='x', pady=25)

        def save():
            if self.controller.update_inventory(
                    self.selected_book.book_id,
                    total_var.get(),
                    available_var.get(),
                    parent=dialog
            ):
                self._load_data()
                dialog.destroy()

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=(0, 10))

        ttk.Button(
            btn_frame,
            text="💾 Lưu thay đổi",
            command=save,
            width=20
        ).pack(side='left', padx=10)

        ttk.Button(
            btn_frame,
            text="❌ Hủy bỏ",
            command=dialog.destroy,
            width=20
        ).pack(side='left', padx=10)

        dialog.bind('<Return>', lambda e: save())
        dialog.bind('<Escape>', lambda e: dialog.destroy())
        total_spinbox.focus()

    def _show_detail(self):
        """Hiển thị chi tiết đầy đủ"""
        if not self.selected_book:
            self.msg_helper.show_warning("Chưa chọn", "Vui lòng chọn sách", parent=self)
            return

        book = self.selected_book

        detail_window = tk.Toplevel(self)
        detail_window.title(f"ℹ️ Chi tiết - {book.title}")
        detail_window.geometry("650x600")
        detail_window.transient(self)

        main_frame = ttk.Frame(detail_window, padding=20)
        main_frame.pack(fill='both', expand=True)

        ttk.Label(
            main_frame,
            text=f"📚 CHI TIẾT SÁCH",
            font=('Arial', 14, 'bold'),
            foreground='#1976D2'
        ).pack(pady=(0, 20))

        info_frame = ttk.Frame(main_frame)
        info_frame.pack(fill='both', expand=True)

        price_str = f"{book.price:,.0f} VNĐ" if book.price else "N/A"

        info_text = f"""
🆔 ID: {book.book_id}
📚 Tựa sách: {book.title}
👤 Tác giả: {book.author_name or 'N/A'}
🏷️ Thể loại: {book.category_name or 'N/A'}
🏭 Nhà xuất bản: {book.publisher_name or 'N/A'}
📅 Năm xuất bản: {book.publish_year or 'N/A'}

📖 ISBN: {book.isbn or 'N/A'}
🔢 Mã vạch: {book.barcode or 'N/A'}
💰 Giá: {price_str}

📦 Tồn kho:
   • Tổng số lượng: {book.total_quantity}
   • Số lượng còn: {book.available_quantity}
   • Đang mượn: {book.total_quantity - book.available_quantity}
   • Trạng thái: {book.get_stock_status()}
   • Tỷ lệ mượn: {book.get_borrow_rate():.1f}%

📝 Mô tả:
{book.description or 'Không có mô tả'}
"""

        text_widget = tk.Text(
            info_frame,
            wrap='word',
            font=('Courier', 10),
            background='#f5f5f5',
            padx=10,
            pady=10
        )
        text_widget.pack(fill='both', expand=True)
        text_widget.insert('1.0', info_text)
        text_widget.config(state='disabled')

        ttk.Button(
            main_frame,
            text="Đóng",
            command=detail_window.destroy,
            width=15
        ).pack(pady=(10, 0))

    def _show_statistics(self):
        """Hiển thị thống kê"""
        stats = self.controller.get_statistics()

        dialog = tk.Toplevel(self)
        dialog.title("📊 Thống kê sách")
        dialog.geometry("750x650")
        dialog.resizable(True, True)
        dialog.transient(self)

        main_frame = ttk.Frame(dialog)
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)

        ttk.Label(
            main_frame,
            text="📊 THỐNG KÊ SÁCH",
            font=('Arial', 18, 'bold'),
            foreground='#1976D2'
        ).pack(pady=(0, 25))

        canvas = tk.Canvas(main_frame, highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient='vertical', command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)

        # TỔNG QUAN
        overview_frame = ttk.LabelFrame(
            scrollable_frame,
            text="📈 Tổng quan",
            padding=20
        )
        overview_frame.pack(fill='x', pady=10)

        overview_text = f"""
📚 Tổng số đầu sách: {stats.get('total_books', 0):,} đầu
📦 Tổng số lượng: {stats.get('total_quantity', 0):,} cuốn
✅ Số lượng còn: {stats.get('available_quantity', 0):,} cuốn
📤 Đang cho mượn: {stats.get('borrowed_quantity', 0):,} cuốn
"""
        ttk.Label(
            overview_frame,
            text=overview_text,
            font=('Arial', 11),
            justify='left'
        ).pack(anchor='w')

        # TỒN KHO
        stock_frame = ttk.LabelFrame(
            scrollable_frame,
            text="📦 Tình trạng tồn kho",
            padding=20
        )
        stock_frame.pack(fill='x', pady=10)

        stock_text = f"""
❌ Hết hàng: {stats.get('out_of_stock', 0)} đầu sách
⚠️ Sắp hết (< 5 cuốn): {stats.get('low_stock', 0)} đầu sách
✅ Còn hàng: {stats.get('total_books', 0) - stats.get('out_of_stock', 0) - stats.get('low_stock', 0)} đầu sách
"""
        ttk.Label(
            stock_frame,
            text=stock_text,
            font=('Arial', 11),
            justify='left'
        ).pack(anchor='w')

        chart_canvas = tk.Canvas(stock_frame, height=120, bg='white', highlightthickness=1,
                                 highlightbackground='#ddd')
        chart_canvas.pack(fill='x', pady=(10, 0))

        total_books = stats.get('total_books', 1) or 1
        out = stats.get('out_of_stock', 0)
        low = stats.get('low_stock', 0)
        good = total_books - out - low

        colors = {'good': '#4CAF50', 'low': '#FF9800', 'out': '#F44336'}
        labels = {'good': f'Còn hàng ({good})', 'low': f'Sắp hết ({low})', 'out': f'Hết hàng ({out})'}

        x = 50
        max_width = 600
        for key, color in colors.items():
            count = good if key == 'good' else (low if key == 'low' else out)
            width = (count / total_books) * max_width if total_books > 0 else 0

            chart_canvas.create_rectangle(x, 30, x + width, 70, fill=color, outline='')

            if width > 30:
                chart_canvas.create_text(
                    x + width / 2, 50,
                    text=str(count),
                    fill='white',
                    font=('Arial', 12, 'bold')
                )

            chart_canvas.create_text(
                x + width / 2, 95,
                text=labels[key],
                font=('Arial', 9)
            )

            x += max_width // 3

        # DANH MỤC
        catalog_frame = ttk.LabelFrame(
            scrollable_frame,
            text="📂 Danh mục",
            padding=20
        )
        catalog_frame.pack(fill='x', pady=10)

        catalog_text = f"""
👤 Số tác giả: {stats.get('total_authors', 0):,} tác giả
🏷️ Số thể loại: {stats.get('total_categories', 0):,} thể loại
🏭 Số nhà xuất bản: {stats.get('total_publishers', 0):,} nhà xuất bản
"""
        ttk.Label(
            catalog_frame,
            text=catalog_text,
            font=('Arial', 11),
            justify='left'
        ).pack(anchor='w')

        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=(20, 0))

        ttk.Button(
            btn_frame,
            text="✅ Đóng",
            command=dialog.destroy,
            width=25
        ).pack()

        dialog.bind('<Escape>', lambda e: dialog.destroy())

    def _export_json(self):
        """Xuất dữ liệu ra JSON"""
        self.controller.export_json(self.current_books, parent=self)

    def _export_csv(self):
        """Xuất dữ liệu ra CSV"""
        self.controller.export_csv(self.current_books, parent=self)

    def _export_excel(self):
        """Xuất dữ liệu ra Excel"""
        self.controller.export_excel(self.current_books, parent=self)

    def _export_pdf(self):
        """Xuất dữ liệu ra PDF"""
        self.controller.export_pdf(self.current_books, parent=self)
