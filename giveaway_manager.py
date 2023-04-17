class GiveawayManager:
    def __init__(self, asset_watchers):
        self.asset_watchers = asset_watchers
        self.giveaway_milestones = [5000, 10000, 15000]  # Define giveaway milestones
        self.current_milestone_index = 0
        self.prize_table = [
            (1, "Diamond", "High Council"),
            (10, "Gold", "Senate"),
            (40, "Silver", "General Assembly")
        ]
        self.next_prize_index = 0

    def check_milestone(self):
        # Get the total number of Ible City Block NFTs in all holding accounts
        total_nfts = sum([watcher.get_total_nfts() for watcher in self.asset_watchers])

        # Check if the next milestone has been reached
        if total_nfts >= self.giveaway_milestones[self.current_milestone_index]:
            self.run_giveaway()
            self.current_milestone_index += 1

    def run_giveaway(self):
        # Get the next prize from the prize table
        prize_quantity, prize_type, prize_level = self.prize_table[self.next_prize_index]

        # Perform the giveaway drawing
        for _ in range(prize_quantity):
            winner_code = self.select_winner()
            if winner_code is not None:
                self.send_prize_to_winner(winner_code, prize_type, prize_level)

        # Update the prize index
        self.next_prize_index += 1

    def select_winner(self):
        # Implement the logic to select a winner based on the tickets
        pass

    def send_prize_to_winner(self, winner_code, prize_type, prize_level):
        # Implement the logic to send the prize to the winner
        pass