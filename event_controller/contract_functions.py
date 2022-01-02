from web3 import Web3
import asyncio

async def get_auction_contract(auction_code):
    return "0x6811261377025BD7c332644C6a93604317abdD02"

async def bidder_confirmed(auction_code, bidder_address):
    contract = await get_auction_contract(auction_code)

    return True