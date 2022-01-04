from asyncio import events
from web3 import Web3
import asyncio

from web3.contract import ContractEvents
from global_defs import AUCTION_DETAILS, AUCTIONS,LOT_DETAIL,web3,auction_abi,abi_contract

async def get_auction_contract(auction_code):
    return "0x0bC05eA568CCB3aF9e697F78019959db7aBbd531"

async def bidder_confirmed(auction_address, bidder_address):
    
    return True

def load_auctions():
    load_auction_data("0x0bC05eA568CCB3aF9e697F78019959db7aBbd531")
    return

def load_auction_data(auction_address):
    print("Loading data for auction " + auction_address)
    if auction_address:
        contract = web3.eth.contract(address=auction_address, abi=abi_contract['abi'])
        na = AUCTION_DETAILS
        na.auctionCode = "MP151"
        na.auctionState =  contract.functions.getAuctionState().call()
        try:
            nLots = contract.functions.getLotQuantity().call()
        except:
            nLots = 0
            
        for x in range(nLots):
            nl = LOT_DETAIL
            nl.lotId = x+1
            nl.startDate = contract.functions.getAuctionStartDate().call()
            nl.endDate = contract.functions.getAuctionEndtDate().call()
            nl.baseValue = contract.functions.getLotBaseValue(x+1).call()
            try:        
                nl.actualTrancheId = contract.functions.getActualTranche(x+1).call()
            except:
                nl.actualTrancheId = 1
            try:
                nl.lastTrancheId = contract.functions.getLastTranche(x+1).call()
            except:
                nl.lastTrancheId = 1
            try:
                nl.extensionsCount = contract.functions.getLotExtensionCount(x+1).call()
            except:
                nl.extensionsCount = 0
            try:
                nl.extendedEndDate = contract.functions.getLotEndDate(x+1).call()
            except:
                nl.extendedEndDate = nl.endDate

            na.lotDetail.append(nl)
        
        event_filter = [evt.createFilter(fromBlock=0,toBlock="latest") for evt in contract.events]
        for evt in event_filter:  
            for single_event in evt.get_all_entries():
                na.events.append(single_event)
                #print(single_event)

        AUCTIONS[auction_address] = na
