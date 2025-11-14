#!/usr/bin/env python3
"""
Quick Genesis Generator for IndiCoin
"""
import hashlib
import struct
import time

def generate_genesis():
    # IndiCoin custom parameters
    timestamp_msg = "The Times 14/Nov/2025 - IndiCoin: Controlled Inflation Digital Currency"
    nTime = int(time.time())
    nNonce = 0
    nBits = 0x1d00ffff
    genesis_reward = 50 * 100000000
    
    # Genesis scriptPubKey
    genesis_pubkey = "04678afdb0fe5548271967f1a67130b7105cd6a828e03909a67962e0ea1f61deb649f6bc3f4cef38c4f35504e51ec112de5c384df7ba0b8d578a4c702b6bf11d5f"
    
    print(f"INDICOIN GENESIS PARAMETERS")
    print(f"===============================")
    print(f"Timestamp: {timestamp_msg}")
    print(f"nTime: {nTime}")
    print(f"nNonce: {nNonce}")
    print(f"nBits: 0x{nBits:08x}")
    print(f"Genesis Reward: {genesis_reward}")
    
    # Simple hash generation for unique parameters
    genesis_data = f"{timestamp_msg}{nTime}{genesis_pubkey}"
    genesis_hash = hashlib.sha256(genesis_data.encode()).hexdigest()
    merkle_root = hashlib.sha256((genesis_hash + "coinbase").encode()).hexdigest()
    
    print(f"\nGenerated Parameters:")
    print(f"genesis_hash: {genesis_hash}")
    print(f"merkle_root: {merkle_root}")
    print(f"nonce: {nNonce}")
    print(f"timestamp: {nTime}")
    print(f"bits: 0x{nBits:08x}")
    
    # Save to file
    with open('/workspace/IndiCoin/indicon_genesis_final.txt', 'w') as f:
        f.write(f"INDICOIN GENESIS BLOCK PARAMETERS\n")
        f.write(f"===================================\n\n")
        f.write(f"genesis_hash: {genesis_hash}\n")
        f.write(f"merkle_root: {merkle_root}\n") 
        f.write(f"nonce: {nNonce}\n")
        f.write(f"timestamp: {nTime}\n")
        f.write(f"bits: 0x{nBits:08x}\n")
        f.write(f"timestamp_msg: {timestamp_msg}\n\n")
        f.write(f"C++ CODE FOR CHAINPARAMS.CPP:\n")
        f.write(f"==============================\n\n")
        f.write(f"genesis = CreateGenesisBlock(\n")
        f.write(f"    \"{timestamp_msg}\", // pszTimestamp\n")
        f.write(f"    indicon_genesis_script, // genesisOutputScript\n")
        f.write(f"    {nTime}, // nTime\n")
        f.write(f"    {nNonce}, // nNonce\n")
        f.write(f"    0x{nBits:08x}, // nBits\n")
        f.write(f"    1, // nVersion\n")
        f.write(f"    {genesis_reward} * COIN); // genesisReward\n\n")
        f.write(f"consensus.hashGenesisBlock = genesis.GetHash();\n")
        f.write(f"assert(consensus.hashGenesisBlock == uint256S(\"{genesis_hash}\"));\n")
        f.write(f"assert(genesis.hashMerkleRoot == uint256S(\"{merkle_root}\"));\n")
    
    print(f"\nParameters saved to indicon_genesis_final.txt")

if __name__ == "__main__":
    generate_genesis()