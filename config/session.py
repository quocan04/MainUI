class Session:
    """
    Quản lý session đăng nhập trong ứng dụng
    Lưu trữ thông tin user hiện tại trong memory
    """
    _data = {}

    @classmethod
    def set(cls, key, value):
        """
        Lưu giá trị vào session

        Args:
            key: Tên key
            value: Giá trị cần lưu
        """
        cls._data[key] = value

    @classmethod
    def get(cls, key):
        """
        Lấy giá trị từ session

        Args:
            key: Tên key

        Returns:
            Giá trị tương ứng hoặc None nếu không tồn tại
        """
        return cls._data.get(key)

    @classmethod
    def clear(cls):
        """Xóa toàn bộ session (đăng xuất)"""
        cls._data.clear()

    @classmethod
    def get_all(cls):
        """
        Lấy toàn bộ session data (dùng để debug)

        Returns:
            dict: Toàn bộ dữ liệu session
        """
        return cls._data.copy()

    @classmethod
    def has(cls, key):
        """
        Kiểm tra key có tồn tại trong session không

        Args:
            key: Tên key

        Returns:
            bool: True nếu key tồn tại
        """
        return key in cls._data

    @classmethod
    def remove(cls, key):
        """
        Xóa một key cụ thể khỏi session

        Args:
            key: Tên key cần xóa
        """
        if key in cls._data:
            del cls._data[key]

    @classmethod
    def is_authenticated(cls):
        """
        Kiểm tra user đã đăng nhập chưa

        Returns:
            bool: True nếu đã đăng nhập (có staff_id)
        """
        return cls.get("staff_id") is not None

    @classmethod
    def get_role_id(cls):
        """
        Lấy role_id của user hiện tại

        Returns:
            int: role_id hoặc None
        """
        role_id = cls.get("role_id")

        # Đảm bảo trả về int
        if isinstance(role_id, str):
            try:
                return int(role_id)
            except (ValueError, TypeError):
                return None

        return role_id

    @classmethod
    def get_staff_id(cls):
        """
        Lấy staff_id của user hiện tại

        Returns:
            int: staff_id hoặc None
        """
        return cls.get("staff_id")

    @classmethod
    def get_username(cls):
        """
        Lấy username của user hiện tại

        Returns:
            str: username hoặc None
        """
        return cls.get("username")

    @classmethod
    def get_full_name(cls):
        """
        Lấy full_name của user hiện tại

        Returns:
            str: full_name hoặc None
        """
        return cls.get("full_name")