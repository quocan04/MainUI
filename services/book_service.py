from typing import List, Optional, Tuple
import logging

from config.database import db
from models.book import Book, Author, Category, Publisher

logger = logging.getLogger(__name__)


class BookService:
    """Service layer xử lý business logic cho Book"""

    def __init__(self):
        pass

    # ========== CRUD OPERATIONS - BOOKS ==========

    def create_book(self, book: Book) -> Tuple[bool, Optional[str], Optional[int]]:
        """
        Thêm sách mới
        Returns: (success, error_message, book_id)
        """
        # Validate
        is_valid, error = book.validate()
        if not is_valid:
            return False, error, None

        try:
            # Check ISBN duplicate
            if book.isbn:
                existing = db.execute_query(
                    "SELECT book_id FROM books WHERE isbn = %s",
                    (book.isbn,),
                    fetch=True
                )
                if existing:
                    return False, f"ISBN '{book.isbn}' đã tồn tại", None

            # Check Barcode duplicate
            if book.barcode:
                existing = db.execute_query(
                    "SELECT book_id FROM books WHERE barcode = %s",
                    (book.barcode,),
                    fetch=True
                )
                if existing:
                    return False, f"Mã vạch '{book.barcode}' đã tồn tại", None

            # Insert book
            query = """
                INSERT INTO books (title, author_id, category_id, publisher_id,
                                   publish_year, isbn, barcode, price, description)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            book_id = db.execute_query(query, book.to_tuple(), commit=True)

            if book_id:
                # Tạo bản ghi tồn kho
                inventory_query = """
                    INSERT INTO book_inventory (book_id, total_quantity, available_quantity)
                    VALUES (%s, 0, 0)
                """
                db.execute_query(inventory_query, (book_id,), commit=True)

                logger.info(f"✅ Đã thêm sách: {book.title} (ID: {book_id})")
                return True, None, book_id
            else:
                return False, "Không thể thêm sách vào database", None

        except Exception as e:
            logger.error(f"❌ Lỗi thêm sách: {e}")
            return False, f"Lỗi database: {str(e)}", None

    def update_book(self, book: Book) -> Tuple[bool, Optional[str]]:
        """Cập nhật thông tin sách"""
        if not book.book_id:
            return False, "ID sách không hợp lệ"

        is_valid, error = book.validate()
        if not is_valid:
            return False, error

        try:
            # Check ISBN duplicate (trừ sách hiện tại)
            if book.isbn:
                existing = db.execute_query(
                    "SELECT book_id FROM books WHERE isbn = %s AND book_id != %s",
                    (book.isbn, book.book_id),
                    fetch=True
                )
                if existing:
                    return False, f"ISBN '{book.isbn}' đã được sử dụng bởi sách khác"

            # Check Barcode duplicate
            if book.barcode:
                existing = db.execute_query(
                    "SELECT book_id FROM books WHERE barcode = %s AND book_id != %s",
                    (book.barcode, book.book_id),
                    fetch=True
                )
                if existing:
                    return False, f"Mã vạch '{book.barcode}' đã được sử dụng bởi sách khác"

            query = """
                UPDATE books
                SET title = %s, author_id = %s, category_id = %s, publisher_id = %s,
                    publish_year = %s, isbn = %s, barcode = %s, price = %s, description = %s
                WHERE book_id = %s
            """
            params = (
                book.title, book.author_id, book.category_id, book.publisher_id,
                book.publish_year, book.isbn, book.barcode, book.price,
                book.description, book.book_id
            )

            result = db.execute_query(query, params, commit=True)

            if result and result > 0:
                logger.info(f"✅ Đã cập nhật sách ID: {book.book_id}")
                return True, None
            else:
                return False, "Không tìm thấy sách để cập nhật"

        except Exception as e:
            logger.error(f"❌ Lỗi cập nhật sách: {e}")
            return False, f"Lỗi database: {str(e)}"

    def delete_book(self, book_id: int) -> Tuple[bool, Optional[str]]:
        """Xóa sách"""
        try:
            # Kiểm tra sách có đang được mượn không
            check_query = """
                SELECT COUNT(*) as count
                FROM borrow_details bd
                JOIN borrow_slips bs ON bd.slip_id = bs.slip_id
                WHERE bd.book_id = %s AND bs.status = 'BORROWING'
            """
            result = db.execute_query(check_query, (book_id,), fetch=True)

            if result and result[0]['count'] > 0:
                return False, "Không thể xóa sách đang được mượn"

            # Xóa inventory trước
            db.execute_query("DELETE FROM book_inventory WHERE book_id = %s", (book_id,), commit=True)

            # Xóa sách
            result = db.execute_query("DELETE FROM books WHERE book_id = %s", (book_id,), commit=True)

            if result and result > 0:
                logger.info(f"✅ Đã xóa sách ID: {book_id}")
                return True, None
            else:
                return False, "Không tìm thấy sách để xóa"

        except Exception as e:
            logger.error(f"❌ Lỗi xóa sách: {e}")
            return False, f"Lỗi database: {str(e)}"

    def get_all_books(self) -> List[Book]:
        """Lấy danh sách tất cả sách với thông tin JOIN"""
        try:
            query = """
                SELECT b.*, a.author_name, c.category_name, p.publisher_name,
                       COALESCE(bi.total_quantity, 0) as total_quantity,
                       COALESCE(bi.available_quantity, 0) as available_quantity
                FROM books b
                LEFT JOIN authors a ON b.author_id = a.author_id
                LEFT JOIN categories c ON b.category_id = c.category_id
                LEFT JOIN publishers p ON b.publisher_id = p.publisher_id
                LEFT JOIN book_inventory bi ON b.book_id = bi.book_id
                ORDER BY b.book_id DESC
            """
            rows = db.execute_query(query, fetch=True)

            if rows is None:
                return []

            books = [Book.from_dict(row) for row in rows]
            logger.info(f"✅ Đã tải {len(books)} sách")
            return books

        except Exception as e:
            logger.error(f"❌ Lỗi lấy danh sách sách: {e}")
            return []

    def get_book_by_id(self, book_id: int) -> Optional[Book]:
        """Lấy thông tin sách theo ID"""
        try:
            query = """
                SELECT b.*, a.author_name, c.category_name, p.publisher_name,
                       COALESCE(bi.total_quantity, 0) as total_quantity,
                       COALESCE(bi.available_quantity, 0) as available_quantity
                FROM books b
                LEFT JOIN authors a ON b.author_id = a.author_id
                LEFT JOIN categories c ON b.category_id = c.category_id
                LEFT JOIN publishers p ON b.publisher_id = p.publisher_id
                LEFT JOIN book_inventory bi ON b.book_id = bi.book_id
                WHERE b.book_id = %s
            """
            rows = db.execute_query(query, (book_id,), fetch=True)

            if rows and len(rows) > 0:
                return Book.from_dict(rows[0])
            return None

        except Exception as e:
            logger.error(f"❌ Lỗi lấy thông tin sách: {e}")
            return None

    def search_books(self, keyword: str, search_by: str = "all") -> List[Book]:
        """
        Tìm kiếm sách
        search_by: 'all', 'title', 'author', 'isbn', 'barcode', 'category'
        """
        try:
            keyword_pattern = f"%{keyword}%"

            base_query = """
                SELECT b.*, a.author_name, c.category_name, p.publisher_name,
                       COALESCE(bi.total_quantity, 0) as total_quantity,
                       COALESCE(bi.available_quantity, 0) as available_quantity
                FROM books b
                LEFT JOIN authors a ON b.author_id = a.author_id
                LEFT JOIN categories c ON b.category_id = c.category_id
                LEFT JOIN publishers p ON b.publisher_id = p.publisher_id
                LEFT JOIN book_inventory bi ON b.book_id = bi.book_id
            """

            if search_by == "title":
                query = base_query + " WHERE b.title LIKE %s ORDER BY b.book_id DESC"
                params = (keyword_pattern,)
            elif search_by == "author":
                query = base_query + " WHERE a.author_name LIKE %s ORDER BY b.book_id DESC"
                params = (keyword_pattern,)
            elif search_by == "isbn":
                query = base_query + " WHERE b.isbn LIKE %s ORDER BY b.book_id DESC"
                params = (keyword_pattern,)
            elif search_by == "barcode":
                query = base_query + " WHERE b.barcode LIKE %s ORDER BY b.book_id DESC"
                params = (keyword_pattern,)
            elif search_by == "category":
                query = base_query + " WHERE c.category_name LIKE %s ORDER BY b.book_id DESC"
                params = (keyword_pattern,)
            else:  # all
                query = base_query + """
                    WHERE b.title LIKE %s OR a.author_name LIKE %s 
                       OR b.isbn LIKE %s OR b.barcode LIKE %s 
                       OR c.category_name LIKE %s
                    ORDER BY b.book_id DESC
                """
                params = (keyword_pattern, keyword_pattern, keyword_pattern,
                         keyword_pattern, keyword_pattern)

            rows = db.execute_query(query, params, fetch=True)

            if rows is None:
                return []

            books = [Book.from_dict(row) for row in rows]
            logger.info(f"🔍 Tìm thấy {len(books)} sách cho '{keyword}'")
            return books

        except Exception as e:
            logger.error(f"❌ Lỗi tìm kiếm sách: {e}")
            return []

    # ========== INVENTORY MANAGEMENT ==========

    def update_inventory(self, book_id: int, total_qty: int, available_qty: int) -> Tuple[bool, Optional[str]]:
        """Cập nhật tồn kho"""
        if total_qty < 0 or available_qty < 0:
            return False, "Số lượng không được âm"

        if available_qty > total_qty:
            return False, "Số lượng còn không được lớn hơn tổng số"

        try:
            query = """
                UPDATE book_inventory
                SET total_quantity = %s, available_quantity = %s
                WHERE book_id = %s
            """
            result = db.execute_query(query, (total_qty, available_qty, book_id), commit=True)

            if result:
                logger.info(f"✅ Đã cập nhật tồn kho sách ID {book_id}: {available_qty}/{total_qty}")
                return True, None
            else:
                return False, "Không tìm thấy sách"

        except Exception as e:
            logger.error(f"❌ Lỗi cập nhật tồn kho: {e}")
            return False, f"Lỗi: {str(e)}"

    # ========== AUTHORS ==========

    def get_all_authors(self) -> List[Author]:
        """Lấy danh sách tác giả"""
        try:
            rows = db.execute_query("SELECT * FROM authors ORDER BY author_name", fetch=True)
            return [Author.from_dict(row) for row in rows] if rows else []
        except Exception as e:
            logger.error(f"❌ Lỗi lấy danh sách tác giả: {e}")
            return []

    def create_author(self, name: str) -> Tuple[bool, Optional[str], Optional[int]]:
        """Thêm tác giả mới"""
        if not name or not name.strip():
            return False, "Tên tác giả không được để trống", None

        try:
            author_id = db.execute_query(
                "INSERT INTO authors (author_name) VALUES (%s)",
                (name.strip(),),
                commit=True
            )
            return True, None, author_id
        except Exception as e:
            return False, f"Lỗi: {str(e)}", None

    # ========== CATEGORIES ==========

    def get_all_categories(self) -> List[Category]:
        """Lấy danh sách thể loại"""
        try:
            rows = db.execute_query("SELECT * FROM categories ORDER BY category_name", fetch=True)
            return [Category.from_dict(row) for row in rows] if rows else []
        except Exception as e:
            logger.error(f"❌ Lỗi lấy danh sách thể loại: {e}")
            return []

    def create_category(self, name: str) -> Tuple[bool, Optional[str], Optional[int]]:
        """Thêm thể loại mới"""
        if not name or not name.strip():
            return False, "Tên thể loại không được để trống", None

        try:
            category_id = db.execute_query(
                "INSERT INTO categories (category_name) VALUES (%s)",
                (name.strip(),),
                commit=True
            )
            return True, None, category_id
        except Exception as e:
            return False, f"Lỗi: {str(e)}", None

    # ========== PUBLISHERS ==========

    def get_all_publishers(self) -> List[Publisher]:
        """Lấy danh sách nhà xuất bản"""
        try:
            rows = db.execute_query("SELECT * FROM publishers ORDER BY publisher_name", fetch=True)
            return [Publisher.from_dict(row) for row in rows] if rows else []
        except Exception as e:
            logger.error(f"❌ Lỗi lấy danh sách NXB: {e}")
            return []

    def create_publisher(self, publisher: Publisher) -> Tuple[bool, Optional[str], Optional[int]]:
        """Thêm nhà xuất bản mới"""
        if not publisher.publisher_name or not publisher.publisher_name.strip():
            return False, "Tên NXB không được để trống", None

        try:
            query = "INSERT INTO publishers (publisher_name, address, phone) VALUES (%s, %s, %s)"
            publisher_id = db.execute_query(
                query,
                (publisher.publisher_name, publisher.address, publisher.phone),
                commit=True
            )
            return True, None, publisher_id
        except Exception as e:
            return False, f"Lỗi: {str(e)}", None

    # ========== STATISTICS ==========

    def get_statistics(self) -> dict:
        """Lấy thống kê sách"""
        try:
            stats = {
                'total_books': 0,
                'total_quantity': 0,
                'available_quantity': 0,
                'borrowed_quantity': 0,
                'out_of_stock': 0,
                'low_stock': 0,
                'total_authors': 0,
                'total_categories': 0,
                'total_publishers': 0
            }

            # Tổng số đầu sách
            result = db.execute_query("SELECT COUNT(*) as count FROM books", fetch=True)
            if result:
                stats['total_books'] = result[0]['count']

            # Tổng số lượng sách
            result = db.execute_query(
                "SELECT SUM(total_quantity) as total, SUM(available_quantity) as available FROM book_inventory",
                fetch=True
            )
            if result and result[0]['total']:
                stats['total_quantity'] = int(result[0]['total'])
                stats['available_quantity'] = int(result[0]['available'])
                stats['borrowed_quantity'] = stats['total_quantity'] - stats['available_quantity']

            # Số sách hết hàng
            result = db.execute_query(
                "SELECT COUNT(*) as count FROM book_inventory WHERE available_quantity = 0",
                fetch=True
            )
            if result:
                stats['out_of_stock'] = result[0]['count']

            # Số sách sắp hết (< 5)
            result = db.execute_query(
                "SELECT COUNT(*) as count FROM book_inventory WHERE available_quantity > 0 AND available_quantity < 5",
                fetch=True
            )
            if result:
                stats['low_stock'] = result[0]['count']

            # Số tác giả
            result = db.execute_query("SELECT COUNT(*) as count FROM authors", fetch=True)
            if result:
                stats['total_authors'] = result[0]['count']

            # Số thể loại
            result = db.execute_query("SELECT COUNT(*) as count FROM categories", fetch=True)
            if result:
                stats['total_categories'] = result[0]['count']

            # Số NXB
            result = db.execute_query("SELECT COUNT(*) as count FROM publishers", fetch=True)
            if result:
                stats['total_publishers'] = result[0]['count']

            return stats

        except Exception as e:
            logger.error(f"❌ Lỗi thống kê: {e}")
            return {}