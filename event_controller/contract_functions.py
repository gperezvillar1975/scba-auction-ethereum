from web3 import Web3
import asyncio

async def get_auction_contract(auction_code):
    return "0xd3Fa06133B2D11B41e6c9F291DCA4329F3caBb6e"

async def bidder_confirmed(auction_code, bidder_address):
    contract = get_auction_contract(auction_code)

    return True