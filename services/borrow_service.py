from datetime import datetime, timedelta
from config.database import db

from models.BorrowSlip import BorrowSlip
from models.BorrowDetail import BorrowDetail
from models.reader import Reader
from models.book import Book


class BorrowService:
    """Service xử lý mượn / trả sách"""

    BORROW_DAYS = 14

    # ==================================================
    # Tạo phiếu mượn (theo tên bạn đọc & tên sách)
    # ==================================================
    def create_borrow(self, reader_name: str, book_name: str):
        # ---------- Lấy bạn đọc ----------
        sql_reader = "SELECT * FROM readers WHERE full_name=%s"
        reader_data = db.fetchone(sql_reader, (reader_name,))
        if not reader_data:
            return False, "Bạn đọc không tồn tại"

        reader = Reader.from_dict(reader_data)
        can_borrow, reason = reader.can_borrow()
        if not can_borrow:
            return False, reason

        # ---------- Lấy sách ----------
        sql_book = "SELECT * FROM books WHERE title=%s"
        book_data = db.fetchone(sql_book, (book_name,))
        if not book_data:
            return False, f"Sách '{book_name}' không tồn tại"

        book = Book.from_dict(book_data)

        # ---------- Kiểm tra tồn kho ----------
        sql_inventory = """
        SELECT available_quantity
        FROM book_inventory
        WHERE book_id=%s
        """
        inv_data = db.fetchone(sql_inventory, (book.book_id,))
        if not inv_data or inv_data["available_quantity"] < 1:
            return False, f"Sách '{book_name}' không đủ số lượng"

        # ---------- Tạo phiếu mượn ----------
        borrow_date = datetime.now().date()
        return_due = borrow_date + timedelta(days=self.BORROW_DAYS)

        slip = BorrowSlip(
            reader_id=reader.reader_id,
            staff_id=1,  # demo
            borrow_date=borrow_date,
            return_due=return_due
        )
        slip_id = self._insert_borrow_slip(slip)

        # ---------- Tạo chi tiết mượn ----------
        detail = BorrowDetail(
            slip_id=slip_id,
            book_id=book.book_id,
            quantity=1
        )
        self._insert_borrow_detail(detail)

        # ---------- Trừ tồn kho ----------
        self._decrease_stock(book.book_id, 1)

        return True, "Tạo phiếu mượn thành công"

    # ==================================================
    # Cập nhật phiếu mượn
    # ==================================================
    def update_borrow(self, slip_id, borrow_date, return_date, status):
        sql_check = "SELECT * FROM borrow_slips WHERE slip_id=%s"
        if not db.fetchone(sql_check, (slip_id,)):
            return False, "Phiếu mượn không tồn tại"

        sql_update = """
        UPDATE borrow_slips
        SET borrow_date=%s,
            return_date=%s,
            status=%s
        WHERE slip_id=%s
        """
        db.execute_query(
            sql_update,
            (borrow_date, return_date, status, slip_id),
            commit=True
        )

        return True, "Cập nhật phiếu mượn thành công"

    # ==================================================
    # Trả sách
    # ==================================================
    def return_books(self, slip_id):
        # ---------- Lấy phiếu ----------
        sql_slip = "SELECT * FROM borrow_slips WHERE slip_id=%s"
        slip = db.fetchone(sql_slip, (slip_id,))
        if not slip:
            return False, "Phiếu mượn không tồn tại"

        if slip["status"] == "RETURNED":
            return False, "Phiếu mượn đã được trả"

        # ---------- Lấy chi tiết mượn ----------
        sql_details = "SELECT * FROM borrow_details WHERE slip_id=%s"
        details = db.fetchall(sql_details, (slip_id,))
        if not details:
            return False, "Không tìm thấy chi tiết mượn"

        # ---------- Hoàn kho ----------
        for d in details:
            sql_inc = """
            UPDATE book_inventory
            SET available_quantity = available_quantity + %s
            WHERE book_id = %s
            """
            db.execute_query(
                sql_inc,
                (d["quantity"], d["book_id"]),
                commit=True
            )

        # ---------- Cập nhật trạng thái ----------
        today = datetime.now().date()
        sql_update = """
        UPDATE borrow_slips
        SET status='RETURNED',
            return_date=%s
        WHERE slip_id=%s
        """
        db.execute_query(sql_update, (today, slip_id), commit=True)

        return True, "Trả sách thành công"

    # ==================================================
    # Lấy danh sách tất cả phiếu mượn / trả
    # ==================================================
    def get_all_borrows(self):
        sql = """
        SELECT
            b.slip_id,
            r.full_name,
            bk.title AS book_name,
            b.borrow_date,
            b.return_due,
            b.return_date,
            b.status
        FROM borrow_slips b
        JOIN readers r ON b.reader_id = r.reader_id
        JOIN borrow_details bd ON b.slip_id = bd.slip_id
        JOIN books bk ON bd.book_id = bk.book_id
        ORDER BY b.borrow_date DESC
        """
        return db.execute_query(sql, fetch=True)

    # ==================================================
    # INTERNAL METHODS
    # ==================================================
    def _insert_borrow_slip(self, slip: BorrowSlip):
        sql = """
        INSERT INTO borrow_slips
        (reader_id, staff_id, borrow_date, return_due, status)
        VALUES (%s, %s, %s, %s, %s)
        """
        return db.execute_query(sql, slip.to_tuple(), commit=True)

    def _insert_borrow_detail(self, detail: BorrowDetail):
        sql = """
        INSERT INTO borrow_details
        (slip_id, book_id, quantity, fine_amount)
        VALUES (%s, %s, %s, %s)
        """
        db.execute_query(sql, detail.to_tuple(), commit=True)

    def _decrease_stock(self, book_id, quantity):
        sql = """
        UPDATE book_inventory
        SET available_quantity = available_quantity - %s
        WHERE book_id=%s
        """
        db.execute_query(sql, (quantity, book_id), commit=True)
