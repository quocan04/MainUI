import tkinter as tk
from tkinter import messagebox
from controllers.system_controller import SystemController


class SystemView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.controller = SystemController()
        self.pack(fill="both", expand=True, padx=20, pady=20)

        # Tiêu đề
        lbl_title = tk.Label(self, text="HỆ THỐNG & CẤU HÌNH", font=("Arial", 16, "bold"), fg="#333")
        lbl_title.pack(pady=(0, 30))

        # --- Phần 1: Form Cài đặt ---
        frame_settings = tk.LabelFrame(self, text="Tham Số Quy Định", font=("Arial", 11, "bold"), padx=10, pady=10)
        frame_settings.pack(fill="x", pady=10)

        # Grid layout cho form
        self.entries = {}
        # Mapping tên hiển thị -> key trong database
        self.setting_map = {
            "Số sách mượn tối đa (cuốn):": "MAX_BORROW",
            "Thời hạn mượn (ngày):": "BORROW_DAYS",
            "Phí phạt quá hạn (VNĐ/ngày):": "LATE_FEE_PER_DAY",
            "Tỷ lệ phạt mất sách (x giá bìa):": "LOST_FINE_RATE"
        }

        row_idx = 0
        for label_text, key in self.setting_map.items():
            lbl = tk.Label(frame_settings, text=label_text, font=("Arial", 10))
            lbl.grid(row=row_idx, column=0, sticky="w", pady=5, padx=5)

            entry = tk.Entry(frame_settings, width=30)
            entry.grid(row=row_idx, column=1, pady=5, padx=5)
            self.entries[key] = entry  # Lưu entry vào dict
            row_idx += 1

        # Nút Lưu cài đặt
        btn_save = tk.Button(frame_settings, text="Lưu Cấu Hình", command=self.save_settings, bg="#2196F3", fg="white")
        btn_save.grid(row=row_idx, column=1, sticky="e", pady=10)

        # --- Phần 2: An Toàn Dữ Liệu (Backup & Restore) ---
        frame_backup = tk.LabelFrame(self, text="An Toàn Dữ Liệu", font=("Arial", 11, "bold"), padx=10, pady=10)
        frame_backup.pack(fill="x", pady=20)

        lbl_backup = tk.Label(frame_backup, text="Sao lưu và Phục hồi cơ sở dữ liệu (JSON).")
        lbl_backup.pack(side="left", padx=10)

        # Nút Phục hồi (Màu đỏ)
        btn_restore = tk.Button(frame_backup, text="♻️ PHỤC HỒI", command=self.perform_restore,
                                bg="#F44336", fg="white", font=("Arial", 10, "bold"))
        btn_restore.pack(side="right", padx=5)

        # Nút Sao lưu (Màu cam)
        btn_backup = tk.Button(frame_backup, text="📦 SAO LƯU NGAY", command=self.perform_backup,
                               bg="#FF9800", fg="white", font=("Arial", 10, "bold"))
        btn_backup.pack(side="right", padx=5)

        # Load dữ liệu ban đầu
        self.load_current_settings()

    def load_current_settings(self):
        current_data = self.controller.get_current_settings()
        for key, entry in self.entries.items():
            if key in current_data:
                entry.delete(0, tk.END)
                entry.insert(0, current_data[key])

    def save_settings(self):
        new_settings = {}
        for key, entry in self.entries.items():
            new_settings[key] = entry.get()

        success, msg = self.controller.save_settings(new_settings)
        if success:
            messagebox.showinfo("Thành công", msg)
        else:
            messagebox.showerror("Lỗi", msg)

    def perform_backup(self):
        if messagebox.askyesno("Xác nhận", "Bạn có muốn sao lưu dữ liệu ngay bây giờ?"):
            success, msg = self.controller.perform_backup()
            if success:
                messagebox.showinfo("Thành công", msg)
            else:
                messagebox.showerror("Lỗi", msg)

    def perform_restore(self):
        if messagebox.askyesno("Cảnh báo nguy hiểm",
                               "Phục hồi sẽ XÓA TOÀN BỘ dữ liệu hiện tại và thay thế bằng bản sao lưu.\n\nBạn có chắc chắn muốn tiếp tục không?"):
            success, msg = self.controller.perform_restore()
            if success:
                messagebox.showinfo("Thành công", msg)
                self.load_current_settings()
            elif "hủy" not in msg:
                messagebox.showerror("Lỗi", msg)


# --- QUAN TRỌNG: Dòng này phải nằm SÁT LỀ TRÁI (Không thụt vào) ---
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Test Màn Hình Hệ Thống")
    root.geometry("600x400")

    view = SystemView(root)
    view.pack(fill="both", expand=True)

    root.mainloop()