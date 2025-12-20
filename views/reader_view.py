import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional, List
import logging
from utils.html_report_helper import HTMLReportHelper

from models.reader import Reader, get_all_statuses, get_status_display_map
from controllers.reader_controller import ReaderController
from views.reader_dialog import ReaderDialog
from utils.messagebox_helper import MessageBoxHelper

logger = logging.getLogger(__name__)


class ReaderView(ttk.Frame):
    """Giao diện quản lý bạn đọc - Enhanced Version"""

    def __init__(self, parent):
        super().__init__(parent)
        self.controller = ReaderController()
        self.msg_helper = MessageBoxHelper()
        self.current_readers: List[Reader] = []
        self.selected_reader: Optional[Reader] = None
        self.search_after_id = None  # For debouncing

        self._create_widgets()
        self._load_data()

        # Auto-refresh every 5 minutes
        self._schedule_auto_refresh()

    def _create_widgets(self):
        """Tạo giao diện"""
        # ========== TOOLBAR ==========
        toolbar = ttk.Frame(self, relief='raised', borderwidth=1)
        toolbar.pack(fill='x', padx=5, pady=5)

        # Left buttons - CRUD
        left_frame = ttk.Frame(toolbar)
        left_frame.pack(side='left')

        # Thêm mới
        self.btn_add = ttk.Button(
            left_frame,
            text="➕ Thêm mới (Ctrl+N)",
            command=self._show_add_dialog,
            width=18
        )
        self.btn_add.pack(side='left', padx=2, pady=3)

        # Sửa
        self.btn_edit = ttk.Button(
            left_frame,
            text="✏️ Sửa (Enter)",
            command=self._show_edit_dialog,
            width=15,
            state='disabled'
        )
        self.btn_edit.pack(side='left', padx=2, pady=3)

        # Xóa
        self.btn_delete = ttk.Button(
            left_frame,
            text="🗑️ Xóa (Delete)",
            command=self._delete_reader,
            width=15,
            state='disabled'
        )
        self.btn_delete.pack(side='left', padx=2, pady=3)

        ttk.Separator(left_frame, orient='vertical').pack(side='left', fill='y', padx=5)

        # Làm mới
        ttk.Button(
            left_frame,
            text="🔄 Làm mới (F5)",
            command=self._load_data,
            width=15
        ).pack(side='left', padx=2, pady=3)

        # Thống kê
        ttk.Button(
            left_frame,
            text="📊 Thống kê",
            command=self._show_statistics,
            width=12
        ).pack(side='left', padx=2, pady=3)

        # Xem chi tiết
        self.btn_detail = ttk.Button(
            left_frame,
            text="ℹ️ Chi tiết",
            command=self._show_detail,
            width=12,
            state='disabled'
        )
        self.btn_detail.pack(side='left', padx=2, pady=3)

        # Right buttons - Export
        right_frame = ttk.Frame(toolbar)
        right_frame.pack(side='right')

        ttk.Label(right_frame, text="📤 Xuất:", font=('Arial', 9, 'bold')).pack(side='left', padx=5)

        ttk.Button(
            right_frame,
            text="JSON",
            command=self._export_json,
            width=8
        ).pack(side='left', padx=2, pady=3)

        ttk.Button(
            right_frame,
            text="CSV",
            command=self._export_csv,
            width=8
        ).pack(side='left', padx=2, pady=3)

        ttk.Button(
            right_frame,
            text="Excel",
            command=self._export_excel,
            width=8
        ).pack(side='left', padx=2, pady=3)

        ttk.Button(
            right_frame,
            text="PDF",
            command=self._export_pdf,
            width=8
        ).pack(side='left', padx=2, pady=3)

        # ========== SEARCH & FILTER FRAME ==========
        search_frame = ttk.LabelFrame(self, text="🔍 Tìm kiếm & Lọc nâng cao", padding=10)
        search_frame.pack(fill='x', padx=5, pady=5)

        # Row 1: Tìm kiếm
        row1 = ttk.Frame(search_frame)
        row1.pack(fill='x', pady=5)

        ttk.Label(row1, text="🔎 Từ khóa:", font=('Arial', 9, 'bold')).pack(side='left', padx=(0, 5))

        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(row1, textvariable=self.search_var, width=35, font=('Arial', 10))
        self.search_entry.pack(side='left', padx=(0, 5))
        self.search_entry.bind('<Return>', lambda e: self._search())
        self.search_entry.bind('<KeyRelease>', self._on_search_key_release)

        ttk.Label(row1, text="Tìm theo:", font=('Arial', 9)).pack(side='left', padx=(15, 5))

        self.search_by_var = tk.StringVar(value="all")
        search_by_combo = ttk.Combobox(
            row1,
            textvariable=self.search_by_var,
            values=["all", "name", "phone", "email", "address"],
            state='readonly',
            width=15,
            font=('Arial', 9)
        )
        search_by_combo.pack(side='left', padx=(0, 5))

        ttk.Button(
            row1,
            text="🔍 Tìm",
            command=self._search,
            width=10
        ).pack(side='left', padx=5)

        ttk.Button(
            row1,
            text="↺ Xóa",
            command=self._reset_search,
            width=10
        ).pack(side='left', padx=2)

        # Search result label
        self.search_result_label = ttk.Label(row1, text="", font=('Arial', 9), foreground='#1976D2')
        self.search_result_label.pack(side='left', padx=10)

        # Row 2: Lọc
        row2 = ttk.Frame(search_frame)
        row2.pack(fill='x', pady=5)

        ttk.Label(row2, text="📋 Trạng thái:", font=('Arial', 9, 'bold')).pack(side='left', padx=(0, 5))

        self.filter_status_var = tk.StringVar(value="Tất cả")
        ttk.Combobox(
            row2,
            textvariable=self.filter_status_var,
            values=["Tất cả"] + get_all_statuses(),
            state='readonly',
            width=15,
            font=('Arial', 9)
        ).pack(side='left', padx=(0, 5))

        ttk.Label(row2, text="⭐ Điểm uy tín:", font=('Arial', 9, 'bold')).pack(side='left', padx=(15, 5))

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
            text="⚠️ Sắp hết hạn (30 ngày)",
            variable=self.filter_expiring_var,
            onvalue=True,
            offvalue=False
        ).pack(side='left', padx=(15, 5))

        ttk.Button(
            row2,
            text="🔎 Áp dụng lọc",
            command=self._filter,
            width=13
        ).pack(side='left', padx=5)

        ttk.Button(
            row2,
            text="🔃 Xóa lọc",
            command=self._reset_filter,
            width=12
        ).pack(side='left', padx=2)

        # Row 3: Quick filters (preset filters)
        row3 = ttk.Frame(search_frame)
        row3.pack(fill='x', pady=5)

        ttk.Label(row3, text="🚀 Lọc nhanh:", font=('Arial', 9, 'bold')).pack(side='left', padx=(0, 10))

        ttk.Button(
            row3,
            text="🟢 Đang hoạt động",
            command=lambda: self._quick_filter('ACTIVE'),
            width=15
        ).pack(side='left', padx=2)

        ttk.Button(
            row3,
            text="🔴 Hết hạn",
            command=lambda: self._quick_filter('EXPIRED'),
            width=12
        ).pack(side='left', padx=2)

        ttk.Button(
            row3,
            text="🔒 Đã khóa",
            command=lambda: self._quick_filter('LOCKED'),
            width=12
        ).pack(side='left', padx=2)

        ttk.Button(
            row3,
            text="⭐ Uy tín cao (≥90)",
            command=self._filter_high_reputation,
            width=17
        ).pack(side='left', padx=2)

        ttk.Button(
            row3,
            text="❌ Uy tín thấp (<50)",
            command=self._filter_low_reputation,
            width=17
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

        # Định nghĩa columns với sorting
        for col in columns:
            self.tree.heading(col, text=col, command=lambda c=col: self._sort_column(c))

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
        self.context_menu.add_command(label="ℹ️ Chi tiết", command=self._show_detail)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="🔒 Khóa", command=self._lock_reader)
        self.context_menu.add_command(label="🔓 Mở khóa", command=self._unlock_reader)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="📅 Gia hạn thẻ", command=self._extend_card)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="🔄 Làm mới", command=self._load_data)

        # Bind events
        self.tree.bind('<<TreeviewSelect>>', self._on_select)
        self.tree.bind('<Double-1>', lambda e: self._show_edit_dialog())
        self.tree.bind('<Button-3>', self._show_context_menu)
        self.tree.bind('<Delete>', lambda e: self._delete_reader())
        self.tree.bind('<Return>', lambda e: self._show_edit_dialog())

        # ========== DETAIL FRAME ==========
        detail_frame = ttk.LabelFrame(self, text="ℹ️ Thông tin chi tiết", padding=10)
        detail_frame.pack(fill='x', padx=5, pady=5)

        self.detail_text = tk.Text(
            detail_frame,
            height=4,
            wrap='word',
            font=('Consolas', 9),
            state='disabled',
            background='#f9f9f9',
            relief='flat'
        )
        self.detail_text.pack(fill='x')

        # ========== STATUS BAR ==========
        status_bar = ttk.Frame(self, relief='sunken', borderwidth=1)
        status_bar.pack(fill='x', padx=5, pady=2)

        self.status_label = ttk.Label(
            status_bar,
            text="✅ Sẵn sàng",
            font=('Arial', 9)
        )
        self.status_label.pack(side='left', padx=5)

        self.count_label = ttk.Label(
            status_bar,
            text="Tổng: 0 bạn đọc",
            font=('Arial', 9, 'bold'),
            foreground='#1976D2'
        )
        self.count_label.pack(side='right', padx=5)

        # Selected count label
        self.selected_label = ttk.Label(
            status_bar,
            text="",
            font=('Arial', 9),
            foreground='#666'
        )
        self.selected_label.pack(side='right', padx=10)

        # Keyboard shortcuts
        self.bind_all('<Control-n>', lambda e: self._show_add_dialog())
        self.bind_all('<F5>', lambda e: self._load_data())
        self.bind_all('<Control-f>', lambda e: self.search_entry.focus())

    def _load_data(self):
        """Load dữ liệu từ database"""
        try:
            self.status_label.config(text="⏳ Đang tải dữ liệu...")
            self.update_idletasks()

            self.current_readers = self.controller.get_all_readers()
            self._populate_tree(self.current_readers)

            self.status_label.config(text=f"✅ Đã tải {len(self.current_readers)} bạn đọc")
            self.search_result_label.config(text="")

            logger.info(f"Loaded {len(self.current_readers)} readers")
        except Exception as e:
            self.status_label.config(text="❌ Lỗi tải dữ liệu")
            self.msg_helper.show_error("Lỗi", f"Không thể tải dữ liệu: {str(e)}", parent=self)
            logger.error(f"Error loading data: {e}")

    def _populate_tree(self, readers: List[Reader]):
        """Hiển thị dữ liệu lên Treeview"""
        # Xóa dữ liệu cũ
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Thêm dữ liệu mới
        for reader in readers:
            days_left = reader.get_days_until_expiry()
            days_display = str(days_left) if days_left is not None else "N/A"

            values = (
                reader.reader_id,
                reader.full_name or '',
                reader.phone or 'N/A',
                reader.email or 'N/A',
                (reader.address or 'N/A')[:50] + '...' if reader.address and len(reader.address) > 50 else (
                            reader.address or 'N/A'),
                reader.card_start or 'N/A',
                reader.card_end or 'N/A',
                days_display,
                get_status_display_map().get(reader.status, reader.status),
                reader.reputation_score
            )

            # Tags cho màu sắc
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
        self._update_button_states()

    def _on_select(self, event):
        """Xử lý khi chọn 1 dòng"""
        selection = self.tree.selection()
        if selection:
            try:
                item = self.tree.item(selection[0])
                reader_id = item['values'][0]
                self.selected_reader = self.controller.get_reader_by_id(reader_id)

                if self.selected_reader:
                    self._update_detail_panel()
                    self._update_button_states()
                    self.selected_label.config(text=f"✓ Đã chọn: {self.selected_reader.full_name}")
                else:
                    self.selected_reader = None
                    self._update_button_states()
                    self.selected_label.config(text="")
                    self.status_label.config(text="⚠️ Không tìm thấy thông tin bạn đọc")
            except Exception as e:
                logger.error(f"Error in _on_select: {e}")
                self.selected_reader = None
                self._update_button_states()
                self.selected_label.config(text="")
                self.status_label.config(text=f"❌ Lỗi: {str(e)}")
        else:
            self.selected_reader = None
            self._update_button_states()
            self.selected_label.config(text="")

    def _update_button_states(self):
        """Cập nhật trạng thái các button"""
        has_selection = self.selected_reader is not None
        state = 'normal' if has_selection else 'disabled'

        self.btn_edit.config(state=state)
        self.btn_delete.config(state=state)
        self.btn_detail.config(state=state)

    def _update_detail_panel(self):
        """Cập nhật panel chi tiết"""
        self.detail_text.config(state='normal')
        self.detail_text.delete('1.0', 'end')

        if self.selected_reader:
            r = self.selected_reader
            detail = f"""📋 ID: {r.reader_id} | 👤 {r.full_name} | 📞 {r.phone or 'N/A'} | 📧 {r.email or 'N/A'}
📍 Địa chỉ: {r.address or 'N/A'}
📅 Thẻ: {r.card_start} → {r.card_end} | {r.get_card_validity_info()}
🎯 {r.get_status_display()} | ⭐ Uy tín: {r.reputation_score}/100 ({r.get_reputation_level()})"""
            self.detail_text.insert('1.0', detail)

        self.detail_text.config(state='disabled')

    def _show_context_menu(self, event):
        """Hiển thị context menu"""
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)

    def _on_search_key_release(self, event):
        """Auto search với debouncing"""
        if self.search_after_id:
            self.after_cancel(self.search_after_id)
        self.search_after_id = self.after(500, self._search)

    def _search(self):
        """Tìm kiếm bạn đọc"""
        keyword = self.search_var.get().strip()
        search_by = self.search_by_var.get()

        if not keyword:
            self._load_data()
            return

        try:
            self.status_label.config(text=f"🔍 Đang tìm kiếm '{keyword}'...")
            self.update_idletasks()

            readers = self.controller.search_readers(keyword, search_by)
            self._populate_tree(readers)

            if readers:
                self.status_label.config(text=f"✅ Hoàn tất tìm kiếm")
                self.search_result_label.config(
                    text=f"🎯 Tìm thấy {len(readers)} kết quả",
                    foreground='#4CAF50'
                )
            else:
                self.status_label.config(text="⚠️ Không tìm thấy")
                self.search_result_label.config(
                    text="❌ Không có kết quả",
                    foreground='#F44336'
                )
        except Exception as e:
            self.status_label.config(text="❌ Lỗi tìm kiếm")
            self.msg_helper.show_error("Lỗi tìm kiếm", str(e), parent=self)

    def _reset_search(self):
        """Reset tìm kiếm"""
        self.search_var.set("")
        self.search_by_var.set("all")
        self.search_result_label.config(text="")
        self._load_data()

    def _filter(self):
        """Lọc dữ liệu"""
        try:
            self.status_label.config(text="🔎 Đang lọc dữ liệu...")
            self.update_idletasks()

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
            self.status_label.config(text=f"✅ Đã lọc: {len(readers)} kết quả")
            self.search_result_label.config(
                text=f"📊 {len(readers)} bạn đọc phù hợp",
                foreground='#1976D2'
            )
        except Exception as e:
            self.status_label.config(text="❌ Lỗi lọc")
            self.msg_helper.show_error("Lỗi lọc", str(e), parent=self)

    def _reset_filter(self):
        """Reset bộ lọc"""
        self.filter_status_var.set("Tất cả")
        self.filter_min_rep_var.set(0)
        self.filter_max_rep_var.set(100)
        self.filter_expiring_var.set(False)
        self.search_result_label.config(text="")
        self._load_data()

    def _quick_filter(self, status: str):
        """Lọc nhanh theo trạng thái"""
        self.filter_status_var.set(status)
        self.filter_min_rep_var.set(0)
        self.filter_max_rep_var.set(100)
        self.filter_expiring_var.set(False)
        self._filter()

    def _filter_high_reputation(self):
        """Lọc bạn đọc có uy tín cao"""
        self.filter_status_var.set("Tất cả")
        self.filter_min_rep_var.set(90)
        self.filter_max_rep_var.set(100)
        self.filter_expiring_var.set(False)
        self._filter()

    def _filter_low_reputation(self):
        """Lọc bạn đọc có uy tín thấp"""
        self.filter_status_var.set("Tất cả")
        self.filter_min_rep_var.set(0)
        self.filter_max_rep_var.set(49)
        self.filter_expiring_var.set(False)
        self._filter()

    def _sort_column(self, col):
        """Sắp xếp theo cột"""
        # TODO: Implement sorting
        pass

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
        dialog.title("📅 Gia hạn thẻ thư viện")
        dialog.geometry("400x200")
        dialog.resizable(False, False)
        dialog.transient(self)
        dialog.grab_set()

        # Header
        header = tk.Frame(dialog, bg='#1976D2', height=60)
        header.pack(fill='x')
        header.pack_propagate(False)

        tk.Label(
            header,
            text=f"📅 GIA HẠN THẺ",
            font=('Arial', 14, 'bold'),
            fg='white',
            bg='#1976D2'
        ).pack(expand=True)

        # Content
        content = ttk.Frame(dialog, padding=20)
        content.pack(fill='both', expand=True)

        ttk.Label(
            content,
            text=f"Bạn đọc: {self.selected_reader.full_name}",
            font=('Arial', 10, 'bold')
        ).pack(pady=(0, 10))

        ttk.Label(
            content,
            text=f"Ngày hết hạn hiện tại: {self.selected_reader.card_end}",
            font=('Arial', 9)
        ).pack(pady=(0, 15))

        # Days input
        days_frame = ttk.Frame(content)
        days_frame.pack(pady=10)

        ttk.Label(days_frame, text="Số ngày gia hạn:", font=('Arial', 10)).pack(side='left', padx=(0, 10))
        days_var = tk.IntVar(value=365)
        ttk.Spinbox(
            days_frame,
            from_=1,
            to=3650,
            textvariable=days_var,
            width=12,
            font=('Arial', 10)
        ).pack(side='left')

        # Buttons
        btn_frame = ttk.Frame(content)
        btn_frame.pack(pady=15)

        def do_extend():
            if self.controller.extend_card(self.selected_reader.reader_id, days_var.get(), parent=self):
                self._load_data()
                dialog.destroy()

        ttk.Button(
            btn_frame,
            text="✅ Xác nhận",
            command=do_extend,
            width=12
        ).pack(side='left', padx=5)

        ttk.Button(
            btn_frame,
            text="❌ Hủy",
            command=dialog.destroy,
            width=12
        ).pack(side='left', padx=5)

    def _show_detail(self):
        """Hiển thị chi tiết đầy đủ"""
        if not self.selected_reader:
            self.msg_helper.show_warning("Chưa chọn", "Vui lòng chọn bạn đọc", parent=self)
            return

        reader = self.selected_reader

        detail_window = tk.Toplevel(self)
        detail_window.title(f"ℹ️ Chi tiết - {reader.full_name}")
        detail_window.geometry("650x550")
        detail_window.transient(self)
        detail_window.grab_set()

        # Header
        header = tk.Frame(detail_window, bg='#1976D2', height=80)
        header.pack(fill='x')
        header.pack_propagate(False)

        tk.Label(
            header,
            text=f"📋 THÔNG TIN CHI TIẾT BẠN ĐỌC",
            font=('Arial', 16, 'bold'),
            fg='white',
            bg='#1976D2'
        ).pack(expand=True)

        # Main content
        main_frame = ttk.Frame(detail_window, padding=20)
        main_frame.pack(fill='both', expand=True)

        # Info sections
        sections = [
            ("👤 Thông tin cá nhân", [
                f"🆔 Mã bạn đọc: {reader.reader_id}",
                f"👤 Họ và tên: {reader.full_name}",
                f"📞 Điện thoại: {reader.phone or 'Chưa cập nhật'}",
                f"📧 Email: {reader.email or 'Chưa cập nhật'}",
                f"📍 Địa chỉ: {reader.address or 'Chưa cập nhật'}"
            ]),
            ("📇 Thông tin thẻ", [
                f"📅 Ngày cấp thẻ: {reader.card_start}",
                f"📅 Ngày hết hạn: {reader.card_end}",
                f"⏰ Tình trạng: {reader.get_card_validity_info()}",
                f"📊 Số ngày còn lại: {reader.get_days_until_expiry() if reader.get_days_until_expiry() is not None else 'N/A'}"
            ]),
            ("⚙️ Trạng thái tài khoản", [
                f"🎯 Trạng thái: {reader.get_status_display()}",
                f"⭐ Điểm uy tín: {reader.reputation_score}/100",
                f"🏆 Xếp loại: {reader.get_reputation_level()}",
                f"✓ Đang hoạt động: {'Có' if reader.is_active() else 'Không'}",
                f"⚠ Đã hết hạn: {'Có' if reader.is_expired() else 'Không'}",
                f"🔒 Bị khóa: {'Có' if reader.is_locked() else 'Không'}"
            ])
        ]

        for section_title, items in sections:
            section_frame = ttk.LabelFrame(main_frame, text=section_title, padding=15)
            section_frame.pack(fill='x', pady=10)

            for item in items:
                ttk.Label(
                    section_frame,
                    text=item,
                    font=('Arial', 10)
                ).pack(anchor='w', pady=3)

        # Action buttons
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=15)

        ttk.Button(
            btn_frame,
            text="✏️ Sửa",
            command=lambda: [detail_window.destroy(), self._show_edit_dialog()],
            width=15
        ).pack(side='left', padx=5)

        ttk.Button(
            btn_frame,
            text="📅 Gia hạn",
            command=lambda: [detail_window.destroy(), self._extend_card()],
            width=15
        ).pack(side='left', padx=5)

        ttk.Button(
            btn_frame,
            text="❌ Đóng",
            command=detail_window.destroy,
            width=15
        ).pack(side='left', padx=5)

    def _show_statistics(self):
        """Hiển thị thống kê nâng cao - Xuất lên web"""
        try:
            # Lấy dữ liệu thống kê
            stats = self.controller.get_statistics()

            # Hiển thị loading
            self.status_label.config(text="⏳ Đang tạo báo cáo...")
            self.update_idletasks()

            # Tạo báo cáo HTML
            html_helper = HTMLReportHelper()
            report_path = html_helper.create_reader_statistics_report(stats, self.current_readers)

            # Mở trong trình duyệt
            if html_helper.open_report_in_browser(report_path):
                self.status_label.config(text=f"✅ Đã mở báo cáo trong trình duyệt")
                self.msg_helper.show_success(
                    f"Báo cáo đã được tạo thành công!\n\n"
                    f"File: {report_path}\n\n"
                    f"Báo cáo đã được mở trong trình duyệt web của bạn.",
                    parent=self
                )
            else:
                self.status_label.config(text="⚠️ Đã tạo báo cáo nhưng không thể mở trình duyệt")
                self.msg_helper.show_warning(
                    "Thông báo",
                    f"Báo cáo đã được tạo tại:\n{report_path}\n\n"
                    f"Vui lòng mở file thủ công trong trình duyệt.",
                    parent=self
                )

        except Exception as e:
            logger.error(f"❌ Lỗi tạo báo cáo: {e}")
            self.status_label.config(text="❌ Lỗi tạo báo cáo")
            self.msg_helper.show_error(
                "Lỗi",
                f"Không thể tạo báo cáo thống kê:\n\n{str(e)}",
                parent=self
            )

    def _auto_update_and_refresh(self, dialog):
        """Tự động cập nhật thẻ hết hạn"""
        if self.controller.auto_update_expired(parent=dialog):
            dialog.destroy()
            self._load_data()
            self._show_statistics()

    def _export_statistics_report(self):
        """Xuất báo cáo thống kê"""
        self.msg_helper.show_info(
            "Xuất báo cáo",
            "Tính năng xuất báo cáo thống kê đang được phát triển",
            parent=self
        )

    def _export_json(self):
        """Xuất dữ liệu ra JSON"""
        if self.controller.export_json(self.current_readers, parent=self):
            self.status_label.config(text="✅ Đã xuất JSON thành công")

    def _export_csv(self):
        """Xuất dữ liệu ra CSV"""
        if self.controller.export_csv(self.current_readers, parent=self):
            self.status_label.config(text="✅ Đã xuất CSV thành công")

    def _export_excel(self):
        """Xuất dữ liệu ra Excel"""
        if self.controller.export_excel(self.current_readers, parent=self):
            self.status_label.config(text="✅ Đã xuất Excel thành công")

    def _export_pdf(self):
        """Xuất dữ liệu ra PDF"""
        if self.controller.export_pdf(self.current_readers, parent=self):
            self.status_label.config(text="✅ Đã xuất PDF thành công")

    def _schedule_auto_refresh(self):
        """Lên lịch auto-refresh mỗi 5 phút"""
        self._load_data()
        self.after(300000, self._schedule_auto_refresh)  # 5 minutes