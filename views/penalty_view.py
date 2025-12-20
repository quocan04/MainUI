import tkinter as tk
from tkinter import ttk, messagebox
from controllers.penalty_controller import PenaltyController

class PenaltyView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.controller = PenaltyController()
        self.selected_penalty_id = None
        self._create_ui()
        self._load_penalties()

    # ===================== UI =====================
    def _create_ui(self):
        ttk.Label(
            self,
            text="💸 Quản lý Phiếu Phạt",
            font=("Arial", 16, "bold")
        ).pack(pady=10)

        # Form
        form = ttk.Frame(self)
        form.pack(pady=10, fill="x")

        ttk.Label(form, text="Reader:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.reader_entry = ttk.Entry(form, width=25)
        self.reader_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form, text="Slip ID:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.slip_entry = ttk.Entry(form, width=25)
        self.slip_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(form, text="Book:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.book_entry = ttk.Entry(form, width=25)
        self.book_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(form, text="Loại phạt:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.penalty_type_cb = ttk.Combobox(
            form, values=["LATE", "LOST", "DAMAGED"], state="readonly", width=22
        )
        self.penalty_type_cb.current(0)
        self.penalty_type_cb.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(form, text="Số tiền phạt:").grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.amount_entry = ttk.Entry(form, width=25)
        self.amount_entry.grid(row=1, column=3, padx=5, pady=5)

        # Buttons
        ttk.Button(form, text="➕ Tạo phiếu phạt", command=self._create_penalty).grid(row=3, column=0, pady=10)
        ttk.Button(form, text="🗑 Xóa", command=self._delete_penalty).grid(row=3, column=1, pady=10)
        ttk.Button(form, text="🔄 Reset", command=self._reset_form).grid(row=3, column=2, pady=10)

        # Treeview
        columns = ("penalty_id", "reader_name", "book_name", "penalty_type", "amount", "created_at")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")

        for col in columns:
            self.tree.heading(col, text=col.replace("_", " ").title())
            self.tree.column(col, width=120)

        self.tree.pack(pady=20, fill="x")
        self.tree.bind("<Double-1>", self._on_row_double_click)

    # ===================== Load data =====================
    def _load_penalties(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        penalties = self.controller.get_all_penalties()
        for p in penalties:
            self.tree.insert("", "end", values=(
                p["penalty_id"],
                p["reader_name"],
                p["book_name"],
                p["penalty_type"],
                p["amount"],
                p["created_at"]
            ))

    # ===================== Actions =====================
    def _create_penalty(self):
        reader_name = self.reader_entry.get()
        slip_id = self.slip_entry.get()
        book_name = self.book_entry.get()
        penalty_type = self.penalty_type_cb.get()
        try:
            amount = float(self.amount_entry.get())
        except ValueError:
            messagebox.showwarning("Sai dữ liệu", "Vui lòng nhập số tiền hợp lệ")
            return

        success = self.controller.create_penalty(reader_name, slip_id, book_name, penalty_type, amount)
        if success:
            self._reset_form()
            self._load_penalties()

    def _delete_penalty(self):
        if not self.selected_penalty_id:
            messagebox.showwarning("Chưa chọn", "Vui lòng chọn phiếu phạt")
            return

        success = self.controller.delete_penalty(self.selected_penalty_id)
        if success:
            self._reset_form()
            self._load_penalties()

    def _reset_form(self):
        self.selected_penalty_id = None
        self.reader_entry.delete(0, tk.END)
        self.slip_entry.delete(0, tk.END)
        self.book_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.penalty_type_cb.current(0)

    # ===================== Treeview double click =====================
    def _on_row_double_click(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        item = self.tree.item(selected[0])
        values = item["values"]

        self.selected_penalty_id = values[0]
        self.reader_entry.delete(0, tk.END)
        self.reader_entry.insert(0, values[1])
        self.book_entry.delete(0, tk.END)
        self.book_entry.insert(0, values[2])
        self.penalty_type_cb.set(values[3])
        self.amount_entry.delete(0, tk.END)
        self.amount_entry.insert(0, values[4])
        self.slip_entry.delete(0, tk.END)
        self.slip_entry.insert(0, "")  # Bạn có thể map slip_id nếu muốn
