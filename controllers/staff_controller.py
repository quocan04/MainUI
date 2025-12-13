from services.staff_service import StaffService


class StaffController:
    """
    Controller xử lý logic điều khiển giữa View và Service
    - Nhận request từ View
    - Gọi Service để xử lý business logic
    - Xử lý exceptions và format response
    - Trả kết quả về View
    """

    def __init__(self):
        self.service = StaffService()

    # ================= QUERY (READ) =================

    def get_all_staff(self):
        """
        Lấy danh sách tất cả nhân viên

        Returns:
            list[Staff]: Danh sách nhân viên

        Raises:
            Exception: Nếu có lỗi khi truy vấn
        """
        try:
            return self.service.get_all_staff()
        except Exception as e:
            raise Exception(f"Lỗi khi lấy danh sách nhân viên: {str(e)}")

    def get_staff_by_id(self, staff_id):
        """
        Lấy thông tin nhân viên theo ID

        Args:
            staff_id: ID của nhân viên

        Returns:
            Staff: Thông tin nhân viên hoặc None

        Raises:
            Exception: Nếu có lỗi
        """
        try:
            return self.service.get_staff_by_id(staff_id)
        except ValueError as e:
            raise ValueError(str(e))
        except Exception as e:
            raise Exception(f"Lỗi khi lấy thông tin nhân viên: {str(e)}")

    def search_staff(self, keyword):
        """
        Tìm kiếm nhân viên theo từ khóa

        Args:
            keyword: Từ khóa tìm kiếm

        Returns:
            list[Staff]: Danh sách nhân viên phù hợp
        """
        try:
            return self.service.search_staff(keyword)
        except Exception as e:
            raise Exception(f"Lỗi khi tìm kiếm: {str(e)}")

    def get_staff_by_role(self, role_id):
        """
        Lấy danh sách nhân viên theo role

        Args:
            role_id: ID của role

        Returns:
            list[Staff]: Danh sách nhân viên
        """
        try:
            return self.service.get_staff_by_role(role_id)
        except Exception as e:
            raise Exception(f"Lỗi khi lấy nhân viên theo role: {str(e)}")

    # ================= COMMAND (CREATE/UPDATE/DELETE) =================

    def register_staff(self, full_name, username, password, role_id):
        """
        Đăng ký nhân viên mới

        Args:
            full_name: Họ tên
            username: Tên đăng nhập
            password: Mật khẩu
            role_id: ID chức vụ

        Returns:
            dict: {'success': True, 'message': str, 'staff_id': int}
                  hoặc {'success': False, 'message': str}
        """
        try:
            staff_id = self.service.register_staff(full_name, username, password, role_id)
            return {
                'success': True,
                'message': 'Đăng ký nhân viên thành công',
                'staff_id': staff_id
            }
        except ValueError as e:
            return {
                'success': False,
                'message': str(e)
            }
        except Exception as e:
            return {
                'success': False,
                'message': f"Lỗi: {str(e)}"
            }

    def update_role(self, staff_id, new_role_id):
        """
        Cập nhật chức vụ cho nhân viên

        Args:
            staff_id: ID nhân viên
            new_role_id: Role ID mới

        Returns:
            dict: {'success': True, 'message': str}
                  hoặc {'success': False, 'message': str}
        """
        try:
            self.service.update_role(staff_id, new_role_id)
            return {
                'success': True,
                'message': 'Cập nhật chức vụ thành công'
            }
        except ValueError as e:
            return {
                'success': False,
                'message': str(e)
            }
        except Exception as e:
            return {
                'success': False,
                'message': f"Lỗi: {str(e)}"
            }

    def update_staff_info(self, staff_id, full_name=None, username=None):
        """
        Cập nhật thông tin nhân viên

        Args:
            staff_id: ID nhân viên
            full_name: Họ tên mới (optional)
            username: Username mới (optional)

        Returns:
            dict: {'success': bool, 'message': str}
        """
        try:
            self.service.update_staff_info(staff_id, full_name, username)
            return {
                'success': True,
                'message': 'Cập nhật thông tin thành công'
            }
        except ValueError as e:
            return {
                'success': False,
                'message': str(e)
            }
        except Exception as e:
            return {
                'success': False,
                'message': f"Lỗi: {str(e)}"
            }

    def change_password(self, staff_id, old_password, new_password):
        """
        Đổi mật khẩu nhân viên

        Args:
            staff_id: ID nhân viên
            old_password: Mật khẩu cũ
            new_password: Mật khẩu mới

        Returns:
            dict: {'success': bool, 'message': str}
        """
        try:
            self.service.change_password(staff_id, old_password, new_password)
            return {
                'success': True,
                'message': 'Đổi mật khẩu thành công'
            }
        except ValueError as e:
            return {
                'success': False,
                'message': str(e)
            }
        except Exception as e:
            return {
                'success': False,
                'message': f"Lỗi: {str(e)}"
            }

    def delete_staff(self, staff_id):
        """
        Xóa nhân viên khỏi hệ thống

        Args:
            staff_id: ID nhân viên cần xóa

        Returns:
            dict: {'success': bool, 'message': str}
        """
        try:
            self.service.delete_staff(staff_id)
            return {
                'success': True,
                'message': 'Xóa nhân viên thành công'
            }
        except ValueError as e:
            return {
                'success': False,
                'message': str(e)
            }
        except Exception as e:
            return {
                'success': False,
                'message': f"Lỗi: {str(e)}"
            }

    def deactivate_staff(self, staff_id):
        """
        Vô hiệu hóa tài khoản nhân viên

        Args:
            staff_id: ID nhân viên

        Returns:
            dict: {'success': bool, 'message': str}
        """
        try:
            self.service.deactivate_staff(staff_id)
            return {
                'success': True,
                'message': 'Đã vô hiệu hóa tài khoản'
            }
        except Exception as e:
            return {
                'success': False,
                'message': f"Lỗi: {str(e)}"
            }

    def activate_staff(self, staff_id):
        """
        Kích hoạt lại tài khoản nhân viên

        Args:
            staff_id: ID nhân viên

        Returns:
            dict: {'success': bool, 'message': str}
        """
        try:
            self.service.activate_staff(staff_id)
            return {
                'success': True,
                'message': 'Đã kích hoạt tài khoản'
            }
        except Exception as e:
            return {
                'success': False,
                'message': f"Lỗi: {str(e)}"
            }

    # ================= STATISTICS =================

    def get_staff_statistics(self):
        """
        Lấy thống kê nhân viên

        Returns:
            dict: Thông tin thống kê
        """
        try:
            return {
                'success': True,
                'by_role': self.service.get_staff_count_by_role(),
                'active_count': self.service.get_active_staff_count()
            }
        except Exception as e:
            return {
                'success': False,
                'message': f"Lỗi: {str(e)}"
            }