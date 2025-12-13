import tkinter as tk
from tkinter import ttk, messagebox
from controllers.report_controller import ReportController


class ReportView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.controller = ReportController()
        self.pack(fill="both", expand=True, padx=10, pady=10)

        # --- Header & Filter ---
        header_frame = tk.Frame(self)
        header_frame.pack(fill="x", pady=(0, 15))

        tk.Label(header_frame, text="BÁO CÁO & THỐNG KÊ", font=("Arial", 16, "bold"), fg="#333").pack(side="left")

        # Bộ lọc thời gian
        filter_frame = tk.Frame(header_frame)
        filter_frame.pack(side="right")
        tk.Label(filter_frame, text="Xem theo:", font=("Arial", 10)).pack(side="left", padx=5)

        self.filter_var = tk.StringVar(value="Tháng")
        self.combo_filter = ttk.Combobox(filter_frame, textvariable=self.filter_var,
                                         values=["Ngày", "Tháng", "Năm"], state="readonly", width=10)
        self.combo_filter.pack(side="left")
        self.combo_filter.bind("<<ComboboxSelected>>", self.on_filter_change)  # Bắt sự kiện chọn

        # --- Phần 1: Tổng quan Tồn kho (Dạng thẻ to đẹp) ---
        frame_inventory = tk.LabelFrame(self, text="📦 Tổng Quan Kho Sách", font=("Arial", 10, "bold"), fg="blue")
        frame_inventory.pack(fill="x", pady=5)

        self.lbl_total = tk.Label(frame_inventory, text="Tổng: ...", font=("Arial", 12, "bold"))
        self.lbl_total.pack(side="left", padx=40, pady=15)

        self.lbl_borrowed = tk.Label(frame_inventory, text="Đang mượn: ...", font=("Arial", 12, "bold"),
                                     fg="#F44336")  # Màu đỏ
        self.lbl_borrowed.pack(side="left", padx=40, pady=15)

        self.lbl_available = tk.Label(frame_inventory, text="Trong kho: ...", font=("Arial", 12, "bold"),
                                      fg="#4CAF50")  # Màu xanh
        self.lbl_available.pack(side="left", padx=40, pady=15)

        # --- Phần 2: Chia đôi (Mượn trả & Top bạn đọc) ---
        paned = tk.PanedWindow(self, orient=tk.HORIZONTAL)
        paned.pack(fill="both", expand=True, pady=10)

        # Cột trái: Thống kê mượn
        frame_borrow = tk.LabelFrame(paned, text="📊 Xu Hướng Mượn Sách")
        paned.add(frame_borrow, width=350)  # Set độ rộng ưu tiên

        cols_borrow = ("time", "count")
        self.tree_borrow = ttk.Treeview(frame_borrow, columns=cols_borrow, show="headings", height=6)
        self.tree_borrow.heading("time", text="Thời gian")
        self.tree_borrow.heading("count", text="Lượt mượn")
        self.tree_borrow.column("time", width=120, anchor="center")
        self.tree_borrow.column("count", width=80, anchor="center")
        self.tree_borrow.pack(fill="both", expand=True, padx=5, pady=5)

        # Cột phải: Top Bạn Đọc
        frame_top = tk.LabelFrame(paned, text="🏆 Top Bạn Đọc Tích Cực")
        paned.add(frame_top)

        cols_reader = ("name", "count")
        self.tree_reader = ttk.Treeview(frame_top, columns=cols_reader, show="headings", height=6)
        self.tree_reader.heading("name", text="Họ Tên")
        self.tree_reader.heading("count", text="Số lần mượn")
        self.tree_reader.column("name", width=180)
        self.tree_reader.column("count", width=80, anchor="center")
        self.tree_reader.pack(fill="both", expand=True, padx=5, pady=5)

        # --- Phần 3: Sách Hư hỏng / Mất (MỚI THÊM) ---
        frame_risk = tk.LabelFrame(self, text="⚠️ Báo Cáo Rủi Ro (Hư Hỏng / Mất)", font=("Arial", 10, "bold"),
                                   fg="#FF9800")
        frame_risk.pack(fill="x", pady=5)

        cols_risk = ("type", "qty", "fine")
        self.tree_risk = ttk.Treeview(frame_risk, columns=cols_risk, show="headings", height=4)
        self.tree_risk.heading("type", text="Loại vi phạm")
        self.tree_risk.heading("qty", text="Số lượng sách")
        self.tree_risk.heading("fine", text="Tổng tiền phạt")

        self.tree_risk.column("type", anchor="center")
        self.tree_risk.column("qty", anchor="center")
        self.tree_risk.column("fine", anchor="e", width=120)  # Căn phải cho số tiền
        self.tree_risk.pack(fill="x", padx=5, pady=5)

        # --- Nút chức năng ---
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="🔄 Cập nhật dữ liệu", command=self.load_data,
                  bg="#4CAF50", fg="white", font=("Arial", 10, "bold")).pack(side="left", padx=10)

        # Nút xuất Excel (Placeholder - nếu bạn đã làm function này thì gắn vào)
        tk.Button(btn_frame, text="📤 Xuất Excel", command=self.export_excel,
                  bg="#2196F3", fg="white", font=("Arial", 10)).pack(side="left", padx=10)

        # Load dữ liệu lần đầu
        self.load_data()

    def on_filter_change(self, event):
        """Khi chọn combobox Ngày/Tháng/Năm thì load lại dữ liệu"""
        self.load_data()

    def load_data(self):
        # Lấy chế độ xem từ combobox (mapped: Tiếng Việt -> code)
        filter_map = {"Ngày": "day", "Tháng": "month", "Năm": "year"}
        selected_mode = filter_map.get(self.filter_var.get(), "month")

        # Gọi Controller
        # Lưu ý: Cần sửa nhẹ ReportController để nhận tham số mode nếu chưa có
        # Ở đây giả định controller.get_dashboard_data đã xử lý, hoặc ta gọi trực tiếp service thông qua controller

        # Để đơn giản, ta sẽ gọi controller lấy full data,
        # nhưng nếu controller chưa hỗ trợ truyền mode, bạn cần sửa controller một chút.
        # Ở đây mình giả định bạn sửa controller như bên dưới hướng dẫn.

        try:
            # Cách gọi cũ: data = self.controller.get_dashboard_data()
            # Cách gọi mới (cần sửa controller):
            data = self.controller.get_dashboard_data(mode=selected_mode)

            # 1. Fill Inventory
            inv = data['inventory']
            self.lbl_total.config(text=f"Tổng: {inv['total']}")
            self.lbl_borrowed.config(text=f"Đang mượn: {inv['borrowed']}")
            self.lbl_available.config(text=f"Trong kho: {inv['available']}")

            # 2. Fill Borrow Stats
            self.clear_tree(self.tree_borrow)
            for row in data['borrow_stats']:
                self.tree_borrow.insert("", "end", values=(row['time_point'], row['total_borrows']))

            # 3. Fill Top Readers
            self.clear_tree(self.tree_reader)
            for row in data['top_readers']:
                self.tree_reader.insert("", "end", values=(row['full_name'], row['borrow_count']))

            # 4. Fill Risk (Damaged/Lost)
            self.clear_tree(self.tree_risk)
            for row in data['damaged_lost']:
                # Định dạng tiền tệ cho đẹp
                fine_fmt = "{:,.0f} VNĐ".format(row['total_fine']) if row['total_fine'] else "0 VNĐ"
                # Dịch loại vi phạm
                type_map = {"LOST": "Mất sách", "DAMAGED": "Hư hỏng", "LATE": "Trễ hạn"}
                type_name = type_map.get(row['penalty_type'], row['penalty_type'])

                self.tree_risk.insert("", "end", values=(type_name, row['quantity'], fine_fmt))

        except Exception as e:
            print(f"Lỗi load data: {e}")

    def clear_tree(self, tree):
        for item in tree.get_children():
            tree.delete(item)

    def export_excel(self):
        # Gọi hàm xuất excel từ controller (nếu bạn đã thêm ở bước trước)
        if hasattr(self.controller, 'export_to_excel'):
            success, msg = self.controller.export_to_excel()
            if success:
                messagebox.showinfo("Thành công", msg)
            elif "hủy" not in msg:
                messagebox.showerror("Lỗi", msg)
        else:
            messagebox.showinfo("Thông báo", "Chức năng đang phát triển")


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Test Màn Hình Báo Cáo")
    root.geometry("900x700")
    view = ReportView(root)
    view.pack(fill="both", expand=True)
    root.mainloop()