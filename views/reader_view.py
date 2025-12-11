import tkinter as tk
from tkinter import ttk
from typing import Optional, List
import logging

from models.reader import Reader, get_all_statuses, get_status_display_map
from controllers.reader_controller import ReaderController
from views.reader_dialog import ReaderDialog
from utils.messagebox_helper import MessageBoxHelper

logger = logging.getLogger(__name__)


class ReaderView(ttk.Frame):
    """Giao diện quản lý bạn đọc"""

    def __init__(self, parent):
        super().__init__(parent)
        self.controller = ReaderController()
        self.msg_helper = MessageBoxHelper()
        self.current_readers: List[Reader] = []
        self.selected_reader: Optional[Reader] = None

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
            command=self._delete_reader,
            width=12
        ).pack(side='left', padx=2, pady=3)

        ttk.Separator(left_frame, orient='vertical').pack(side='left', fill='y', padx=5)

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

        # ========== SEARCH & FILTER FRAME ==========
        search_frame = ttk.LabelFrame(self, text="🔍 Tìm kiếm & Lọc", padding=10)
        search_frame.pack(fill='x', padx=5, pady=5)

        # Row 1:  Tìm kiếm
        row1 = ttk.Frame(search_frame)
        row1.pack(fill='x', pady=5)

        ttk.Label(row1, text="Từ khóa:", font=('Arial', 9)).pack(side='left', padx=(0, 5))

        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(row1, textvariable=self.search_var, width=35, font=('Arial', 9))
        search_entry.pack(side='left', padx=(0, 5))
        search_entry.bind('<Return>', lambda e: self._search())
        search_entry.bind('<KeyRelease>', self._on_search_key_release)

        ttk.Label(row1, text="Tìm theo:", font=('Arial', 9)).pack(side='left', padx=(15, 5))

        self.search_by_var = tk.StringVar(value="all")
        ttk.Combobox(
            row1,
            textvariable=self.search_by_var,
            values=[
                ("all", "Tất cả"),
                ("name", "Họ tên"),
                ("phone", "Điện thoại"),
                ("email", "Email"),
                ("address", "Địa chỉ")
            ],
            state='readonly',
            width=15,
            font=('Arial', 9)
        ).pack(side='left', padx=(0, 5))

        ttk.Button(
            row1,
            text="🔍 Tìm",
            command=self._search,
            width=10
        ).pack(side='left', padx=5)

        ttk.Button(
            row1,
            text="↺ Reset",
            command=self._reset_search,
            width=10
        ).pack(side='left', padx=2)

        # Row 2: Lọc
        row2 = ttk.Frame(search_frame)
        row2.pack(fill='x', pady=5)

        ttk.Label(row2, text="Trạng thái:", font=('Arial', 9)).pack(side='left', padx=(0, 5))

        self.filter_status_var = tk.StringVar(value="Tất cả")
        ttk.Combobox(
            row2,
            textvariable=self.filter_status_var,
            values=["Tất cả"] + get_all_statuses(),
            state='readonly',
            width=15,
            font=('Arial', 9)
        ).pack(side='left', padx=(0, 5))

        ttk.Label(row2, text="Điểm uy tín:", font=('Arial', 9)).pack(side='left', padx=(15, 5))

        ttk.Label(row2, text="Từ:", font=('Arial', 9)).pack(side='left', padx=(0, 5))
        self.filter_min_rep_var = tk.IntVar(value=0)
        ttk.Spinbox(
            row2,
            from_=0,
            to=100,
            textvariable=self.filter_min_rep_var,
            width=8,
            font=('Arial', 9)
        ).pack(side='left', padx=(0, 5))

        ttk.Label(row2, text="Đến:", font=('Arial', 9)).pack(side='left', padx=(5, 5))
        self.filter_max_rep_var = tk.IntVar(value=100)
        ttk.Spinbox(
            row2,
            from_=0,
            to=100,
            textvariable=self.filter_max_rep_var,
            width=8,
            font=('Arial', 9)
        ).pack(side='left', padx=(0, 5))

        self.filter_expiring_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            row2,
            text="Sắp hết hạn (30 ngày)",
            variable=self.filter_expiring_var,
            onvalue=True,
            offvalue=False
        ).pack(side='left', padx=(15, 5))

        ttk.Button(
            row2,
            text="🔎 Lọc",
            command=self._filter,
            width=10
        ).pack(side='left', padx=5)

        ttk.Button(
            row2,
            text="🔃 Reset Lọc",
            command=self._reset_filter,
            width=12
        ).pack(side='left', padx=2)

        # ========== TABLE FRAME ==========
        table_frame = ttk.Frame(self)
        table_frame.pack(fill='both', expand=True, padx=5, pady=5)

        # Treeview
        columns = (
            'ID', 'Họ tên', 'Điện thoại', 'Email', 'Địa chỉ',
            'Ngày cấp thẻ', 'Ngày hết hạn', 'Còn lại', 'Trạng thái', 'Điểm UT'
        )

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show='headings',
            selectmode='browse',
            height=15
        )

        # Định nghĩa columns
        self.tree.heading('ID', text='ID')
        self.tree.heading('Họ tên', text='Họ tên')
        self.tree.heading('Điện thoại', text='Điện thoại')
        self.tree.heading('Email', text='Email')
        self.tree.heading('Địa chỉ', text='Địa chỉ')
        self.tree.heading('Ngày cấp thẻ', text='Ngày cấp thẻ')
        self.tree.heading('Ngày hết hạn', text='Ngày hết hạn')
        self.tree.heading('Còn lại', text='Còn lại (ngày)')
        self.tree.heading('Trạng thái', text='Trạng thái')
        self.tree.heading('Điểm UT', text='Điểm UT')

        # Cấu hình độ rộng cột
        self.tree.column('ID', width=50, anchor='center')
        self.tree.column('Họ tên', width=180, anchor='w')
        self.tree.column('Điện thoại', width=110, anchor='center')
        self.tree.column('Email', width=180, anchor='w')
        self.tree.column('Địa chỉ', width=200, anchor='w')
        self.tree.column('Ngày cấp thẻ', width=100, anchor='center')
        self.tree.column('Ngày hết hạn', width=100, anchor='center')
        self.tree.column('Còn lại', width=100, anchor='center')
        self.tree.column('Trạng thái', width=100, anchor='center')
        self.tree.column('Điểm UT', width=80, anchor='center')

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
        self.context_menu.add_command(label="🗑️ Xóa", command=self._delete_reader)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="🔒 Khóa", command=self._lock_reader)
        self.context_menu.add_command(label="🔓 Mở khóa", command=self._unlock_reader)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="📅 Gia hạn thẻ", command=self._extend_card)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="ℹ️ Chi tiết", command=self._show_detail)

        # Bind events
        self.tree.bind('<<TreeviewSelect>>', self._on_select)
        self.tree.bind('<Double-1>', lambda e: self._show_edit_dialog())
        self.tree.bind('<Button-3>', self._show_context_menu)  # Right click
        self.tree.bind('<Delete>', lambda e: self._delete_reader())

        # ========== DETAIL FRAME ==========
        detail_frame = ttk.LabelFrame(self, text="ℹ️ Chi tiết bạn đọc", padding=10)
        detail_frame.pack(fill='x', padx=5, pady=5)

        self.detail_text = tk.Text(
            detail_frame,
            height=4,
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
            text="Tổng:  0 bạn đọc",
            font=('Arial', 9, 'bold')
        )
        self.count_label.pack(side='right', padx=5)

    def _load_data(self):
        """Load dữ liệu từ database"""
        try:
            self.current_readers = self.controller.get_all_readers()
            self._populate_tree(self.current_readers)
            self.status_label.config(text="✅ Đã tải dữ liệu thành công")
            logger.info(f"Loaded {len(self.current_readers)} readers")
        except Exception as e:
            self.msg_helper.show_error("Lỗi", f"Không thể tải dữ liệu: {str(e)}")
            logger.error(f"Error loading data: {e}")

    def _populate_tree(self, readers: List[Reader]):
        """Hiển thị dữ liệu lên Treeview"""
        # Xóa dữ liệu cũ
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Thêm dữ liệu mới
        for reader in readers:
            # Tính số ngày còn lại
            days_left = reader.get_days_until_expiry()
            days_display = str(days_left) if days_left is not None else "N/A"

            values = (
                reader.reader_id,
                reader.full_name or '',
                reader.phone or '',
                reader.email or '',
                (reader.address or '')[:50] + '...' if reader.address and len(reader.address) > 50 else (
                            reader.address or ''),
                reader.card_start or '',
                reader.card_end or '',
                days_display,
                get_status_display_map().get(reader.status, reader.status),
                reader.reputation_score
            )

            # Thêm tag màu theo trạng thái và điểm uy tín
            tags = []

            if reader.status == 'ACTIVE':
                tags.append('active')
            elif reader.status == 'EXPIRED':
                tags.append('expired')
            elif reader.status == 'LOCKED':
                tags.append('locked')

            if reader.reputation_score >= 90:
                tags.append('high_rep')
            elif reader.reputation_score < 50:
                tags.append('low_rep')

            # Thẻ sắp hết hạn
            if days_left is not None and 0 <= days_left <= 7:
                tags.append('expiring_soon')

            self.tree.insert('', 'end', values=values, tags=tuple(tags))

        # Cấu hình màu tag
        self.tree.tag_configure('active', foreground='#4CAF50')
        self.tree.tag_configure('expired', foreground='#F44336')
        self.tree.tag_configure('locked', foreground='#FF9800')
        self.tree.tag_configure('high_rep', background='#E8F5E9')
        self.tree.tag_configure('low_rep', background='#FFEBEE')
        self.tree.tag_configure('expiring_soon', background='#FFF9C4')

        # Cập nhật count
        self.count_label.config(text=f"Tổng: {len(readers)} bạn đọc")

    def _on_select(self, event):
        """Xử lý khi chọn 1 dòng"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            reader_id = item['values'][0]
            self.selected_reader = self.controller.get_reader_by_id(reader_id)
            self._update_detail_panel()

    def _update_detail_panel(self):
        """Cập nhật panel chi tiết"""
        self.detail_text.config(state='normal')
        self.detail_text.delete('1.0', 'end')

        if self.selected_reader:
            detail = f"""📋 ID: {self.selected_reader.reader_id} | 👤 {self.selected_reader.full_name}
