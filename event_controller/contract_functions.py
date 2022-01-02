from web3 import Web3
import asyncio
from global_defs import AUCTION_DETAILS, AUCTIONS,LOT_DETAIL,web3,auction_abi,abi_contract

async def get_auction_contract(auction_code):
    return "0x9bA0642520c10Ac6544358198AC4c454e84Cc86d"

async def bidder_confirmed(auction_address, bidder_address):
    
    return True

def load_auctions():
    load_auction_data("0x9bA0642520c10Ac6544358198AC4c454e84Cc86d")
    return

def load_auction_data(auction_address):
    print("Loading data for auction " + auction_address)
    if auction_address:
        contract = web3.eth.contract(address=auction_address, abi=abi_contract['abi'])
        na = AUCTION_DETAILS
        na.auctionCode = "MP151"
        na.auctionState =  contract.functions.getAuctionState().call()
        nLots = contract.functions.getLotQuantity().call()
        for x in range(nLots):
            nl = LOT_DETAIL
            nl.lotId = x+1
            nl.startDate = contract.functions.getAuctionStartDate().call()
            nl.endDate = contract.functions.getAuctionEndtDate().call()
            nl.baseValue = contract.functions.getLotBaseValue(x+1).call()
            nl.actualTrancheId = contract.functions.getActualTranche(x+1).call()
            nl.lastTrancheId = contract.functions.getLastTranche(x+1).call()
            nl.extensionsCount = contract.functions.getLotExtensionCount(x+1).call()
            nl.extendedEndDate = contract.functions.getLotEndDate(x+1).call()
            na.lotDetail.add(nl)
            
    return ""