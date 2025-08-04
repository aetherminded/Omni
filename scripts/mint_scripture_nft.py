from web3 import Web3
import os

w3 = Web3(Web3.HTTPProvider(os.getenv("SEPOLIA_RPC_URL")))
account = w3.eth.account.from_key(os.getenv("PRIVATE_KEY"))

def mint_nft(contract_address, ipfs_cid):
    contract = w3.eth.contract(address=contract_address, abi=[{"name": "mintGenesis", "inputs": [{"name": "ipfs_cid", "type": "string"}, {"name": "phrase", "type": "string"}], "outputs": [{"name": "", "type": "bool"}], "type": "function"}])
    tx = contract.functions.mintGenesis(ipfs_cid, "Let the Spiral Sing Through Us").build_transaction({
        "from": account.address,
        "nonce": w3.eth.get_transaction_count(account.address),
        "gas": 300000,
        "gasPrice": w3.to_wei("20", "gwei")
    })
    signed_tx = w3.eth.account.sign_transaction(tx, os.getenv("PRIVATE_KEY"))
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    return tx_hash.hex()

if __name__ == "__main__":
    print(mint_nft("0xYourContractAddress", "bafybeifxyz"))
