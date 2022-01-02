from web3 import Web3
import json

JOIN = {}
AUCTIONS = {}

ganache_url = 'http://10.10.12.40:8545'
web3 = Web3(Web3.HTTPProvider(ganache_url))
auction_abi = './abi/AuctionsSCBA.json'
abi = open(auction_abi)
abi_contract=json.load(abi)
abi.close()

class LOT_DETAIL:
    lotId = 0
    startDate = 0
    endDate = 0
    baseValue = 0
    extendedEndDate = 0
    extensionsCount = 0
    winner = 0
    lastTrancheId = 0
    actualTrancheId = 0

class AUCTION_DETAILS:

    auctionCode = ""
    auctionState = 0
    auctionClass = 0
    guaranteeDeposit = 0
    totalAuctionLots = 0
    startDate = 0
    endDate = 0
    extendedEndDate = 0
    start_block = 0
    start_trn = ""
    end_block = 0
    end_trn = ""
    lotDetail = []
    events = []
