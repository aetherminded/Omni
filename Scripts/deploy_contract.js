require("dotenv").config();
const hre = require("hardhat");

async function main() {
  const GenesisSigil = await hre.ethers.getContractFactory("GenesisSigil");
  const contract = await GenesisSigil.deploy();
  await contract.deployed();
  console.log("Deployed to:", contract.address);
}

main().catch(console.error);
