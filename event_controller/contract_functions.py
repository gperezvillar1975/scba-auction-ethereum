from web3 import Web3
import asyncio
from global_defs import AUCTION_DETAILS, AUCTIONS,LOT_DETAIL,web3,auction_abi,abi_contract

async def get_auction_contract(auction_code):
    return "0x6811261377025BD7c332644C6a93604317abdD02"

async def bidder_confirmed(auction_address, bidder_address):
    
    return True

def load_auctions():
    load_auction_data("0x6811261377025BD7c332644C6a93604317abdD02")
    return

def load_auction_data(auction_address):
    print("Loading data for auction " + auction_address)
    if auction_address:
        contract = web3.eth.contract(address=auction_address, abi=abi_contract['abi'])
        na = AUCTION_DETAILS
        na.auctionCode = "MP151"


    return ""