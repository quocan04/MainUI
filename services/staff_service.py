from models.staff_model import StaffModel


class StaffService:
    """
    Business logic cho quản lý Nhân viên
    - Xử lý các quy tắc nghiệp vụ
    - Validate dữ liệu
    - Gọi Model để thao tác database
    """

    def __init__(self):
        self.model = StaffModel()

    # =========================
    # AUTHENTICATION
    # =========================

    def authenticate(self, username: str, password: str):
        """
        Xác thực đăng nhập nhân viên

        Args:
            username: Tên đăng nhập
            password: Mật khẩu

        Returns:
            Staff: Object nhân viên nếu hợp lệ
            None: Nếu thông tin không đúng hoặc tài khoản inactive

        Raises:
            ValueError: Nếu username hoặc password rỗng
        """
        if not username or not username.strip():
            raise ValueError("Username không được để trống")

        if not password or not password.strip():
            raise ValueError("Password không được để trống")

        return self.model.authenticate(username.strip(), password)

    # =========================
    # QUERY (READ)
    # =========================

    def get_all_staff(self):
        """
        Lấy danh sách tất cả nhân viên

        Returns:
            list[Staff]: Danh sách nhân viên
        """
        return self.model.get_all_staff()

    def get_staff_by_id(self, staff_id: int):
        """
        Lấy thông tin nhân viên theo ID

        Args:
            staff_id: ID của nhân viên

        Returns:
            Staff: Thông tin nhân viên hoặc None

        Raises:
            ValueError: Nếu staff_id không hợp lệ
        """
        if not staff_id or staff_id <= 0:
            raise ValueError("Staff ID phải là số nguyên dương")

        return self.model.get_by_id(staff_id)

    def search_staff(self, keyword: str):
        """
        Tìm kiếm nhân viên theo từ khóa

        Args:
            keyword: Từ khóa tìm kiếm (họ tên, username)

        Returns:
            list[Staff]: Danh sách nhân viên phù hợp
        """
        if not keyword or not keyword.strip():
            return self.get_all_staff()

        return self.model.search(keyword.strip())

    def get_staff_by_role(self, role_id: int):
        """
        Lấy danh sách nhân viên theo role

        Args:
            role_id: ID của role

        Returns:
            list[Staff]: Danh sách nhân viên có role_id tương ứng
        """
        if not role_id or role_id <= 0:
            raise ValueError("Role ID không hợp lệ")

        return self.model.get_by_role(role_id)

    # =========================
    # COMMAND (CREATE/UPDATE/DELETE)
    # =========================

    def register_staff(self, full_name: str, username: str, password: str, role_id: int):
        """
        Đăng ký nhân viên mới

        Args:
            full_name: Họ tên nhân viên
            username: Tên đăng nhập (unique)
            password: Mật khẩu
            role_id: ID chức vụ (1=Admin, 2=Thủ thư, 3=Nhân viên, 5=Super Admin)

        Returns:
            int: ID của nhân viên vừa tạo

        Raises:
            ValueError: Nếu dữ liệu không hợp lệ
            Exception: Nếu username đã tồn tại
        """
        # Validate input
        if not full_name or not full_name.strip():
            raise ValueError("Họ tên không được để trống")

        if not username or not username.strip():
            raise ValueError("Username không được để trống")

        if len(username.strip()) < 4:
            raise ValueError("Username phải có ít nhất 4 ký tự")

        if not password or len(password) < 6:
            raise ValueError("Mật khẩu phải có ít nhất 6 ký tự")

        if role_id not in [1, 2, 3, 5]:
            raise ValueError("Role ID không hợp lệ (chỉ chấp nhận 1, 2, 3, 5)")

        # Kiểm tra username đã tồn tại chưa
        if self.model.check_username_exists(username.strip()):
            raise Exception(f"Username '{username}' đã tồn tại")

        # Tạo nhân viên mới
        return self.model.create(
            full_name=full_name.strip(),
            username=username.strip(),
            password=password,
            role_id=role_id
        )

    def update_role(self, staff_id: int, new_role_id: int):
        """
        Cập nhật chức vụ cho nhân viên

        Args:
            staff_id: ID nhân viên cần cập nhật
            new_role_id: Role ID mới

        Raises:
            ValueError: Nếu dữ liệu không hợp lệ
            Exception: Nếu nhân viên không tồn tại
        """
        if not staff_id or staff_id <= 0:
            raise ValueError("Staff ID không hợp lệ")

        if new_role_id not in [1, 2, 3, 5]:
            raise ValueError("Role ID không hợp lệ (chỉ chấp nhận 1, 2, 3, 5)")

        # Kiểm tra nhân viên có tồn tại không
        staff = self.model.get_by_id(staff_id)
        if not staff:
            raise Exception(f"Không tìm thấy nhân viên với ID: {staff_id}")

        # Kiểm tra role có thay đổi không
        if staff.role_id == new_role_id:
            raise Exception("Role mới giống role hiện tại")

        # Cập nhật role
        self.model.update_role(staff_id, new_role_id)

    def update_staff_info(self, staff_id: int, full_name: str = None, username: str = None):
        """
        Cập nhật thông tin nhân viên

        Args:
            staff_id: ID nhân viên
            full_name: Họ tên mới (optional)
            username: Username mới (optional)

        Raises:
            ValueError: Nếu dữ liệu không hợp lệ
            Exception: Nếu nhân viên không tồn tại hoặc username đã tồn tại
        """
        if not staff_id or staff_id <= 0:
            raise ValueError("Staff ID không hợp lệ")

        # Kiểm tra nhân viên có tồn tại không
        staff = self.model.get_by_id(staff_id)
        if not staff:
            raise Exception(f"Không tìm thấy nhân viên với ID: {staff_id}")

        # Validate và cập nhật full_name
        if full_name is not None:
            if not full_name.strip():
                raise ValueError("Họ tên không được để trống")
            self.model.update_full_name(staff_id, full_name.strip())

        # Validate và cập nhật username
        if username is not None:
            if not username.strip():
                raise ValueError("Username không được để trống")
            if len(username.strip()) < 4:
                raise ValueError("Username phải có ít nhất 4 ký tự")
            if username.strip() != staff.username and self.model.check_username_exists(username.strip()):
                raise Exception(f"Username '{username}' đã tồn tại")
            self.model.update_username(staff_id, username.strip())

    def change_password(self, staff_id: int, old_password: str, new_password: str):
        """
        Đổi mật khẩu nhân viên

        Args:
            staff_id: ID nhân viên
            old_password: Mật khẩu cũ
            new_password: Mật khẩu mới

        Raises:
            ValueError: Nếu mật khẩu không hợp lệ
            Exception: Nếu mật khẩu cũ không đúng
        """
        if not staff_id or staff_id <= 0:
            raise ValueError("Staff ID không hợp lệ")

        if not old_password:
            raise ValueError("Mật khẩu cũ không được để trống")

        if not new_password or len(new_password) < 6:
            raise ValueError("Mật khẩu mới phải có ít nhất 6 ký tự")

        if old_password == new_password:
            raise ValueError("Mật khẩu mới phải khác mật khẩu cũ")

        # Kiểm tra mật khẩu cũ
        if not self.model.verify_password(staff_id, old_password):
            raise Exception("Mật khẩu cũ không chính xác")

        # Cập nhật mật khẩu mới
        self.model.update_password(staff_id, new_password)

    def delete_staff(self, staff_id: int):
        """
        Xóa nhân viên khỏi hệ thống

        Business rule:
        - Không được xóa chính mình
        - Không được xóa Super Admin (role_id = 5)
        - Chỉ Admin và Super Admin mới được xóa nhân viên

        Args:
            staff_id: ID nhân viên cần xóa

        Raises:
            ValueError: Nếu staff_id không hợp lệ
            Exception: Nếu vi phạm business rule
        """
        if not staff_id or staff_id <= 0:
            raise ValueError("Staff ID không hợp lệ")

        # Kiểm tra nhân viên có tồn tại không
        staff = self.model.get_by_id(staff_id)
        if not staff:
            raise Exception(f"Không tìm thấy nhân viên với ID: {staff_id}")

        # Business rule: Không được xóa Super Admin
        if staff.role_id == 5:
            raise Exception("Không thể xóa Super Admin")

        # Xóa nhân viên (soft delete hoặc hard delete)
        self.model.delete_staff(staff_id)

    def deactivate_staff(self, staff_id: int):
        """
        Vô hiệu hóa tài khoản nhân viên (soft delete)

        Args:
            staff_id: ID nhân viên

        Raises:
            ValueError: Nếu staff_id không hợp lệ
            Exception: Nếu nhân viên không tồn tại
        """
        if not staff_id or staff_id <= 0:
            raise ValueError("Staff ID không hợp lệ")

        staff = self.model.get_by_id(staff_id)
        if not staff:
            raise Exception(f"Không tìm thấy nhân viên với ID: {staff_id}")

        if staff.status == "INACTIVE":
            raise Exception("Nhân viên đã ở trạng thái INACTIVE")

        self.model.update_status(staff_id, "INACTIVE")

    def activate_staff(self, staff_id: int):
        """
        Kích hoạt lại tài khoản nhân viên

        Args:
            staff_id: ID nhân viên

        Raises:
            ValueError: Nếu staff_id không hợp lệ
            Exception: Nếu nhân viên không tồn tại
        """
        if not staff_id or staff_id <= 0:
            raise ValueError("Staff ID không hợp lệ")

        staff = self.model.get_by_id(staff_id)
        if not staff:
            raise Exception(f"Không tìm thấy nhân viên với ID: {staff_id}")

        if staff.status == "ACTIVE":
            raise Exception("Nhân viên đã ở trạng thái ACTIVE")

        self.model.update_status(staff_id, "ACTIVE")

    # =========================
    # STATISTICS & REPORTING
    # =========================

    def get_staff_count_by_role(self):
        """
        Thống kê số lượng nhân viên theo role

        Returns:
            dict: {role_id: count}
        """
        return self.model.count_by_role()

    def get_active_staff_count(self):
        """
        Đếm số nhân viên đang hoạt động

        Returns:
            int: Số lượng nhân viên có status = 'ACTIVE'
        """
        return self.model.count_active()