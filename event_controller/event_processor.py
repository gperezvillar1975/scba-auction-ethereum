# define function to handle events and print to the console
from datetime import datetime
import asyncio
import json
from web3 import Web3
from  contract_functions import get_auction_contract,load_auction_data
from global_defs import AUCTIONS,web3,auction_abi,abi_contract
from socket_server import broadcast_event


async def process_auctionEvent(event):
    auction_contract = event['address']
    auction_object = AUCTIONS[auction_contract]
    auction_object.events.append(event)        

    await broadcast_event(Web3.toJSON(event),auction_contract)

async def handle_event(event):    
    if (event['event'] == 'evt_AuctionInit'):
        load_auction_data(event['address'])
        await process_auctionEvent(event)
    if (event['event'] == 'evt_LotInit'):
        load_auction_data(event['address'])
        await process_auctionEvent(event)
    if (event['event'] == 'evt_bidderInscription'):
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

    auction_contract = await get_auction_contract("MP151")
  

    contract = web3.eth.contract(address=auction_contract, abi=abi_contract['abi'])
    event_filter = [evt.createFilter(fromBlock='latest',toBlock="pending") for evt in contract.events]

    print('Listening events...')
    while True:
        for evt in event_filter:
            for single_event in evt.get_new_entries():
                await handle_event(single_event)

        await asyncio.sleep(poll_interval)