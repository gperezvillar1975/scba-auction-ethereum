# scba-auction-ethereum
Smart contract for implementing auctions on the blockchain

Review the [Architecture Diagram](https://github.com/gperezvillar1975/scba-auction-ethereum/blob/main/Architecture.txt)

# Auction Lifecycle

# Contract external callable methods

## Auction init

The auction init process is the first step to enable the bidder inscription and confirmation process, for running this function the auction should be in NO INIT state, wich is the starting state inmediatly after the auction contract is deployed. Each bidder is free to push in one or more auction lots.

```
function auctionInit(
        string memory __auctionCode,  // Auction code assigned from the web portal.
        AuctionClass __auctionClass,  // Auction Class: 0 - Real State, 1 - Mobile Assets, registrable mobile assets
        uint __guaranteeDeposit,      // Amount for the guarantee deposit expresed in WEI.
        uint __totalAuctionLots,      // Number of auctions lot
        uint __startDate,             // Predefined start date
        uint __endDate                // Predefined end date ( 10 working days may exists between start and end date )
    ) 

```

## Auction Auction add lots

Every lot inside the auction behaves like a self independent auction, the parent auctions ends when the last lot finishes the push process.

```
function auctionAddLot(
        uint __baseValue   // Minimun amount of WEI for starting the auction process, the first auction tranche is equal to the base value.
    ) 
   
```
## Auction state query functions

- getAuctionState()
- getAuctionBalance()
- getAuctionStartDate()
- getAuctionEndtDate()
- getAuctionClass()

## Auction lots query functions

- getActualTranche(uint _lotId)
- getLastTranche(uint _lotId)
- getLotQuantity()
- getLotBaseValue(uint _lotId)
- getLotTrancheValue(uint _lotId, uint _trancheId)
- getLotEndDate(uint _lotId)
- getLotExtensionCount(uint _lotId)

## Confirmed bidders query functions

- getConfirmedBiddders()
- isBidderConfirmed(address _queryBidder)
- getBidderMaximunSecretBid(uint _lotId, address _bidder)
