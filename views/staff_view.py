import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

from controllers.staff_controller import StaffController
from config.session import Session
from permissions.role_permissions import has_permission


class StaffView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.controller = StaffController()
        self.pack(fill="both", expand=True)
        self._build_ui()

        # Load dữ liệu và áp dụng permissions sau khi UI sẵn sàng
        self.after(100, self.initialize_view)

    def _build_ui(self):
        # Tiêu đề
        tk.Label(
            self,
            text="QUẢN LÍ NHÂN VIÊN",
            font=("Arial", 16, "bold")
        ).pack(pady=10)

        # Frame chứa các nút
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=5)

        # Các nút chức năng
        self.btn_add = tk.Button(
            btn_frame,
            text="Đăng ký nhân viên",
            command=self.add_staff,
            width=15,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 10, "bold")
        )
        self.btn_update = tk.Button(
            btn_frame,
            text="Cập nhật chức vụ",
            command=self.update_role,
            width=15,
            bg="#2196F3",
            fg="white",
            font=("Arial", 10, "bold")
        )
        self.btn_view = tk.Button(
            btn_frame,
            text="Thông tin nhân viên",
            command=self.load_staff,
            width=15,
            bg="#9E9E9E",
            fg="white",
            font=("Arial", 10, "bold")
        )
        self.btn_delete = tk.Button(
            btn_frame,
            text="Xóa nhân viên",
            command=self.delete_staff,
            width=15,
            bg="#F44336",
            fg="white",
            font=("Arial", 10, "bold")
        )
        self.btn_export = tk.Button(
            btn_frame,
            text="Xuất Excel",
            command=self.export_excel,
            width=15,
            bg="#FF9800",
            fg="white",
            font=("Arial", 10, "bold")
        )

        # Sắp xếp các nút
        for i, btn in enumerate([
            self.btn_add,
            self.btn_update,
            self.btn_view,
            self.btn_delete,
            self.btn_export
        ]):
            btn.grid(row=0, column=i, padx=5)

        # Frame tìm kiếm
        search_frame = tk.Frame(self)
        search_frame.pack(pady=10)

        tk.Label(search_frame, text="Tìm kiếm:", font=("Arial", 10)).pack(side="left", padx=5)
        self.search_entry = tk.Entry(search_frame, width=30, font=("Arial", 10))
        self.search_entry.pack(side="left", padx=5)
        self.search_entry.bind("<KeyRelease>", self.on_search)

        tk.Button(
            search_frame,
            text="Làm mới",
            command=self.load_staff,
            bg="#607D8B",
            fg="white",
            font=("Arial", 10)
        ).pack(side="left", padx=5)

        # Frame chứa Treeview và Scrollbar
        tree_frame = tk.Frame(self)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Treeview
        self.tree = ttk.Treeview(
            tree_frame,
            columns=("id", "name", "user", "role", "status"),
            show="headings",
            height=20
        )

        # Đặt tiêu đề các cột
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Họ tên")
        self.tree.heading("user", text="Username")
        self.tree.heading("role", text="Role")
        self.tree.heading("status", text="Trạng thái")

        # Đặt độ rộng và căn chỉnh các cột
        self.tree.column("id", width=80, anchor="center")
        self.tree.column("name", width=200)
        self.tree.column("user", width=150)
        self.tree.column("role", width=100, anchor="center")
        self.tree.column("status", width=120, anchor="center")

        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Bind double-click để xem chi tiết
        self.tree.bind("<Double-1>", self.on_double_click)

    def initialize_view(self):
        """Khởi tạo view: áp dụng permissions và load dữ liệu"""
        self.apply_permissions()
        self.load_staff()

    # ================= AUTH & PERMISSIONS =================

    def ensure_login(self):
        """Kiểm tra xem user đã đăng nhập chưa"""
        if not Session.get("staff_id"):
            messagebox.showwarning("Đăng nhập", "Vui lòng đăng nhập để tiếp tục")
            self.event_generate("<<ShowLogin>>")
            return False
        return True

    def apply_permissions(self):
        """Áp dụng phân quyền dựa trên role_id"""
        role_id = Session.get("role_id")

        # Debug
        print(f"[DEBUG] Applying permissions for role_id: {role_id} (type: {type(role_id)})")

        # Chuyển đổi role_id sang int nếu là string
        if isinstance(role_id, str):
            try:
                role_id = int(role_id)
                print(f"[DEBUG] Converted role_id to int: {role_id}")
            except (ValueError, TypeError):
                role_id = None
                print(f"[DEBUG] Failed to convert role_id to int")

        # Nếu chưa đăng nhập, disable tất cả các nút
        if not role_id:
            print("[DEBUG] No role_id found, disabling all buttons")
            for btn in [self.btn_add, self.btn_update, self.btn_delete, self.btn_export]:
                btn.config(state="disabled")
            self.btn_view.config(state="normal")  # Cho phép xem
            return

        # Mapping giữa buttons và permissions
        permission_map = {
            self.btn_add: "register_staff",
            self.btn_update: "update_role",
            self.btn_delete: "delete_staff",
            self.btn_export: "export_excel",
            self.btn_view: "view_staff"
        }

        # Áp dụng permissions cho từng nút
        for button, permission in permission_map.items():
            has_perm = has_permission(role_id, permission)
            print(f"[DEBUG] Button '{button['text']}' - Permission '{permission}': {has_perm}")

            if has_perm:
                button.config(state="normal")
            else:
                button.config(state="disabled")

    # ================= ACTIONS =================

    def load_staff(self):
        """Load danh sách nhân viên từ database"""
        if not self.ensure_login():
            return

        try:
            # Xóa dữ liệu cũ
            self.tree.delete(*self.tree.get_children())

            # Lấy danh sách nhân viên
            staff_list = self.controller.get_all_staff()

            if not staff_list:
                messagebox.showinfo("Thông báo", "Không có dữ liệu nhân viên")
                return

            # Thêm vào tree
            for s in staff_list:
                # Chuyển role_id thành tên role
                role_name = self.get_role_name(s.role_id)
                self.tree.insert(
                    "",
                    "end",
                    values=(s.staff_id, s.full_name, s.username, role_name, s.status)
                )

            print(f"[INFO] Loaded {len(staff_list)} staff members")

        except Exception as e:
            print(f"[ERROR] Failed to load staff: {str(e)}")
            messagebox.showerror("Lỗi", f"Không thể tải dữ liệu: {str(e)}")

    def on_search(self, event=None):
        """Tìm kiếm nhân viên theo keyword"""
        keyword = self.search_entry.get().strip()

        if not keyword:
            self.load_staff()
            return

        try:
            self.tree.delete(*self.tree.get_children())
            staff_list = self.controller.search_staff(keyword)

            for s in staff_list:
                role_name = self.get_role_name(s.role_id)
                self.tree.insert(
                    "",
                    "end",
                    values=(s.staff_id, s.full_name, s.username, role_name, s.status)
                )
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi tìm kiếm: {str(e)}")

    def add_staff(self):
        """Đăng ký nhân viên mới"""
        if not self.ensure_login():
            return

        # Tạo dialog đăng ký nhân viên
        dialog = StaffRegistrationDialog(self, self.controller)
        if dialog.result:
            self.load_staff()  # Reload sau khi thêm thành công

    def update_role(self):
        """Cập nhật chức vụ cho nhân viên"""
        if not self.ensure_login():
            return

        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("Chọn nhân viên", "Vui lòng chọn nhân viên cần cập nhật")
            return

        values = self.tree.item(selected)["values"]
        staff_id = values[0]
        staff_name = values[1]

        # Dialog chọn role mới
        dialog = RoleUpdateDialog(self, staff_id, staff_name, self.controller)
        if dialog.result:
            self.load_staff()  # Reload sau khi cập nhật

    def delete_staff(self):
        """Xóa nhân viên khỏi hệ thống"""
        if not self.ensure_login():
            return

        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("Chọn nhân viên", "Vui lòng chọn nhân viên cần xóa")
            return

        values = self.tree.item(selected)["values"]
        staff_id = values[0]
        staff_name = values[1]

        # Xác nhận xóa
        confirm = messagebox.askyesno(
            "Xác nhận xóa",
            f"Bạn có chắc chắn muốn xóa nhân viên:\n\nID: {staff_id}\nTên: {staff_name}\n\nHành động này không thể hoàn tác!"
        )

        if confirm:
            result = self.controller.delete_staff(staff_id)

            if result['success']:
                messagebox.showinfo("Thành công", result['message'])
                self.load_staff()
            else:
                messagebox.showerror("Lỗi", result['message'])

    def export_excel(self):
        """Xuất file Excel lịch sử thao tác"""
        if not self.ensure_login():
            return
        messagebox.showinfo("TODO", "Chức năng xuất Excel đang được phát triển")

    def on_double_click(self, event):
        """Xem chi tiết nhân viên khi double-click"""
        selected = self.tree.focus()
        if not selected:
            return

        values = self.tree.item(selected)["values"]
        staff_id = values[0]

        # Hiển thị chi tiết
        try:
            staff = self.controller.get_staff_by_id(staff_id)
            if staff:
                detail_msg = f"""
Thông tin nhân viên:

ID: {staff.staff_id}
Họ tên: {staff.full_name}
Username: {staff.username}
Chức vụ: {self.get_role_name(staff.role_id)}
Trạng thái: {staff.status}
                """
                messagebox.showinfo("Chi tiết nhân viên", detail_msg.strip())
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể lấy thông tin: {str(e)}")

    # ================= HELPERS =================

    @staticmethod
    def get_role_name(role_id):
        """Chuyển role_id thành tên role"""
        role_names = {
            1: "Admin",
            2: "Thủ thư",
            3: "Nhân viên",
            5: "Super Admin"
        }
        return role_names.get(role_id, f"Role {role_id}")


