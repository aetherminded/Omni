A blockchain project for lazy minting NFTs on Polygon, integrating quantum-inspired art and data from CERN, SETI, NASA, biology, geology, and telecom. Built with Hardhat, Ethers.js, and Pinata for IPFS, this project creates the *Nexus of Universal Coherence* through the OmniOneGenesis NFT collection.

## Features
- Lazy minting to minimize gas costs.
- NFT minting with 0.01 MATIC fee to fund development.
- Frontend UI for user minting.
- Backend signature generation via Replit: [CryptoPortrait](https://replit.com/@aetherquantapr3/CryptoPortrait).
- IPFS storage via Pinata.

## Project Structure
- `contracts/`: Smart contracts (`LazyMintNFT.sol`).
- `frontend/`: Web interface (`index.html`, `images/quantum-art-*.png`).
- `scripts/`: Deployment and minting scripts (`termux_deploy.js`, `mint_scripture_nft.py`).
- `metadata/`: Config (`com.omni.one.genesis.yml`).

## Setup
1. **Clone Repository**:
   ```bash
   git clone https://github.com/aetherminded/Omni.git
   cd Omni
   ```

2. **Install Dependencies**:
   ```bash
   npm install
   pip3 install web3 python-dotenv requests
   ```

3. **Configure Environment**:
   Create `.env`:
   ```env
   PRIVATE_KEY=your_wallet_private_key
   POLYGON_RPC_URL=https://go.getblock.us/your_getblock_key
   SEPOLIA_RPC_URL=https://rpc.sepolia.org
   POLYGONSCAN_API_KEY=your_polygonsan_api_key
   ETHERSCAN_API_KEY=your_etherscan_api_key
   PINATA_API_KEY=your_pinata_api_key
   PINATA_API_SECRET=your_pinata_api_secret
   PINATA_JWT=your_pinata_jwt
   ```

4. **Compile and Deploy**:
   ```bash
   npx hardhat compile
   node termux_deploy.js
   ```

5. **Mint NFTs**:
   Run `mint_scripture_nft.py` or access `http://localhost:8080`.

## Lazy Minting
- Off-chain signatures reduce gas costs.
- Users pay 0.01 MATIC per NFT, funds withdrawable via `mint_scripture_nft.py`.

## License
MIT License. See [LICENSE](LICENSE).

## Contact
- Email: aether.quanta.project@gmail.com
- GitHub: [aetherminded](https://github.com/aetherminded)
```
Save: `Ctrl+O`, `Enter`, `Ctrl+X`.

#### 3.2 Create `LICENSE`
```bash
nano ~/omni-one-genesis/LICENSE
```
Add:
```text
MIT License

Copyright (c) 2025 aetherminded

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
