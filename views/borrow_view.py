import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from controllers.borrow_controller import BorrowController
from datetime import datetime


class BorrowView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.controller = BorrowController()
        self.selected_slip_id = None  # Lưu slip đang chọn
        self._create_ui()
        self._load_borrows()  # Load dữ liệu ngay khi tạo view

    def _create_ui(self):
        ttk.Label(self, text="📋 Quản lý Mượn / Trả sách", font=("Arial", 16, "bold")).pack(pady=10)

        form = ttk.Frame(self)
        form.pack(pady=10, fill="x")

        # -----------------------
        # Form thông tin phiếu
        # -----------------------
        ttk.Label(form, text="Tên Bạn đọc:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.reader_entry = ttk.Entry(form, width=30)
        self.reader_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form, text="Tên Sách:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.book_entry = ttk.Entry(form, width=30)
        self.book_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(form, text="Ngày mượn:").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.borrow_date_entry = DateEntry(form, width=15, date_pattern="yyyy-mm-dd")
        self.borrow_date_entry.set_date(datetime.now())  # Mặc định là hôm nay khi tạo
        self.borrow_date_entry.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(form, text="Ngày trả:").grid(row=1, column=2, sticky="w", padx=5, pady=5)
        self.return_date_entry = DateEntry(form, width=15, date_pattern="yyyy-mm-dd")
        self.return_date_entry.set_date(datetime.now())  # Để trống mặc định
        self.return_date_entry.grid(row=1, column=3, padx=5, pady=5)

        # -----------------------
        # Nút hành động
        # -----------------------
        ttk.Button(form, text="📥 Tạo phiếu mượn", command=self._create_borrow).grid(row=2, column=0, pady=10)
        ttk.Button(form, text="💾 Cập nhật", command=self._update_borrow).grid(row=2, column=1, pady=10)
        ttk.Button(form, text="📤 Trả sách", command=self._return_borrow).grid(row=2, column=2, pady=10)
        ttk.Button(form, text="🔄 Reset", command=self._reset_form).grid(row=2, column=3, pady=10)

        # -----------------------
        # Treeview hiển thị phiếu mượn/trả
        # -----------------------
        columns = ("slip_id", "reader_name", "book_name", "borrow_date", "return_due", "return_date", "status")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col.replace("_", " ").title())
            self.tree.column(col, width=100)
        self.tree.pack(pady=20, fill="x")

        self.tree.bind("<Double-1>", self._on_row_click)

    # -----------------------
    # Load dữ liệu phiếu mượn/trả
    # -----------------------
    def _load_borrows(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        borrows = self.controller.get_all_borrows()
        for b in borrows:
            self.tree.insert("", "end", values=(
                b["slip_id"],
                b["full_name"],
                b["book_name"],
                b["borrow_date"],
                b["return_due"],
                b["return_date"] if b["return_date"] else "",
                b["status"]
            ))

    # -----------------------
    # Reset form
    # -----------------------
    def _reset_form(self):
        self.selected_slip_id = None
        self.reader_entry.delete(0, tk.END)
        self.book_entry.delete(0, tk.END)
        self.borrow_date_entry.set_date("")
        self.return_date_entry.set_date("")

    # -----------------------
    # Tạo phiếu mượn
    # -----------------------
    def _create_borrow(self):
        reader_name = self.reader_entry.get().strip()
        book_name = self.book_entry.get().strip()

        if not reader_name or not book_name:
            messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đầy đủ tên bạn đọc và sách")
            return

        success, msg = self.controller.create_borrow_by_name(
            reader_name=reader_name,
            book_name=book_name,
        )
        messagebox.showinfo("Kết quả", msg)
        if success:
            self._reset_form()
            self._load_borrows()

    # -----------------------
    # Cập nhật phiếu mượn
    # -----------------------
    def _update_borrow(self):
        if not self.selected_slip_id:
            messagebox.showwarning("Chưa chọn", "Vui lòng chọn phiếu để cập nhật")
            return

        borrow_date = self.borrow_date_entry.get_date()
        return_date = self.return_date_entry.get_date()
        status = "BORROWING"
        if return_date:
            status = "RETURNED"

        success, msg = self.controller.update_borrow(
            slip_id=self.selected_slip_id,
            borrow_date=borrow_date,
            return_date=return_date,
            status=status
        )
        messagebox.showinfo("Kết quả", msg)
        if success:
            self._reset_form()
            self._load_borrows()

    # -----------------------
    # Trả sách
    # -----------------------
    def _return_borrow(self):
        if not self.selected_slip_id:
            messagebox.showwarning("Chưa chọn", "Vui lòng chọn phiếu để trả sách")
            return

        success, msg = self.controller.return_books(self.selected_slip_id)
        messagebox.showinfo("Kết quả", msg)
        if success:
            self._reset_form()
            self._load_borrows()

    # -----------------------
    # Khi click vào row
    # -----------------------
    def _on_row_click(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        item = self.tree.item(selected[0])
        values = item["values"]

        self.selected_slip_id = values[0]
        self.reader_entry.delete(0, tk.END)
        self.reader_entry.insert(0, values[1])
        self.book_entry.delete(0, tk.END)
        self.book_entry.insert(0, values[2])
        self.borrow_date_entry.set_date(values[3])
        self.return_date_entry.set_date(values[5] if values[5] else "")
