const SubastasSCBA = artifacts.require("AuctionsSCBA");

module.exports = function (deployer) {
  deployer.deploy(SubastasSCBA);
};
