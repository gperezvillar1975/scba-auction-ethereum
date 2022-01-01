import json
import asyncio
from web3 import Web3
import secrets

import websockets
import contract_functions

from event_controller.main import JOIN, WATCH

async def error(websocket, message):
    #Send an error message.
    event = {
        "type": "error",
        "message": message,
    }
    await websocket.send(json.dumps(event))

async def join_auction(websocket,event):
    bidder = event["bidder"]
    connected = {websocket}
    auction = await contract_functions.get_auction_contract(event["auction"])

    if auction:
        # Verify if bidder is inscripted
        if await contract_functions.bidder_confirmed(bidder):
            join_key = secrets.token_urlsafe(12)
            JOIN[join_key] = auction,bidder,connected
            ret_event = {
                "type" : "join",
                "status" : "join",
                "data" : "{key: " + join_key + "}"
            }
        else:
            watch_key = secrets.token_urlsafe(12)
            WATCH[watch_key] = auction,bidder,connected            
            ret_event = {
                "type" : "join",
                "status" : "watch",
                "data" : ""
            }
        try:
            await websocket.send(json.dumps(event))
        finally:
            del JOIN[join_key]
            del WATCH[watch_key]
    else:
        await error(websocket,'Auction not found')

async def handler(websocket,path):
    # Receive and parse the "init" event from the UI.
    # events: 
    # {type: join, auction: <auction code>, bidder: <bidder_address>}
    # {type: watch, auction: <auction code>}

    message = await websocket.recv()
    event = json.loads(message)
    
    if event["type"] == "join":
        await join_auction(websocket,event)
    elif event["type"] == "watch":
        pass

    async for message in websocket:
        await websocket.send(message)
