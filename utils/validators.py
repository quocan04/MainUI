import re
from datetime import datetime
from typing import Tuple, Optional


class Validator:
    """Class chứa các hàm validation"""

    @staticmethod
    def validate_full_name(name: str) -> Tuple[bool, Optional[str]]:
        """Validate họ tên"""
        if not name or not name.strip():
            return False, "Họ tên không được để trống"

        if len(name.strip()) < 2:
            return False, "Họ tên phải có ít nhất 2 ký tự"

        if len(name.strip()) > 150:
            return False, "Họ tên không được quá 150 ký tự"

        # Chỉ cho phép chữ cái, khoảng trắng và một số ký tự đặc biệt
        if not re.match(r'^[a-zA-ZÀ-ỹ\s.\'-]+$', name):
            return False, "Họ tên chỉ được chứa chữ cái và khoảng trắng"

        return True, None

    @staticmethod
    def validate_date(date_str: str, field_name: str = "Ngày") -> Tuple[bool, Optional[str]]:
        """Validate định dạng ngày tháng"""
        if not date_str:
            return True, None  # Cho phép để trống

        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True, None
        except ValueError:
            return False, f"{field_name} phải theo định dạng YYYY-MM-DD"

    @staticmethod
    def validate_phone(phone: str) -> Tuple[bool, Optional[str]]:
        """Validate số điện thoại"""
        if not phone:
            return True, None  # Cho phép để trống

        # Loại bỏ khoảng trắng và dấu gạch ngang
        phone = phone.replace(" ", "").replace("-", "").replace(".", "")

        # Kiểm tra định dạng:  10-11 số, bắt đầu bằng 0
        if not re.match(r'^0\d{9,10}$', phone):
            return False, "Số điện thoại phải có 10-11 chữ số và bắt đầu bằng 0"

        return True, None

    @staticmethod
    def validate_email(email: str) -> Tuple[bool, Optional[str]]:
        """Validate email"""
        if not email:
            return True, None  # Cho phép để trống

        # Regex đơn giản cho email
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, email):
            return False, "Email không hợp lệ"

        if len(email) > 100:
            return False, "Email không được quá 100 ký tự"

        return True, None

    @staticmethod
    def validate_date_range(start_date: str, end_date: str) -> Tuple[bool, Optional[str]]:
        """Validate khoảng thời gian"""
        if not start_date or not end_date:
            return True, None

        try:
            start = datetime.strptime(start_date, "%Y-%m-%d")
            end = datetime.strptime(end_date, "%Y-%m-%d")

            if start > end:
                return False, "Ngày bắt đầu phải trước ngày kết thúc"

            return True, None
        except ValueError:
            return False, "Định dạng ngày không hợp lệ"

    @staticmethod
    def validate_reputation_score(score: int) -> Tuple[bool, Optional[str]]:
        """Validate điểm uy tín"""
        try:
            score = int(score)
            if not (0 <= score <= 100):
                return False, "Điểm uy tín phải từ 0 đến 100"
            return True, None
        except (ValueError, TypeError):
            return False, "Điểm uy tín phải là số nguyên"

    @staticmethod
    def validate_address(address: str) -> Tuple[bool, Optional[str]]:
        """Validate địa chỉ"""
        if not address:
            return True, None

        if len(address) > 255:
            return False, "Địa chỉ không được quá 255 ký tự"

        return True, None