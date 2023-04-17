import json
from deposit_nfts import DepositNFTs

class User:
    def __init__(self, unique_code):
        self.unique_code = unique_code
        self.blockchains = []
        self.algorand_address = None
        self.total_value_deposited = 0
        self.governance_nft_eligible = False
        self.governance_nft_received = False

        with open("users.json") as f:
            users = json.load(f)

        if unique_code not in users:
            users[unique_code] = {
                "blockchains": [],
                "algorand_address": None,
                "total_value_deposited": 0,
                "governance_nft_eligible": False,
                "governance_nft_received": False
            }
            with open("users.json", "w") as f:
                json.dump(users, f)

        self.blockchains = users[unique_code]["blockchains"]
        self.algorand_address = users[unique_code]["algorand_address"]
        self.total_value_deposited = users[unique_code]["total_value_deposited"]
        self.governance_nft_eligible = users[unique_code]["governance_nft_eligible"]
        self.governance_nft_received = users[unique_code]["governance_nft_received"]

    def add_blockchain(self, blockchain):
        if blockchain not in self.blockchains:
            self.blockchains.append(blockchain)

            with open("users.json") as f:
                users = json.load(f)

            users[self.unique_code]["blockchains"] = self.blockchains

            with open("users.json", "w") as f:
                json.dump(users, f)

    def set_algorand_address(self, algorand_address):
        self.algorand_address = algorand_address

        with open("users.json") as f:
            users = json.load(f)

        users[self.unique_code]["algorand_address"] = self.algorand_address

        with open("users.json", "w") as f:
            json.dump(users, f)

    def get_algorand_address(self):
        return self.algorand_address

    def update_total_value_deposited(self, value):
        self.total_value_deposited += value

        with open("users.json") as f:
            users = json.load(f)

        users[self.unique_code]["total_value_deposited"] = self.total_value_deposited

        with open("users.json", "w") as f:
            json.dump(users, f)

    def set_governance_nft_eligible(self):
        self.governance_nft_eligible = True

        with open("users.json") as f:
            users = json.load(f)

        users[self.unique_code]["governance_nft_eligible"] = True

        with open("users.json", "w") as f:
            json.dump(users, f)

    def set_governance_nft_received(self):
        self.governance_nft_received = True

        with open("users.json") as f:
            users = json.load(f)

        users[self.unique_code]["governance_nft_received"] = True

        with open("users.json", "w") as f:
            json.dump(users, f)

    def is_governance_nft_eligible(self):
        return self.governance_nft_eligible

    def is_governance_nft_received(self):
        return self.governance_nft_received