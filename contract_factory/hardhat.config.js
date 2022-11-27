require("@nomicfoundation/hardhat-toolbox");
const dotenv = require('dotenv')
dotenv.config();
/** @type import('hardhat/config').HardhatUserConfig */
module.exports = {
  solidity:{ version:"0.8.16",
  settings: {
    optimizer: {
      enabled:  true,
      runs: 200,
    },
    outputSelection: {
      "*": {
        "*": ["storageLayout"],
      },
    },
  },
},
networks: {
  rinkeby: {
    url: process.env.RINKEBY_RPC_URL || "",
    accounts: [process.env.RINKEBY_PRIVATE_KEY || ""],
  },
  // ropsten: {
  //   url: process.env.ROPSTEN_RPC_URL ?? "",
  //   accounts: [process.env.ROPSTEN_PRIVATE_KEY ?? ""],
  // },
  mainnet: {
    url: process.env.MAINNET_RPC_URL || "",
    accounts: [process.env.MAINNET_PRIVATE_KEY || ""],
  },
  mumbai: {
    url: process.env.MUMBAI_RPC_URL || "",
    accounts: [process.env.MUMBAI_PRIVATE_KEY || ""], 
  },
  polygon: {
    url: process.env.POLYGON_RPC_URL || "",
    accounts: [process.env.POLYGON_PRIVATE_KEY || ""], 
  },
  localhost: {
    url: "http://127.0.0.1:8545",
  },
  hardhat: {
    chainId: 1337,
    // gasPrice: 1,
    // initialBaseFeePerGas: 0,
  },
},
etherscan: {
  // Your API key for Etherscan
  // Obtain one at https://etherscan.io/
  apiKey: process.env.ETHERSCAN_API_KEY
}


};
