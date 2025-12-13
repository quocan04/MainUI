from config.database import db
import json
import os
from datetime import datetime, date


class SystemService:
    def __init__(self):
        # Tạo thư mục backups nếu chưa có
        self.backup_dir = os.path.join(os.getcwd(), 'backups')
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)

    # --- Phần Settings ---
    def get_settings(self):
        try:
            conn = db.get_connection()
            if conn is None: return {}

            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM system_settings")
            result = cursor.fetchall()

            cursor.close()
            conn.close()
            return {item['setting_key']: item['setting_value'] for item in result}
        except Exception as e:
            print(f"Error loading settings: {e}")
            return {}

    def update_settings(self, settings_dict):
        try:
            conn = db.get_connection()
            if conn is None: return False

            cursor = conn.cursor()
            for key, value in settings_dict.items():
                cursor.execute(
                    "UPDATE system_settings SET setting_value = %s WHERE setting_key = %s",
                    (str(value), key)
                )
            conn.commit()

            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Error updating settings: {e}")
            return False

    # --- Phần Backup ---
    def backup_data(self):
        tables = ['categories', 'authors', 'publishers', 'books', 'book_inventory',
                  'readers', 'borrow_slips', 'borrow_details', 'penalties', 'system_settings']
        data = {}

        try:
            conn = db.get_connection()
            if conn is None: return False, "No database connection"

            cursor = conn.cursor(dictionary=True)

            for table in tables:
                cursor.execute(f"SELECT * FROM {table}")
                rows = cursor.fetchall()
                for row in rows:
                    for k, v in row.items():
                        if isinstance(v, (datetime, date)):
                            row[k] = str(v)
                data[table] = rows

            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"backup_{timestamp}.json"
            filepath = os.path.join(self.backup_dir, filename)

            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

            cursor.close()
            conn.close()
            return True, filepath
        except Exception as e:
            return False, str(e)

    # --- Phần Restore ---
    def restore_data(self, filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)

            conn = db.get_connection()
            if conn is None: return False, "Lỗi kết nối CSDL"

            cursor = conn.cursor()
            cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")

            tables = ['categories', 'authors', 'publishers', 'books', 'book_inventory',
                      'readers', 'borrow_slips', 'borrow_details', 'penalties', 'system_settings']

            for table in tables:
                if table in data:
                    rows = data[table]
                    if not rows: continue
                    cursor.execute(f"TRUNCATE TABLE {table}")
                    for row in rows:
                        cols = ', '.join(f"`{k}`" for k in row.keys())
                        placeholders = ', '.join(['%s'] * len(row))
                        sql = f"INSERT INTO `{table}` ({cols}) VALUES ({placeholders})"
                        cursor.execute(sql, list(row.values()))

            cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
            conn.commit()
            cursor.close()
            conn.close()
            return True, "Phục hồi dữ liệu thành công!"

        except Exception as e:
            print(f"Restore Error: {e}")
            return False, str(e)