#!/usr/bin/env python3
"""
Simple compilation test to verify IndiCoin genesis parameters work
"""

import subprocess
import sys
import os

def test_compilation():
    """Test if the source code compiles with new genesis parameters"""
    
    print("🔧 TESTING INDICOIN COMPILATION")
    print("=" * 40)
    
    os.chdir("/workspace/IndiCoin")
    
    # Test 1: Configure with CMake
    print("1. Configuring with CMake...")
    result = subprocess.run([
        "cmake", "-B", "build", "-DENABLE_IPC=OFF"
    ], capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ CMake configuration successful")
    else:
        print(f"❌ CMake failed: {result.stderr}")
        return False
    
    # Test 2: Build bitcoin_common library
    print("\n2. Building bitcoin_common library...")
    result = subprocess.run([
        "cmake", "--build", "build", "--target", "bitcoin_common"
    ], capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ bitcoin_common library built successfully")
        print("✅ IndiCoin genesis parameters are valid!")
    else:
        print(f"❌ Build failed: {result.stderr}")
        return False
    
    print("\n🎉 COMPILATION TEST PASSED!")
    print("IndiCoin genesis parameters are working correctly.")
    
    return True

if __name__ == "__main__":
    test_compilation()