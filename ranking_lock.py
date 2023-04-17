import time
from datetime import datetime, timedelta
from threading import Timer
from user import User


class RankingLock:
    def __init__(self, lock_time):
        self.lock_time = lock_time
        self.timer = None
        self.set_lock_timer()

    def set_lock_timer(self):
        current_time = datetime.now()
        time_difference = self.lock_time - current_time
        seconds_until_lock = time_difference.total_seconds()

        if seconds_until_lock > 0:
            self.timer = Timer(seconds_until_lock, self.lock_and_confirm_ranks)
            self.timer.start()
        else:
            print("Lock time has already passed. No timer set.")

    def lock_and_confirm_ranks(self):
        # Lock and confirm ranks for all users
        User.lock_and_confirm_all_ranks()

    def update_lock_time(self, new_lock_time: datetime):
        if self.timer:
            self.timer.cancel()

        self.lock_time = new_lock_time
        self.set_lock_timer()