import json
import asyncio
from web3 import Web3
import websockets
import contract_functions
from global_defs import AUCTIONS, JOIN

async def replay_bids(websocket):
    pass

async def replay_events(auction,websocket):
    try:
        auction_events = AUCTIONS[auction]
        for evt in auction_events:
            await websocket.send(Web3.toJSON(evt))
    except:
        await error(websocket,'No events available')

async def receive_bids(websocket):
    pass

async def broadcast_event(json_message, auction_contract):
    bidders,connected = JOIN[auction_contract]
    if connected:
        for socket in connected:
            await socket.send(json_message)

async def error(websocket, message):
    #Send an error message.
    event = {
        "type": "error",
        "message": message,
    }
    await websocket.send(json.dumps(event))

async def join_auction(websocket,event):
    auction = await contract_functions.get_auction_contract(event["auction"])
    bidder = event["bidder"]     


    if auction:
        # Verify if bidder is inscripted
        is_confirmed = await contract_functions.bidder_confirmed(auction, bidder)
        if is_confirmed :
            if not auction in JOIN:       
                connected={websocket}
                bidders = {bidder}
                JOIN[auction] = bidders,connected
                print("Connecting bidder " + bidder + " to auction " + auction)
            else:
                if not any(bidder in sublist for sublist in JOIN[auction]):
                    bidders,connected = JOIN[auction]
                    bidders.add(bidder)
                    connected.add(websocket)                    
            ret_event = {
                "type" : "join",
                "status" : "ok",
                "data" : ""
            }
        else:
            await error(websocket,'Bidder not confirmed')        

        try:
            print("Joining bidder")            
            await websocket.send(json.dumps(ret_event))
            await replay_events(auction,websocket)
            await websocket.wait_closed()
            #await replay_bids(websocket)
            #await receive_bids(websocket)
        finally:
            connected.remove(websocket)
            print("Bidder " + bidder + " leaving...")
    else:
        bidders,connected = JOIN[auction]
        await error(websocket,'Auction not found')

async def handler(websocket,path):
    # Receive and parse the "init" event from the UI.
    # events: 
    # {type: join, auction: <auction code>, bidder: <bidder_address>}

    message = await websocket.recv()
    event = json.loads(message)
    
    if event["type"] == "join":
        await join_auction(websocket,event)