📞 {self.selected_reader.phone or 'N/A'} | 📧 {self.selected_reader.email or 'N/A'}
📍 {self.selected_reader.address or 'N/A'}
📅 Thẻ: {self.selected_reader.card_start} → {self.selected_reader.card_end} | {self.selected_reader.get_card_validity_info()}
🎯 Trạng thái: {self.selected_reader.get_status_display()} | ⭐ Uy tín: {self.selected_reader.reputation_score}/100 ({self.selected_reader.get_reputation_level()})"""

            self.detail_text.insert('1.0', detail)

        self.detail_text.config(state='disabled')

    def _show_context_menu(self, event):
        """Hiển thị context menu"""
        # Select item under cursor
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)

    def _on_search_key_release(self, event):
        """Auto search khi gõ (debounced)"""
        # Cancel previous scheduled search
        if hasattr(self, '_search_after_id'):
            self.after_cancel(self._search_after_id)

        # Schedule new search after 500ms
        self._search_after_id = self.after(500, self._search)

    def _search(self):
        """Tìm kiếm"""
        keyword = self.search_var.get().strip()
        search_by = self.search_by_var.get()

        if not keyword:
            self._load_data()
            return

        try:
            readers = self.controller.search_readers(keyword, search_by)
            self._populate_tree(readers)
            self.status_label.config(text=f"🔍 Tìm thấy {len(readers)} kết quả")
        except Exception as e:
            self.msg_helper.show_error("Lỗi tìm kiếm", str(e))

    def _reset_search(self):
        """Reset tìm kiếm"""
        self.search_var.set("")
        self.search_by_var.set("all")
        self._load_data()

    def _filter(self):
        """Lọc dữ liệu"""
        try:
            status = self.filter_status_var.get()
            status = None if status == "Tất cả" else status

            min_rep = self.filter_min_rep_var.get()
            max_rep = self.filter_max_rep_var.get()
            expiring = self.filter_expiring_var.get()

            readers = self.controller.filter_readers(
                status=status,
                min_reputation=min_rep,
                max_reputation=max_rep,
                expiring_soon=expiring
            )
            self._populate_tree(readers)
            self.status_label.config(text=f"🔎 Lọc được {len(readers)} kết quả")
        except Exception as e:
            self.msg_helper.show_error("Lỗi lọc", str(e))

    def _reset_filter(self):
        """Reset bộ lọc"""
        self.filter_status_var.set("Tất cả")
        self.filter_min_rep_var.set(0)
        self.filter_max_rep_var.set(100)
        self.filter_expiring_var.set(False)
        self._load_data()

    def _show_add_dialog(self):
        """Hiển thị dialog thêm mới"""
        dialog = ReaderDialog(self, title="➕ Thêm bạn đọc mới")
        self.wait_window(dialog)

        if dialog.result:
            if self.controller.add_reader(dialog.result, parent=self):
                self._load_data()

    def _show_edit_dialog(self):
        """Hiển thị dialog sửa"""
        if not self.selected_reader:
            self.msg_helper.show_warning("Chưa chọn", "Vui lòng chọn bạn đọc cần sửa", parent=self)
            return

        dialog = ReaderDialog(
            self,
            title="✏️ Cập nhật thông tin bạn đọc",
            reader=self.selected_reader
        )
        self.wait_window(dialog)

        if dialog.result:
            if self.controller.update_reader(dialog.result, parent=self):
                self._load_data()

    def _delete_reader(self):
        """Xóa bạn đọc"""
        if not self.selected_reader:
            self.msg_helper.show_warning("Chưa chọn", "Vui lòng chọn bạn đọc cần xóa", parent=self)
            return

        if self.controller.delete_reader(
                self.selected_reader.reader_id,
                self.selected_reader.full_name,
                parent=self
        ):
            self.selected_reader = None
            self._load_data()

    def _lock_reader(self):
        """Khóa bạn đọc"""
        if not self.selected_reader:
            self.msg_helper.show_warning("Chưa chọn", "Vui lòng chọn bạn đọc cần khóa", parent=self)
            return

        if self.controller.lock_reader(self.selected_reader.reader_id, parent=self):
            self._load_data()

    def _unlock_reader(self):
        """Mở khóa bạn đọc"""
        if not self.selected_reader:
            self.msg_helper.show_warning("Chưa chọn", "Vui lòng chọn bạn đọc cần mở khóa", parent=self)
            return

        if self.controller.unlock_reader(self.selected_reader.reader_id, parent=self):
            self._load_data()

    def _extend_card(self):
        """Gia hạn thẻ"""
        if not self.selected_reader:
            self.msg_helper.show_warning("Chưa chọn", "Vui lòng chọn bạn đọc cần gia hạn", parent=self)
            return

        # Dialog nhập số ngày
        dialog = tk.Toplevel(self)
        dialog.title("📅 Gia hạn thẻ")
        dialog.geometry("300x150")
        dialog.resizable(False, False)
        dialog.transient(self)
        dialog.grab_set()

        ttk.Label(
            dialog,
            text=f"Gia hạn thẻ cho:\n{self.selected_reader.full_name}",
            font=('Arial', 10, 'bold')
        ).pack(pady=10)

        frame = ttk.Frame(dialog)
        frame.pack(pady=10)

        ttk.Label(frame, text="Số ngày: ").pack(side='left', padx=5)
        days_var = tk.IntVar(value=365)
        ttk.Spinbox(frame, from_=1, to=3650, textvariable=days_var, width=10).pack(side='left')

        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(pady=10)

        def do_extend():
            if self.controller.extend_card(self.selected_reader.reader_id, days_var.get(), parent=self):
                self._load_data()
                dialog.destroy()

        ttk.Button(btn_frame, text="Gia hạn", command=do_extend, width=10).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Hủy", command=dialog.destroy, width=10).pack(side='left', padx=5)

    def _show_detail(self):
        """Hiển thị chi tiết đầy đủ"""
        if not self.selected_reader:
            self.msg_helper.show_warning("Chưa chọn", "Vui lòng chọn bạn đọc", parent=self)
            return

        reader = self.selected_reader

        detail_window = tk.Toplevel(self)
        detail_window.title(f"ℹ️ Chi tiết - {reader.full_name}")
        detail_window.geometry("600x500")
        detail_window.transient(self)

        main_frame = ttk.Frame(detail_window, padding=20)
        main_frame.pack(fill='both', expand=True)

        # Title
        ttk.Label(
            main_frame,
            text=f"📋 CHI TIẾT BẠN ĐỌC",
            font=('Arial', 14, 'bold'),
            foreground='#1976D2'
        ).pack(pady=(0, 20))

        # Info frame
        info_frame = ttk.Frame(main_frame)
        info_frame.pack(fill='both', expand=True)

        info_text = f"""
