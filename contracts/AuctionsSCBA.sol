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
    event evt_maximunSecretBidBeaten(uint timeStamp, address beatenBidder);
    event evt_bidConfirmed(uint timeStamp, uint lotId, uint trancheId, address _bidder);
    event evt_auctionLotExtended(uint timeStamp, uint lotId, uint newEndDate);

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
        uint extendedEndDate_;
    }
    struct Bidder {
        uint guaranteeDeposit_; // Deposited amount in wei for confirm auction inscription
        bool preserveLastBid_;  // If he wants to preserve his last bid in case the winner doesn't confirm the buy. 
                                // if preserve bid is true, the bidder cannot withdraw founds after auction ending.
        uint[] lotSecretBid_;   // Secrets bid per lot. lotSecretBid_[lotId-1] = secretBid. Secret Bid is expressed as trancheid
    }
    struct AuctionTranches {
        uint trancheId_;
        uint trancheValue_;
        address trancheBidder_;
        bool trancheConfirmed_;
        uint trancheBidTimestamp_;
    }

    // State Variables

    AuctionLot[] private _auctionLots; // Auction lots array
    AuctionState private _auctionState; // Actual auction state
    Auction private _auctionObject; // Instance of auction data
    mapping (address => Bidder) private _validBidders; // Valid registered bidders
    mapping (uint => AuctionTranches[]) private _tranchesPerLot;
    address[] private _bidderList;
    mapping (address => mapping(uint => bool)) _bidderLotMSBBeaten; // True if bidder's maximun secret bed has bean beaten for a particular lot

   // Constructor

    constructor () {
        // State variables initialization
        _auctionState = AuctionState.NO_INIT;
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
        //require(block.timestamp < __startDate && (__startDate + 10 days) <= __endDate,"Invalid dates");
        _auctionState = AuctionState.INIT;
        _auctionObject.auctionCode_ = __auctionCode;
        _auctionObject.auctionClass_ = __auctionClass;
        _auctionObject.guaranteeDeposit_ = __guaranteeDeposit;
        _auctionObject.totalAuctionLots_ = __totalAuctionLots;
        _auctionObject.startDate_ = __startDate;
        _auctionObject.endDate_ = __endDate;
        _auctionObject.extendedEndDate_ = __endDate;
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
        return _bidderList.length;
    }

    function isBidderConfirmed(address _queryBidder) public view returns(bool) {   
        return (_validBidders[_queryBidder].guaranteeDeposit_ > 0);
    }

    function getAuctionStartDate() public view returns(uint) {     
        return _auctionObject.startDate_;
    }

    function getAuctionEndtDate() public view returns(uint) {     
        return _auctionObject.extendedEndDate_;
    }

    function getAuctionClass() public view returns(AuctionClass) {     
        return _auctionObject.auctionClass_;
    }

    function getActualTranche(uint _lotId) public view returns (uint,uint) {
        uint retTrancheId_;
        uint retValue_;
        retTrancheId_ = _auctionLots[_lotId-1].actualTrancheId_;
        if (retTrancheId_ > 0 ) {
            retValue_ = _tranchesPerLot[_lotId-1][retTrancheId_-1].trancheValue_;
        } else {
            retValue_ = _tranchesPerLot[_lotId-1][0].trancheValue_;
        }
        return (retTrancheId_, retValue_);
    }

    function getLastTranche(uint _lotId) public view returns (uint,uint,address) {
        uint retTrancheId_;
        uint retValue_;
        address retBidder_;
        retTrancheId_ = _auctionLots[_lotId-1].lastTrancheId_;
        if (retTrancheId_ > 0) {
            retValue_ = _tranchesPerLot[_lotId-1][retTrancheId_-1].trancheValue_;
        } else {
            retValue_ = _tranchesPerLot[_lotId-1][0].trancheValue_;
        }
        retBidder_ = _tranchesPerLot[_lotId-1][retTrancheId_-1].trancheBidder_;
        
        return (retTrancheId_, retValue_, retBidder_);
    }

    function getBidderMaximunSecretBid(uint _lotId, address _bidder) public view returns (uint,uint) {
        uint _retTranche = _validBidders[_bidder].lotSecretBid_[_lotId-1];
        uint _retAmount = _getLotTrancheValue(_lotId,_retTranche);
        return (_retTranche, _retAmount);
    }
        
    function getLotQuantity() public view returns (uint) {
        return _auctionLots.length;
    }

    function getLotBaseValue(uint _lotId) public view returns (uint) {
        return _auctionLots[_lotId-1].baseValue_;
    }

    function getLotTrancheValue(uint _lotId, uint _trancheId) public view returns (uint) {
        
        return _getLotTrancheValue(_lotId,_trancheId);
    }
    
    function getLotEndDate(uint _lotId) public view returns (uint) {
        
        return _auctionLots[_lotId-1].extendedEndDate_;
    }
    function getLotExtensionCount(uint _lotId) public view returns (uint) {
        
        return _auctionLots[_lotId-1].extensionsCount_;
    }

    function bidderSetPreservelastBid(bool _value) public {
        require(_auctionState == AuctionState.LOT,"Preserve Last Bid - There must be at least one lot defined."); 
        require(_validBidders[msg.sender].guaranteeDeposit_ > 0,"Bidder is not confirmed"); 
        require((msg.sender != this.owner()));
        
        _validBidders[msg.sender].preserveLastBid_ = _value;

    }

    function bidderSetMaximunSecretBidAmount(uint _lotId, uint _value) public {
        require(_auctionState == AuctionState.LOT,"Set Maximun Secret Bid - There must be at least one lot defined."); 
        require(_validBidders[msg.sender].guaranteeDeposit_ > 0,"Bidder is not confirmed"); 
        require((msg.sender != this.owner()),"Function cannot be called by contract owner");
        require(_value > _auctionLots[_lotId-1].baseValue_,"Maximun Secret Bid MUST be greater than lot base value."); 
        uint _msbTranche;
        uint _fivePercent;
        
        _fivePercent = ((_auctionLots[_lotId-1].baseValue_ / 100) * 5);
        _msbTranche = ((_value - _auctionLots[_lotId-1].baseValue_) / _fivePercent) + 1;
        _validBidders[msg.sender].lotSecretBid_[_lotId-1] = _msbTranche-1; // -1 for approaching lower tranche.
        
    }
    function bidderSetMaximunSecretBidTranche(uint _lotId, uint _value) public {
        require(_auctionState == AuctionState.LOT,"Set MSB x Tranche - There must be at least one lot defined."); 
        require(_validBidders[msg.sender].guaranteeDeposit_ > 0,"Bidder is not confirmed"); 
        require((msg.sender != this.owner()),"Function cannot be called by contract owner");
        require(_value >= 1 ,"Tranche MUST be greater than zero."); 
        
        _validBidders[msg.sender].lotSecretBid_[_lotId-1] = _value;
    }

    function bid(uint _lotId, uint _trancheId) public {
        _bid(msg.sender, _lotId, _trancheId);
        _secretBidPush();
    } 
    // Internal Functions

    function _getLotTrancheValue(uint _lotId, uint _trancheId) internal view returns (uint) {
        uint _baseValue = _auctionLots[_lotId-1].baseValue_;
        uint _factor = _trancheId * 5;

        return _baseValue + ((_baseValue * _factor) / 100);
    }

    function _confirmBidderInscription(address _bidderAddress, uint _depositAmount, bool _preserveGuaranteeDeposit) internal     {
        Bidder memory _tmpBidder;
        uint _LotsLength = _auctionLots.length;
        require(_auctionState == AuctionState.LOT,"Confirm Inscription - There must be at least one lot defined."); 
        require(_validBidders[_bidderAddress].guaranteeDeposit_ == 0,"Bidder already confirmed"); 
        require(_depositAmount >= _auctionObject.guaranteeDeposit_,"The deposit for confirm inscription MUST be equal or greater than teh guarantee deposit.");
        require (block.timestamp <= _auctionObject.startDate_,"Bidder registration window expired.");
        require((msg.sender != this.owner()));

        _tmpBidder.guaranteeDeposit_ = _depositAmount;
        _tmpBidder.preserveLastBid_ = _preserveGuaranteeDeposit;
        // initialize Maximun Secret Bid array
        _validBidders[_bidderAddress] = _tmpBidder;
        for (uint i=0; i<_LotsLength; i++) {
            _validBidders[_bidderAddress].lotSecretBid_.push(0);
        }
        _bidderList.push(_bidderAddress);

        emit evt_bidderConfirmedInscription(_bidderAddress,"Confirmed bidder inscription.");
    }

    function _setAuctionStart() internal  {
        require(_auctionState == AuctionState.LOT,"Auction Start - There must be at least one lot defined."); 
        require((block.timestamp + 5 seconds) >= _auctionObject.startDate_ && block.timestamp <= _auctionObject.endDate_,"Actual time outside auction boundaries");
        
        if (_bidderList.length == 0) {
             _auctionCancelation("No confirmed bidders at auction start");
        } else {
            _auctionState = AuctionState.STARTED;
            _initTranches();
            _secretBidPush();

            emit evt_auctionStart(block.timestamp, _auctionObject.auctionCode_);        }
    }
    
    function _auctionCancelation(string memory _cause) internal {
        require(_auctionState != AuctionState.CANCELED,"The auction was previusly canceled."); 
        require(block.timestamp <= _auctionObject.extendedEndDate_,"Auction end date reached");
        
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
            _tranchesPerLot[i].push(_tmpTranche);
            _auctionLots[i].actualTrancheId_ = 1; 
        }
    }

    /*
    This function iterates over each bidder for every lot pushing using the Maximun Secret Bid commited before
    auction start. The push order is related to the inscription order and the loops ends when no maximun secret bid
    can beat the last valid automatic bid pushed.
    */
    function _secretBidPush() internal  {
        require(_auctionState == AuctionState.STARTED || _auctionState == AuctionState.EXTENDED,"The auction MUST be in STARTED state");
        require(block.timestamp <= _auctionObject.extendedEndDate_,"Auction end date reached");
        bool _doBid = true;        
        while (_doBid == true) {
            _doBid = false;
            for (uint x=0;x<=_auctionLots.length-1;x++) {
                for (uint i=0; i<=_bidderList.length-1;i++) {
                    // if the current iteration bidder has a maximun secret bid greater than auction current tranche and the bidder 
                    // is not the winner of te past tranch, the system pushes a bid in his name.
                    if (_validBidders[_bidderList[i]].lotSecretBid_[x] > 0 && _validBidders[_bidderList[i]].lotSecretBid_[x] >= _auctionLots[x].actualTrancheId_) {
                        if (_auctionLots[x].lastTrancheId_ == 0) {
                            _bid(_bidderList[i], x+1, 1);
                            _doBid = true;
                            break;
                        } else {
                            if ( _tranchesPerLot[x][_auctionLots[x].lastTrancheId_ -1].trancheBidder_ != _bidderList[i] ) {
                                _bid(_bidderList[i], x+1, _auctionLots[x].actualTrancheId_);
                                _doBid=true;
                                break;
                            }
                        }
                    } else {
                        if (_validBidders[_bidderList[i]].lotSecretBid_[x] >= _auctionLots[x].actualTrancheId_ &&
                            _bidderLotMSBBeaten[_bidderList[i]][_auctionLots[x].actualTrancheId_] == false) {
                            //Bidder's maximun secret bid has been beaten                            
                            _bidderLotMSBBeaten[_bidderList[i]][_auctionLots[x].actualTrancheId_] = true;
                            emit evt_maximunSecretBidBeaten(block.timestamp, _bidderList[i]);
                        }
                    }
                }
            }
        }
    }

    function _bid(address _bidder, uint _lotId, uint _bidTranche) internal {
        require(_auctionState == AuctionState.STARTED || _auctionState == AuctionState.EXTENDED ,"The auction MUST be in STARTED or EXTENDED state");
        require(block.timestamp <= _auctionObject.extendedEndDate_,"Auction end date reached");
        require(_tranchesPerLot[_lotId-1][_bidTranche-1].trancheConfirmed_ == false, "The tranche is already confirmed.");        
        require(_validBidders[_bidder].guaranteeDeposit_ > 0, "Message sender MUST be a valid bidder");
        if (_auctionLots[_lotId-1].lastTrancheId_ > 0) {
            require(_tranchesPerLot[_lotId-1][_auctionLots[_lotId-1].lastTrancheId_-1].trancheBidder_ != _bidder, "The bidder already has pushed the last valid bid");
        }
        require(_bidTranche == _auctionLots[_lotId-1].actualTrancheId_,"Invalid tranche");
        AuctionTranches memory _tmpTranche;
        
        // updates lot info
        _auctionLots[_lotId-1].lastTrancheId_ += 1;
        _auctionLots[_lotId-1].actualTrancheId_ += 1;

        
        // updates tranche info
        _tranchesPerLot[_lotId-1][_bidTranche-1].trancheBidder_ = _bidder;
        _tranchesPerLot[_lotId-1][_bidTranche-1].trancheConfirmed_ = true;
        _tranchesPerLot[_lotId-1][_bidTranche-1].trancheBidTimestamp_ = block.timestamp;

        // Init next tranche
        _tmpTranche.trancheId_ = _auctionLots[_lotId-1].actualTrancheId_;
        _tmpTranche.trancheValue_ = _getLotTrancheValue(_lotId,_auctionLots[_lotId-1].actualTrancheId_);
        _tmpTranche.trancheConfirmed_ = false;
        _tranchesPerLot[_lotId-1].push(_tmpTranche);

        // check extension period
        _extendAuction(_lotId);

        // generates events
        emit evt_bidConfirmed(block.timestamp, _lotId, _bidTranche, _bidder);
        
    }

    function _extendAuction(uint _lotId) internal {
        require(_auctionState == AuctionState.STARTED || _auctionState == AuctionState.EXTENDED ,"The auction MUST be in STARTED or EXTENDED state");
        require(block.timestamp <= _auctionObject.extendedEndDate_,"Auction end date reached");
        uint extensionPeriod = (_auctionLots[_lotId-1].extendedEndDate_ - 3 minutes);

        // the current bid should be in the last 3 minutes near the end to extend the auction.
        if (block.timestamp >= extensionPeriod) {
            _auctionLots[_lotId-1].extendedEndDate_ = ( _auctionLots[_lotId-1].endDate_ + 2 minutes);
            _auctionLots[_lotId-1].extensionsCount_ += 1;
            _auctionObject.extendedEndDate_ = ( _auctionLots[_lotId-1].endDate_ + 2 minutes);
            emit evt_auctionLotExtended(block.timestamp, _lotId, _auctionObject.extendedEndDate_);
        }
    } 
    

}
