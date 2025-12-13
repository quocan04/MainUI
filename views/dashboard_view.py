"""
Dashboard View - Trang chủ chính của hệ thống
"""
import tkinter as tk
from tkinter import ttk
from datetime import datetime
import logging

from controllers.reader_controller import ReaderController

logger = logging.getLogger(__name__)


class DashboardView(ttk.Frame):
    """View trang chủ Dashboard"""

    def __init__(self, parent, navigate_callback):
        super().__init__(parent)
        self.navigate_callback = navigate_callback
        self.reader_controller = ReaderController()

        # Statistics variables
        self.stats_labels = {}

        self._create_widgets()
        self._load_statistics()

        # Auto refresh mỗi 30 giây
        self._schedule_refresh()

    def _create_widgets(self):
        """Tạo giao diện Dashboard"""

        # Header
        header_frame = ttk.Frame(self)
        header_frame.pack(fill='x', padx=20, pady=(20, 10))

        ttk.Label(
            header_frame,
            text="📊 TRANG CHỦ HỆ THỐNG QUẢN LÝ THƯ VIỆN",
            font=('Arial', 20, 'bold'),
            foreground='#1976D2'
        ).pack(anchor='w')

        # Clock label
        self.clock_label = ttk.Label(
            header_frame,
            text="",
            font=('Arial', 10),
            foreground='#666'
        )
        self.clock_label.pack(anchor='w', pady=(5, 0))
        self._update_clock()

        # Main container
        main_container = ttk.Frame(self)
        main_container.pack(fill='both', expand=True, padx=20, pady=10)

        # Statistics Cards (Top)
        self._create_statistics_section(main_container)

        # Quick Access Menu (Middle)
        self._create_quick_access_section(main_container)

        # Recent Activities (Bottom)
        self._create_recent_activities_section(main_container)

    def _create_statistics_section(self, parent):
        """Tạo phần thống kê tổng quan"""
        stats_frame = ttk.LabelFrame(parent, text="📈 Thống kê tổng quan", padding=15)
        stats_frame.pack(fill='x', pady=(0, 15))

        # Container cho các card
        cards_container = ttk.Frame(stats_frame)
        cards_container.pack(fill='x')

        # Statistics data structure
        self.stats_data = [
            {
                "key": "readers",
                "icon": "👥",
                "title": "Bạn đọc",
                "value": "0",
                "color": "#4CAF50",
                "subtext": "Đang hoạt động"
            },
            {
                "key": "books",
                "icon": "📚",
                "title": "Sách",
                "value": "0",
                "color": "#2196F3",
                "subtext": "Tổng số sách"
            },
            {
                "key": "borrowing",
                "icon": "📋",
                "title": "Đang mượn",
                "value": "0",
                "color": "#FF9800",
                "subtext": "Phiếu mượn"
            },
            {
                "key": "expired",
                "icon": "⏰",
                "title": "Sắp hết hạn",
                "value": "0",
                "color": "#F44336",
                "subtext": "Thẻ bạn đọc"
            }
        ]

        for i, stat in enumerate(self.stats_data):
            self._create_stat_card(cards_container, stat, i)

    def _create_stat_card(self, parent, data, column):
        """Tạo card thống kê"""
        card = tk.Frame(parent, bg='white', relief='raised', borderwidth=2)
        card.grid(row=0, column=column, padx=10, pady=10, sticky='nsew')
        parent.columnconfigure(column, weight=1)

        # Click to navigate
        if data['key'] == 'readers':
            card.bind('<Button-1>', lambda e: self.navigate_callback(1))
            card.config(cursor='hand2')

        # Icon
        icon_label = tk.Label(
            card,
            text=data['icon'],
            font=('Arial', 36),
            bg='white'
        )
        icon_label.pack(pady=(15, 5))
        if data['key'] == 'readers':
            icon_label.bind('<Button-1>', lambda e: self.navigate_callback(1))
            icon_label.config(cursor='hand2')

        # Value - Store reference
        value_label = tk.Label(
            card,
            text=data['value'],
            font=('Arial', 28, 'bold'),
            fg=data['color'],
            bg='white'
        )
        value_label.pack()
        self.stats_labels[f"{data['key']}_value"] = value_label
        if data['key'] == 'readers':
            value_label.bind('<Button-1>', lambda e: self.navigate_callback(1))
            value_label.config(cursor='hand2')

        # Title
        title_label = tk.Label(
            card,
            text=data['title'],
            font=('Arial', 12, 'bold'),
            fg='#333',
            bg='white'
        )
        title_label.pack(pady=(5, 0))
        if data['key'] == 'readers':
            title_label.bind('<Button-1>', lambda e: self.navigate_callback(1))
            title_label.config(cursor='hand2')

        # Subtext - Store reference
        subtext_label = tk.Label(
            card,
            text=data['subtext'],
            font=('Arial', 9),
            fg='#666',
            bg='white'
        )
        subtext_label.pack(pady=(0, 15))
        self.stats_labels[f"{data['key']}_subtext"] = subtext_label
        if data['key'] == 'readers':
            subtext_label.bind('<Button-1>', lambda e: self.navigate_callback(1))
            subtext_label.config(cursor='hand2')

        # Hover effect for readers card
        if data['key'] == 'readers':
            def on_enter(e):
                card.config(bg='#f0f0f0')
                icon_label.config(bg='#f0f0f0')
                value_label.config(bg='#f0f0f0')
                title_label.config(bg='#f0f0f0')
                subtext_label.config(bg='#f0f0f0')

            def on_leave(e):
                card.config(bg='white')
                icon_label.config(bg='white')
                value_label.config(bg='white')
                title_label.config(bg='white')
                subtext_label.config(bg='white')

            card.bind('<Enter>', on_enter)
            card.bind('<Leave>', on_leave)
            icon_label.bind('<Enter>', on_enter)
            icon_label.bind('<Leave>', on_leave)
            value_label.bind('<Enter>', on_enter)
            value_label.bind('<Leave>', on_leave)
            title_label.bind('<Enter>', on_enter)
            title_label.bind('<Leave>', on_leave)
            subtext_label.bind('<Enter>', on_enter)
            subtext_label.bind('<Leave>', on_leave)

    def _create_quick_access_section(self, parent):
        """Tạo phần truy cập nhanh"""
        access_frame = ttk.LabelFrame(parent, text="🚀 Truy cập nhanh", padding=15)
        access_frame.pack(fill='both', expand=True, pady=(0, 15))

        # Container cho các nút
        buttons_container = ttk.Frame(access_frame)
        buttons_container.pack(expand=True)

        # Quick access buttons
        buttons = [
            {"text": "👥 Quản lý\nBạn đọc", "color": "#4CAF50", "tab": 1},
            {"text": "📚 Quản lý\nSách", "color": "#2196F3", "tab": 2},
            {"text": "📋 Mượn/Trả\nSách", "color": "#FF9800", "tab": 3},
            {"text": "💰 Quản lý\nPhạt", "color": "#F44336", "tab": 4},
            {"text": "👨‍💼 Quản lý\nNhân viên", "color": "#9C27B0", "tab": 5},
            {"text": "📊 Báo cáo\nThống kê", "color": "#607D8B", "tab": 6}
        ]

        # Tạo grid 2 hàng x 3 cột
        for i, btn in enumerate(buttons):
            row = i // 3
            col = i % 3
            self._create_quick_button(buttons_container, btn, row, col)

    def _create_quick_button(self, parent, data, row, col):
        """Tạo nút truy cập nhanh"""
        btn = tk.Button(
            parent,
            text=data['text'],
            font=('Arial', 12, 'bold'),
            bg=data['color'],
            fg='white',
            activebackground=self._darken_color(data['color']),
            activeforeground='white',
            width=15,
            height=4,
            cursor='hand2',
            relief='flat',
            command=lambda: self.navigate_callback(data['tab'])
        )
        btn.grid(row=row, column=col, padx=15, pady=15, sticky='nsew')
        parent.rowconfigure(row, weight=1)
        parent.columnconfigure(col, weight=1)

        # Hover effect
        def on_enter(e):
            btn['bg'] = self._darken_color(data['color'])

        def on_leave(e):
            btn['bg'] = data['color']

        btn.bind('<Enter>', on_enter)
        btn.bind('<Leave>', on_leave)

    def _create_recent_activities_section(self, parent):
        """Tạo phần hoạt động gần đây"""
        activity_frame = ttk.LabelFrame(parent, text="🕒 Thông tin hệ thống", padding=15)
        activity_frame.pack(fill='both', expand=True)

        # Info container
        info_container = ttk.Frame(activity_frame)
        info_container.pack(fill='both', expand=True)

        # System info
        info_items = [
            ("📅 Ngày khởi động:", datetime.now().strftime('%d/%m/%Y %H:%M:%S')),
            ("👤 Người dùng:", "Administrator"),
            ("💾 Database:", "MySQL - Connected"),
            ("📊 Phiên bản:", "v1.0.0"),
            ("🔄 Trạng thái:", "🟢 Hoạt động bình thường")
        ]

        for i, (label, value) in enumerate(info_items):
            item_frame = ttk.Frame(info_container)
            item_frame.pack(fill='x', pady=8)

            ttk.Label(
                item_frame,
                text=label,
                font=('Arial', 10, 'bold'),
                foreground='#666'
            ).pack(side='left', padx=(0, 10))

            ttk.Label(
                item_frame,
                text=value,
                font=('Arial', 10),
                foreground='#1976D2'
            ).pack(side='left')

        # Refresh button
        refresh_btn = ttk.Button(
            activity_frame,
            text="🔄 Làm mới thống kê",
            command=self._load_statistics
        )
        refresh_btn.pack(pady=(15, 0))

    def _load_statistics(self):
        """Load dữ liệu thống kê từ database"""
        try:
            # Lấy thống kê bạn đọc
            reader_stats = self.reader_controller.get_statistics()

            # Cập nhật số liệu
            total_readers = reader_stats.get('total', 0)
            active_readers = reader_stats.get('active', 0)
            expiring_soon = reader_stats.get('expiring_soon', 0)

            # Update readers card
            if 'readers_value' in self.stats_labels:
                self.stats_labels['readers_value'].config(text=str(total_readers))
            if 'readers_subtext' in self.stats_labels:
                self.stats_labels['readers_subtext'].config(
                    text=f"{active_readers} đang hoạt động"
                )

            # Update expired card
            if 'expired_value' in self.stats_labels:
                self.stats_labels['expired_value'].config(text=str(expiring_soon))
            if 'expired_subtext' in self.stats_labels:
                self.stats_labels['expired_subtext'].config(
                    text=f"Trong 30 ngày tới"
                )

            # TODO: Cập nhật sách và mượn sách khi có controller
            # book_stats = self.book_controller.get_statistics()
            # self.stats_labels['books_value'].config(text=str(book_stats['total']))

            logger.info("✅ Đã cập nhật thống kê Dashboard")

        except Exception as e:
            logger.error(f"❌ Lỗi load thống kê Dashboard: {e}")

    def _update_clock(self):
        """Cập nhật đồng hồ"""
        now = datetime.now()
        weekdays = {
            0: 'Thứ Hai',
            1: 'Thứ Ba',
            2: 'Thứ Tư',
            3: 'Thứ Năm',
            4: 'Thứ Sáu',
            5: 'Thứ Bảy',
            6: 'Chủ Nhật'
        }
        weekday = weekdays[now.weekday()]
        time_str = f"🕐 {weekday}, {now.strftime('%d/%m/%Y - %H:%M:%S')}"
        self.clock_label.config(text=time_str)
        self.after(1000, self._update_clock)

    def _schedule_refresh(self):
        """Lên lịch tự động refresh thống kê"""
        self._load_statistics()
        # Refresh mỗi 30 giây
        self.after(30000, self._schedule_refresh)

    def _darken_color(self, hex_color, factor=0.8):
        """Làm tối màu"""
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
        darkened = tuple(int(c * factor) for c in rgb)
        return f'#{darkened[0]:02x}{darkened[1]:02x}{darkened[2]:02x}'