🆔 ID: {reader.reader_id}
👤 Họ tên: {reader.full_name}
📞 Điện thoại: {reader.phone or 'N/A'}
📧 Email: {reader.email or 'N/A'}
📍 Địa chỉ: {reader.address or 'N/A'}

📅 Ngày cấp thẻ: {reader.card_start}
📅 Ngày hết hạn: {reader.card_end}
⏰ Thời hạn: {reader.get_card_validity_info()}

🎯 Trạng thái: {reader.get_status_display()}
⭐ Điểm uy tín: {reader.reputation_score}/100 ({reader.get_reputation_level()})

📊 Tình trạng: 
   • Đang hoạt động: {'Có' if reader.is_active() else 'Không'}
   • Đã hết hạn: {'Có' if reader.is_expired() else 'Không'}
   • Bị khóa: {'Có' if reader.is_locked() else 'Không'}
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

        # Close button
        ttk.Button(
            main_frame,
            text="Đóng",
            command=detail_window.destroy,
            width=15
        ).pack(pady=(10, 0))

    def _show_statistics(self):
        """Hiển thị thống kê"""
        stats = self.controller.get_statistics()

        # Tạo dialog thống kê
        dialog = tk.Toplevel(self)
        dialog.title("📊 Thống kê bạn đọc")
        dialog.geometry("550x500")
        dialog.resizable(False, False)
        dialog.transient(self)

        # Main frame
        main_frame = ttk.Frame(dialog, padding=20)
        main_frame.pack(fill='both', expand=True)

        # Tiêu đề
        ttk.Label(
            main_frame,
            text="📊 THỐNG KÊ BẠN ĐỌC",
            font=('Arial', 16, 'bold'),
            foreground='#1976D2'
        ).pack(pady=(0, 20))

        # Tổng quan
        overview_frame = ttk.LabelFrame(main_frame, text="📈 Tổng quan", padding=15)
        overview_frame.pack(fill='x', pady=10)

        overview_text = f"""
📚 Tổng số bạn đọc: {stats['total']}
🟢 Đang hoạt động: {stats['active']}
🔴 Hết hạn: {stats['expired']}
🔒 Bị khóa: {stats['locked']}
⏰ Sắp hết hạn (30 ngày): {stats['expiring_soon']}
"""
        ttk.Label(overview_frame, text=overview_text, font=('Arial', 10)).pack(anchor='w')

        # Điểm uy tín
        rep_frame = ttk.LabelFrame(main_frame, text="⭐ Điểm uy tín", padding=15)
        rep_frame.pack(fill='x', pady=10)

        rep_text = f"""
📊 Điểm trung bình: {stats['avg_reputation']:. 2f}/100
⭐ Xuất sắc (≥90): {stats['high_reputation']} bạn đọc
❌ Kém (<50): {stats['low_reputation']} bạn đọc
"""
        ttk.Label(rep_frame, text=rep_text, font=('Arial', 10)).pack(anchor='w')

        # Biểu đồ đơn giản
        chart_frame = ttk.LabelFrame(main_frame, text="📊 Biểu đồ trạng thái", padding=15)
        chart_frame.pack(fill='x', pady=10)

        total = stats['total'] or 1  # Tránh chia cho 0

        canvas = tk.Canvas(chart_frame, height=100, bg='white')
        canvas.pack(fill='x')

        # Vẽ bar chart đơn giản
        colors = {'active': '#4CAF50', 'expired': '#F44336', 'locked': '#FF9800'}
        x = 50
        for key, color in colors.items():
            count = stats[key]
            width = (count / total) * 400 if total > 0 else 0
            canvas.create_rectangle(x, 20, x + width, 50, fill=color)
            canvas.create_text(x + width / 2, 35, text=str(count), fill='white', font=('Arial', 10, 'bold'))
            canvas.create_text(x + width / 2, 70, text=key.capitalize(), font=('Arial', 9))
            x += 150

        # Buttons
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=(20, 0))

        ttk.Button(
            btn_frame,
            text="🔄 Cập nhật tự động thẻ HH",
            command=lambda: self._auto_update_and_refresh(dialog),
            width=25
        ).pack(side='left', padx=5)

        ttk.Button(
            btn_frame,
            text="Đóng",
            command=dialog.destroy,
            width=15
        ).pack(side='left', padx=5)

    def _auto_update_and_refresh(self, dialog):
        """Tự động cập nhật thẻ hết hạn và refresh"""
        if self.controller.auto_update_expired(parent=dialog):
            dialog.destroy()
            self._load_data()
            self._show_statistics()

    def _export_json(self):
        """Xuất dữ liệu ra JSON"""
        self.controller.export_json(self.current_readers, parent=self)

    def _export_csv(self):
        """Xuất dữ liệu ra CSV"""
        self.controller.export_csv(self.current_readers, parent=self)

    def _export_excel(self):
        """Xuất dữ liệu ra Excel"""
        self.controller.export_excel(self.current_readers, parent=self)

    def _export_pdf(self):
        """Xuất dữ liệu ra PDF"""
        self.controller.export_pdf(self.current_readers, parent=self)