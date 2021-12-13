var assert = require('assert');
const web3 = global.web3;
const auctionContract = artifacts.require("AuctionsSCBA");

var auctionStartDate = new Date('2021/12/14').getTime() / 1000; //secs
var auctionEndDate = new Date('2021/12/24').getTime() / 1000; //secs
contract('auctionContract', (accounts) => {
    let instance;
    beforeEach('should setup the contract instance', async () => {
        instance = await auctionContract.deployed();
    });
    it("should initialize a new auction", async ()=> {
        await instance.auctionInit("MP151",0,100,1,auctionStartDate,auctionEndDate);
        const valueState = await  instance.getAuctionState()
        assert.equal(valueState.toNumber(),1);

      });
      it("should define a new lot", async ()=> {
        await instance.auctionAddLot(200);
        const valueState = await  instance.getAuctionState()
        assert.equal(valueState.toNumber(),2);
      });
      it("should test auction get data functions", async ()=> {
        var auctionClass = await  instance.getAuctionClass()
        assert.equal(await instance.getAuctionStartDate(),auctionStartDate)
        assert.equal(await instance.getAuctionEndtDate(),auctionEndDate)
        assert.equal(auctionClass.toNumber(),0)
      });

      it("should confirm bidder 1 inscription", async ()=> {
        await instance.confirmBidderInscription.sendTransaction(true,{from : accounts[1],value: web3.utils.toWei(web3.utils.toBN(1)) });
        var confirmedBidders = await instance.getConfirmedBiddders();
        assert.equal(confirmedBidders.toNumber(),1)
        var testInscription = await instance.isBidderConfirmed(accounts[1]);
        assert.equal(testInscription,true);
      });
      it("should confirm bidder 2 inscription", async ()=> {
        await instance.confirmBidderInscription.sendTransaction(true,{from : accounts[2],value: web3.utils.toWei(web3.utils.toBN(1)) });
        var confirmedBidders = await instance.getConfirmedBiddders();
        assert.equal(confirmedBidders.toNumber(),2)
        var testInscription = await instance.isBidderConfirmed(accounts[2]);
        assert.equal(testInscription,true);
      });
      it("should confirm bidder 3 inscription", async ()=> {
        await instance.confirmBidderInscription.sendTransaction(false,{from : accounts[3],value: web3.utils.toWei(web3.utils.toBN(1)) });
        var confirmedBidders = await instance.getConfirmedBiddders();
        assert.equal(confirmedBidders.toNumber(),3)
        var testInscription = await instance.isBidderConfirmed(accounts[3]);
        assert.equal(testInscription,true);
      });
      it("should confirm bidder 4 inscription", async ()=> {
        await instance.confirmBidderInscription.sendTransaction(false,{from : accounts[4],value: web3.utils.toWei(web3.utils.toBN(1)) });
        var confirmedBidders = await instance.getConfirmedBiddders();
        assert.equal(confirmedBidders.toNumber(),4)
        var testInscription = await instance.isBidderConfirmed(accounts[4]);
        assert.equal(testInscription,true);
      });
      it("should verify unconfirmed bidder inscription", async ()=> {
        var testInscription = await instance.isBidderConfirmed(accounts[5]);
        assert.equal(testInscription,false);
      });
      it("should verify correct contract balance", async ()=> {
        var auctionBalance = await instance.getAuctionBalance();
        assert.equal(web3.utils.fromWei(web3.utils.BN(auctionBalance)),4);
      });
      it("should verify confirmed bidders quantity", async ()=> {
        var confirmedBidders = await instance.getConfirmedBiddders();
        assert.equal(confirmedBidders.toNumber(),4);
      });
  });

