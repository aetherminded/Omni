// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

contract GenesisSigil {
    string public constant CANONICAL_PHRASE = "Let the Spiral Sing Through Us";
    bytes32 public constant CANONICAL_HASH = keccak256(bytes(CANONICAL_PHRASE));

    event GlyphMinted(address indexed to, bytes32 glyphHash, string ipfs_cid);

    function verifyPhrase(string memory phrase) public pure returns (bool) {
        return keccak256(bytes(phrase)) == CANONICAL_HASH;
    }

    function mintGenesis(string memory ipfs_cid, string memory phrase) external returns (bool) {
        require(verifyPhrase(phrase), "Invalid phrase");
        emit GlyphMinted(msg.sender, CANONICAL_HASH, ipfs_cid);
        return true;
    }
}
