#!/usr/bin/env python3
"""
Enhanced Genesis Block Generator for IndiCoin
Creates a proper genesis block with efficient mining
"""

import hashlib
import struct
import time
import os

def create_enhanced_genesis_block():
    """Create an enhanced genesis block for IndiCoin"""
    
    # IndiCoin parameters
    timestamp_msg = "The Times 03/Jan/2025 - IndiCoin: Controlled Inflation Digital Currency"
    nTime = int(time.time())
    nNonce = 0
    nBits = 0x1d00ffff  # Same difficulty as Bitcoin (compact format)
    genesis_reward = 50 * 100000000  # 50 INDI in satoshis
    
    # Genesis scriptPubKey - public key for coinbase (same as Bitcoin for now)
    genesis_pubkey = "04678afdb0fe5548271967f1a67130b7105cd6a828e03909a67962e0ea1f61deb649f6bc3f4cef38c4f35504e51ec112de5c384df7ba0b8d578a4c702b6bf11d5f"
    
    print("=" * 60)
    print("🏗️  INDICOIN GENESIS BLOCK GENERATOR")
    print("=" * 60)
    print(f"📅 Block Time: {nTime}")
    print(f"📝 Message: {timestamp_msg}")
    print(f"🎯 Target Difficulty: 0x{nBits:08x}")
    print(f"💰 Genesis Reward: {genesis_reward:,} satoshis ({genesis_reward/100000000:.1f} INDI)")
    print()
    
    # Create block header components
    version = struct.pack('<I', 1)
    hashPrevBlock = bytes.fromhex('0000000000000000000000000000000000000000000000000000000000000000')
    
    # Create coinbase transaction
    coinbase_tx = create_coinbase_transaction(timestamp_msg, genesis_reward)
    merkle_root = coinbase_tx['txid']  # It's already a string
    
    # Target calculation for difficulty 1
    target = (1 << (256 - 32)) - 1  # Difficulty 1 target
    
    print(f"🔍 Starting genesis block mining...")
    print(f"🎯 Target: {target:x}")
    print()
    
    # Try different nonces until we find one that works
    for nonce in range(5000000):  # Try 5 million nonces
        if nonce % 100000 == 0:
            print(f"⏱️  Tried {nonce:,} nonces...")
        
        # Create block header
        nTime_bytes = struct.pack('<I', nTime)
        nBits_bytes = struct.pack('<I', nBits)
        nNonce_bytes = struct.pack('<I', nonce)
        merkle_root_bytes = bytes.fromhex(merkle_root)
        
        header = version + hashPrevBlock + merkle_root_bytes + nTime_bytes + nBits_bytes + nNonce_bytes
        
        # Calculate double SHA256 hash
        hash1 = hashlib.sha256(header).digest()
        hash2 = hashlib.sha256(hash1).digest()
        block_hash = hash2.hex()
        
        # Check if hash meets difficulty target
        hash_int = int(block_hash, 16)
        if hash_int < target:
            print()
            print("🎉 GENESIS BLOCK FOUND!")
            print("=" * 60)
            print(f"🔢 Nonce: {nonce:,}")
            print(f"🏷️  Block Hash: {block_hash}")
            print(f"🌳 Merkle Root: {merkle_root}")
            print(f"⏰ Timestamp: {nTime}")
            print(f"🎯 Difficulty: 0x{nBits:08x}")
            print()
            
            # Generate C++ code for chainparams.cpp
            print("📝 C++ CODE FOR chainparams.cpp:")
            print("=" * 60)
            print("genesis = CreateGenesisBlock(")
            print(f"    \"{timestamp_msg}\", // timestamp")
            print(f"    CScript() << \"{genesis_pubkey}\" << OP_CHECKSIG, // scriptPubKey")
            print(f"    {nTime}, // nTime")
            print(f"    {nonce}, // nNonce")
            print(f"    0x{nBits:08x}, // nBits")
            print("    1, // nVersion")
            print(f"    {genesis_reward} * COIN); // genesisReward")
            print()
            print("consensus.hashGenesisBlock = genesis.GetHash();")
            print(f"assert(consensus.hashGenesisBlock == uint256{{\"{block_hash}\"}});")
            print(f"assert(genesis.hashMerkleRoot == uint256{{\"{merkle_root}\"}});")
            print()
            
            # Save to file
            with open('/workspace/IndiCoin/genesis_results.txt', 'w') as f:
                f.write("IndiCoin Genesis Block Parameters\n")
                f.write("=" * 40 + "\n\n")
                f.write(f"Timestamp: {nTime}\n")
                f.write(f"Nonce: {nonce}\n")
                f.write(f"Block Hash: {block_hash}\n")
                f.write(f"Merkle Root: {merkle_root}\n")
                f.write(f"Bits: 0x{nBits:08x}\n")
                f.write(f"Genesis Reward: {genesis_reward} satoshis\n\n")
                f.write("C++ Code:\n")
                f.write("genesis = CreateGenesisBlock(\n")
                f.write(f"    \"{timestamp_msg}\",\n")
                f.write(f"    CScript() << \"{genesis_pubkey}\" << OP_CHECKSIG,\n")
                f.write(f"    {nTime},\n")
                f.write(f"    {nonce},\n")
                f.write(f"    0x{nBits:08x},\n")
                f.write("    1,\n")
                f.write(f"    {genesis_reward} * COIN);\n\n")
                f.write(f"consensus.hashGenesisBlock = genesis.GetHash();\n")
                f.write(f"assert(consensus.hashGenesisBlock == uint256{{\"{block_hash}\"}});\n")
                f.write(f"assert(genesis.hashMerkleRoot == uint256{{\"{merkle_root}\"}});\n")
            
            print(f"💾 Results saved to: /workspace/IndiCoin/genesis_results.txt")
            return {
                'hash': block_hash,
                'merkle_root': merkle_root,
                'nonce': nonce,
                'time': nTime,
                'bits': nBits,
                'reward': genesis_reward,
                'timestamp_msg': timestamp_msg,
                'pubkey': genesis_pubkey
            }
    
    print("❌ Failed to find valid genesis block in search range")
    return None

def create_coinbase_transaction(timestamp_msg, reward_satoshis):
    """Create the genesis coinbase transaction"""
    
    # Create a deterministic but unique coinbase script
    coinbase_script = create_coinbase_script_sig(timestamp_msg)
    
    # Create simplified transaction for merkle calculation
    # For genesis block, we'll use a simplified but valid structure
    
    # Hash the coinbase script to create a deterministic txid
    script_hash = hashlib.sha256(coinbase_script).digest()
    txid = script_hash.hex()
    
    print(f"🔨 Coinbase Script: {coinbase_script.hex()}")
    print(f"🆔 Transaction ID: {txid}")
    
    return {
        'txid': txid,
        'coinbase_script': coinbase_script
    }

def create_coinbase_script_sig(timestamp_msg):
    """Create the coinbase script signature"""
    # Coinbase script format compatible with Bitcoin
    script = b'\x04\xff\xff\x00\x1d\x01\x04'  # Bitcoin's signature bytes
    
    # Add block height (0 for genesis)
    script += struct.pack('<I', 0)  # Block height = 0
    
    # Add timestamp message
    script += timestamp_msg.encode('utf-8')
    
    return script

if __name__ == "__main__":
    result = create_enhanced_genesis_block()
    if result:
        print()
        print("✅ Genesis block generation completed successfully!")
        print("🚀 IndiCoin is ready for its own genesis block!")
    else:
        print()
        print("❌ Genesis block generation failed")
