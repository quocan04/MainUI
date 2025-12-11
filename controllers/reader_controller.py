from typing import List, Optional
import logging

from models.reader import Reader
from services.reader_service import ReaderService
from utils.messagebox_helper import MessageBoxHelper
from utils. export_helper import ExportHelper

logger = logging.getLogger(__name__)


class ReaderController:
    """Controller xử lý logic giữa View và Service"""

    def __init__(self):
        self.service = ReaderService()
        self.msg_helper = MessageBoxHelper()
        self.export_helper = ExportHelper()

    # ========== CRUD OPERATIONS ==========

    def add_reader(self, reader:  Reader, parent=None) -> bool:
        """
        Thêm bạn đọc mới
        Returns: True nếu thành công
        """
        success, error, reader_id = self.service.create_reader(reader)

        if success:
            self.msg_helper.show_success(
                f"Thêm bạn đọc thành công!\nID: {reader_id}",
                parent=parent
            )
            return True
        else:
            self.msg_helper.show_error("Lỗi thêm bạn đọc", error, parent=parent)
            return False

    def update_reader(self, reader:  Reader, parent=None) -> bool:
        """
        Cập nhật thông tin bạn đọc
        Returns: True nếu thành công
        """
        success, error = self.service.update_reader(reader)

        if success:
            self.msg_helper.show_success("Cập nhật thông tin thành công!", parent=parent)
            return True
        else:
            self.msg_helper.show_error("Lỗi cập nhật", error, parent=parent)
            return False

    def delete_reader(self, reader_id: int, reader_name: str, parent=None) -> bool:
        """
        Xóa bạn đọc
        Returns: True nếu thành công
        """
        # Xác nhận xóa
        if not self.msg_helper.ask_delete(f"bạn đọc '{reader_name}'", parent=parent):
            return False

        success, error = self. service.delete_reader(reader_id)

        if success:
            self.msg_helper.show_success("Xóa bạn đọc thành công!", parent=parent)
            return True
        else:
            self.msg_helper.show_error("Lỗi xóa bạn đọc", error, parent=parent)
            return False

    # ========== QUERY OPERATIONS ==========

    def get_all_readers(self) -> List[Reader]:
        """Lấy danh sách tất cả bạn đọc"""
        return self.service.get_all_readers()

    def get_reader_by_id(self, reader_id: int) -> Optional[Reader]:
        """Lấy thông tin bạn đọc theo ID"""
        return self. service.get_reader_by_id(reader_id)

    def search_readers(self, keyword: str, search_by: str = "all") -> List[Reader]:
        """Tìm kiếm bạn đọc"""
        if not keyword. strip():
            return self.get_all_readers()
        return self.service.search_readers(keyword, search_by)

    def filter_readers(
        self,
        status: Optional[str] = None,
        min_reputation: Optional[int] = None,
        max_reputation: Optional[int] = None,
        expiring_soon: bool = False
    ) -> List[Reader]:
        """Lọc bạn đọc"""
        return self.service.filter_readers(status, min_reputation, max_reputation, expiring_soon)

    def get_statistics(self) -> dict:
        """Lấy thống kê"""
        return self.service.get_statistics()

    # ========== STATUS OPERATIONS ==========

    def update_status(self, reader_id: int, new_status: str, parent=None) -> bool:
        """Cập nhật trạng thái bạn đọc"""
        success, error = self.service.update_reader_status(reader_id, new_status)

        if success:
            self.msg_helper. show_success(f"Đã cập nhật trạng thái thành {new_status}", parent=parent)
            return True
        else:
            self.msg_helper.show_error("Lỗi cập nhật trạng thái", error, parent=parent)
            return False

    def lock_reader(self, reader_id: int, parent=None) -> bool:
        """Khóa bạn đọc"""
        if self.msg_helper.confirm("Xác nhận khóa", "Bạn có chắc muốn khóa bạn đọc này? ", parent=parent):
            return self.update_status(reader_id, Reader.STATUS_LOCKED, parent)
        return False

    def unlock_reader(self, reader_id: int, parent=None) -> bool:
        """Mở khóa bạn đọc"""
        return self.update_status(reader_id, Reader.STATUS_ACTIVE, parent)

    def extend_card(self, reader_id: int, days: int = 365, parent=None) -> bool:
        """Gia hạn thẻ"""
        success, error = self.service.extend_card_validity(reader_id, days)

        if success:
            self.msg_helper. show_success(f"Đã gia hạn thẻ thêm {days} ngày", parent=parent)
            return True
        else:
            self.msg_helper.show_error("Lỗi gia hạn thẻ", error, parent=parent)
            return False

    def check_expired_cards(self) -> List[Reader]:
        """Kiểm tra thẻ hết hạn"""
        return self.service.check_expired_cards()

    def auto_update_expired(self, parent=None) -> bool:
        """Tự động cập nhật trạng thái hết hạn"""
        count, message = self.service.auto_update_expired_status()
        if count > 0:
            self.msg_helper.show_info("Cập nhật hoàn tất", message, parent=parent)
            return True
        else:
            self.msg_helper.show_info("Không có gì thay đổi", message, parent=parent)
            return False

    # ========== EXPORT OPERATIONS ==========

    def export_json(self, readers: List[Reader], parent=None) -> bool:
        """Xuất ra JSON"""
        if not readers:
            self.msg_helper.show_warning("Không có dữ liệu", "Không có bạn đọc để xuất", parent=parent)
            return False

        success, message = self.export_helper.export_to_json(readers)

        if success:
            self. msg_helper.show_success(
                f"Đã xuất {len(readers)} bạn đọc ra JSON\n{message}",
                parent=parent
            )
            return True
        else:
            self. msg_helper.show_error("Lỗi xuất JSON", message, parent=parent)
            return False

    def export_csv(self, readers: List[Reader], parent=None) -> bool:
        """Xuất ra CSV"""
        if not readers:
            self.msg_helper. show_warning("Không có dữ liệu", "Không có bạn đọc để xuất", parent=parent)
            return False

        success, message = self.export_helper. export_to_csv(readers)

        if success:
            self.msg_helper.show_success(
                f"Đã xuất {len(readers)} bạn đọc ra CSV\n{message}",
                parent=parent
            )
            return True
        else:
            self.msg_helper.show_error("Lỗi xuất CSV", message, parent=parent)
            return False

    def export_excel(self, readers: List[Reader], parent=None) -> bool:
        """Xuất ra Excel"""
        if not readers:
            self.msg_helper.show_warning("Không có dữ liệu", "Không có bạn đọc để xuất", parent=parent)
            return False

        success, message = self.export_helper.export_to_excel(readers)

        if success:
            self. msg_helper.show_success(
                f"Đã xuất {len(readers)} bạn đọc ra Excel\n{message}",
                parent=parent
            )
            return True
        else:
            self. msg_helper.show_error("Lỗi xuất Excel", message, parent=parent)
            return False

    def export_pdf(self, readers: List[Reader], parent=None) -> bool:
        """Xuất ra PDF"""
        if not readers:
            self.msg_helper. show_warning("Không có dữ liệu", "Không có bạn đọc để xuất", parent=parent)
            return False

        success, message = self.export_helper. export_to_pdf(readers)

        if success:
            self.msg_helper.show_success(
                f"Đã xuất {len(readers)} bạn đọc ra PDF\n{message}",
                parent=parent
            )
            return True
        else:
            self.msg_helper.show_error("Lỗi xuất PDF", message, parent=parent)
            return False