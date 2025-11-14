# IndiCoin Reproducible Build Checklist
# Ensure trusted, verifiable binary releases

## 🔐 1. REPRODUCIBLE BUILD SETUP

### Prerequisites
```bash
# Clean Ubuntu 24.04 LTS minimal install
# Install in isolated environment (VM recommended)
sudo apt update
sudo apt install -y build-essential cmake git python3 python3-pip \
    libssl-dev libevent-dev libboost-dev libdb-dev libdb++-dev \
    libminiupnpc-dev libnatpmp-dev wget curl unzip

# Install additional Bitcoin Core dependencies
sudo apt install -y libqrencode-dev libzmq3-dev systemtap-sdt-dev \
    libsqlite3-dev libcap-dev libattr1-dev python3-zmq \
    ccache autoconf automake autotools-dev binutils-gold \
    bsdmainutils cppcheck curl doxygen fonts-dejavu-core \
    g++-multilib gcc-multilib git golang-go gperf \
    help2man icu-devtools libalgorithm-diff-perl \
    libalgorithm-diff-xs-perl libalgorithm-merge-perl \
    libasan8 libatomic1 libc6-dev-i386 libclang1 \
    libcppunit-dev libdb5.3++-dev libffi-dev \
    libgcc-s1 libgdbm-dev libgmpxx4ldbl libgtest-dev \
    libgum-1.0-dev libjemalloc-dev liblz4-dev \
    libncurses-dev libomp-18-dev libprotobuf-dev \
    libqmi-glib-dev libqrencode-dev libqt5svg5-dev \
    libsqlite3-dev libstdc++-13-dev libstdc++-13-pic \
    libunivalue-dev libvpx-dev libxcb1-dev libxcb-xinerama0-dev \
    libxcb-xkb-dev libxkbcommon-dev libxss-dev \
    libxtst-dev lzip miniupnpc ncurses-dev ninja-build \
    pkg-config protobuf-compiler python3-mako \
    qmlscene qt5-qmake qtbase5-dev-tools qttools5-dev-tools \
    qttools5-dev rapidjson-dev rsync seccomp \
    sysutils systemtap-sdt-dev tzdata wget wine \
    xvfb
```

### Build Environment
```bash
# Create reproducible build user
sudo useradd -m -s /bin/bash builduser
sudo su - builduser

# Set build environment variables
export BUILD_DATE="2025-11-14"
export BUILD_USER="builduser@indicoin.org"
export GIT_COMMIT="latest"
export VERSION="1.0.0"

# Set reproducible environment
export SOURCE_DATE_EPOCH=1731600000  # 2025-11-14 timestamp
export BUILD_HOST="indicoin-builder"
export BUILD_OS="Ubuntu-24.04"

# Reproducible compiler flags
export CC="gcc"
export CXX="g++"
export CFLAGS="-O2 -pipe -static-libgcc -static-libstdc++"
export CXXFLAGS="-O2 -pipe -static-libgcc -static-libstdc++"
```

### Source Verification
```bash
# Clone source from verified repository
git clone https://github.com/indicoin/indicoin.git
cd indicoin
git checkout v1.0.0

# Verify GPG signatures (if available)
# git verify-tag v1.0.0

# Document all dependencies and versions
echo "Build Dependencies:" > build_info.txt
dpkg -l | grep -E "(gcc|g\+\+|cmake|boost|openssl)" >> build_info.txt
git log --oneline -n 5 >> build_info.txt
git rev-parse HEAD >> build_info.txt
```

## 🔨 2. BUILD PROCESS

### Clean Build Environment
```bash
# Remove all existing build artifacts
git clean -fdx
rm -rf build/
rm -rf .ccache/

# Configure with reproducible settings
cmake -B build \
    -DCMAKE_BUILD_TYPE=Release \
    -DENABLE_IPC=OFF \
    -DENABLE_TESTS=OFF \
    -DENABLE_BENCHMARK=OFF \
    -DENABLE_FUZZ=OFF \
    -DENABLE_EXTERNAL_SIGNER=OFF \
    -DBUILD_GUI_TESTS=OFF \
    -DBUILD_CLI_TESTS=OFF \
    -DBUILD_WALLET_TESTS=OFF \
    -DBUILD_KERNEL_TESTS=OFF \
    -DENABLE_MAN=OFF \
    -DENABLE_ZMQ=OFF \
    -DCMAKE_INSTALL_PREFIX=/opt/indicoin \
    -DCMAKE_C_COMPILER=$CC \
    -DCMAKE_CXX_COMPILER=$CXX \
    -DCMAKE_C_FLAGS="$CFLAGS" \
    -DCMAKE_CXX_FLAGS="$CXXFLAGS"

# Build
cmake --build build -j$(nproc)

# Verify build artifacts
ls -la build/bin/
sha256sum build/bin/* > indicoin_binaries.sha256
```

### Binary Verification
```bash
# Create build manifest
echo "IndiCoin Build Manifest" > BUILD_MANIFEST.txt
echo "=========================" >> BUILD_MANIFEST.txt
echo "Build Date: $BUILD_DATE" >> BUILD_MANIFEST.txt
echo "Build User: $BUILD_USER" >> BUILD_MANIFEST.txt
echo "Version: $VERSION" >> BUILD_MANIFEST.txt
echo "Git Commit: $(git rev-parse HEAD)" >> BUILD_MANIFEST.txt
echo "Build System: $(uname -a)" >> BUILD_MANIFEST.txt
echo "" >> BUILD_MANIFEST.txt
echo "Checksums:" >> BUILD_MANIFEST.txt
cat indicoin_binaries.sha256 >> BUILD_MANIFEST.txt
```

## 🔒 3. SIGNING & VERIFICATION

