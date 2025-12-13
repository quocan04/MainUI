from services.system_service import SystemService
from tkinter import filedialog


class SystemController:
    def __init__(self):
        self.service = SystemService()

    def get_current_settings(self):
        return self.service.get_settings()

    def save_settings(self, settings_data):
        # --- 1. VALIDATION: Kiểm tra nhập liệu ---
        # Đảm bảo người dùng nhập số chứ không nhập chữ
        try:
            int(settings_data.get('MAX_BORROW', 0))
            int(settings_data.get('BORROW_DAYS', 0))
            float(settings_data.get('LATE_FEE_PER_DAY', 0))
            float(settings_data.get('LOST_FINE_RATE', 0))
        except ValueError:
            return False, "Vui lòng chỉ nhập số vào các ô cài đặt!"

        # --- 2. LƯU DỮ LIỆU ---
        if self.service.update_settings(settings_data):
            return True, "Cập nhật thành công!"
        else:
            return False, "Cập nhật thất bại!"

    def perform_backup(self):
        success, message = self.service.backup_data()
        if success:
            return True, f"Sao lưu thành công!\nFile lưu tại: {message}"
        else:
            return False, f"Lỗi sao lưu: {message}"

    def perform_restore(self):
        """Mở hộp thoại chọn file và thực hiện restore"""
        filepath = filedialog.askopenfilename(
            title="Chọn file sao lưu (.json)",
            filetypes=[("JSON Files", "*.json")]
        )

        if not filepath:
            return False, "Đã hủy chọn file."

        success, msg = self.service.restore_data(filepath)
        return success, msg