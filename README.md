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

## Bidder confirmation process

The bidder confirmation process enables bidder to push in any auction lot. The bidder is identified by his public address and it must confirm the auction guarantee deposit to participate.

```
function _confirmBidderInscription(
    address _bidderAddress // Bidder public addres - Extracted from payable transaction call. msg.address
    uint _depositAmount,   // Extracted from payable transaction call. msg.value
    bool _preserveGuaranteeDeposit) // If the bidder wants to preserve his deposit in case that the winner bidder quit from the auction. In case hi decide to preserve de guarantee deposit the bidder could't withdraw founds at auction end.

```

## Set per bidder auction parameters 

- Preserve last bid: Idem Preserve Guarantee deposit.
- Maximun Secret Bid: The bidder can define an auction lot tranche or a amount of wei for what the system will push in bidder's name. It's like a authorization to push in the name of the bidder. When the maximun secret bid is beaten, the contract will emit an event.

```

function bidderSetPreservelastBid(bool _value)
function bidderSetMaximunSecretBidAmount(uint _lotId, uint _value) // Set maximun secret bid with a specific amount of wei that the system will equate to the corresponding tranche.

function bidderSetMaximunSecretBidTranche(uint _lotId, uint _value) // Set the maximun secrer bid with a specific lot tranche number.

```

## Auction state functions

- auctionStart()
- auctionClose()
- auctionCancel(string memory _cause)

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
