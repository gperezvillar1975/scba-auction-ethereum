// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;

import "@openzeppelin/contracts/access/Ownable.sol";

/***
 * This contract implementas public auctions at Supreme Court in Buenos Aires Province @ Argetina.
 * The auction process has an hybrid architecture, where the auction data and administrative flow is centralizad in a 
 * traditional web application, and the push process and winner definition happens in the blockchain.
 * 
 * Author: Lic. Gustavo Perez Villar @ Buenos Aires - Argentina
 */

contract AuctionsSCBA is Ownable {
    
    // Events

    event evt_bidderConfirmedInscription(address indexed sender, string message);
    event evt_auctionStart(uint timeStamp, string auctionID);
    event evt_auctionCanceled(uint timeStamp, string auctionID, string cause);

    // Custom data types

    enum AuctionClass {REAL_STATE,MOBILE,MOBILE_REGISTER}
    enum AuctionState {NO_INIT,INIT,LOT,STARTED,EXTENDED,ENDED,CANCELED}
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
        uint actualTrancheId_;
    }
    struct Auction {
        string auctionCode_;
        AuctionClass auctionClass_;
        uint guaranteeDeposit_;
        uint totalAuctionLots_;
        uint startDate_;
        uint endDate_;
    }
    struct Bidder {
        uint guaranteeDeposit_; // Deposited amount in wei for confirm auction inscription
        bool preserveLastBid_;  // If he wants to preserve his last bid in case the winner doesn't confirm the buy. 
                                // if preserve bid is true, the bidder cannot withdraw founds after auction ending.
        uint[] lotSecretBid_;   // Secrets bid per lot. lotSecretBid_[lotId-1] = secretBid
    }
    struct AuctionTranches {
        uint trancheId_;
        uint trancheValue_;
        address trancheBidder_;
        bool trancheConfirmed_;
        uint trancheBidTimestamp;
    }

    // State Variables

    AuctionLot[] private _auctionLots; // Auction lots array
    AuctionState private _auctionState; // Actual auction state
    Auction private _auctionObject; // Instance of auction data
    mapping (address => Bidder) private _validBidders; // Valid registered bidders
    mapping (uint => AuctionTranches) private _tranchesPerLot;
    uint private _confirmedBidders;

   // Constructor

    constructor () {
        // State variables initialization
        _auctionState = AuctionState.NO_INIT;
        _confirmedBidders = 0;
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
        uint __totalAuctionLots,
        uint __startDate,
        uint __endDate 
    ) external onlyOwner  {
        require(_auctionState  == AuctionState.NO_INIT, "Auction already initialized");
        require(block.timestamp < __startDate && (__startDate + 10 days) <= __endDate,"Invalid dates");
        _auctionState = AuctionState.INIT;
        _auctionObject.auctionCode_ = __auctionCode;
        _auctionObject.auctionClass_ = __auctionClass;
        _auctionObject.guaranteeDeposit_ = __guaranteeDeposit;
        _auctionObject.totalAuctionLots_ = __totalAuctionLots;
        _auctionObject.startDate_ = __startDate;
        _auctionObject.endDate_ = __endDate;
    }

    function auctionAddLot(uint __baseValue) external onlyOwner {
        require(_auctionState == AuctionState.INIT || _auctionState == AuctionState.LOT ,"Auction is NOT initialized. Initialize auction before adding lots.");
        // Can't add more tha one lot if the auction class is Realstate
        if (_auctionObject.auctionClass_ == AuctionClass.REAL_STATE && _auctionLots.length == 1) { revert("Real State auctions only allows one lot"); }
        if (_auctionLots.length > _auctionObject.totalAuctionLots_) { revert("Cant't add more lots than definded in totalAuctionLots"); }
        AuctionLot memory tmpLot;
        _auctionState = AuctionState.LOT;
        tmpLot.lotId_ = _auctionLots.length + 1;  //Start at lot 1
        tmpLot.extensionsCount_ = 0;
        tmpLot.startDate_ = _auctionObject.startDate_;
        tmpLot.endDate_ = _auctionObject.endDate_;
        tmpLot.extendedEndDate_ = _auctionObject.endDate_;
        tmpLot.winnerTranche_ = 0;
        tmpLot.baseValue_ = __baseValue;
        tmpLot.lastTrancheId_ = 0;
        _auctionLots.push(tmpLot); // Add lot to lot array
    }  

    function auctionStart() external onlyOwner {
        _setAuctionStart();
    }

   function auctionCancel(string memory _cause) external onlyOwner {
        _auctionCancelation(_cause);
    }

    // Public Functions

    function getAuctionState() public view returns (AuctionState) {
        return _auctionState;
    }
    
    // Get contract address blance (sum of all guarantee deposits for each confirmed bidder)
    function getAuctionBalance() public view returns (uint) {
        return address(this).balance;
    } 
    
    function getConfirmedBiddders() public view returns (uint){
        return _confirmedBidders;
    }

    function isBidderConfirmed(address _queryBidder) public view returns(bool) {     
        return (_validBidders[_queryBidder].guaranteeDeposit_ > 0);
    }

    function getAuctionStartDate() public view returns(uint) {     
        return _auctionObject.startDate_;
    }

    function getAuctionEndtDate() public view returns(uint) {     
        return _auctionObject.endDate_;
    }

    function getAuctionClass() public view returns(AuctionClass) {     
        return _auctionObject.auctionClass_;
    }

    function getActualTranche(uint _lotId) public view returns (uint,uint) {
        uint retTrancheId_;
        uint retValue_;

        retTrancheId_ = _auctionLots[_lotId-1].actualTrancheId_;
        retValue_ = _tranchesPerLot[_lotId-1].trancheValue_;
        
        return (retTrancheId_, retValue_);
    }

    function getLastTranche(uint _lotId) public view returns (uint,uint,address) {
        uint retTrancheId_;
        uint retValue_;
        address retBidder_;

        retTrancheId_ = _auctionLots[_lotId-1].actualTrancheId_;
        retValue_ = _tranchesPerLot[_lotId-1].trancheValue_;
        retBidder_ = _tranchesPerLot[_lotId-1].trancheBidder_;
        
        return (retTrancheId_, retValue_, retBidder_);
    }


    function bidderSetPreservelastBid(bool _value) public {
        require(_auctionState == AuctionState.LOT,"There must be at least one lot defined."); 
        require(_validBidders[msg.sender].guaranteeDeposit_ > 0,"Bidder is not confirmed"); 
        require((msg.sender != this.owner()));
        
        _validBidders[msg.sender].preserveLastBid_ = _value;

    }

    function bidderSetMaximunSecretBid(uint _lotId, uint _value) public {
        require(_auctionState == AuctionState.LOT,"There must be at least one lot defined."); 
        require(_validBidders[msg.sender].guaranteeDeposit_ > 0,"Bidder is not confirmed"); 
        require((msg.sender != this.owner()));
        
        _validBidders[msg.sender].lotSecretBid_[_lotId-1] = _value;

    }

    // Internal Functions

    function _confirmBidderInscription(address _bidderAddress, uint _depositAmount, bool _preserveGuaranteeDeposit) internal     {
        Bidder memory _tmpBidder;
        require(_auctionState == AuctionState.LOT,"There must be at least one lot defined."); 
        require(_validBidders[_bidderAddress].guaranteeDeposit_ == 0,"Bidder already confirmed"); 
        require(_depositAmount >= _auctionObject.guaranteeDeposit_,"The deposit for confirm inscription MUST be equal or greater than teh guarantee deposit.");
        require (block.timestamp <= _auctionObject.startDate_,"Bidder registration window expired.");
        require((msg.sender != this.owner()));

        _tmpBidder.guaranteeDeposit_ = _depositAmount;
        _tmpBidder.preserveLastBid_ = _preserveGuaranteeDeposit;
        _validBidders[_bidderAddress] = _tmpBidder;
        _confirmedBidders += 1;

        emit evt_bidderConfirmedInscription(_bidderAddress,"Confirmed bidder inscription.");
    }

    function _setAuctionStart() internal  {
        require(_auctionState == AuctionState.LOT,"There must be at least one lot defined."); 
        require(block.timestamp >= _auctionObject.startDate_ && block.timestamp <= _auctionObject.endDate_,"Actual time outside auction boundaries");
        
        if (_confirmedBidders == 0) {
             _auctionCancelation("No confirmed bodders at auction start");
        } else {
            _auctionState = AuctionState.STARTED;
            _initTranches();
            emit evt_auctionStart(block.timestamp, _auctionObject.auctionCode_);
        }
    }
    
    function _auctionCancelation(string memory _cause) internal {
        require(_auctionState != AuctionState.CANCELED,"The auction was previusly canceled."); 
        require(block.timestamp <= _auctionObject.endDate_,"Auction end date reached");
        
        _auctionState = AuctionState.CANCELED;
        emit evt_auctionCanceled(block.timestamp, _auctionObject.auctionCode_, _cause);
    }

    function _initTranches() internal {
        require(_auctionState == AuctionState.STARTED,"The auction MUST be in STARTED state");
        uint _LotsLength = _auctionLots.length;
        AuctionTranches memory _tmpTranche;

        for (uint i=0; i<_LotsLength; i++) {
            _tmpTranche.trancheId_ = i+1;
            _tmpTranche.trancheValue_ = _auctionLots[i].baseValue_;
            _tmpTranche.trancheConfirmed_ = false;
            _tranchesPerLot[i] = _tmpTranche;
            _auctionLots[i].actualTrancheId_ = 1; 
        }
    }

}
