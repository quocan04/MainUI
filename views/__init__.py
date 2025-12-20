"""Views package"""
# from .main_window import MainWindow
from .reader_view import ReaderView
from .reader_dialog import ReaderDialog
from .staff_login_view import StaffLoginView
from .staff_view import StaffView

__all__ = ['ReaderView', 'ReaderDialog', 'borrow_view', 'book_view','book_dialog','report_view', 'system_view', 'StaffView', 'StaffLoginView', 'penalty_view']