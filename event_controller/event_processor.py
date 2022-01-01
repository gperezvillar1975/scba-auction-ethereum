# define function to handle events and print to the console
from datetime import datetime
import asyncio

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

async def log_loop(event_filter, poll_interval):
    print('Listening events...')
    while True:
        for evt in event_filter:
            for single_event in evt.get_new_entries():
                handle_event(single_event)

        await asyncio.sleep(poll_interval)