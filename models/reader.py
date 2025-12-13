from datetime import datetime, timedelta
from typing import Optional


class Reader:
    """
    Model đại diện cho Bạn đọc
    Mapping với bảng 'readers' trong MySQL database

    Schema:
        - reader_id: INT (Primary Key, Auto Increment)
        - full_name: VARCHAR(150) NOT NULL
        - address: VARCHAR(255)
        - phone: VARCHAR(20)
        - email: VARCHAR(100)
        - card_start: DATE (Ngày bắt đầu thẻ)
        - card_end: DATE (Ngày hết hạn thẻ)
        - status: ENUM('ACTIVE','EXPIRED','LOCKED')
        - reputation_score: INT (Điểm uy tín, mặc định 100)
        - created_at: TIMESTAMP (Tự động)
        - updated_at: TIMESTAMP (Tự động)
    """

    # Constants cho status
    STATUS_ACTIVE = 'ACTIVE'
    STATUS_EXPIRED = 'EXPIRED'
    STATUS_LOCKED = 'LOCKED'

    # List tất cả status hợp lệ
    VALID_STATUSES = [STATUS_ACTIVE, STATUS_EXPIRED, STATUS_LOCKED]

    def __init__(
            self,
            full_name: str,
            address: Optional[str] = None,
            phone: Optional[str] = None,
            email: Optional[str] = None,
            card_start: Optional[str] = None,
            card_end: Optional[str] = None,
            status: str = STATUS_ACTIVE,
            reputation_score: int = 100,
            reader_id: Optional[int] = None,
            created_at: Optional[str] = None,
            updated_at: Optional[str] = None
    ):
        """
        Khởi tạo Reader object

        Args:
            full_name: Họ tên bạn đọc (bắt buộc)
            address: Địa chỉ
            phone: Số điện thoại
            email: Email
            card_start: Ngày bắt đầu thẻ (YYYY-MM-DD)
            card_end: Ngày hết hạn thẻ (YYYY-MM-DD)
            status: Trạng thái (ACTIVE/EXPIRED/LOCKED)
            reputation_score: Điểm uy tín (0-100)
            reader_id: ID (tự động tăng khi insert vào DB)
            created_at: Thời gian tạo
            updated_at: Thời gian cập nhật
        """
        self.reader_id = reader_id
        self.full_name = full_name
        self.address = address
        self.phone = phone
        self.email = email
        self.card_start = card_start or datetime.now().strftime("%Y-%m-%d")
        self.card_end = card_end
        self.status = status
        self.reputation_score = reputation_score
        self.created_at = created_at
        self.updated_at = updated_at

    def to_dict(self) -> dict:
        """
        Chuyển đổi object thành dictionary

        Returns:
            dict: Dictionary chứa tất cả thuộc tính
        """
        return {
            'reader_id': self.reader_id,
            'full_name': self.full_name,
            'address': self.address,
            'phone': self.phone,
            'email': self.email,
            'card_start': self.card_start,
            'card_end': self.card_end,
            'status': self.status,
            'reputation_score': self.reputation_score,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    def to_tuple(self) -> tuple:
        """
        Chuyển đổi object thành tuple (dùng cho INSERT)
        Không bao gồm reader_id, created_at, updated_at vì tự động

        Returns:
            tuple: Tuple các giá trị để insert
        """
        return (
            self.full_name,
            self.address,
            self.phone,
            self.email,
            self.card_start,
            self.card_end,
            self.status,
            self.reputation_score
        )

    @staticmethod
    def from_dict(data: dict) -> 'Reader':
        """
        Tạo object Reader từ dictionary (thường từ database result)

        Args:
            data: Dictionary chứa dữ liệu reader

        Returns:
            Reader: Object Reader mới
        """

        # Xử lý date nếu là datetime object (MySQL trả về)
        def convert_date(date_value):
            if date_value and hasattr(date_value, 'strftime'):
                return date_value.strftime('%Y-%m-%d')
            elif date_value:
                return str(date_value)
            return None

        card_start = convert_date(data.get('card_start'))
        card_end = convert_date(data.get('card_end'))
        created_at = convert_date(data.get('created_at'))
        updated_at = convert_date(data.get('updated_at'))

        return Reader(
            reader_id=data.get('reader_id'),
            full_name=data.get('full_name', ''),
            address=data.get('address'),
            phone=data.get('phone'),
            email=data.get('email'),
            card_start=card_start,
            card_end=card_end,
            status=data.get('status', Reader.STATUS_ACTIVE),
            reputation_score=data.get('reputation_score', 100),
            created_at=created_at,
            updated_at=updated_at
        )

    @staticmethod
    def from_tuple(data: tuple, columns: list) -> 'Reader':
        """
        Tạo object Reader từ tuple và danh sách columns

        Args:
            data: Tuple chứa dữ liệu
            columns: List tên các cột

        Returns:
            Reader: Object Reader mới
        """
        data_dict = dict(zip(columns, data))
        return Reader.from_dict(data_dict)

    def is_active(self) -> bool:
        """
        Kiểm tra bạn đọc có đang hoạt động không

        Returns:
            bool: True nếu status = ACTIVE
        """
        return self.status == self.STATUS_ACTIVE

    def is_expired(self) -> bool:
        """
        Kiểm tra thẻ có hết hạn không (dựa vào card_end)

        Returns:
            bool: True nếu thẻ đã hết hạn
        """
        if not self.card_end:
            return False

        try:
            end_date = datetime.strptime(self.card_end, '%Y-%m-%d')
            return datetime.now() > end_date
        except (ValueError, TypeError):
            return False

    def is_locked(self) -> bool:
        """
        Kiểm tra bạn đọc có bị khóa không

        Returns:
            bool: True nếu status = LOCKED
        """
        return self.status == self.STATUS_LOCKED

    def get_days_until_expiry(self) -> Optional[int]:
        """
        Tính số ngày còn lại đến khi thẻ hết hạn

        Returns:
            int: Số ngày còn lại (âm nếu đã hết hạn)
            None: Nếu không có card_end
        """
        if not self.card_end:
            return None

        try:
            end_date = datetime.strptime(self.card_end, '%Y-%m-%d')
            delta = end_date - datetime.now()
            return delta.days
        except (ValueError, TypeError):
            return None

    def get_card_validity_info(self) -> str:
        """
        Lấy thông tin về thời hạn thẻ (dùng cho hiển thị)

        Returns:
            str: Thông tin thời hạn thẻ
        """
        days = self.get_days_until_expiry()

        if days is None:
            return "⚠️ Chưa xác định"
        elif days < 0:
            return f"🔴 Đã hết hạn {abs(days)} ngày"
        elif days == 0:
            return "⚠️ Hết hạn hôm nay"
        elif days <= 7:
            return f"⚠️ Còn {days} ngày (sắp hết hạn)"
        elif days <= 30:
            return f"🟡 Còn {days} ngày"
        else:
            return f"🟢 Còn {days} ngày"

    def get_status_display(self) -> str:
        """
        Lấy text hiển thị cho status (tiếng Việt)

        Returns:
            str: Text hiển thị
        """
        status_map = {
            self.STATUS_ACTIVE: '🟢 Hoạt động',
            self.STATUS_EXPIRED: '🔴 Hết hạn',
            self.STATUS_LOCKED: '🔒 Đã khóa'
        }
        return status_map.get(self.status, self.status)

    def get_reputation_level(self) -> str:
        """
        Lấy cấp độ uy tín dựa vào điểm

        Returns:
            str: Cấp độ uy tín
        """
        if self.reputation_score >= 90:
            return '⭐ Xuất sắc'
        elif self.reputation_score >= 75:
            return '✅ Tốt'
        elif self.reputation_score >= 50:
            return '⚠️ Trung bình'
        else:
            return '❌ Kém'

    def can_borrow(self) -> tuple[bool, Optional[str]]:
        """
        Kiểm tra bạn đọc có thể mượn sách không

        Returns:
            tuple: (can_borrow, reason_if_not)
        """
        if self.status == self.STATUS_LOCKED:
            return False, "Tài khoản đã bị khóa"

        if self.status == self.STATUS_EXPIRED:
            return False, "Thẻ đã hết hạn"

        if self.is_expired():
            return False, "Thẻ đã hết hạn, vui lòng gia hạn"

        if self.reputation_score < 30:
            return False, "Điểm uy tín quá thấp, không được mượn sách"

        return True, None

    def adjust_reputation(self, points: int, reason: str = "") -> int:
        """
        Điều chỉnh điểm uy tín

        Args:
            points: Số điểm cần thay đổi (+ hoặc -)
            reason: Lý do thay đổi

        Returns:
            int: Điểm uy tín mới
        """
        old_score = self.reputation_score
        self.reputation_score = max(0, min(100, self.reputation_score + points))

        if reason:
            print(f"📊 Điều chỉnh uy tín: {old_score} → {self.reputation_score} | Lý do: {reason}")

        return self.reputation_score

    def validate(self) -> tuple[bool, Optional[str]]:
        """
        Validate dữ liệu cơ bản của reader

        Returns:
            tuple: (is_valid, error_message)
        """
        # Kiểm tra họ tên
        if not self.full_name or not self.full_name.strip():
            return False, "Họ tên không được để trống"

        if len(self.full_name) > 150:
            return False, "Họ tên không được vượt quá 150 ký tự"

        # Kiểm tra phone
        if self.phone and len(self.phone) > 20:
            return False, "Số điện thoại không được vượt quá 20 ký tự"

        # Kiểm tra email
        if self.email:
            if len(self.email) > 100:
                return False, "Email không được vượt quá 100 ký tự"

            # Validate email format
            import re
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, self.email):
                return False, "Email không đúng định dạng"

        # Kiểm tra address
        if self.address and len(self.address) > 255:
            return False, "Địa chỉ không được vượt quá 255 ký tự"

        # Kiểm tra status
        if self.status not in self.VALID_STATUSES:
            return False, f"Trạng thái phải là một trong: {', '.join(self.VALID_STATUSES)}"

        # Kiểm tra reputation_score
        if not (0 <= self.reputation_score <= 100):
            return False, "Điểm uy tín phải trong khoảng 0-100"

        # Kiểm tra date range
        if self.card_start and self.card_end:
            try:
                start = datetime.strptime(self.card_start, '%Y-%m-%d')
                end = datetime.strptime(self.card_end, '%Y-%m-%d')
                if start > end:
                    return False, "Ngày bắt đầu phải trước ngày hết hạn"
            except ValueError:
                return False, "Định dạng ngày không hợp lệ (YYYY-MM-DD)"

        return True, None

    def get_summary(self) -> str:
        """
        Lấy thông tin tóm tắt của bạn đọc

        Returns:
            str: Thông tin tóm tắt
        """
        return (
            f"ID: {self.reader_id} | {self.full_name} | "
            f"{self.get_status_display()} | "
            f"Uy tín: {self.reputation_score}/100 | "
            f"Thẻ: {self.get_card_validity_info()}"
        )

    def __str__(self) -> str:
        """String representation"""
        return f"Reader(ID:{self.reader_id} - {self.full_name} - {self.get_status_display()})"

    def __repr__(self) -> str:
        """Detailed representation"""
        return (
            f"Reader(reader_id={self.reader_id}, "
            f"full_name='{self.full_name}', "
            f"status='{self.status}', "
            f"reputation_score={self.reputation_score})"
        )

    def __eq__(self, other) -> bool:
        """So sánh 2 reader objects"""
        if not isinstance(other, Reader):
            return False
        return self.reader_id == other.reader_id

    def __hash__(self) -> int:
        """Hash function cho Reader (dùng cho set, dict)"""
        return hash(self.reader_id) if self.reader_id else hash(id(self))


# ==================== UTILITY FUNCTIONS ====================

def create_sample_reader() -> Reader:
    """
    Tạo một reader mẫu để test

    Returns:
        Reader: Reader object mẫu
    """
    return Reader(
        full_name="Nguyễn Văn A",
        address="123 Đường ABC, Quận 1, TP. HCM",
        phone="0901234567",
        email="nguyenvana@example.com",
        card_start=datetime.now().strftime("%Y-%m-%d"),
        card_end=(datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d"),
        status=Reader.STATUS_ACTIVE,
        reputation_score=100
    )


def get_all_statuses() -> list[str]:
    """
    Lấy danh sách tất cả các trạng thái

    Returns:
        list: Danh sách các status
    """
    return Reader.VALID_STATUSES.copy()


def get_status_display_map() -> dict[str, str]:
    """
    Lấy mapping từ status code sang text hiển thị

    Returns:
        dict: Mapping status -> display text
    """
    return {
        Reader.STATUS_ACTIVE: 'Hoạt động',
        Reader.STATUS_EXPIRED: 'Hết hạn',
        Reader.STATUS_LOCKED: 'Đã khóa'
    }