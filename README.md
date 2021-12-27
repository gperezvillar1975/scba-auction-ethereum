# scba-auction-ethereum
Smart contract for implementing auctions on the blockchain

# Auction architecture

```
                                     ┌──────────────────┐
                                     │   ASYNC          │
                                     │   NOTIFICATIONS  │
                                     │   SERVICE        │
                                     │                  │
                                     └──────────────────┘
                                                ▲
                                                │
                                                │
                                                │
     ┌──────────────────────────────────────────┴─────────────────────────────────────────┐
     │                         KAFKA TOPIC                                                │
     │                                                                                    │
     └────────────────────────────────────────────────────────────────────────────────────┘
                                                ▲
                                                │
                                                │
                                                │
┌──────────────────────┐                ┌───────┴─────────┐                  ┌──────────────┐
│                      │                │WebSocket Server │   Commands       │              │
│                      │ ─────────────► │                 ├────────────────► │              │
│    JavaScript        │                │Event Controller │                  │              │
│                      │ ◄───────────── │                 │◄──────────────── │              │
│                      │                └─────────────────┘   Events         │   Contract   │
│    FrontEND          │                                                     │              │
│                      │                                                     │              │
│                      │                                                     │              │
│                      │                                                     └──────────────┘
│                      │                ┌─────────────────┐                         ▲
│                      │                │                 │                         │
│                      │ ◄───────────── │  REST API       │ ────────────────────────┘
│                      │                │                 │      Commands
└──────────────────────┘ ─────────────► └─────────────────┘

```

# Auction Lifecycle

```

                   ┌───────────────────┐
                   │                   │
                   │    NO INIT        │
                   └────────┬──────────┘
                            │
                            │ auctionInit()
                   ┌────────▼──────────┐
                   │                   │
                   │     INIT          │
                   └────────┬──────────┘
                            │
                            │ auctionAddLot()
                   ┌────────▼──────────┐
                   │                   │
                   │    LOT            │              ┌────────────────────┐
                   └────────┬──────────┤              │                    │
                            ├──────────┴─────────────►│  Bidder Inscription│
                            │ auctionStart()          │                    │
                   ┌────────▼──────────┐              └────────────────────┘
                   │                   │
                   │     STARTED       │
                   └─────────┬─────────┘
                             │
         bid                 │no bid for 3 minutes
         ┌───────────────────┼─────────────────────────┐
         │                   │                         │  auction Cancel()
┌────────▼────────┐   ┌──────▼──────────┐   ┌──────────▼───────┐
│                 │   │                 │   │                  │
│    EXTENDED     │   │  CLOSED         │   │   CANCELED       │
│                 │   │                 │   │                  │
└─────────────────┘   └─────────────────┘   └──────────────────┘

```

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

- **auctionStart()**: On auction start the contract starts an automatic push between all the maximun secrets bid, until one of them wins the push. At this moment the remaining maximun secret bid continues pushing against manual bids.
- **auctionClose()**: On auction close, the contract will persist each auction lot winner and enable those bidders who didn't preserve the guarantee deposit  to withdraw the deposited amount in wei. The remaining bidders will be enabled to withdraw later by the judge.
- **auctionCancel(string memory _cause)**: The cancel method will pause the contract forever. enabling all bidders to withdraw founds.

## The bid push process

The contract receipts bids between start and end dates, at auction starts it calculates the auction tranches, each tranche amount differs from the previous one in a 5% from the auction base value. Every received bid moves the auction to the nex available tranche. The bidder can invoke bid function to push for the current tranche in each auction lot.

```
function _bid(
    address _bidder, // Message sender public addres.
    uint _lotId,     // Auction Lot id
    uint _bidTranche // Tranche id for the bid
)

```
## Auction end date extension

at the auction INIT state you define the auction start and end dates, the contract copies those dates into each lot. So all the auction lots starts at the same time, but if a valid bid is received in the last 3 minutes of the lot duration, the contract extends the end date of that particular lot for a 10 minutes period after the predefined end date for that lot. This behavior repeats until no bid received during the last 3 minutes of the bid push for that lot. The auction end date is equated to the higher lot end date.

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

## Auction events

- evt_bidderConfirmedInscription(address indexed sender, string message);
- evt_auctionStart(uint timeStamp, string auctionID);
- evt_auctionCanceled(uint timeStamp, string auctionID, string cause);
- evt_maximunSecretBidBeaten(uint timeStamp, address beatenBidder);
- evt_bidConfirmed(uint timeStamp, uint lotId, uint trancheId, address _bidder);
- evt_auctionLotExtended(uint timeStamp, uint lotId, uint newEndDate);
- evt_auctionClosed(uint timeStamp, string auctionID);
- evt_bidderWithDraw(uint timeStamp, address bidderId, uint amount);
- evt_bidderEnabledToWithDraw(uint timeStamp, address bidderId);

