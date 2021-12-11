// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;

import "@openzeppelin/contracts/access/Ownable.sol";

/***
 * This contract implementas public auctions at Supreme Court in Buenos Aires Province @ Argetina.
 */

contract AuctionsSCBA is Ownable {
    
    // Events

    event evt_bidderConfirmedInscription(address indexed sender, string message);
    
    // Custom data types

    enum AuctionClass {REAL_STATE,MOBILE,MOBILE_REGISTER}
    enum AuctionState {NO_INIT,INIT,LOT,STARTED,EXTENDED,ENDED}
    struct AuctionLot {
        uint lotId_;
        uint startDate_;
        uint endDate_;
        uint baseValue_;
        uint extendedEndDate_;
        uint extensionsCount_;
        address winner_;
        uint winnerTranche_;
        uint lastTrancheId_;
    }
    struct Auction {
        string auctionCode_;
        AuctionClass auctionClass_;
        uint guaranteeDeposit_;
        uint totalAuctionLots_;
    }
    struct Bidder {
        uint guaranteeDeposit_; // Deposited amount in wei for confirm auction inscription
        bool preserveLastBid_;  // If he wants to preserve his last bid in case the winner doesn't confirm the buy. 
                               // if preserve bid is true, the bidder cannot withdraw founds after auction ending.
        uint secretBidAmount_;  // top limit amount for wich the contract will push bids in behalf the bidder. 
        uint lastBidderTrancheId_; // last correct bid amount for this bidder.
    }
    struct AuctionTranches {
        uint trancheId_;
        uint trancheValue_;
        address trancheBidder_;
    }

    // State Variables

    AuctionLot[] private _auctionLots; // Auction lots array
    AuctionState private _auctionState; // Actual auction state
    Auction private _auctionObject; // Instance of auction data
    mapping (address => Bidder) private _validBidders; // Valid registered bidders
    mapping (uint => AuctionTranches) private _tranchesPerLot;
    uint private  _lastTrancheId; // Last valid received bid 
    address private _lastBidderAddress; // Last bidder with a valid bid accepted

   // Constructor

    constructor () {
      _auctionState = AuctionState.NO_INIT;
      _lastTrancheId = 0;
    }

    // Receive functions

    function confirmBidderInscription(bool _preserveGuranteeDeposit) external payable {
        _confirmBidderInscription(msg.sender, msg.value, _preserveGuranteeDeposit);
    }

    // Fallback function

    receive() external payable {
       _confirmBidderInscription(msg.sender, msg.value,false); 
    } 

    // External Functions

    function auctionInit(
        string memory __auctionCode,
        AuctionClass __auctionClass, 
        uint __guaranteeDeposit, 
        uint __totalAuctionLots
    ) external onlyOwner  {
        require(_auctionState  == AuctionState.NO_INIT, "Auction already initialized");
        _auctionState = AuctionState.INIT;
        _auctionObject.auctionCode_ = __auctionCode;
        _auctionObject.auctionClass_ = __auctionClass;
        _auctionObject.guaranteeDeposit_ = __guaranteeDeposit;
        _auctionObject.totalAuctionLots_ = __totalAuctionLots;
    }

    function auctionAddLot(uint __startDate, uint __endDate, uint __baseValue) external onlyOwner {
        require(_auctionState == AuctionState.INIT || _auctionState == AuctionState.LOT ,"Auction is NOT initialized. Initialize auction before adding lots.");
        // Can't add more tha one lot if the auction class is Realstate
        if (_auctionObject.auctionClass_ == AuctionClass.REAL_STATE && _auctionLots.length == 1) { revert("Real State auctions only allows one lot"); }
        if (_auctionLots.length > _auctionObject.totalAuctionLots_) { revert("Cant't add more lots than definded in totalAuctionLots"); }
        AuctionLot memory tmpLot;
        AuctionTranches memory tmpTranches;
        _auctionState = AuctionState.LOT;
         _lastTrancheId += 1;
        tmpLot.lotId_ = _auctionLots.length + 1;  //Start at lot 1
        tmpLot.extensionsCount_ = 0;
        tmpLot.startDate_ = __startDate;
        tmpLot.endDate_ = __endDate;
        tmpLot.extendedEndDate_ = __endDate;
        tmpLot.winnerTranche_ = 0;
        tmpLot.baseValue_ = __baseValue;
        tmpLot.lastTrancheId_ = 0;
        _auctionLots.push(tmpLot); // Add lot to lot array
        tmpTranches.trancheId_ = _lastTrancheId; // Start at tranche 1
        tmpTranches.trancheValue_ = __baseValue;
        _tranchesPerLot[tmpTranches.trancheId_] = tmpTranches; // add tranche data to auctionTranches mapping;
    }  

    // Public Functions

    function getAuctionState() public view returns (AuctionState) {
        return _auctionState;
    }
    
    // Get contract address blance (sum of all guarantee deposits for each confirmed bidder)
    function getAuctionBalance() public view returns(uint) {
        return address(this).balance;
    }
    
    function bidderSetPreservelastBid(bool _value) public {
        require(_auctionState == AuctionState.LOT,"There must be at least one lot defined."); 
        require(_validBidders[msg.sender].guaranteeDeposit_ > 0,"Bidder is not confirmed"); 
        require((msg.sender != this.owner()));
        
        _validBidders[msg.sender].preserveLastBid_ = _value;

    }

    function bidderSetMaximunSecretBid(uint _value) public {
        require(_auctionState == AuctionState.LOT,"There must be at least one lot defined."); 
        require(_validBidders[msg.sender].guaranteeDeposit_ > 0,"Bidder is not confirmed"); 
        require((msg.sender != this.owner()));
        
        _validBidders[msg.sender].secretBidAmount_ = _value;

    }

    // Internal Functions

    function _confirmBidderInscription(address _bidderAddress, uint _depositAmount, bool _preserveGuaranteeDeposit) internal     {
        Bidder memory _tmpBidder;
        _tmpBidder.guaranteeDeposit_ = _depositAmount;
        _tmpBidder.preserveLastBid_ = _preserveGuaranteeDeposit;
        _tmpBidder.secretBidAmount_ = 0;
        _tmpBidder.lastBidderTrancheId_ = 0;

        require(_auctionState == AuctionState.LOT,"There must be at least one lot defined."); 
        require(_validBidders[_bidderAddress].guaranteeDeposit_ == 0,"Bidder already confirmed"); 
        require(_depositAmount >= _auctionObject.guaranteeDeposit_,"The deposit for confirm inscription MUST be equal or greater than teh guarantee deposit.");
        require((msg.sender != this.owner()));

        _validBidders[_bidderAddress] = _tmpBidder;
        emit evt_bidderConfirmedInscription(_bidderAddress,"Confirmed bidder inscription.");
    }

    // Implementar funciones para obtener info de la subasta
    // Lotes
    // Tramos
    // Postores inscriptos
}
