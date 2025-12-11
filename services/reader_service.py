from typing import List, Optional, Tuple
from datetime import datetime, timedelta
import logging

from config.database import db
from models.reader import Reader
from utils.validators import Validator

logger = logging.getLogger(__name__)


class ReaderService:
    """Service layer xử lý business logic cho Reader"""

    def __init__(self):
        self.validator = Validator()

    def validate_reader(self, reader: Reader, is_update: bool = False) -> Tuple[bool, Optional[str]]:
        """
        Validate toàn bộ thông tin reader
        Returns:  (is_valid, error_message)
        """
        # Validate bằng method của model trước
        is_valid, error = reader.validate()
        if not is_valid:
            return False, error

        # Validate họ tên
        is_valid, error = self.validator.validate_full_name(reader.full_name)
        if not is_valid:
            return False, error

        # Validate số điện thoại
        if reader.phone:
            is_valid, error = self.validator.validate_phone(reader.phone)
            if not is_valid:
                return False, error

        # Validate email
        if reader.email:
            is_valid, error = self.validator.validate_email(reader.email)
            if not is_valid:
                return False, error

        # Validate địa chỉ
        if reader.address:
            is_valid, error = self.validator.validate_address(reader.address)
            if not is_valid:
                return False, error

        # Validate ngày cấp thẻ và ngày hết hạn
        if reader.card_start:
            is_valid, error = self.validator.validate_date(reader.card_start, "Ngày cấp thẻ")
            if not is_valid:
                return False, error

        if reader.card_end:
            is_valid, error = self.validator.validate_date(reader.card_end, "Ngày hết hạn")
            if not is_valid:
                return False, error

        # Validate khoảng thời gian
        if reader.card_start and reader.card_end:
            is_valid, error = self.validator.validate_date_range(
                reader.card_start,
                reader.card_end
            )
            if not is_valid:
                return False, error

        # Validate điểm uy tín
        is_valid, error = self.validator.validate_reputation_score(reader.reputation_score)
        if not is_valid:
            return False, error

        return True, None

    def create_reader(self, reader: Reader) -> Tuple[bool, Optional[str], Optional[int]]:
        """
        Thêm bạn đọc mới
        Returns: (success, error_message, reader_id)
        """
        # Validate
        is_valid, error = self.validate_reader(reader, is_update=False)
        if not is_valid:
            return False, error, None

        try:
            query = """
                    INSERT INTO readers (full_name, address, phone, email, \
                                         card_start, card_end, status, reputation_score) \
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s) \
                    """

            params = reader.to_tuple()
            reader_id = db.execute_query(query, params, commit=True)

            if reader_id:
                logger.info(f"✅ Đã thêm bạn đọc:  {reader.full_name} (ID: {reader_id})")
                return True, None, reader_id
            else:
                return False, "Không thể thêm bạn đọc vào database", None

        except Exception as e:
            logger.error(f"❌ Lỗi thêm bạn đọc: {e}")
            return False, f"Lỗi database: {str(e)}", None

    def update_reader(self, reader: Reader) -> Tuple[bool, Optional[str]]:
        """
        Cập nhật thông tin bạn đọc
        Returns: (success, error_message)
        """
        if not reader.reader_id:
            return False, "ID bạn đọc không hợp lệ"

        # Validate
        is_valid, error = self.validate_reader(reader, is_update=True)
        if not is_valid:
            return False, error

        try:
            query = """
                    UPDATE readers \
                    SET full_name        = %s, \
                        address          = %s, \
                        phone            = %s, \
                        email            = %s, \
                        card_start       = %s, \
                        card_end         = %s, \
                        status           = %s, \
                        reputation_score = %s
                    WHERE reader_id = %s \
                    """

            params = (
                reader.full_name,
                reader.address,
                reader.phone,
                reader.email,
                reader.card_start,
                reader.card_end,
                reader.status,
                reader.reputation_score,
                reader.reader_id
            )

            result = db.execute_query(query, params, commit=True)

            if result and result > 0:
                logger.info(f"✅ Đã cập nhật bạn đọc ID: {reader.reader_id}")
                return True, None
            else:
                return False, "Không tìm thấy bạn đọc để cập nhật"

        except Exception as e:
            logger.error(f"❌ Lỗi cập nhật bạn đọc: {e}")
            return False, f"Lỗi database:  {str(e)}"

    def delete_reader(self, reader_id: int) -> Tuple[bool, Optional[str]]:
        """
        Xóa bạn đọc
        Returns: (success, error_message)
        """
        try:
            # Kiểm tra xem bạn đọc có đang mượn sách không
            check_query = """
                          SELECT COUNT(*) as count
                          FROM borrow_slips
                          WHERE reader_id = %s AND status = 'BORROWING' \
                          """
            result = db.execute_query(check_query, (reader_id,), fetch_one=True)

            if result and result['count'] > 0:
                return False, "Không thể xóa bạn đọc đang mượn sách"

            # Xóa bạn đọc
            query = "DELETE FROM readers WHERE reader_id = %s"
            result = db.execute_query(query, (reader_id,), commit=True)

            if result and result > 0:
                logger.info(f"✅ Đã xóa bạn đọc ID: {reader_id}")
                return True, None
            else:
                return False, "Không tìm thấy bạn đọc để xóa"

        except Exception as e:
            logger.error(f"❌ Lỗi xóa bạn đọc: {e}")
            return False, f"Lỗi database:  {str(e)}"

    def get_all_readers(self) -> List[Reader]:
        """Lấy danh sách tất cả bạn đọc"""
        try:
            query = "SELECT * FROM readers ORDER BY reader_id DESC"
            rows = db.execute_query(query, fetch=True)

            if rows is None:
                return []

            readers = [Reader.from_dict(row) for row in rows]
            logger.info(f"✅ Đã tải {len(readers)} bạn đọc")
            return readers

        except Exception as e:
            logger.error(f"❌ Lỗi lấy danh sách:  {e}")
            return []

    def get_reader_by_id(self, reader_id: int) -> Optional[Reader]:
        """Lấy thông tin bạn đọc theo ID"""
        try:
            query = "SELECT * FROM readers WHERE reader_id = %s"
            row = db.execute_query(query, (reader_id,), fetch_one=True)

            if row:
                return Reader.from_dict(row)
            return None

        except Exception as e:
            logger.error(f"❌ Lỗi lấy thông tin:  {e}")
            return None

    def search_readers(self, keyword: str, search_by: str = "all") -> List[Reader]:
        """
        Tìm kiếm bạn đọc
        search_by: 'all', 'name', 'phone', 'email', 'address'
        """
        try:
            keyword_pattern = f"%{keyword}%"

            if search_by == "name":
                query = "SELECT * FROM readers WHERE full_name LIKE %s ORDER BY reader_id DESC"
                params = (keyword_pattern,)
            elif search_by == "phone":
                query = "SELECT * FROM readers WHERE phone LIKE %s ORDER BY reader_id DESC"
                params = (keyword_pattern,)
            elif search_by == "email":
                query = "SELECT * FROM readers WHERE email LIKE %s ORDER BY reader_id DESC"
                params = (keyword_pattern,)
            elif search_by == "address":
                query = "SELECT * FROM readers WHERE address LIKE %s ORDER BY reader_id DESC"
                params = (keyword_pattern,)
            else:  # search all
                query = """
                        SELECT * \
                        FROM readers
                        WHERE full_name LIKE %s
                           OR phone LIKE %s
                           OR email LIKE %s
                           OR address LIKE %s
                        ORDER BY reader_id DESC \
                        """
                params = (keyword_pattern, keyword_pattern, keyword_pattern, keyword_pattern)

            rows = db.execute_query(query, params, fetch=True)

            if rows is None:
                return []

            readers = [Reader.from_dict(row) for row in rows]
            logger.info(f"🔍 Tìm thấy {len(readers)} kết quả cho '{keyword}'")
            return readers

        except Exception as e:
            logger.error(f"❌ Lỗi tìm kiếm: {e}")
            return []

    def filter_readers(
            self,
            status: Optional[str] = None,
            min_reputation: Optional[int] = None,
            max_reputation: Optional[int] = None,
            expiring_soon: bool = False
    ) -> List[Reader]:
        """Lọc bạn đọc theo các tiêu chí"""
        try:
            query = "SELECT * FROM readers WHERE 1=1"
            params = []

            # Lọc theo trạng thái
            if status and status != "Tất cả":
                query += " AND status = %s"
                params.append(status)

            # Lọc theo điểm uy tín
            if min_reputation is not None:
                query += " AND reputation_score >= %s"
                params.append(min_reputation)

            if max_reputation is not None:
                query += " AND reputation_score <= %s"
                params.append(max_reputation)

            # Lọc thẻ sắp hết hạn (trong 30 ngày)
            if expiring_soon:
                date_30_days = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
                query += " AND card_end <= %s AND card_end >= CURDATE()"
                params.append(date_30_days)

            query += " ORDER BY reader_id DESC"

            rows = db.execute_query(query, tuple(params) if params else None, fetch=True)

            if rows is None:
                return []

            readers = [Reader.from_dict(row) for row in rows]
            logger.info(f"🔎 Lọc được {len(readers)} bạn đọc")
            return readers

        except Exception as e:
            logger.error(f"❌ Lỗi lọc dữ liệu: {e}")
            return []

    def get_statistics(self) -> dict:
        """Lấy thống kê bạn đọc"""
        try:
            stats = {
                'total': 0,
                'active': 0,
                'expired': 0,
                'locked': 0,
                'avg_reputation': 0,
                'expiring_soon': 0,
                'high_reputation': 0,
                'low_reputation': 0
            }

            # Tổng số bạn đọc
            result = db.execute_query("SELECT COUNT(*) as total FROM readers", fetch_one=True)
            if result:
                stats['total'] = result['total']

            # Số bạn đọc theo trạng thái
            query = "SELECT status, COUNT(*) as count FROM readers GROUP BY status"
            rows = db.execute_query(query, fetch=True)

            if rows:
                for row in rows:
                    status = row['status']
                    if status == 'ACTIVE':
                        stats['active'] = row['count']
                    elif status == 'EXPIRED':
                        stats['expired'] = row['count']
                    elif status == 'LOCKED':
                        stats['locked'] = row['count']

            # Điểm uy tín trung bình
            result = db.execute_query("SELECT AVG(reputation_score) as avg_rep FROM readers", fetch_one=True)
            if result and result['avg_rep']:
                stats['avg_reputation'] = round(result['avg_rep'], 2)

            # Số thẻ sắp hết hạn (trong 30 ngày)
            date_30_days = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
            query = """
                    SELECT COUNT(*) as count \
                    FROM readers
                    WHERE card_end <= %s AND card_end >= CURDATE() \
                    """
            result = db.execute_query(query, (date_30_days,), fetch_one=True)
            if result:
                stats['expiring_soon'] = result['count']

            # Số bạn đọc có điểm uy tín cao (>= 90)
            result = db.execute_query(
                "SELECT COUNT(*) as count FROM readers WHERE reputation_score >= 90",
                fetch_one=True
            )
            if result:
                stats['high_reputation'] = result['count']

            # Số bạn đọc có điểm uy tín thấp (< 50)
            result = db.execute_query(
                "SELECT COUNT(*) as count FROM readers WHERE reputation_score < 50",
                fetch_one=True
            )
            if result:
                stats['low_reputation'] = result['count']

            return stats

        except Exception as e:
            logger.error(f"❌ Lỗi thống kê: {e}")
            return {
                'total': 0,
                'active': 0,
                'expired': 0,
                'locked': 0,
                'avg_reputation': 0,
                'expiring_soon': 0,
                'high_reputation': 0,
                'low_reputation': 0
            }

    def update_reader_status(self, reader_id: int, new_status: str) -> Tuple[bool, Optional[str]]:
        """Cập nhật trạng thái bạn đọc"""
        if new_status not in Reader.VALID_STATUSES:
            return False, f"Trạng thái không hợp lệ.  Phải là:  {', '.join(Reader.VALID_STATUSES)}"

        try:
            query = "UPDATE readers SET status = %s WHERE reader_id = %s"
            result = db.execute_query(query, (new_status, reader_id), commit=True)

            if result and result > 0:
                logger.info(f"✅ Đã cập nhật trạng thái bạn đọc ID {reader_id} thành {new_status}")
                return True, None
            else:
                return False, "Không tìm thấy bạn đọc"

        except Exception as e:
            logger.error(f"❌ Lỗi cập nhật trạng thái: {e}")
            return False, f"Lỗi database: {str(e)}"

    def update_reputation_score(self, reader_id: int, score: int) -> Tuple[bool, Optional[str]]:
        """Cập nhật điểm uy tín"""
        if not (0 <= score <= 100):
            return False, "Điểm uy tín phải từ 0 đến 100"

        try:
            query = "UPDATE readers SET reputation_score = %s WHERE reader_id = %s"
            result = db.execute_query(query, (score, reader_id), commit=True)

            if result and result > 0:
                logger.info(f"✅ Đã cập nhật điểm uy tín bạn đọc ID {reader_id} thành {score}")
                return True, None
            else:
                return False, "Không tìm thấy bạn đọc"

        except Exception as e:
            logger.error(f"❌ Lỗi cập nhật điểm uy tín: {e}")
            return False, f"Lỗi database: {str(e)}"

    def extend_card_validity(self, reader_id: int, days: int = 365) -> Tuple[bool, Optional[str]]:
        """Gia hạn thẻ bạn đọc"""
        try:
            reader = self.get_reader_by_id(reader_id)
            if not reader:
                return False, "Không tìm thấy bạn đọc"

            # Tính ngày hết hạn mới
            if reader.card_end:
                current_end = datetime.strptime(reader.card_end, '%Y-%m-%d')
                if current_end > datetime.now():
                    # Nếu chưa hết hạn, cộng thêm từ ngày hết hạn hiện tại
                    new_end = current_end + timedelta(days=days)
                else:
                    # Nếu đã hết hạn, cộng thêm từ hôm nay
                    new_end = datetime.now() + timedelta(days=days)
            else:
                # Nếu chưa có ngày hết hạn, cộng từ hôm nay
                new_end = datetime.now() + timedelta(days=days)

            new_end_str = new_end.strftime('%Y-%m-%d')

            query = "UPDATE readers SET card_end = %s, status = 'ACTIVE' WHERE reader_id = %s"
            result = db.execute_query(query, (new_end_str, reader_id), commit=True)

            if result and result > 0:
                logger.info(f"✅ Đã gia hạn thẻ bạn đọc ID {reader_id} đến {new_end_str}")
                return True, None
            else:
                return False, "Không thể gia hạn thẻ"

        except Exception as e:
            logger.error(f"❌ Lỗi gia hạn thẻ: {e}")
            return False, f"Lỗi:  {str(e)}"

    def check_expired_cards(self) -> List[Reader]:
        """Kiểm tra và trả về danh sách thẻ đã hết hạn"""
        try:
            query = """
                    SELECT * \
                    FROM readers
                    WHERE card_end < CURDATE() \
                      AND status = 'ACTIVE'
                    ORDER BY card_end ASC \
                    """
            rows = db.execute_query(query, fetch=True)

            if rows is None:
                return []

            readers = [Reader.from_dict(row) for row in rows]
            logger.info(f"🔍 Tìm thấy {len(readers)} thẻ đã hết hạn")
            return readers

        except Exception as e:
            logger.error(f"❌ Lỗi kiểm tra thẻ hết hạn: {e}")
            return []

    def auto_update_expired_status(self) -> Tuple[int, str]:
        """Tự động cập nhật trạng thái EXPIRED cho thẻ đã hết hạn"""
        try:
            query = """
                    UPDATE readers
                    SET status = 'EXPIRED'
                    WHERE card_end < CURDATE() \
                      AND status = 'ACTIVE' \
                    """
            result = db.execute_query(query, commit=True)

            if result:
                logger.info(f"✅ Đã cập nhật {result} thẻ thành EXPIRED")
                return result, f"Đã cập nhật {result} thẻ thành trạng thái hết hạn"
            else:
                return 0, "Không có thẻ nào cần cập nhật"

        except Exception as e:
            logger.error(f"❌ Lỗi cập nhật trạng thái tự động:  {e}")
            return 0, f"Lỗi: {str(e)}"