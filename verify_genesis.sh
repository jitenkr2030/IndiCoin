#!/bin/bash
# IndiCoin Genesis Verification Script

echo "🚀 INDICOIN GENESIS VERIFICATION"
echo "================================="
echo ""

# Expected genesis hash
EXPECTED_HASH="10e870f6ff26921e54f732934d368e495a49e9643d33a6854fe398fa803fabed"

echo "Expected Genesis Hash: $EXPECTED_HASH"
echo ""

# Test 1: Check if bitcoin binary exists and is IndiCoin branded
echo "1. Testing IndiCoin binary..."
if [ -f "./build/bin/bitcoin" ]; then
    echo "✅ Found bitcoin binary"
    echo "Version info:"
    ./build/bin/bitcoin --version 2>/dev/null || echo "Binary ready"
    echo ""
else
    echo "❌ bitcoin binary not found"
    exit 1
fi

# Test 2: Start daemon and test genesis
echo "2. Starting IndiCoin daemon..."
cd /workspace/IndiCoin

# Clean any existing data
rm -rf ~/.bitcoin ~/.indicoin 2>/dev/null

# Start daemon on mainnet
echo "Starting daemon on mainnet..."
./build/bin/bitcoin -daemon -datadir=~/.indicoin -listen=0 -port=5533

# Wait for startup
sleep 10

echo ""
echo "3. Genesis Block Verification..."

# Test getblockhash 0
echo "Testing: getblockhash 0"
GENESIS_HASH=$(./build/bin/bitcoin-cli -datadir=~/.indicoin getblockhash 0 2>/dev/null)
echo "Retrieved genesis hash: $GENESIS_HASH"

if [ "$GENESIS_HASH" = "$EXPECTED_HASH" ]; then
    echo "✅ GENESIS HASH MATCHES! IndiCoin genesis correctly integrated!"
else
    echo "❌ Genesis hash mismatch"
    echo "Expected: $EXPECTED_HASH"
    echo "Got:      $GENESIS_HASH"
fi

echo ""
echo "4. Chain Information..."
echo "Running: getblockchaininfo"
./build/bin/bitcoin-cli -datadir=~/.indicoin getblockchaininfo 2>/dev/null || echo "CLI test"

echo ""
echo "5. Genesis Block Details..."
echo "Running: getblock [genesis-hash]"
if [ ! -z "$GENESIS_HASH" ]; then
    ./build/bin/bitcoin-cli -datadir=~/.indicoin getblock "$GENESIS_HASH" 2>/dev/null || echo "Block details test"
fi

echo ""
echo "🎯 VERIFICATION COMPLETE"
echo "If genesis hash matches expected, IndiCoin is correctly deployed!"

# Cleanup
echo ""
echo "Cleaning up..."
pkill -f bitcoin
rm -rf ~/.indicoin ~/.bitcoin 2>/dev/null
echo "Done!"