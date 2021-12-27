const SubastasSCBA = artifacts.require("AuctionsSCBA");
const JUSToken = artifacts.require("JUSToken");

module.exports = async function (deployer) {
  await deployer.deploy(JUSToken,10000000);
  const token = await JUSToken.deployed();
  await deployer.deploy(SubastasSCBA,token.address);
};
