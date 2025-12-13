from typing import Optional, Dict

from services.staff_service import StaffService
from config.session import Session


class StaffAuthController:
    """
    Controller xử lý xác thực + phân quyền nhân viên
    """

    def __init__(self):
        self.staff_service = StaffService()

    # ======================
    # AUTHENTICATION
    # ======================
    def login(self, username: str, password: str) -> bool:
        """
        Đăng nhập nhân viên

        Returns:
            bool: True nếu đăng nhập thành công
        """
        try:
            # Authenticate qua service - trả về Staff object
            staff = self.staff_service.authenticate(username, password)

            if not staff:
                print("[LOGIN FAILED] Invalid credentials")
                return False

            # ✅ LƯU VÀO SESSION (sử dụng Session thay vì StaffSession riêng)
            Session.set("staff_id", staff.staff_id)
            Session.set("full_name", staff.full_name)
            Session.set("username", staff.username)
            Session.set("role_id", staff.role_id)  # ⚠️ QUAN TRỌNG!
            Session.set("status", staff.status)

            # Debug log
            print(f"[LOGIN SUCCESS] Staff: {staff.full_name}, Role ID: {staff.role_id}")
            print(f"[SESSION] {Session.get_all()}")

            return True

        except Exception as e:
            print(f"[LOGIN ERROR] {str(e)}")
            return False

    def logout(self):
        """Đăng xuất - xóa toàn bộ session"""
        Session.clear()
        print("[LOGOUT] Session cleared")

    def is_logged_in(self) -> bool:
        """Kiểm tra đã đăng nhập chưa"""
        return Session.get("staff_id") is not None

    def get_current_staff(self) -> Optional[Dict]:
        """
        Lấy thông tin nhân viên hiện tại từ session

        Returns:
            dict: Thông tin nhân viên hoặc None
        """
        staff_id = Session.get("staff_id")
        if not staff_id:
            return None

        return {
            "staff_id": staff_id,
            "full_name": Session.get("full_name"),
            "username": Session.get("username"),
            "role_id": Session.get("role_id"),
            "status": Session.get("status")
        }

    def get_role_id(self) -> Optional[int]:
        """Lấy role_id của user hiện tại"""
        role_id = Session.get("role_id")

        # Chuyển sang int nếu là string
        if isinstance(role_id, str):
            try:
                return int(role_id)
            except (ValueError, TypeError):
                return None

        return role_id

    # ======================
    # AUTHORIZATION
    # ======================
    def can_register_staff(self) -> bool:
        """Kiểm tra quyền đăng ký nhân viên"""
        role = self.get_role_id()
        return role in (1, 2, 5)  # Admin, Thủ thư, Super Admin

    def can_update_role(self) -> bool:
        """Kiểm tra quyền cập nhật chức vụ"""
        role = self.get_role_id()
        return role in (1, 5)  # Admin, Super Admin

    def can_delete_staff(self) -> bool:
        """Kiểm tra quyền xóa nhân viên"""
        role = self.get_role_id()
        return role in (1, 5)  # Admin, Super Admin

    def can_view_staff(self) -> bool:
        """Kiểm tra quyền xem thông tin nhân viên"""
        role = self.get_role_id()
        return role in (1, 2, 3, 5)  # Tất cả

    def can_export_excel(self) -> bool:
        """Kiểm tra quyền xuất Excel"""
        role = self.get_role_id()
        return role in (1, 2, 3, 5)  # Tất cả

    def has_permission(self, permission: str) -> bool:
        """
        Kiểm tra quyền dựa trên tên permission

        Args:
            permission: Tên permission (register_staff, update_role, etc.)

        Returns:
            bool: True nếu có quyền
        """
        permission_map = {
            "register_staff": self.can_register_staff,
            "update_role": self.can_update_role,
            "delete_staff": self.can_delete_staff,
            "view_staff": self.can_view_staff,
            "export_excel": self.can_export_excel
        }

        check_func = permission_map.get(permission)
        if check_func:
            return check_func()

        return False