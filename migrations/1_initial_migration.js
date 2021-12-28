const web3 = global.web3;
const SubastasSCBA = artifacts.require("AuctionsSCBA");
const JUSToken = artifacts.require("JUSToken");

module.exports = async function (deployer) {
  await deployer.deploy(JUSToken);
  const token = await JUSToken.deployed();
  await deployer.deploy(SubastasSCBA,token.address);
};
