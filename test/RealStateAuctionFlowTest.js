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
  });