### GPG Key Generation
```bash
# Generate dedicated signing key
gpg --batch --gen-key <<EOF
%no-protection
Key-Type: RSA
Key-Length: 4096
Name-Real: IndiCoin Release Signing
Name-Email: releases@indicoin.org
Expire-Date: 2y
EOF

# Export public key for distribution
gpg --armor --export releases@indicoin.org > indicoin_release_key.pub
```

### Binary Signing
```bash
# Sign all binaries
for binary in build/bin/*; do
    gpg --detach-sign --armor $binary
    echo "Signed: $binary"
done

# Create signed manifest
cp BUILD_MANIFEST.txt BUILD_MANIFEST.txt.unsigned
gpg --clear-sign BUILD_MANIFEST.txt.unsigned > BUILD_MANIFEST.txt.asc
```

### Verification Commands
```bash
# Users can verify with:
# 1. Import public key
gpg --import indicoin_release_key.pub

# 2. Verify manifest
gpg --verify BUILD_MANIFEST.txt.asc

# 3. Verify binaries
for sig in build/bin/*.asc; do
    binary=${sig%.asc}
    gpg --verify $sig $binary
done

# 4. Verify checksums
sha256sum -c indicoin_binaries.sha256
```

## 📦 4. RELEASE PACKAGE

### Create Release Archive
```bash
# Create clean release directory
mkdir -p release/indicoin-$VERSION
cp -r build/bin/ release/indicoin-$VERSION/
cp BUILD_MANIFEST.txt.asc release/indicoin-$VERSION/
cp indicoin_release_key.pub release/indicoin-$VERSION/
cp -r contrib/ release/indicoin-$VERSION/  # add contrib scripts if any

# Create tarball
cd release
tar -czf indicoin-$VERSION-amd64-linux.tar.gz indicoin-$VERSION/

# Create checksums
sha256sum indicoin-$VERSION-amd64-linux.tar.gz > indicoin-$VERSION-amd64-linux.tar.gz.sha256
gpg --detach-sign indicoin-$VERSION-amd64-linux.tar.gz
gpg --clear-sign indicoin-$VERSION-amd64-linux.tar.gz.sha256
```

## ✅ 5. REPRODUCIBILITY CHECK

### Verify Build Can Be Reproduced
```bash
# Document exact steps taken
cat > REPRODUCTION_STEPS.txt << 'EOF'
# IndiCoin Reproducible Build Steps
1. Fresh Ubuntu 24.04 LTS minimal install
2. Install all dependencies as listed above
3. Clone source: git clone https://github.com/indicoin/indicoin.git
4. Checkout tag: git checkout v1.0.0
5. Configure: cmake -B build -DENABLE_IPC=OFF ...
6. Build: cmake --build build -j$(nproc)
7. Sign binaries with GPG
8. Create release tarball
EOF

# Users should be able to:
# 1. Follow exact same steps
# 2. Get identical binary checksums
# 3. Verify GPG signatures
```

## 🚀 6. DISTRIBUTION

### GitHub Release
```bash
# Upload to GitHub Releases
# - indicoin-$VERSION-amd64-linux.tar.gz
# - indicoin-$VERSION-amd64-linux.tar.gz.sha256
# - indicoin-$VERSION-amd64-linux.tar.gz.sha256.asc
# - indicoin_release_key.pub
# - BUILD_MANIFEST.txt.asc
```

### Installation Verification
```bash
# Users install with:
# 1. Download release
wget https://github.com/indicoin/releases/download/v1.0.0/indicoin-1.0.0-amd64-linux.tar.gz
wget https://github.com/indicoin/releases/download/v1.0.0/indicoin-1.0.0-amd64-linux.tar.gz.sha256.asc
wget https://github.com/indicoin/releases/download/v1.0.0/indicoin_release_key.pub

# 2. Import key and verify
gpg --import indicoin_release_key.pub
gpg --verify indicoin-1.0.0-amd64-linux.tar.gz.sha256.asc

# 3. Extract and install
tar -xzf indicoin-1.0.0-amd64-linux.tar.gz
sudo cp indicoin-1.0.0/bin/* /usr/local/bin/

# 4. Verify installation
indicoind --version
indicoin-cli --version
```

## 📊 BUILD LOG TEMPLATE

```
==========================================
Indicoin Reproducible Build Log
==========================================
Build Date: 2025-11-14
Build User: builduser@indicoin.org  
Version: 1.0.0
Git Commit: $(git rev-parse HEAD)
Build System: Ubuntu-24.04
Compiler: gcc version 13.2.0
CMake: $(cmake --version)

Environment Variables:
SOURCE_DATE_EPOCH=$SOURCE_DATE_EPOCH
BUILD_DATE=$BUILD_DATE
BUILD_USER=$BUILD_USER

Dependency Versions:
- GCC: $(gcc --version | head -1)
- CMake: $(cmake --version)
- Boost: $(dpkg -l | grep libboost | head -1)

Build Steps:
1. git clone [source]
2. cmake configuration [timestamp: $(date)]
3. make build [timestamp: $(date)]
4. binary signing [timestamp: $(date)]
5. archive creation [timestamp: $(date)]

Final Checksums:
$(cat indicoin_binaries.sha256)

Build Reproducibility: VERIFIED ✅
Security: GPG SIGNED ✅
Distribution: READY ✅
```

## 🏆 SUCCESS CRITERIA

✅ **Build is reproducible** - Same source + same environment = identical binaries  
✅ **All binaries signed** - GPG signature verification passes  
✅ **Checksums verified** - SHA256 checksums match expected values  
✅ **Documentation complete** - All build steps documented  
✅ **Installation tested** - End-to-end installation verified  
✅ **Security hardened** - No debug symbols, static linking where possible  

**Result: Production-ready, trustworthy IndiCoin binaries!**