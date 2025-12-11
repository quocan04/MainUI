import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
from typing import Optional

from models.reader import Reader, get_all_statuses


class ReaderDialog(tk.Toplevel):
    """Dialog thêm/sửa bạn đọc"""

    def __init__(self, parent, title="Bạn đọc", reader: Optional[Reader] = None):
        super().__init__(parent)
        self.title(title)
        self.geometry("600x750")
        self.resizable(False, False)

        self.reader = reader
        self.result: Optional[Reader] = None
        self.is_edit_mode = reader is not None

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
        title_text = f"{icon} {'CẬP NHẬT' if self.is_edit_mode else 'THÊM MỚI'} BẠN ĐỌC"

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

        # ========== FORM FIELDS ==========

        # Họ tên *
        self._create_field_label(scrollable_frame, 0, "Họ tên:", required=True)
        self.full_name_var = tk.StringVar()
        self.full_name_entry = ttk.Entry(
            scrollable_frame,
            textvariable=self.full_name_var,
            width=40,
            font=('Arial', 10)
        )
        self.full_name_entry.grid(row=0, column=1, sticky='w', pady=8, padx=(0, 10))
        self.full_name_entry.focus()

        # Số điện thoại
        self._create_field_label(scrollable_frame, 1, "Số điện thoại:")
        self.phone_var = tk.StringVar()
        ttk.Entry(
            scrollable_frame,
            textvariable=self.phone_var,
            width=40,
            font=('Arial', 10)
        ).grid(row=1, column=1, sticky='w', pady=8, padx=(0, 10))

        # Email
        self._create_field_label(scrollable_frame, 2, "Email:")
        self.email_var = tk.StringVar()
        ttk.Entry(
            scrollable_frame,
            textvariable=self.email_var,
            width=40,
            font=('Arial', 10)
        ).grid(row=2, column=1, sticky='w', pady=8, padx=(0, 10))

        # Địa chỉ
        self._create_field_label(scrollable_frame, 3, "Địa chỉ:")
        self.address_text = tk.Text(
            scrollable_frame,
            width=40,
            height=3,
            font=('Arial', 10),
            wrap='word'
        )
        self.address_text.grid(row=3, column=1, sticky='w', pady=8, padx=(0, 10))

        # Separator
        ttk.Separator(scrollable_frame, orient='horizontal').grid(
            row=4, column=0, columnspan=2, sticky='ew', pady=15
        )

        # Ngày cấp thẻ
        self._create_field_label(scrollable_frame, 5, "Ngày cấp thẻ:")
        date_frame1 = ttk.Frame(scrollable_frame)
        date_frame1.grid(row=5, column=1, sticky='w', pady=8)

        self.card_start_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        ttk.Entry(
            date_frame1,
            textvariable=self.card_start_var,
            width=20,
            font=('Arial', 10)
        ).pack(side='left', padx=(0, 5))

        ttk.Button(
            date_frame1,
            text="Hôm nay",
            command=lambda: self.card_start_var.set(datetime.now().strftime("%Y-%m-%d")),
            width=10
        ).pack(side='left')

        # Ngày hết hạn
        self._create_field_label(scrollable_frame, 6, "Ngày hết hạn:")
        date_frame2 = ttk.Frame(scrollable_frame)
        date_frame2.grid(row=6, column=1, sticky='w', pady=8)

        default_end = (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d")
        self.card_end_var = tk.StringVar(value=default_end)
        ttk.Entry(
            date_frame2,
            textvariable=self.card_end_var,
            width=20,
            font=('Arial', 10)
        ).pack(side='left', padx=(0, 5))

        # ✅ FIX:  Nút +1 năm
        ttk.Button(
            date_frame2,
            text="+1 năm",
            command=self._add_one_year_to_card_end,
            width=10
        ).pack(side='left')

        # Separator
        ttk.Separator(scrollable_frame, orient='horizontal').grid(
            row=7, column=0, columnspan=2, sticky='ew', pady=15
        )

        # Trạng thái
        self._create_field_label(scrollable_frame, 8, "Trạng thái:")
        self.status_var = tk.StringVar(value="ACTIVE")
        status_combo = ttk.Combobox(
            scrollable_frame,
            textvariable=self.status_var,
            values=get_all_statuses(),
            state='readonly',
            width=37,
            font=('Arial', 10)
        )
        status_combo.grid(row=8, column=1, sticky='w', pady=8, padx=(0, 10))

        # Điểm uy tín
        self._create_field_label(scrollable_frame, 9, "Điểm uy tín:")
        reputation_frame = ttk.Frame(scrollable_frame)
        reputation_frame.grid(row=9, column=1, sticky='w', pady=8)

        self.reputation_var = tk.IntVar(value=100)
        ttk.Spinbox(
            reputation_frame,
            from_=0,
            to=100,
            textvariable=self.reputation_var,
            width=10,
            font=('Arial', 10)
        ).pack(side='left', padx=(0, 5))

        ttk.Label(
            reputation_frame,
            text="/100",
            font=('Arial', 10)
        ).pack(side='left', padx=(0, 10))

        # Progress bar cho reputation
        self.reputation_progress = ttk.Progressbar(
            reputation_frame,
            length=150,
            mode='determinate',
            maximum=100
        )
        self.reputation_progress.pack(side='left')
        self.reputation_progress['value'] = 100

        # Bind để update progress bar
        self.reputation_var.trace('w', self._update_reputation_progress)

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

    def _update_reputation_progress(self, *args):
        """Update progress bar khi điểm uy tín thay đổi"""
        try:
            value = self.reputation_var.get()
            self.reputation_progress['value'] = value
        except:
            pass

    def _add_one_year_to_card_end(self):
        """✅ FIX: Cộng 1 năm vào ngày hết hạn dựa trên ngày cấp thẻ"""
        try:
            # Lấy ngày cấp thẻ
            card_start = self.card_start_var.get().strip()

            if not card_start:
                # Nếu chưa có ngày cấp thẻ, dùng hôm nay
                base_date = datetime.now()
            else:
                # Parse ngày cấp thẻ
                base_date = datetime.strptime(card_start, "%Y-%m-%d")

            # Cộng 365 ngày
            new_end = base_date + timedelta(days=365)

            # Set vào field
            self.card_end_var.set(new_end.strftime("%Y-%m-%d"))

        except ValueError:
            # Nếu ngày cấp thẻ không hợp lệ, dùng hôm nay + 1 năm
            new_end = datetime.now() + timedelta(days=365)
            self.card_end_var.set(new_end.strftime("%Y-%m-%d"))

    def _fill_data(self):
        """Điền dữ liệu khi sửa"""
        if not self.reader:
            return

        self.full_name_var.set(self.reader.full_name or '')
        self.phone_var.set(self.reader.phone or '')
        self.email_var.set(self.reader.email or '')

        if self.reader.address:
            self.address_text.delete('1.0', 'end')
            self.address_text.insert('1.0', self.reader.address)

        self.card_start_var.set(self.reader.card_start or '')
        self.card_end_var.set(self.reader.card_end or '')
        self.status_var.set(self.reader.status or 'ACTIVE')
        self.reputation_var.set(self.reader.reputation_score or 100)

    def _save(self):
        """Lưu dữ liệu"""
        # Lấy dữ liệu từ form
        full_name = self.full_name_var.get().strip()
        phone = self.phone_var.get().strip()
        email = self.email_var.get().strip()
        address = self.address_text.get('1.0', 'end').strip()
        card_start = self.card_start_var.get().strip()
        card_end = self.card_end_var.get().strip()
        status = self.status_var.get()
        reputation = self.reputation_var.get()

        # Validate cơ bản
        if not full_name:
            from utils.messagebox_helper import MessageBoxHelper
            MessageBoxHelper.show_error("Lỗi", "Vui lòng nhập họ tên", parent=self)
            self.full_name_entry.focus()
            return

        # Tạo Reader object
        reader = Reader(
            full_name=full_name,
            phone=phone if phone else None,
            email=email if email else None,
            address=address if address else None,
            card_start=card_start if card_start else None,
            card_end=card_end if card_end else None,
            status=status,
            reputation_score=reputation
        )

        # Nếu là edit mode, giữ lại ID
        if self.is_edit_mode and self.reader:
            reader.reader_id = self.reader.reader_id

        self.result = reader
        self.destroy()