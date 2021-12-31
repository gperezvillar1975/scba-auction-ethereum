# import the following dependencies
import json
from web3 import Web3
import asyncio
import event_processor

# add your blockchain connection information
ganache_url = 'http://10.10.12.40:8545'
web3 = Web3(Web3.HTTPProvider(ganache_url))

# auction contract address and abi
auction_contract = '0x747c2CBC88243871593C49f1c5af6d5a1F8740CB'
auction_abi = './abi/AuctionsSCBA.json'

abi = open(auction_abi)
abi_contract=json.load(abi)
abi.close()
contract = web3.eth.contract(address=auction_contract, abi=abi_contract['abi'])


async def log_loop(event_filter, poll_interval):
    print('Listening events...')
    while True:
        for evt in event_filter:
            for single_event in evt.get_new_entries():
                event_processor.handle_event(single_event)

        await asyncio.sleep(poll_interval)

def main():
    event_filters = [evt.createFilter(fromBlock='latest') for evt in contract.events]
    loop = asyncio.get_event_loop()
    print('Starting Event Loop')
    try:
        loop.run_until_complete(
            asyncio.gather(
                log_loop(event_filters, 2)
                )
            )
    finally:
        loop.close()



if __name__ == "__main__":
    main()