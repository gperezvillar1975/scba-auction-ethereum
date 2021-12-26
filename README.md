# scba-auction-ethereum
Smart contract for implementing auctions on the blockchain

Review the [Architecture Diagram](https://github.com/gperezvillar1975/scba-auction-ethereum/blob/main/Architecture.txt)

# Auction Lifecycle

# Contract external callable methods

## Auction init

```
The auction init process is the first step to enable the bidder inscription and confirmation process, for running this function the auction should be in NO INIT state, wich is the starting state inmediatly after the auction contract is deployed.  

function auctionInit(
        string memory __auctionCode,  // Auction code assigned from the web portal.
        AuctionClass __auctionClass,  // Auction Class: 0 - Real State, 1 - Mobile Assets, registrable mobile assets
        uint __guaranteeDeposit,      // Amount for the guarantee deposit expresed in WEI.
        uint __totalAuctionLots,      // Number of auctions lot
        uint __startDate,             // Predefined start date
        uint __endDate                // Predefined end date ( 10 working days may exists between start and end date )
    ) external onlyOwner  {
```
