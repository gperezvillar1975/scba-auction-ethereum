# scba-auction-ethereum
Smart contract for implementing auctions on the blockchain

Review the [Architecture Diagram](https://github.com/gperezvillar1975/scba-auction-ethereum/blob/main/Architecture.txt)

# Auction Lifecycle

# Contract external callable methods
```
function auctionInit(
        string memory __auctionCode,  // Auction code assigned from the web portal.
        AuctionClass __auctionClass,  // Auction Class: 0 - Real State, 1 - Mobile Assets, registrable mobile assets
        uint __guaranteeDeposit,      // Amount for the guarantee deposit expresed in WEI.
        uint __totalAuctionLots,      // Number of auctions lot
        uint __startDate,             // Predefined start date
        uint __endDate                // Predefined end date ( 10 working days may exists between start and end date )
    ) external onlyOwner  {
```