# ================= DIALOGS =================

class StaffRegistrationDialog:
    """Dialog đăng ký nhân viên mới"""

    def __init__(self, parent, controller):
        self.result = None
        self.controller = controller

        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Đăng ký nhân viên mới")
        self.dialog.geometry("400x300")
        self.dialog.resizable(False, False)

        # Center dialog
        self.dialog.transient(parent)
        self.dialog.grab_set()

        self._build_ui()

        # Wait for dialog to close
        parent.wait_window(self.dialog)

    def _build_ui(self):
        frame = tk.Frame(self.dialog, padx=20, pady=20)
        frame.pack(fill="both", expand=True)

        # Họ tên
        tk.Label(frame, text="Họ tên:").grid(row=0, column=0, sticky="w", pady=5)
        self.full_name_entry = tk.Entry(frame, width=30)
        self.full_name_entry.grid(row=0, column=1, pady=5)

        # Username
        tk.Label(frame, text="Username:").grid(row=1, column=0, sticky="w", pady=5)
        self.username_entry = tk.Entry(frame, width=30)
        self.username_entry.grid(row=1, column=1, pady=5)

        # Password
        tk.Label(frame, text="Password:").grid(row=2, column=0, sticky="w", pady=5)
        self.password_entry = tk.Entry(frame, width=30, show="*")
        self.password_entry.grid(row=2, column=1, pady=5)

        # Role
        tk.Label(frame, text="Chức vụ:").grid(row=3, column=0, sticky="w", pady=5)
        self.role_var = tk.StringVar(value="3")
        role_frame = tk.Frame(frame)
        role_frame.grid(row=3, column=1, sticky="w", pady=5)

        roles = [
            ("Admin", "1"),
            ("Thủ thư", "2"),
            ("Nhân viên", "3"),
            ("Super Admin", "5")
        ]

        for text, value in roles:
            tk.Radiobutton(
                role_frame,
                text=text,
                variable=self.role_var,
                value=value
            ).pack(anchor="w")

        # Buttons
        btn_frame = tk.Frame(frame)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=20)

        tk.Button(
            btn_frame,
            text="Đăng ký",
            command=self.on_submit,
            bg="#4CAF50",
            fg="white",
            width=10
        ).pack(side="left", padx=5)

        tk.Button(
            btn_frame,
            text="Hủy",
            command=self.dialog.destroy,
            width=10
        ).pack(side="left", padx=5)

    def on_submit(self):
        full_name = self.full_name_entry.get().strip()
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        role_id = int(self.role_var.get())

        result = self.controller.register_staff(full_name, username, password, role_id)

        if result['success']:
            messagebox.showinfo("Thành công", result['message'])
            self.result = True
            self.dialog.destroy()
        else:
            messagebox.showerror("Lỗi", result['message'])


