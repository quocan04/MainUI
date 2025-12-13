class RolePermissions:


    PERMISSIONS = {
        1: {  # Admin - Full quyền
            "register_staff",
            "update_role",
            "delete_staff",
            "view_staff",
            "export_excel"
        },
        2: {  # Thủ thư - Không có quyền cập nhật chức vụ và xóa
            "register_staff",
            "view_staff",
            "export_excel"
        },
        3: {  # Nhân viên thường - Chỉ xem và xuất excel
            "view_staff",      # ← THÊM DÒNG NÀY
            "export_excel"
        },
        5: {  # Super Admin - Full quyền như Admin
            "register_staff",
            "update_role",
            "delete_staff",
            "view_staff",
            "export_excel"
        }
    }

    @classmethod
    def has_permission(cls, role_id: int, permission: str) -> bool:
        """
        Kiểm tra role_id có quyền permission hay không
        """
        if role_id not in cls.PERMISSIONS:
            return False
        return permission in cls.PERMISSIONS[role_id]


def has_permission(role_id: int, permission: str) -> bool:
    """Helper function để gọi ngắn gọn hơn"""
    return RolePermissions.has_permission(role_id, permission)
