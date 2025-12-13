from datetime import datetime
from typing import Optional


class Book:
    """
    Model đại diện cho Sách
    Mapping với bảng 'books' trong MySQL database
    """

    def __init__(
            self,
            title: str,
            author_id: Optional[int] = None,
            category_id: Optional[int] = None,
            publisher_id: Optional[int] = None,
            publish_year: Optional[int] = None,
            isbn: Optional[str] = None,
            barcode: Optional[str] = None,
            price: Optional[float] = None,
            description: Optional[str] = None,
            book_id: Optional[int] = None,
            # Thông tin join (không lưu DB)
            author_name: Optional[str] = None,
            category_name: Optional[str] = None,
            publisher_name: Optional[str] = None,
            total_quantity: int = 0,
            available_quantity: int = 0
    ):
        self.book_id = book_id
        self.title = title
        self.author_id = author_id
        self.category_id = category_id
        self.publisher_id = publisher_id
        self.publish_year = publish_year
        self.isbn = isbn
        self.barcode = barcode
        self.price = float(price) if price else None
        self.description = description

        # Thông tin JOIN
        self.author_name = author_name
        self.category_name = category_name
        self.publisher_name = publisher_name
        self.total_quantity = total_quantity
        self.available_quantity = available_quantity

    def to_dict(self) -> dict:
        """Chuyển đổi object thành dictionary"""
        return {
            'book_id': self.book_id,
            'title': self.title,
            'author_id': self.author_id,
            'category_id': self.category_id,
            'publisher_id': self.publisher_id,
            'publish_year': self.publish_year,
            'isbn': self.isbn,
            'barcode': self.barcode,
            'price': self.price,
            'description': self.description,
            'author_name': self.author_name,
            'category_name': self.category_name,
            'publisher_name': self.publisher_name,
            'total_quantity': self.total_quantity,
            'available_quantity': self.available_quantity
        }

    def to_tuple(self) -> tuple:
        """Chuyển đổi object thành tuple (dùng cho INSERT)"""
        return (
            self.title,
            self.author_id,
            self.category_id,
            self.publisher_id,
            self.publish_year,
            self.isbn,
            self.barcode,
            self.price,
            self.description
        )

    @staticmethod
    def from_dict(data: dict) -> 'Book':
        """Tạo object Book từ dictionary"""
        return Book(
            book_id=data.get('book_id'),
            title=data.get('title', ''),
            author_id=data.get('author_id'),
            category_id=data.get('category_id'),
            publisher_id=data.get('publisher_id'),
            publish_year=data.get('publish_year'),
            isbn=data.get('isbn'),
            barcode=data.get('barcode'),
            price=data.get('price'),
            description=data.get('description'),
            author_name=data.get('author_name'),
            category_name=data.get('category_name'),
            publisher_name=data.get('publisher_name'),
            total_quantity=data.get('total_quantity', 0),
            available_quantity=data.get('available_quantity', 0)
        )

    def get_stock_status(self) -> str:
        """Lấy trạng thái tồn kho"""
        if self.available_quantity == 0:
            return '❌ Hết hàng'
        elif self.available_quantity < 5:
            return '⚠️ Sắp hết'
        else:
            return '✅ Còn hàng'

    def get_borrow_rate(self) -> float:
        """Tính tỷ lệ đang được mượn (%)"""
        if self.total_quantity == 0:
            return 0.0
        borrowed = self.total_quantity - self.available_quantity
        return (borrowed / self.total_quantity) * 100

    def is_available(self) -> bool:
        """Kiểm tra sách có sẵn để mượn không"""
        return self.available_quantity > 0

    def validate(self) -> tuple[bool, Optional[str]]:
        """Validate dữ liệu cơ bản"""
        if not self.title or not self.title.strip():
            return False, "Tựa sách không được để trống"

        if len(self.title) > 255:
            return False, "Tựa sách không được vượt quá 255 ký tự"

        if self.isbn and len(self.isbn) > 20:
            return False, "ISBN không được vượt quá 20 ký tự"

        if self.barcode and len(self.barcode) > 50:
            return False, "Mã vạch không được vượt quá 50 ký tự"

        if self.publish_year:
            current_year = datetime.now().year
            if not (1000 <= self.publish_year <= current_year + 1):
                return False, f"Năm xuất bản phải từ 1000 đến {current_year + 1}"

        if self.price is not None and self.price < 0:
            return False, "Giá sách không được âm"

        return True, None

    def __str__(self) -> str:
        """String representation"""
        return f"Book(ID:{self.book_id} - {self.title} - {self.author_name})"

    def __repr__(self) -> str:
        """Detailed representation"""
        return (
            f"Book(book_id={self.book_id}, "
            f"title='{self.title}', "
            f"author='{self.author_name}', "
            f"available={self.available_quantity}/{self.total_quantity})"
        )


class Author:
    """Model cho Tác giả"""

    def __init__(self, author_id: Optional[int] = None, author_name: str = ''):
        self.author_id = author_id
        self.author_name = author_name

    @staticmethod
    def from_dict(data: dict) -> 'Author':
        return Author(
            author_id=data.get('author_id'),
            author_name=data.get('author_name', '')
        )

    def to_dict(self) -> dict:
        return {
            'author_id': self.author_id,
            'author_name': self.author_name
        }


class Category:
    """Model cho Thể loại"""

    def __init__(self, category_id: Optional[int] = None, category_name: str = ''):
        self.category_id = category_id
        self.category_name = category_name

    @staticmethod
    def from_dict(data: dict) -> 'Category':
        return Category(
            category_id=data.get('category_id'),
            category_name=data.get('category_name', '')
        )

    def to_dict(self) -> dict:
        return {
            'category_id': self.category_id,
            'category_name': self.category_name
        }


class Publisher:
    """Model cho Nhà xuất bản"""

    def __init__(
            self,
            publisher_id: Optional[int] = None,
            publisher_name: str = '',
            address: Optional[str] = None,
            phone: Optional[str] = None
    ):
        self.publisher_id = publisher_id
        self.publisher_name = publisher_name
        self.address = address
        self.phone = phone

    @staticmethod
    def from_dict(data: dict) -> 'Publisher':
        return Publisher(
            publisher_id=data.get('publisher_id'),
            publisher_name=data.get('publisher_name', ''),
            address=data.get('address'),
            phone=data.get('phone')
        )

    def to_dict(self) -> dict:
        return {
            'publisher_id': self.publisher_id,
            'publisher_name': self.publisher_name,
            'address': self.address,
            'phone': self.phone
        }