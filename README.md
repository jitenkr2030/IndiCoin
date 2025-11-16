IndiCoin Integration/Staging Tree
===================================

IndiCoin is a decentralized digital currency with controlled inflation, built on a fork of Bitcoin Core. It implements a 5% annual inflation rate to ensure sustainable growth and adoption while maintaining the security and decentralization principles of Bitcoin.

**Official Website**: https://indicoin.money  
**Community**: [Discord](https://discord.gg/indicoin) | [Telegram](https://t.me/indicoinofficial)  
**Documentation**: https://docs.indicoin.money

What is IndiCoin?
-----------------

IndiCoin is a peer-to-peer cryptocurrency that enables secure, fast, and low-cost transactions globally. Built on Bitcoin Core technology, IndiCoin introduces a controlled inflation mechanism that ensures the long-term sustainability of the network while maintaining strong security and decentralization.

### Key Features

- **Controlled Inflation**: 5% annual inflation rate for sustainable growth
- **Bitcoin Core Foundation**: Built on battle-tested Bitcoin Core codebase
- **Enhanced Security**: Maintains Bitcoin's security model with additional protections
- **Fast Transactions**: Optimized network parameters for efficient processing
- **Decentralized**: Community-driven governance and development
- **Open Source**: Fully transparent and auditable codebase

### Network Specifications

- **Consensus Algorithm**: SHA-256 Proof-of-Work
- **Block Time**: ~10 minutes (difficulty adjustment every 2016 blocks)
- **Initial Block Reward**: 50 IND per block
- **Inflation Rate**: 5% annually
- **Network Magic**: 0xf1c2d3e4
- **Default Port**: 5533
- **RPC Port**: 5534
- **Genesis Block Hash**: `10e870f6ff26921e54f732934d368e495a49e9643d33a6854fe398fa803fabed`
- **Genesis Timestamp**: November 14, 2025

Getting Started
---------------

### Prerequisites

- 64-bit Linux, macOS, or Windows
- 4GB+ RAM
- 50GB+ free disk space
- Internet connection

### Building from Source

1. **Clone the repository:**
   ```bash
   git clone https://github.com/indicoinofficial/indicoin.git
   cd indicoin
   ```

2. **Install dependencies:**
   
   **Ubuntu/Debian:**
   ```bash
   sudo apt-get update
   sudo apt-get install build-essential pkg-config libc6-dev m4 g++-multilib \
       autoconf libtool ncurses-dev unzip git python3 python3-zmq zlib1g-dev \
       wget curl bsdmainutils automake cmake
   ```

   **macOS:**
   ```bash
   brew install automake cmake pkg-config libtool boost miniupnpc zeromq
   ```

3. **Build IndiCoin:**
   ```bash
   # Configure the build
   cmake -B build -DENABLE_IPC=OFF

   # Build (using all available cores)
   cmake --build build -j$(nproc)

   # Install system-wide (optional)
   sudo cmake --build build --target install
   ```

### Binary Installation

For the latest stable release, visit [indicoin.money/downloads](https://indicoin.money/downloads).

**Linux (Ubuntu/Debian):**
```bash
wget https://releases.indicoin.org/indicoin-latest-x86_64-linux-gnu.tar.gz
tar -xzf indicoin-latest-x86_64-linux-gnu.tar.gz
sudo cp bin/* /usr/local/bin/
```

**macOS:**
```bash
brew tap indicoinofficial/tap
brew install indicoin
```

**Windows:**
Download the installer from [indicoin.money/downloads](https://indicoin.money/downloads).

Running IndiCoin
----------------

### Start the Daemon

```bash
# Start the IndiCoin daemon
indicoind -daemon

# Check daemon status
indicoin-cli getblockchaininfo

# View recent blocks
indicoin-cli getblockchaininfo | jq '.blocks'
```

### Configuration

Create `~/.indiCoin/indiCoin.conf` for custom configuration:

```ini
# Basic settings
rpcuser=your_username
rpcpassword=your_secure_password
rpcallowip=127.0.0.1
rpcport=5534

# Network settings
listen=1
server=1
port=5533

# Peers
addnode=seed1.indicoin.money
addnode=seed2.indicoin.money
addnode=seed3.indicoin.money

# Performance
dbcache=4000
maxconnections=125

# Wallet
wallet=1
```

### Testing the Installation

```bash
# Verify genesis block
indicoin-cli getblockhash 0
# Expected: 10e870f6ff26921e54f732934d368e495a49e9643d33a6854fe398fa803fabed

# Check network info
indicoin-cli getnetworkinfo

# View blockchain info
indicoin-cli getblockchaininfo

# Check total coins in circulation
indicoin-cli gettxoutsetinfo
```

Mining
------

IndiCoin uses SHA-256 Proof-of-Work mining. Solo mining is possible but pool mining is recommended for consistent rewards.

### Solo Mining

1. **Start the daemon with mining enabled:**
   ```bash
   indicoind -gen -genproclimit=1
   ```

2. **Or use the built-in miner:**
   ```bash
   indicoin-cli setgenerate true 1
   ```

### Pool Mining

Join any IndiCoin mining pool that supports our network. Popular pools include:

- **IndiCoin Pool**: https://pool.indicoin.money
- **NiceHash**: https://nicehash.com
- **F2Pool**: https://www.f2pool.com

Configure your miner to use the pool's stratum address and port.

Development
-----------

### Development Process

The `master` branch represents the latest stable release. Development occurs on feature branches with regular integration to `master` after thorough testing.

### Testing

**Unit Tests:**
```bash
cd build
ctest --output-on-failure
```

**Integration Tests:**
```bash
test/functional/test_runner.py
```

**Manual Testing:**
```bash
# Start testnet
indicoind -testnet -daemon

# Run specific test
test/functional/feature_rbf.py
```

### Contributing

We welcome contributions from developers worldwide!

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

Please read our [Contributing Guidelines](CONTRIBUTING.md) before submitting changes.

Security
--------

Security is our top priority. If you discover a vulnerability, please report it responsibly:

**Security Contact**: security@indicoin.money  
**PGP Key**: [Download](https://indicoin.money/security-pgp.txt)  
**Bug Bounty Program**: [indicoin.money/bounty](https://indicoin.money/bounty)

### Security Best Practices

- Always verify downloads using GPG signatures
- Use hardware wallets for storing IND coins
- Keep your node software updated
- Run nodes on secure, dedicated machines
- Never share private keys or wallet.dat files

Network Status
--------------

- **Mainnet Status**: Live
- **Testnet**: Available for testing (-testnet flag)
- **Block Explorer**: https://explorer.indicoin.money
- **Network Statistics**: https://stats.indicoin.money

Community
---------

Join our growing community:

- **Website**: https://indicoin.money
- **Discord**: https://discord.gg/indicoin
- **Telegram**: https://t.me/indicoinofficial
- **Twitter**: https://twitter.com/indicoinofficial
- **Reddit**: https://reddit.com/r/indicoin
- **Forum**: https://forum.indicoin.money

Roadmap
-------

**Q4 2025**:
- [x] Genesis block launch
- [x] Core wallet release
- [x] Block explorer
- [ ] Mobile wallet (iOS/Android)
- [ ] Lightning Network support

**Q1 2026**:
- [ ] Smart contracts support
- [ ] Cross-chain bridges
- [ ] DeFi protocols
- [ ] Hardware wallet integration

**Q2 2026**:
- [ ] Governance system
- [ ] Treasury management
- [ ] Advanced privacy features
- [ ] Institutional services

FAQ
---

**Q: What makes IndiCoin different from Bitcoin?**
A: IndiCoin implements a 5% controlled inflation rate, making it more suitable for long-term adoption while maintaining Bitcoin's security and decentralization.

**Q: How is the inflation implemented?**
A: The inflation rate is programmed into the consensus rules, increasing the money supply by 5% annually through reduced block rewards over time.

**Q: Can I mine IndiCoin?**
A: Yes! IndiCoin uses SHA-256 Proof-of-Work mining, compatible with Bitcoin mining hardware.

**Q: Is IndiCoin compatible with Bitcoin wallets?**
A: While IndiCoin uses the same cryptographic standards, it has its own network and requires IndiCoin-specific software.

**Q: What's the total supply of IndiCoin?**
A: IndiCoin has no hard cap but implements controlled inflation of 5% annually for sustainable growth.

License
-------

IndiCoin is released under the terms of the MIT license. See [COPYING](COPYING) for more information or see https://opensource.org/license/MIT.

### Third-Party Licenses

- Bitcoin Core: MIT License
- LevelDB: BSD 3-Clause License
- secp256k1: MIT License
- See individual source files for complete license information.

Support
-------

Need help? Our support team is here to assist you:

- **Documentation**: https://docs.indicoin.money
- **Community Support**: Discord/Telegram channels
- **Bug Reports**: GitHub Issues
- **General Inquiries**: support@indicoin.money

Thank you for being part of the IndiCoin community!

---

**IndiCoin: Empowering the future of digital finance with controlled inflation and sustainable growth.**
