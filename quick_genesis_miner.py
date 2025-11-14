#!/usr/bin/env python3
"""
Quick Genesis Block Generator for IndiCoin - Simplified Version
Generates genesis parameters efficiently
"""

import hashlib
import struct
import time

def quick_genesis_miner():
    """Generate IndiCoin genesis block with moderate difficulty"""
    
    # Use a more reasonable target for faster mining
    nTime = int(time.time())
    nBits = 0x1fffff00  # Lower difficulty for faster mining
    genesis_reward = 50 * 100000000  # 50 INDI
    
    print("🏗️  IndiCoin Genesis Block Mining (Simplified)")
    print("=" * 50)
    print(f"⏰ Time: {nTime}")
    print(f"🎯 Difficulty: 0x{nBits:08x}")
    print(f"💰 Reward: {genesis_reward/100000000:.1f} INDI")
    print()
    
    # Simple merkle root (will be replaced later)
    merkle_root = "4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b"
    
    # Target calculation
    target = (1 << (256 - nBits.bit_length() + 1)) - 1
    
    print(f"🔍 Mining with target: {target:x}")
    
    # Try many nonces
    for nonce in range(1000000):
        if nonce % 50000 == 0:
            print(f"⏱️  Tried {nonce:,} nonces...")
        
        # Create block header
        version = struct.pack('<I', 1)
        prev_hash = bytes.fromhex('0000000000000000000000000000000000000000000000000000000000000000')
        merkle_bytes = bytes.fromhex(merkle_root)
        nTime_bytes = struct.pack('<I', nTime)
        nBits_bytes = struct.pack('<I', nBits)
        nNonce_bytes = struct.pack('<I', nonce)
        
        header = version + prev_hash + merkle_bytes + nTime_bytes + nBits_bytes + nNonce_bytes
        
        # Calculate hash
        hash1 = hashlib.sha256(header).digest()
        hash2 = hashlib.sha256(hash1).digest()
        block_hash = hash2.hex()
        
        # Check if found
        hash_int = int(block_hash, 16)
        if hash_int < target:
            print(f"\n🎉 GENESIS BLOCK FOUND!")
            print(f"Nonce: {nonce:,}")
            print(f"Hash: {block_hash}")
            
            # Generate C++ parameters
            print("\n📝 C++ Parameters:")
            print("genesis = CreateGenesisBlock(")
            print(f'    "{nTime}",  // nTime')
            print(f"    {nonce},    // nNonce")
            print(f"    0x{nBits:08x}, // nBits")
            print("    1,         // nVersion")
            print(f"    {genesis_reward} * COIN); // genesisReward")
            
            # Save to file
            with open('/workspace/IndiCoin/indicon_genesis_block_params.txt', 'w') as f:
                f.write("IndiCoin Genesis Block Parameters\n")
                f.write("=" * 40 + "\n\n")
                f.write(f"Block Time: {nTime}\n")
                f.write(f"Nonce: {nonce}\n")
                f.write(f"Block Hash: {block_hash}\n")
                f.write(f"Difficulty Bits: 0x{nBits:08x}\n")
                f.write(f"Genesis Reward: {genesis_reward} satoshis\n\n")
                f.write("C++ Code:\n")
                f.write("genesis = CreateGenesisBlock(\n")
                f.write(f'    "{nTime}",  // nTime\n')
                f.write(f"    {nonce},    // nNonce\n")
                f.write(f"    0x{nBits:08x}, // nBits\n")
                f.write("    1,         // nVersion\n")
                f.write(f"    {genesis_reward} * COIN); // genesisReward\n")
            
            print(f"\n💾 Parameters saved to: indicon_genesis_block_params.txt")
            return True
    
    print("\n❌ No genesis block found in search range")
    return False

if __name__ == "__main__":
    success = quick_genesis_miner()
    if success:
        print("\n🚀 IndiCoin genesis block ready!")
    else:
        print("\n💡 Will use Bitcoin genesis temporarily for development")
