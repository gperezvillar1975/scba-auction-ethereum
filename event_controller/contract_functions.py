from web3 import Web3
import asyncio

async def get_auction_contract(auction_code):
    return "0xdfA88aB35b2c5d44Eb6684C7F660d5937AcebA77"

async def bidder_confirmed(auction_code, bidder_address):
    contract = await get_auction_contract(auction_code)

    return True