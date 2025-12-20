from config.database import db

class PenaltyService:
    def get_all_penalties(self):
        query = """
            SELECT p.penalty_id AS penalty_id,
                   r.full_name AS reader_name,
                   b.title AS book_name,
                   p.penalty_type,
                   p.amount,
                   p.created_at
            FROM penalties p
            JOIN readers r ON p.reader_id = r.reader_id
            JOIN books b ON p.book_id = b.book_id
            ORDER BY p.created_at DESC
        """
        return db.fetchall(query)

    def create_penalty(self, reader_id, slip_id, book_id, penalty_type, amount):
        query = """
            INSERT INTO penalties (reader_id, slip_id, book_id, penalty_type, amount, created_at)
            VALUES (%s, %s, %s, %s, %s, NOW())
        """
        try:
            db.execute(query, (reader_id, slip_id, book_id, penalty_type, amount))
            return True
        except Exception as e:
            print(f"Error creating penalty: {e}")
            return False

    def delete_penalty(self, penalty_id):
        query = "DELETE FROM penalties WHERE id = %s"
        try:
            db.execute(query, (penalty_id,))
            return True
        except Exception as e:
            print(f"Error deleting penalty: {e}")
            return False
