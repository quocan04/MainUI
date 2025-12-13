# --- SỬA DÒNG IMPORT ---
from config.database import db  # <-- Import biến 'db' (cục database), không import hàm get_connection


class ReportService:
    def get_borrow_stats(self, mode='month'):
        formats = {'day': '%Y-%m-%d', 'month': '%Y-%m', 'year': '%Y'}
        sql_format = formats.get(mode, '%Y-%m')

        query = f"""
            SELECT DATE_FORMAT(borrow_date, '{sql_format}') as time_point, 
                   COUNT(*) as total_borrows
            FROM borrow_slips
            GROUP BY time_point
            ORDER BY time_point DESC;
        """
        return self._execute_query(query)

    def get_top_readers(self, limit=5):
        query = """
            SELECT r.reader_id, r.full_name, COUNT(b.slip_id) as borrow_count
            FROM readers r
            JOIN borrow_slips b ON r.reader_id = b.reader_id
            GROUP BY r.reader_id, r.full_name
            ORDER BY borrow_count DESC
            LIMIT %s;
        """
        return self._execute_query(query, (limit,))

    def get_damaged_lost_books(self):
        query = """
            SELECT p.penalty_type, COUNT(*) as quantity, SUM(p.amount) as total_fine
            FROM penalties p
            WHERE p.penalty_type IN ('LOST', 'DAMAGED')
            GROUP BY p.penalty_type;
        """
        return self._execute_query(query)

    def get_inventory_stats(self):
        query_cat = """
            SELECT c.category_name, SUM(i.total_quantity) as quantity
            FROM book_inventory i
            JOIN books b ON i.book_id = b.book_id
            JOIN categories c ON b.category_id = c.category_id
            GROUP BY c.category_name;
        """
        query_general = """
             SELECT SUM(total_quantity) as total, 
                    SUM(available_quantity) as available 
             FROM book_inventory
        """
        categories = self._execute_query(query_cat)
        general = self._execute_query(query_general)

        # Xử lý trường hợp database trả về None
        total = general[0]['total'] if general and general[0]['total'] else 0
        available = general[0]['available'] if general and general[0]['available'] else 0

        return {
            "categories": categories,
            "total": total,
            "available": available,
            "borrowed": total - available
        }

    def _execute_query(self, query, params=None):
        # --- SỬA DÒNG NÀY ---
        # Thay vì gọi get_connection(), hãy gọi db.get_connection()
        conn = db.get_connection()

        if conn is None: return []

        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, params or ())
            result = cursor.fetchall()

            cursor.close()
            conn.close()
            return result
        except Exception as e:
            print(f"Report Service Error: {e}")
            return []