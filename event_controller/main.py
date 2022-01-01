# import the following dependencies
import json
from web3 import Web3
import asyncio
import event_processor
import socket_server
import websockets
import contract_functions

# add your blockchain connection information
ganache_url = 'http://10.10.12.40:8545'
web3 = Web3(Web3.HTTPProvider(ganache_url))
# auction contract address and abi
auction_contract = contract_functions.get_auction_contract()
auction_abi = './abi/AuctionsSCBA.json'

# Websocket connections lists
JOIN = {}
WATCH = {}

abi = open(auction_abi)
abi_contract=json.load(abi)
abi.close()
contract = web3.eth.contract(address=auction_contract, abi=abi_contract['abi'])


def main():
    event_filters = [evt.createFilter(fromBlock='latest') for evt in contract.events]
    loop = asyncio.get_event_loop()
    print('Starting Event Loop')
    try:
        loop.run_until_complete(
            asyncio.gather(
                event_processor.log_loop(event_filters, 2),
                websockets.serve(socket_server.handler, "localhost", 8765)
                )
            )
    finally:
        loop.close()



if __name__ == "__main__":
    main()