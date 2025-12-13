import tkinter as tk
from tkinter import ttk, messagebox

from controllers.staff_auth_controller import StaffAuthController


class StaffLoginView(tk.Toplevel):
    """
    Dialog đăng nhập nhân viên
    """

    def __init__(self, parent):
        super().__init__(parent)
        self.title("🔐 Đăng nhập nhân viên")
        self.geometry("350x220")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        self.parent = parent
        self.auth = StaffAuthController()
        self.login_success = False

        self._build_ui()
        self._center(parent)

    def _build_ui(self):
        container = ttk.Frame(self, padding=20)
        container.pack(fill="both", expand=True)

        ttk.Label(
            container,
            text="ĐĂNG NHẬP NHÂN VIÊN",
            font=("Arial", 12, "bold")
        ).pack(pady=(0, 15))

        # Username
        ttk.Label(container, text="Tên đăng nhập").pack(anchor="w")
        self.username_entry = ttk.Entry(container)
        self.username_entry.pack(fill="x", pady=5)

        # Password
        ttk.Label(container, text="Mật khẩu").pack(anchor="w")
        self.password_entry = ttk.Entry(container, show="*")
        self.password_entry.pack(fill="x", pady=5)

        # Buttons
        btn_frame = ttk.Frame(container)
        btn_frame.pack(pady=15)

        ttk.Button(
            btn_frame,
            text="Đăng nhập",
            command=self._login
        ).pack(side="left", padx=5)

        ttk.Button(
            btn_frame,
            text="Hủy",
            command=self.destroy
        ).pack(side="left", padx=5)

        # Bind Enter key
        self.username_entry.bind("<Return>", lambda e: self.password_entry.focus())
        self.password_entry.bind("<Return>", lambda e: self._login())

        self.username_entry.focus()

    def _login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập đầy đủ")
            return

        # Đăng nhập
        if self.auth.login(username, password):
            staff = self.auth.get_current_staff()
            role_name = self._get_role_name(staff['role_id'])

            messagebox.showinfo(
                "Thành công",
                f"Chào mừng {staff['full_name']}!\nChức vụ: {role_name}"
            )

            self.login_success = True

            # ✅ Trigger event để MainWindow refresh permissions
            self.parent.event_generate("<<LoginSuccess>>")

            self.destroy()
        else:
            messagebox.showerror(
                "Thất bại",
                "Sai tài khoản, mật khẩu hoặc tài khoản bị khóa"
            )

    def _center(self, parent):
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (self.winfo_width() // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (self.winfo_height() // 2)
        self.geometry(f"+{x}+{y}")

    @staticmethod
    def _get_role_name(role_id):
        """Chuyển role_id thành tên role"""
        role_names = {
            1: "Admin",
            2: "Thủ thư",
            3: "Nhân viên",
            5: "Super Admin"
        }
        return role_names.get(role_id, f"Role {role_id}")