import threading
from collections import defaultdict


class NFTWithdrawalManager:
    def __init__(self):
        self.withdrawal_requests_lock = threading.Lock()
        self.withdrawal_requests = defaultdict(int)

    def request_withdrawal(self, unique_code, amount):
        with self.withdrawal_requests_lock:
            self.withdrawal_requests[unique_code] += amount

    def process_withdrawals(self):
        with self.withdrawal_requests_lock:
            # Process withdrawals here, e.g., by sending transactions on the blockchain
            # and removing processed requests from self.withdrawal_requests.
            pass

    def get_pending_withdrawals(self, unique_code):
        with self.withdrawal_requests_lock:
            return self.withdrawal_requests[unique_code]