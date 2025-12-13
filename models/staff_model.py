from config.database import db


class Staff:
    def __init__(self, staff_id, full_name, username, role_id, status):
        self.staff_id = staff_id
        self.full_name = full_name
        self.username = username
        self.role_id = role_id
        self.status = status


class StaffModel:

    # =========================
    # AUTHENTICATION
    # =========================
    def authenticate(self, username, password):
        """Xác thực đăng nhập"""
        query = """
            SELECT 
                staff_id,
                full_name,
                username,
                role_id,
                status
            FROM staff
            WHERE username = %s
              AND password = %s
              AND status = 'ACTIVE'
            LIMIT 1
        """
        rows = db.execute_query(
            query,
            params=(username, password),
            fetch=True  # ✅ SELECT dùng fetch=True
        )

        if rows:
            row = rows[0]
            return self._row_to_staff(row)
        return None

    # =========================
    # QUERY (READ)
    # =========================

    def get_all_staff(self):
        """Lấy tất cả nhân viên"""
        query = """
            SELECT 
                staff_id,
                full_name,
                username,
                role_id,
                status
            FROM staff
            ORDER BY staff_id
        """
        rows = db.execute_query(query, fetch=True)  # ✅ SELECT

        if not rows:
            return []

        return [self._row_to_staff(row) for row in rows]

    def get_by_id(self, staff_id):
        """Lấy nhân viên theo ID"""
        query = """
            SELECT 
                staff_id,
                full_name,
                username,
                role_id,
                status
            FROM staff
            WHERE staff_id = %s
            LIMIT 1
        """
        rows = db.execute_query(query, params=(staff_id,), fetch=True)  # ✅ SELECT

        if rows:
            return self._row_to_staff(rows[0])
        return None

    def search(self, keyword):
        """Tìm kiếm nhân viên theo từ khóa"""
        query = """
            SELECT 
                staff_id,
                full_name,
                username,
                role_id,
                status
            FROM staff
            WHERE full_name LIKE %s
               OR username LIKE %s
            ORDER BY staff_id
        """
        search_pattern = f"%{keyword}%"
        rows = db.execute_query(
            query,
            params=(search_pattern, search_pattern),
            fetch=True  # ✅ SELECT
        )

        if not rows:
            return []

        return [self._row_to_staff(row) for row in rows]

    def get_by_role(self, role_id):
        """Lấy nhân viên theo role"""
        query = """
            SELECT 
                staff_id,
                full_name,
                username,
                role_id,
                status
            FROM staff
            WHERE role_id = %s
            ORDER BY staff_id
        """
        rows = db.execute_query(query, params=(role_id,), fetch=True)  # ✅ SELECT

        if not rows:
            return []

        return [self._row_to_staff(row) for row in rows]

    def check_username_exists(self, username):
        """Kiểm tra username đã tồn tại chưa"""
        query = "SELECT COUNT(*) as count FROM staff WHERE username = %s"
        rows = db.execute_query(query, params=(username,), fetch=True)  # ✅ SELECT

        if rows:
            return rows[0]['count'] > 0  # Dictionary cursor
        return False

    # =========================
    # COMMAND (CREATE/UPDATE/DELETE)
    # =========================

    def create(self, full_name, username, password, role_id):
        """
        Tạo nhân viên mới

        Returns:
            int: ID của nhân viên vừa tạo
        """
        query = """
            INSERT INTO staff (full_name, username, password, role_id, status)
            VALUES (%s, %s, %s, %s, 'ACTIVE')
        """

        print(f"[MODEL] Creating staff: {full_name}, {username}, role={role_id}")

        # ⚠️ QUAN TRỌNG: commit=True để lưu vào database
        last_id = db.execute_query(
            query,
            params=(full_name, username, password, role_id),
            fetch=False,
            commit=True  # ✅ INSERT phải commit=True
        )

        print(f"[MODEL] Staff created with ID: {last_id}")

        return last_id

    def update_role(self, staff_id, new_role_id):
        """Cập nhật role cho nhân viên"""
        query = "UPDATE staff SET role_id = %s WHERE staff_id = %s"

        print(f"[MODEL] Updating role for staff {staff_id} to role {new_role_id}")

        # ⚠️ QUAN TRỌNG: commit=True
        result = db.execute_query(
            query,
            params=(new_role_id, staff_id),
            fetch=False,
            commit=True  # ✅ UPDATE phải commit=True
        )

        print(f"[MODEL] Role updated, rows affected: {result}")
        return result

    def update_full_name(self, staff_id, full_name):
        """Cập nhật họ tên"""
        query = "UPDATE staff SET full_name = %s WHERE staff_id = %s"

        return db.execute_query(
            query,
            params=(full_name, staff_id),
            fetch=False,
            commit=True  # ✅ UPDATE
        )

    def update_username(self, staff_id, username):
        """Cập nhật username"""
        query = "UPDATE staff SET username = %s WHERE staff_id = %s"

        return db.execute_query(
            query,
            params=(username, staff_id),
            fetch=False,
            commit=True  # ✅ UPDATE
        )

    def update_password(self, staff_id, new_password):
        """Cập nhật mật khẩu"""
        query = "UPDATE staff SET password = %s WHERE staff_id = %s"

        return db.execute_query(
            query,
            params=(new_password, staff_id),
            fetch=False,
            commit=True  # ✅ UPDATE
        )

    def update_status(self, staff_id, status):
        """Cập nhật trạng thái"""
        query = "UPDATE staff SET status = %s WHERE staff_id = %s"

        return db.execute_query(
            query,
            params=(status, staff_id),
            fetch=False,
            commit=True  # ✅ UPDATE
        )

    def delete_staff(self, staff_id):
        """Xóa nhân viên (hard delete)"""
        query = "DELETE FROM staff WHERE staff_id = %s"

        print(f"[MODEL] Deleting staff {staff_id}")

        result = db.execute_query(
            query,
            params=(staff_id,),
            fetch=False,
            commit=True  # ✅ DELETE phải commit=True
        )

        print(f"[MODEL] Staff deleted, rows affected: {result}")
        return result

    def verify_password(self, staff_id, password):
        """Kiểm tra mật khẩu có đúng không"""
        query = "SELECT COUNT(*) as count FROM staff WHERE staff_id = %s AND password = %s"
        rows = db.execute_query(query, params=(staff_id, password), fetch=True)  # ✅ SELECT

        if rows:
            return rows[0]['count'] > 0
        return False

    # =========================
    # STATISTICS
    # =========================

    def count_by_role(self):
        """Đếm số nhân viên theo role"""
        query = """
            SELECT role_id, COUNT(*) as count
            FROM staff
            GROUP BY role_id
        """
        rows = db.execute_query(query, fetch=True)  # ✅ SELECT

        result = {}
        for row in rows:
            result[row['role_id']] = row['count']  # Dictionary cursor
        return result

    def count_active(self):
        """Đếm số nhân viên đang hoạt động"""
        query = "SELECT COUNT(*) as count FROM staff WHERE status = 'ACTIVE'"
        rows = db.execute_query(query, fetch=True)  # ✅ SELECT

        if rows:
            return rows[0]['count']
        return 0

    # =========================
    # HELPER
    # =========================

    def _row_to_staff(self, row):
        """
        Convert row (dict) thành Staff object
        Database trả về dictionary vì dùng cursor(dictionary=True)
        """
        return Staff(
            staff_id=row['staff_id'],
            full_name=row['full_name'],
            username=row['username'],
            role_id=row['role_id'],
            status=row['status']
        )