class RoleUpdateDialog:
    """Dialog cập nhật chức vụ"""

    def __init__(self, parent, staff_id, staff_name, controller):
        self.result = None
        self.staff_id = staff_id
        self.controller = controller

        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Cập nhật chức vụ")
        self.dialog.geometry("350x250")
        self.dialog.resizable(False, False)

        self.dialog.transient(parent)
        self.dialog.grab_set()

        self._build_ui(staff_name)

        parent.wait_window(self.dialog)

    def _build_ui(self, staff_name):
        frame = tk.Frame(self.dialog, padx=20, pady=20)
        frame.pack(fill="both", expand=True)

        tk.Label(
            frame,
            text=f"Cập nhật chức vụ cho: {staff_name}",
            font=("Arial", 11, "bold")
        ).pack(pady=10)

        tk.Label(frame, text="Chọn chức vụ mới:").pack(anchor="w", pady=5)

        self.role_var = tk.StringVar(value="3")

        roles = [
            ("Admin", "1"),
            ("Thủ thư", "2"),
            ("Nhân viên", "3"),
            ("Super Admin", "5")
        ]

        for text, value in roles:
            tk.Radiobutton(
                frame,
                text=text,
                variable=self.role_var,
                value=value
            ).pack(anchor="w", padx=20)

        btn_frame = tk.Frame(frame)
        btn_frame.pack(pady=20)

        tk.Button(
            btn_frame,
            text="Cập nhật",
            command=self.on_submit,
            bg="#2196F3",
            fg="white",
            width=10
        ).pack(side="left", padx=5)

        tk.Button(
            btn_frame,
            text="Hủy",
            command=self.dialog.destroy,
            width=10
        ).pack(side="left", padx=5)

    def on_submit(self):
        new_role_id = int(self.role_var.get())

        result = self.controller.update_role(self.staff_id, new_role_id)

        if result['success']:
            messagebox.showinfo("Thành công", result['message'])
            self.result = True
            self.dialog.destroy()
        else:
            messagebox.showerror("Lỗi", result['message'])