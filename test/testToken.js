var assert = require('assert');
const web3 = global.web3;
const auctionContract = artifacts.require("AuctionsSCBA");
const jusContract = artifacts.require("JUSToken");

var auctionStartDate = new Date().getTime();
var auctionStartDateTimeStamp = Math.floor(auctionStartDate / 1000) + 40
var auctionEndDateTimeStamp = auctionStartDateTimeStamp + 120

contract('auctionContract', (accounts) => {
    let instance;
    beforeEach('should setup the contract instance', async () => {
        instance = await auctionContract.deployed();
        token = await jusContract.deployed();
    });
    it("Check JUSToken Balance", async ()=> {    
        let balance;
        balance = await token.balanceOf(instance.address);
        console.log(web3.utils.fromWei(balance));
        balance = web3.utils.BN(await token.balanceOf(accounts[0]));
        console.log(web3.utils.fromWei(balance));
        balance = web3.utils.BN(await token.balanceOf(accounts[1]));
        console.log(web3.utils.fromWei(balance));
        balance = web3.utils.BN(await token.balanceOf(accounts[2]));
        console.log(web3.utils.fromWei(balance));
        balance = web3.utils.BN(await token.balanceOf(accounts[3]));
        console.log(web3.utils.fromWei(balance));
        balance = web3.utils.BN(await token.balanceOf(accounts[4]));
        console.log(web3.utils.fromWei(balance));
    });    
    it("Transfer JUSTokens to bidders", async ()=> {    
        await token.transfer.sendTransaction(accounts[1],web3.utils.toWei(web3.utils.toBN(100)),{from : accounts[0]});
        await token.transfer.sendTransaction(accounts[2],web3.utils.toWei(web3.utils.toBN(100)),{from : accounts[0]});
        await token.transfer.sendTransaction(accounts[3],web3.utils.toWei(web3.utils.toBN(100)),{from : accounts[0]});
        await token.transfer.sendTransaction(accounts[4],web3.utils.toWei(web3.utils.toBN(100)),{from : accounts[0]});
    });    
    it("Check JUSToken Balance", async ()=> {    
        let balance;
        balance = await token.balanceOf(token.address);
        console.log(web3.utils.fromWei(balance));
        balance = web3.utils.BN(await token.balanceOf(accounts[0]));
        console.log(web3.utils.fromWei(balance));
        balance = web3.utils.BN(await token.balanceOf(accounts[1]));
        console.log(web3.utils.fromWei(balance));
        balance = web3.utils.BN(await token.balanceOf(accounts[2]));
        console.log(web3.utils.fromWei(balance));
        balance = web3.utils.BN(await token.balanceOf(accounts[3]));
        console.log(web3.utils.fromWei(balance));
        balance = web3.utils.BN(await token.balanceOf(accounts[4]));
        console.log(web3.utils.fromWei(balance)); 
    });    
    it("Bidders approve to auction contrat", async ()=> {    
        await token.approve.sendTransaction(instance.address,web3.utils.toWei(web3.utils.toBN(100)),{from : accounts[1]});
        await token.approve.sendTransaction(instance.address,web3.utils.toWei(web3.utils.toBN(100)),{from : accounts[2]});
        await token.approve.sendTransaction(instance.address,web3.utils.toWei(web3.utils.toBN(100)),{from : accounts[3]});
        await token.approve.sendTransaction(instance.address,web3.utils.toWei(web3.utils.toBN(100)),{from : accounts[4]});
    });        
    it("Check allowances", async ()=> {    
        let x;
        x = await token.allowance(accounts[1],instance.address);
        console.log(web3.utils.fromWei(x)); 
        x = await token.allowance(accounts[2],instance.address);
        console.log(web3.utils.fromWei(x)); 
        x = await token.allowance(accounts[3],instance.address);
        console.log(web3.utils.fromWei(x)); 
        x = await token.allowance(accounts[4],instance.address);
        console.log(web3.utils.fromWei(x)); 

    });        

    it("Check JUSToken Balance", async ()=> {    
        let balance;
        balance = await token.balanceOf(instance.address);
        console.log(web3.utils.fromWei(balance));
        balance = web3.utils.BN(await token.balanceOf(accounts[0]));
        console.log(web3.utils.fromWei(balance));
        balance = web3.utils.BN(await token.balanceOf(accounts[1]));
        console.log(web3.utils.fromWei(balance));
        balance = web3.utils.BN(await token.balanceOf(accounts[2]));
        console.log(web3.utils.fromWei(balance));
        balance = web3.utils.BN(await token.balanceOf(accounts[3]));
        console.log(web3.utils.fromWei(balance));
        balance = web3.utils.BN(await token.balanceOf(accounts[4]));
        console.log(web3.utils.fromWei(balance)); 
    });    

});
  
