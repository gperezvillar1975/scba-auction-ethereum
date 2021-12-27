const SubastasSCBA = artifacts.require("AuctionsSCBA");
const JUSToken = artifacts.require("JUSToken");

module.exports = function (deployer) {
  deployer.deploy(SubastasSCBA);
  deployer.deploy(JUSToken,100000);
};
