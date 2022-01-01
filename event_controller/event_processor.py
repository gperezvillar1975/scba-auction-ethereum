# define function to handle events and print to the console
from datetime import datetime
import asyncio
import json
from web3 import Web3
from  contract_functions import get_auction_contract
from global_defs import AUCTIONS
from socket_server import broadcast_event

async def process_auctionStart(event):
    auction_code = event['args']['auctionID']
    auction_contract = await get_auction_contract(auction_code)

    if not auction_contract in AUCTIONS:
        auction_events = {event}
        AUCTIONS[auction_contract] = auction_events
        await broadcast_event(event,auction_contract)

async def handle_event(event):    
    if (event['event'] == 'evt_bidderConfirmedInscription'):
        print(str(datetime.fromtimestamp((event['args']['timeStamp']))) + ' - ' + 'Confirmed Inscription Bidder: ' + event['args']['_bidder'])
    elif (event['event'] == 'evt_auctionStart'):
        print(str(datetime.fromtimestamp((event['args']['timeStamp']))) + ' - ' + 'Started auction: ' + event['args']['auctionID'])
        await process_auctionStart(event)
    elif (event['event'] == 'evt_bidConfirmed'):
        print(str(datetime.fromtimestamp((event['args']['timeStamp']))) + ' - ' + 'Bid confirmed for lot: ' + str(event['args']['lotId']) + ' - Tranche: ' + str(event['args']['trancheId']) + ' - Bidder: ' +  event['args']['_bidder'])
    elif (event['event'] == 'evt_auctionClosed'):
        print(str(datetime.fromtimestamp((event['args']['timeStamp']))) + ' - ' + 'Closed auction: ' + event['args']['auctionID'])
    elif (event['event'] == 'evt_maximunSecretBidBeaten'):
        print(str(datetime.fromtimestamp((event['args']['timeStamp']))) + ' - ' + 'Maximun Secret Bid beaten for bidder: ' + event['args']['beatenBidder'] + '- Lot: ' + str(event['args']['lotId']))
    elif (event['event'] == 'evt_auctionLotExtended'):
        print(str(datetime.fromtimestamp((event['args']['timeStamp']))) + ' - ' + 'Lot ' + str(event['args']['lotId']) + ' end date extended. New end date: ' + str(datetime.fromtimestamp((event['args']['newEndDate']))))
    #print(Web3.toJSON(event))

async def log_loop(poll_interval):

    # add your blockchain connection information
    ganache_url = 'http://10.10.12.40:8545'
    web3 = Web3(Web3.HTTPProvider(ganache_url))
    # auction contract address and abi
    auction_contract = await get_auction_contract("MP151")
    auction_abi = './abi/AuctionsSCBA.json'
    abi = open(auction_abi)
    abi_contract=json.load(abi)
    abi.close()

    contract = web3.eth.contract(address=auction_contract, abi=abi_contract['abi'])
    event_filter = [evt.createFilter(fromBlock='latest') for evt in contract.events]

    print('Listening events...')
    while True:
        for evt in event_filter:
            for single_event in evt.get_new_entries():
                await handle_event(single_event)

        await asyncio.sleep(poll_interval)