var assert = require('assert');
const web3 = global.web3;
const auctionContract = artifacts.require("AuctionsSCBA");

var auctionStartDate = new Date().getTime();
var auctionStartDateTimeStamp = Math.floor(auctionStartDate / 1000) + 40
var auctionEndDateTimeStamp = auctionStartDateTimeStamp + 120

console.log(auctionStartDateTimeStamp)
console.log(auctionEndDateTimeStamp)
contract('auctionContract', (accounts) => {
    let instance;
    beforeEach('should setup the contract instance', async () => {
        instance = await auctionContract.deployed();
    });
    it("should initialize a new auction", async ()=> {
        await instance.auctionInit("MP151",0,web3.utils.toWei(web3.utils.toBN(5)),1,auctionStartDateTimeStamp,auctionEndDateTimeStamp);
        const valueState = await  instance.getAuctionState()
        assert.equal(valueState.toNumber(),1);

      });
      it("should define a new lot", async ()=> {
        await instance.auctionAddLot(web3.utils.toWei(web3.utils.toBN(10)));
        const valueState = await  instance.getAuctionState()
        assert.equal(valueState.toNumber(),2);
      });
      it("should test auction get data functions", async ()=> {
        var auctionClass = await  instance.getAuctionClass()
        assert.equal(await instance.getAuctionStartDate(),auctionStartDateTimeStamp)
        assert.equal(await instance.getAuctionEndtDate(),auctionEndDateTimeStamp)
        assert.equal(auctionClass.toNumber(),0)
      });

      it("should confirm bidder 1 inscription", async ()=> {
        await instance.confirmBidderInscription.sendTransaction(true,{from : accounts[1],value: web3.utils.toWei(web3.utils.toBN(10)) });
        var confirmedBidders = await instance.getConfirmedBiddders();
        assert.equal(confirmedBidders.toNumber(),1)
        var testInscription = await instance.isBidderConfirmed(accounts[1]);
        assert.equal(testInscription,true);
      });
      it("should confirm bidder 2 inscription", async ()=> {
        await instance.confirmBidderInscription.sendTransaction(true,{from : accounts[2],value: web3.utils.toWei(web3.utils.toBN(10)) });
        var confirmedBidders = await instance.getConfirmedBiddders();
        assert.equal(confirmedBidders.toNumber(),2)
        var testInscription = await instance.isBidderConfirmed(accounts[2]);
        assert.equal(testInscription,true);
      });
      it("should confirm bidder 3 inscription", async ()=> {
        await instance.confirmBidderInscription.sendTransaction(false,{from : accounts[3],value: web3.utils.toWei(web3.utils.toBN(10)) });
        var confirmedBidders = await instance.getConfirmedBiddders();
        assert.equal(confirmedBidders.toNumber(),3)
        var testInscription = await instance.isBidderConfirmed(accounts[3]);
        assert.equal(testInscription,true);
      });
      it("should confirm bidder 4 inscription", async ()=> {
        await instance.confirmBidderInscription.sendTransaction(false,{from : accounts[4],value: web3.utils.toWei(web3.utils.toBN(10)) });
        var confirmedBidders = await instance.getConfirmedBiddders();
        assert.equal(confirmedBidders.toNumber(),4)
        var testInscription = await instance.isBidderConfirmed(accounts[4]);
        assert.equal(testInscription,true);
      });
      it("should verify unconfirmed bidder inscription", async ()=> {
        var testInscription = await instance.isBidderConfirmed(accounts[5]);
        assert.equal(testInscription,false);
      });
      it("should verify correct contract balance in 40 ether", async ()=> {
        var auctionBalance = await instance.getAuctionBalance();
        assert.equal(web3.utils.fromWei(web3.utils.BN(auctionBalance)),40);
      });
      it("should verify confirmed bidders quantity", async ()=> {
        var confirmedBidders = await instance.getConfirmedBiddders();
        assert.equal(confirmedBidders.toNumber(),4);
      });
      it("should set bidder 1 maximun secret bid in 14 ethers", async ()=> {
        await instance.bidderSetMaximunSecretBidAmount.sendTransaction(1,web3.utils.toWei(web3.utils.toBN(14)),{from : accounts[1]});
        let secretBid = await instance.getBidderMaximunSecretBid(1,accounts[1]);
        assert.equal(web3.utils.BN(secretBid[0]),8);
        assert.equal(web3.utils.fromWei(web3.utils.BN(secretBid[1])),14)
      });
      it("should set bidder 2 maximun secret bid in 12 tranche", async ()=> {
        await instance.bidderSetMaximunSecretBidTranche.sendTransaction(1,12,{from : accounts[2]});
        let secretBid = await instance.getBidderMaximunSecretBid(1,accounts[2]);
        assert.equal(web3.utils.BN(secretBid[0]),12);
      });
      it("should set bidder 4 maximun secret bid in 13 ethers", async ()=> {
        await instance.bidderSetMaximunSecretBidAmount.sendTransaction(1,web3.utils.toWei(web3.utils.toBN(13)),{from : accounts[4]});
        let secretBid = await instance.getBidderMaximunSecretBid(1,accounts[4]);
        assert.equal(web3.utils.BN(secretBid[0]),6);
      });
      it("should check lots quantity", async ()=> {
        var lots = web3.utils.BN(await instance.getLotQuantity());
        assert.equal(lots, 1);
      });
      it("should check lots base value", async ()=> {
        var varBase = web3.utils.fromWei(web3.utils.BN(await instance.getLotBaseValue(1)));
        assert.equal(varBase, 10);
      });
      it("should check lots tranch 9 value", async ()=> {
        var varBase = web3.utils.fromWei(web3.utils.BN(await instance.getLotTrancheValue(1,9)));
        assert.equal(varBase, 14.5);
      });
      it("should start auction process at defined time", async ()=> {
        let looping = true;
        while (looping) {
          var auctionDate = new Date().getTime();
          var auctionDateTimeStamp = Math.floor(auctionDate / 1000) 
          if (auctionDateTimeStamp > auctionStartDateTimeStamp) {
            await instance.auctionStart();
            looping = false;
          }
        }
        const valueState = await instance.getAuctionState();
        assert.equal(valueState.toNumber(),3);
      });
      it("Check last tranche after initial automatic push", async ()=> {
        let retValue = await instance.getActualTranche(1);
        assert(web3.utils.BN(retValue[0]),9);
      });
      it("Bidder 1 bid tranche 9", async ()=> {
        await instance.bid.sendTransaction(1,9,{from : accounts[1]});
      });
      it("Bidder 3 bid tranche 11", async ()=> {
        await instance.bid.sendTransaction(1,11,{from : accounts[3]});
      });
      it("Bidder 1 bid tranche 13", async ()=> {
        await instance.bid.sendTransaction(1,13,{from : accounts[1]});
      });
      it("Bidder 2 bid tranche 14", async ()=> {
        await instance.bid.sendTransaction(1,14,{from : accounts[2]});
      });
      it("Bidder 4 bid tranche 15", async ()=> {
        await instance.bid.sendTransaction(1,15,{from : accounts[4]});
      });
      it("Check last tranche after manual push", async ()=> {
        let retValue = await instance.getActualTranche(1);
        assert(web3.utils.BN(retValue[0]),16);
      });
      it("Chek extended enddate", async ()=> {
        assert(web3.utils.BN(await instance.getLotExtensionCount(1)),1);
      });
      it("delayed push bidder 1 tranche 16 for second auction extension", async ()=> {
        let looping = true;
        while (looping) {
          var auctionDate = new Date().getTime();
          var auctionDateTimeStamp = Math.floor(auctionDate / 1000) 
          if (auctionDateTimeStamp > auctionEndDateTimeStamp - 10) {
            await instance.bid.sendTransaction(1,16,{from : accounts[1]});
            looping = false;
          }
        }
      });
      it("Chek extended enddate", async ()=> {
        assert(web3.utils.BN(await instance.getLotExtensionCount(1)),2);
      });  
      it("should close the auction", async ()=> {
        let looping = true;
        while (looping) {
          var auctionDate = new Date().getTime();
          var auctionDateTimeStamp = Math.floor(auctionDate / 1000) 
          if (auctionDateTimeStamp >= auctionEndDateTimeStamp + 125) {
            await instance.auctionClose();
            looping = false;
          }
        }
      });
      it("should withdraw founds for bidder 3", async ()=> {
        await instance.withDraw.sendTransaction({from : accounts[3]});
      });
      it("should withdraw founds for bidder 4", async ()=> {
        await instance.withDraw.sendTransaction({from : accounts[4]});
      });
      it("should withdraw founds for bidder 1", async ()=> {
        await instance.withDraw.sendTransaction({from : accounts[1]});
      });
      it("should enable withdraw founds for bidder 1", ()=> {
        instance.enableWithDraw(accounts[1]);
      });
      it("should enable withdraw founds for bidder 2", ()=> {
         instance.enableWithDraw(accounts[2]);
      });
      it("should withdraw founds for bidder 1", async ()=> {
        await instance.withDraw.sendTransaction({from : accounts[1]});
      });
      it("should withdraw founds for bidder 2", async ()=> {
        await instance.withDraw.sendTransaction({from : accounts[2]});
      });

  });
