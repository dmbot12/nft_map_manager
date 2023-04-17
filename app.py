from flask import Flask, request, jsonify
from datetime import datetime
from user import User
from asset_watchers import AssetWatchers
from nft_withdrawal_manager import NFTWithdrawalManager
from leaderboard import Leaderboard
from ranking_lock import RankingLock
from giveaway_manager import GiveawayManager
from governance_nft_distributor import GovernanceNFTDistributor
from doug import Brought

app = Flask(__name__)

@app.route('/user', methods=['POST'])
def add_user():
    data = request.get_json()
    unique_code = data['unique_code']
    algorand_address = data['algorand_address']
    ethereum_address = data['ethereum_address']
    polygon_address = data['polygon_address']
    vechain_address = data['vechain_address']

    user = User(unique_code)
    user.set_algorand_address(algorand_address)
    user.set_ethereum_address(ethereum_address)
    user.set_polygon_address(polygon_address)
    user.set_vechain_address(vechain_address)
    user.create()

    return jsonify({'message': 'User created successfully'}), 201


@app.route('/nft/deposit', methods=['POST'])
def deposit_nft():
    data = request.get_json()
    unique_code = data['unique_code']
    blockchain = data['blockchain']
    asset_type = data['asset_type']
    asset_amount = data['asset_amount']

    user = User(unique_code)
    user.load()

    if not user.is_blockchain_connected(blockchain):
        return jsonify({'message': 'User has not connected to this blockchain'}), 400

    asset_watchers = AssetWatchers(blockchain)
    holding_address = asset_watchers.get_holding_address(asset_type)
    if holding_address is None:
        return jsonify({'message': 'Asset type not supported on this blockchain'}), 400

    tx = user.build_nft_deposit_transaction(blockchain, holding_address, asset_type, asset_amount)
    if tx is None:
        return jsonify({'message': 'Insufficient NFT balance for deposit'}), 400

    return jsonify({'message': 'Please sign this transaction', 'transaction': tx}), 200


@app.route('/nft/deposit/confirm', methods=['POST'])
def confirm_nft_deposit():
    data = request.get_json()
    unique_code = data['unique_code']
    blockchain = data['blockchain']
    tx_id = data['tx_id']

    user = User(unique_code)
    user.load()

    if not user.is_blockchain_connected(blockchain):
        return jsonify({'message': 'User has not connected to this blockchain'}), 400

    asset_watchers = AssetWatchers(blockchain)
    holding_address = asset_watchers.get_holding_address_from_txid(tx_id)
    if holding_address is None:
        return jsonify({'message': 'Transaction not found or not yet confirmed'}), 400

    tx_status = user.confirm_nft_deposit_transaction(blockchain, tx_id, holding_address)
    if not tx_status:
        return jsonify({'message': 'Failed to confirm transaction'}), 400

    leaderboard = Leaderboard()
    leaderboard.update_user_deposits(unique_code, holding_address, asset_watchers.get_asset_value(blockchain, holding_address))

    ranking_lock = RankingLock()
    if ranking_lock.is_locked():
        giveaway_manager = GiveawayManager()
        giveaway_manager.update_deposit_count(unique_code, holding_address)

    return jsonify({'message': 'NFT deposit confirmed successfully'}), 200


@app.route('/nft/withdraw', methods=['POST'])
def withdraw_nft():
