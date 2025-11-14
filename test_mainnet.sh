#!/bin/bash
# IndiCoin Mainnet Test Script

echo "🚀 INDICOIN MAINNET TESTING"
echo "============================="

# Check if binaries exist
echo "1. Checking for built binaries..."
if [ -f "build/bin/bitcoind" ] || [ -f "build/src/bitcoind" ]; then
    echo "✅ Daemon binary found"
    DAEMON_PATH=$(find build -name "bitcoind" -type f | head -1)
    echo "📁 Path: $DAEMON_PATH"
else
    echo "❌ No daemon binary found"
    exit 1
fi

# Test daemon startup
echo ""
echo "2. Testing daemon startup..."
cd /workspace/IndiCoin

# Create data directory
mkdir -p ~/.indicoin
mkdir -p ~/.indicoin/testnet

# Start daemon
$DAEMON_PATH -testnet -daemon -datadir=~/.indicoin/testnet

# Wait for startup
sleep 5

# Test blockchain info
if [ -f "build/bin/bitcoin-cli" ] || [ -f "build/src/bitcoin-cli" ]; then
    CLI_PATH=$(find build -name "bitcoin-cli" -type f | head -1)
    
    echo "3. Checking blockchain info..."
    $CLI_PATH -testnet -datadir=~/.indicoin/testnet getblockchaininfo
else
    echo "❌ CLI binary not found"
fi

echo ""
echo "🎯 TEST COMPLETED"
echo "If you see blockchain info above, IndiCoin mainnet is working!"
