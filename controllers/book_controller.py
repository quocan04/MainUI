from typing import List, Optional
import logging

from models.book import Book, Author, Category, Publisher
from services.book_service import BookService
from utils.messagebox_helper import MessageBoxHelper
from utils.export_helper import ExportHelper

logger = logging.getLogger(__name__)


class BookController:
    """Controller xử lý logic giữa View và Service"""

    def __init__(self):
        self.service = BookService()
        self.msg_helper = MessageBoxHelper()
        self.export_helper = ExportHelper()

    # ========== CRUD OPERATIONS - BOOKS ==========

    def add_book(self, book: Book, parent=None) -> bool:
        """
        Thêm sách mới
        Returns: True nếu thành công
        """
        success, error, book_id = self.service.create_book(book)

        if success:
            self.msg_helper.show_success(
                f"Thêm sách thành công!\nID: {book_id}",
                parent=parent
            )
            return True
        else:
            self.msg_helper.show_error("Lỗi thêm sách", error, parent=parent)
            return False

    def update_book(self, book: Book, parent=None) -> bool:
        """
        Cập nhật thông tin sách
        Returns: True nếu thành công
        """
        success, error = self.service.update_book(book)

        if success:
            self.msg_helper.show_success("Cập nhật thông tin thành công!", parent=parent)
            return True
        else:
            self.msg_helper.show_error("Lỗi cập nhật", error, parent=parent)
            return False

    def delete_book(self, book_id: int, book_title: str, parent=None) -> bool:
        """
        Xóa sách
        Returns: True nếu thành công
        """
        # Xác nhận xóa
        if not self.msg_helper.ask_delete(f"sách '{book_title}'", parent=parent):
            return False

        success, error = self.service.delete_book(book_id)

        if success:
            self.msg_helper.show_success("Xóa sách thành công!", parent=parent)
            return True
        else:
            self.msg_helper.show_error("Lỗi xóa sách", error, parent=parent)
            return False

    # ========== QUERY OPERATIONS ==========

    def get_all_books(self) -> List[Book]:
        """Lấy danh sách tất cả sách"""
        return self.service.get_all_books()

    def get_book_by_id(self, book_id: int) -> Optional[Book]:
        """Lấy thông tin sách theo ID"""
        return self.service.get_book_by_id(book_id)

    def search_books(self, keyword: str, search_by: str = "all") -> List[Book]:
        """Tìm kiếm sách"""
        if not keyword.strip():
            return self.get_all_books()
        return self.service.search_books(keyword, search_by)

    def get_statistics(self) -> dict:
        """Lấy thống kê"""
        return self.service.get_statistics()

    # ========== INVENTORY OPERATIONS ==========

    def update_inventory(self, book_id: int, total_qty: int, available_qty: int, parent=None) -> bool:
        """Cập nhật tồn kho"""
        success, error = self.service.update_inventory(book_id, total_qty, available_qty)

        if success:
            self.msg_helper.show_success(
                f"Đã cập nhật tồn kho:\nTổng: {total_qty}, Còn: {available_qty}",
                parent=parent
            )
            return True
        else:
            self.msg_helper.show_error("Lỗi cập nhật tồn kho", error, parent=parent)
            return False

    # ========== AUTHORS ==========

    def get_all_authors(self) -> List[Author]:
        """Lấy danh sách tác giả"""
        return self.service.get_all_authors()

    def add_author(self, name: str, parent=None) -> Optional[int]:
        """Thêm tác giả mới"""
        success, error, author_id = self.service.create_author(name)

        if success:
            self.msg_helper.show_success(f"Đã thêm tác giả: {name}", parent=parent)
            return author_id
        else:
            self.msg_helper.show_error("Lỗi thêm tác giả", error, parent=parent)
            return None

    # ========== CATEGORIES ==========

    def get_all_categories(self) -> List[Category]:
        """Lấy danh sách thể loại"""
        return self.service.get_all_categories()

    def add_category(self, name: str, parent=None) -> Optional[int]:
        """Thêm thể loại mới"""
        success, error, category_id = self.service.create_category(name)

        if success:
            self.msg_helper.show_success(f"Đã thêm thể loại: {name}", parent=parent)
            return category_id
        else:
            self.msg_helper.show_error("Lỗi thêm thể loại", error, parent=parent)
            return None

    # ========== PUBLISHERS ==========

    def get_all_publishers(self) -> List[Publisher]:
        """Lấy danh sách nhà xuất bản"""
        return self.service.get_all_publishers()

    def add_publisher(self, publisher: Publisher, parent=None) -> Optional[int]:
        """Thêm nhà xuất bản mới"""
        success, error, publisher_id = self.service.create_publisher(publisher)

        if success:
            self.msg_helper.show_success(
                f"Đã thêm nhà xuất bản: {publisher.publisher_name}",
                parent=parent
            )
            return publisher_id
        else:
            self.msg_helper.show_error("Lỗi thêm nhà xuất bản", error, parent=parent)
            return None

    # ========== EXPORT OPERATIONS ==========

    def export_json(self, books: List[Book], parent=None) -> bool:
        """Xuất ra JSON"""
        if not books:
            self.msg_helper.show_warning("Không có dữ liệu", "Không có sách để xuất", parent=parent)
            return False

        success, message = self.export_helper.export_books_to_json(books)

        if success:
            self.msg_helper.show_success(
                f"Đã xuất {len(books)} sách ra JSON\n{message}",
                parent=parent
            )
            return True
        else:
            self.msg_helper.show_error("Lỗi xuất JSON", message, parent=parent)
            return False

    def export_csv(self, books: List[Book], parent=None) -> bool:
        """Xuất ra CSV"""
        if not books:
            self.msg_helper.show_warning("Không có dữ liệu", "Không có sách để xuất", parent=parent)
            return False

        success, message = self.export_helper.export_books_to_csv(books)

        if success:
            self.msg_helper.show_success(
                f"Đã xuất {len(books)} sách ra CSV\n{message}",
                parent=parent
            )
            return True
        else:
            self.msg_helper.show_error("Lỗi xuất CSV", message, parent=parent)
            return False

    def export_excel(self, books: List[Book], parent=None) -> bool:
        """Xuất ra Excel"""
        if not books:
            self.msg_helper.show_warning("Không có dữ liệu", "Không có sách để xuất", parent=parent)
            return False

        success, message = self.export_helper.export_books_to_excel(books)

        if success:
            self.msg_helper.show_success(
                f"Đã xuất {len(books)} sách ra Excel\n{message}",
                parent=parent
            )
            return True
        else:
            self.msg_helper.show_error("Lỗi xuất Excel", message, parent=parent)
            return False

    def export_pdf(self, books: List[Book], parent=None) -> bool:
        """Xuất ra PDF"""
        if not books:
            self.msg_helper.show_warning("Không có dữ liệu", "Không có sách để xuất", parent=parent)
            return False

        success, message = self.export_helper.export_books_to_pdf(books)

        if success:
            self.msg_helper.show_success(
                f"Đã xuất {len(books)} sách ra PDF\n{message}",
                parent=parent
            )
            return True
        else:
            self.msg_helper.show_error("Lỗi xuất PDF", message, parent=parent)
            return False