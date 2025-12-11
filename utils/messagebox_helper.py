import tkinter as tk
from tkinter import messagebox
from typing import Optional


class MessageBoxHelper:
    """Helper class cho các thông báo"""

    @staticmethod
    def show_error(title: str, message: str, parent=None):
        """Hiển thị thông báo lỗi"""
        messagebox.showerror(title, message, parent=parent)

    @staticmethod
    def show_warning(title: str, message: str, parent=None):
        """Hiển thị cảnh báo"""
        messagebox.showwarning(title, message, parent=parent)

    @staticmethod
    def show_info(title: str, message: str, parent=None):
        """Hiển thị thông tin"""
        messagebox.showinfo(title, message, parent=parent)

    @staticmethod
    def show_success(message: str, parent=None):
        """Hiển thị thông báo thành công"""
        messagebox.showinfo("✅ Thành công", message, parent=parent)

    @staticmethod
    def confirm(title: str, message: str, parent=None) -> bool:
        """Hiển thị hộp thoại xác nhận"""
        return messagebox.askyesno(title, message, parent=parent)

    @staticmethod
    def ask_delete(item_name: str = "mục này", parent=None) -> bool:
        """Xác nhận xóa"""
        return messagebox.askyesno(
            "⚠️ Xác nhận xóa",
            f"Bạn có chắc chắn muốn xóa {item_name}?\n\n"
            f"Hành động này không thể hoàn tác! ",
            icon='warning',
            parent=parent
        )

    @staticmethod
    def ask_yes_no(title: str, message: str, parent=None) -> bool:
        """Hỏi Yes/No"""
        return messagebox.askyesno(title, message, parent=parent)

    @staticmethod
    def ask_ok_cancel(title: str, message: str, parent=None) -> bool:
        """Hỏi OK/Cancel"""
        return messagebox.askokcancel(title, message, parent=parent)

    @staticmethod
    def ask_retry_cancel(title: str, message: str, parent=None) -> bool:
        """Hỏi Retry/Cancel"""
        return messagebox.askretrycancel(title, message, parent=parent)