# define function to handle events and print to the console
from datetime import datetime
import asyncio
import json
from web3 import Web3
from  contract_functions import get_auction_contract
from global_defs import AUCTIONS
from socket_server import broadcast_event


async def process_auctionEvent(event):
    auction_contract = event['address']
    if not auction_contract in AUCTIONS:
        auction_events = {event}
        AUCTIONS[auction_contract] = auction_events        
    else:
        auction_events = AUCTIONS[auction_contract]
        auction_events.add(event)        

    await broadcast_event(Web3.toJSON(event),auction_contract)

async def handle_event(event):    
    if (event['event'] == 'evt_bidderConfirmedInscription'):
        await process_auctionEvent(event)
    elif (event['event'] == 'evt_auctionStart'):        
        await process_auctionEvent(event)
    elif (event['event'] == 'evt_bidConfirmed'):
        await process_auctionEvent(event)
    elif (event['event'] == 'evt_auctionClosed'):        
        await process_auctionEvent(event)
    elif (event['event'] == 'evt_maximunSecretBidBeaten'):
        await process_auctionEvent(event)
    elif (event['event'] == 'evt_auctionLotExtended'):
        await process_auctionEvent(event)
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