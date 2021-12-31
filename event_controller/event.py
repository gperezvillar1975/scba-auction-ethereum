# import the following dependencies
import json
from web3 import Web3
import asyncio
from datetime import datetime

# add your blockchain connection information
ganache_url = 'http://10.10.12.40:8545'
web3 = Web3(Web3.HTTPProvider(ganache_url))

# uniswap address and abi
auction_contract = '0x747c2CBC88243871593C49f1c5af6d5a1F8740CB'
auction_abi = './abi/AuctionsSCBA.json'

abi = open(auction_abi)
abi_contract=json.load(abi)
abi.close()
contract = web3.eth.contract(address=auction_contract, abi=abi_contract['abi'])

# define function to handle events and print to the console
def handle_event(event):    
    if (event['event'] == 'evt_bidderConfirmedInscription'):
        print(str(datetime.fromtimestamp((event['args']['timeStamp']))) + ' - ' + 'Confirmed Inscription Bidder: ' + event['args']['_bidder'])
    elif (event['event'] == 'evt_auctionStart'):
        print(str(datetime.fromtimestamp((event['args']['timeStamp']))) + ' - ' + 'Started auction: ' + event['args']['auctionID'])
    elif (event['event'] == 'evt_bidConfirmed'):
        print(str(datetime.fromtimestamp((event['args']['timeStamp']))) + ' - ' + 'Bid confirmed for lot: ' + str(event['args']['lotId']) + ' - Tranche: ' + str(event['args']['trancheId']) + ' - Bidder: ' +  event['args']['_bidder'])
    elif (event['event'] == 'evt_auctionClosed'):
        print(str(datetime.fromtimestamp((event['args']['timeStamp']))) + ' - ' + 'Closed auction: ' + event['args']['auctionID'])
    elif (event['event'] == 'evt_maximunSecretBidBeaten'):
        print(str(datetime.fromtimestamp((event['args']['timeStamp']))) + ' - ' + 'Maximun Secret Bid beaten for bidder: ' + event['args']['beatenBidder'] + '- Lot: ' + str(event['args']['lotId']))
    elif (event['event'] == 'evt_auctionLotExtended'):
        print(str(datetime.fromtimestamp((event['args']['timeStamp']))) + ' - ' + 'Lot ' + str(event['args']['lotId']) + ' end date extended. New end date: ' + str(datetime.fromtimestamp((event['args']['newEndDate']))))
    #print(Web3.toJSON(event))

# asynchronous defined function to loop
# this loop sets up an event filter and is looking for new entires for the "PairCreated" event
# this loop runs on a poll interval
async def log_loop(event_filter, poll_interval):
    print('Listening events...')
    while True:
        for evt in event_filter:
            for single_event in evt.get_new_entries():
                handle_event(single_event)

        await asyncio.sleep(poll_interval)


# when main is called
# create a filter for the latest block and look for the "PairCreated" event for the uniswap factory contract
# run an async loop
# try to run the log_loop function above every 2 seconds
def main():
    event_filters = [evt.createFilter(fromBlock='latest') for evt in contract.events]
    #event_filter = contract.events.evt_bidConfirmed.createFilter(fromBlock='latest')
    #block_filter = web3.eth.filter('latest')
    # tx_filter = web3.eth.filter('pending')
    loop = asyncio.get_event_loop()
    print('Starting Event Loop')
    try:
        loop.run_until_complete(
            asyncio.gather(
                log_loop(event_filters, 2)))
                # log_loop(block_filter, 2),
                # log_loop(tx_filter, 2)))
    finally:
        # close loop to free up system resources
        loop.close()


if __name__ == "__main__":
    main()