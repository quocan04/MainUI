from services.penalty_service import PenaltyService

class PenaltyController:
    def __init__(self):
        self.service = PenaltyService()

    def get_all_penalties(self):
        return self.service.get_all_penalties()

    def create_penalty(self, reader_name, slip_id, book_name, penalty_type, amount):
        return self.service.create_penalty(reader_name, slip_id, book_name, penalty_type, amount)

    def delete_penalty(self, penalty_id):
        return self.service.delete_penalty(penalty_id)

    def update_penalty(self, penalty_id, penalty_type, amount):
        return self.service.update_penalty(penalty_id, penalty_type, amount)
