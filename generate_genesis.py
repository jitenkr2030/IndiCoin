#!/usr/bin/env python3
"""
Genesis Block Generator for IndiCoin
Creates a new genesis block with custom parameters for IndiCoin
"""

import hashlib
import struct
import time

def create_genesis_block():
    # IndiCoin parameters
    name = "IndiCoin"
    timestamp = "The Times 03/Jan/2025 - IndiCoin: Controlled Inflation Digital Currency"
    nTime = int(time.time())
    nNonce = 0
    nBits = 0x1d00ffff  # Same difficulty as Bitcoin
    genesis_reward = 50 * 100000000  # 50 INDI in satoshis
    
    # Genesis scriptPubKey - public key for coinbase
    genesis_pubkey = "04678afdb0fe5548271967f1a67130b7105cd6a828e03909a67962e0ea1f61deb649f6bc3f4cef38c4f35504e51ec112de5c384df7ba0b8d578a4c702b6bf11d5f"
    
    print(f"Generating Genesis Block for {name}")
    print(f"Timestamp: {timestamp}")
    print(f"Block Time: {nTime}")
    print(f"Genesis Reward: {genesis_reward} satoshis ({genesis_reward / 100000000:.1f} INDI)")
    print()
    
    # Create coinbase transaction
    coinbase_tx = create_coinbase_transaction(timestamp, genesis_reward, genesis_pubkey)
    
    # Create genesis block
    genesis_block = {
        'version': 1,
        'hashPrevBlock': '0000000000000000000000000000000000000000000000000000000000000000',
        'hashMerkleRoot': '',
        'nTime': nTime,
        'nBits': nBits,
        'nNonce': nNonce,
        'vtx': [coinbase_tx]
    }
    
    # Calculate merkle root
    genesis_block['hashMerkleRoot'] = calculate_merkle_root([coinbase_tx['txid']])
    
    # Mine genesis block (find nonce that makes hash < target)
    genesis_block = mine_genesis_block(genesis_block, nBits)
    
    # Print results
    print("Genesis Block Details:")
    print(f"Hash: {genesis_block['hash']}")
    print(f"Merkle Root: {genesis_block['hashMerkleRoot']}")
    print(f"Nonce: {genesis_block['nNonce']}")
    print(f"Time: {genesis_block['nTime']}")
    print(f"Bits: 0x{genesis_block['nBits']:08x}")
    print()
    
    print("C++ Code for chainparams.cpp:")
    print()
    print("genesis = CreateGenesisBlock(")
    print(f"    {genesis_block['nTime']}, // nTime")
    print(f"    {genesis_block['nNonce']}, // nNonce") 
    print(f"    0x{genesis_block['nBits']:08x}, // nBits")
    print("    1, // nVersion")
    print(f"    {genesis_reward} * COIN); // genesisReward")
    print()
    print("consensus.hashGenesisBlock = genesis.GetHash();")
    print(f"assert(consensus.hashGenesisBlock == uint256{{\"{genesis_block['hash']}\"}});")
    print(f"assert(genesis.hashMerkleRoot == uint256{{\"{genesis_block['hashMerkleRoot']}\"}});")
    
    return genesis_block

def create_coinbase_transaction(timestamp, reward_satoshis, pubkey):
    """Create the genesis coinbase transaction"""
    
    # Create input (coinbase)
    coinbase_input = {
        'prevout': '0000000000000000000000000000000000000000000000000000000000000000',
        'script_sig': create_coinbase_script_sig(timestamp),
        'sequence': 0xffffffff
    }
    
    # Create output
    script_pubkey = f"21{pubkey}ac"  # P2PKH script
    script_pubkey_bytes = bytes.fromhex(script_pubkey)
    
    coinbase_output = {
        'value': reward_satoshis,
        'script_pubkey': script_pubkey
    }
    
    # Create transaction
    tx = {
        'version': 1,
        'vin': [coinbase_input],
        'vout': [coinbase_output],
        'lock_time': 0
    }
    
    # Calculate transaction ID
    txid = calculate_transaction_id(tx)
    tx['txid'] = txid
    
    return tx

def create_coinbase_script_sig(timestamp):
    """Create the coinbase script signature"""
    # Bitcoin-style coinbase with height and timestamp
    height = 0
    script = struct.pack('<I', height)  # block height
    script += b'\x04ffff001d0104'  # Bitcoin's signature
    script += timestamp.encode('utf-8')
    return script.hex()

def calculate_merkle_root(txids):
    """Calculate merkle root from transaction IDs"""
    if len(txids) == 1:
        return txids[0]
    
    # Convert hex strings to bytes
    hashes = [bytes.fromhex(txid) for txid in txids]
    
    # While more than 1 hash, pairwise hash
    while len(hashes) > 1:
        new_hashes = []
        for i in range(0, len(hashes), 2):
            if i + 1 < len(hashes):
                combined = hashes[i] + hashes[i + 1]
            else:
                combined = hashes[i] + hashes[i]  # Duplicate if odd
            new_hash = hashlib.sha256(hashlib.sha256(combined).digest()).digest()
            new_hashes.append(new_hash)
        hashes = new_hashes
    
    return hashes[0].hex()

def calculate_transaction_id(tx):
    """Calculate transaction ID"""
    # This is a simplified version - in reality we'd need to serialize the transaction properly
    # For genesis block, we'll use a deterministic calculation
    
    # Create a fake but deterministic txid for the genesis block
    # In real Bitcoin Core, this would be calculated from the actual serialized transaction
    tx_data = f"{tx['version']}{len(tx['vin'])}{len(tx['vout'])}{tx['lock_time']}"
    tx_hash = hashlib.sha256(tx_data.encode()).hexdigest()
    return tx_hash

def mine_genesis_block(block, target_bits):
    """Simple genesis block mining - find a nonce that produces a valid hash"""
    target = (1 << (256 - target_bits.bit_length() + 1)) - 1
    
    for nonce in range(1000000):  # Try up to 1 million nonces
        block['nNonce'] = nonce
        
        # Create block header
        header = create_block_header(block)
        
        # Calculate hash
        block_hash = double_sha256(header)
        
        # Check if hash is less than target
        if int(block_hash, 16) < target:
            block['hash'] = block_hash
            print(f"Genesis block found with nonce: {nonce}")
            return block
    
    raise Exception("Failed to find valid genesis block nonce")

def create_block_header(block):
    """Create serialized block header"""
    # Bitcoin block header format
    version = struct.pack('<I', block['version'])
    prev_hash = bytes.fromhex(block['hashPrevBlock'])
    merkle_root = bytes.fromhex(block['hashMerkleRoot'])
    timestamp = struct.pack('<I', block['nTime'])
    bits = struct.pack('<I', block['nBits'])
    nonce = struct.pack('<I', block['nNonce'])
    
    return version + prev_hash + merkle_root + timestamp + bits + nonce

def double_sha256(data):
    """Calculate double SHA256 hash"""
    first_hash = hashlib.sha256(data).digest()
    second_hash = hashlib.sha256(first_hash).digest()
    return second_hash.hex()

if __name__ == "__main__":
    genesis_block = create_genesis_block()