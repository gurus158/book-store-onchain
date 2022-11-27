// We require the Hardhat Runtime Environment explicitly here. This is optional
// but useful for running the script in a standalone fashion through `node <script>`.
//
// You can also run a script with `npx hardhat run <script>`. If you do that, Hardhat
// will compile your contracts, add the Hardhat Runtime Environment's members to the
// global scope, and execute the script.
const hre = require("hardhat");

async function main() {
  const BookStore = await hre.ethers.getContractFactory("BookStore");
  const bookStore = await BookStore.deploy('0x4b202D403bb4C4354F1b30066B05D2E610bC9e65','Book Store','BSOC');

  await bookStore.deployed();

  console.log(
    `BookStore deployed to ${bookStore.address}`
  );
}

// We recommend this pattern to be able to use async/await everywhere
// and properly handle errors.
main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
