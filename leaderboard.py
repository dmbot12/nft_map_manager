import heapq
import threading


class Leaderboard:
    def __init__(self):
        self.leaderboard_lock = threading.Lock()
        self.leaderboard = []

    def update_points(self, unique_code, points):
        with self.leaderboard_lock:
            for entry in self.leaderboard:
                if entry[1] == unique_code:
                    entry[0] += points
                    heapq.heapify(self.leaderboard)
                    return

            heapq.heappush(self.leaderboard, [-points, unique_code])

    def get_top_users(self, n):
        with self.leaderboard_lock:
            return heapq.nsmallest(n, self.leaderboard, key=lambda x: (x[0], x[1]))

    def get_user_position(self, unique_code):
        with self.leaderboard_lock:
            sorted_leaderboard = sorted(self.leaderboard, key=lambda x: (x[0], x[1]))
            for i, entry in enumerate(sorted_leaderboard):
                if entry[1] == unique_code:
                    return i + 1
        return -1