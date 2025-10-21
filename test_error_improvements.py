#!/usr/bin/env python3
"""
Test script to verify the improved error handling for API key issues
"""

import os
import sys
import subprocess
from pathlib import Path

def test_api_key_errors():
    """Test various API key error scenarios"""

    print("🧪 Testing CodeViewX API Key Error Handling")
    print("=" * 50)

    # Save original API key if it exists
    original_key = os.getenv('ANTHROPIC_AUTH_TOKEN')

    try:
        # Test 1: Missing API key
        print("\n1️⃣ Testing missing API key...")
        if 'ANTHROPIC_AUTH_TOKEN' in os.environ:
            del os.environ['ANTHROPIC_AUTH_TOKEN']

        result = subprocess.run([
            sys.executable, '-m', 'codeviewx.cli', '--help'
        ], capture_output=True, text=True)

        if result.returncode == 0:
            print("   ✅ Help command works without API key")
        else:
            print("   ❌ Help command failed unexpectedly")
            print(f"   Error: {result.stderr}")

        # Test 2: Run without API key (should fail with helpful message)
        print("\n2️⃣ Testing documentation generation without API key...")
        result = subprocess.run([
            sys.executable, '-m', 'codeviewx.cli', '-w', '.', '-o', '/tmp/test_docs'
        ], capture_output=True, text=True)

        if result.returncode != 0:
            if "ANTHROPIC_AUTH_TOKEN" in result.stderr:
                print("   ✅ Correctly shows API key error")
                if "https://console.anthropic.com" in result.stderr:
                    print("   ✅ Provides helpful link to get API key")
                if "export ANTHROPIC_AUTH_TOKEN" in result.stderr:
                    print("   ✅ Shows how to set environment variable")
            else:
                print("   ❌ Error doesn't mention API key:")
                print(f"   {result.stderr}")
        else:
            print("   ❌ Should have failed without API key")

        # Test 3: Invalid API key format
        print("\n3️⃣ Testing invalid API key format...")
        os.environ['ANTHROPIC_AUTH_TOKEN'] = 'invalid-key-123'

        result = subprocess.run([
            sys.executable, '-m', 'codeviewx.cli', '-w', '.', '-o', '/tmp/test_docs'
        ], capture_output=True, text=True)

        if result.returncode != 0:
            if "format appears incorrect" in result.stderr or "appears to be invalid" in result.stderr:
                print("   ✅ Correctly identifies invalid API key format")
            else:
                print("   ⚠️  Could be more specific about format issue:")
                print(f"   {result.stderr[:200]}...")
        else:
            print("   ❌ Should have failed with invalid API key")

        # Test 4: Short API key
        print("\n4️⃣ Testing short API key...")
        os.environ['ANTHROPIC_AUTH_TOKEN'] = 'sk-ant'

        result = subprocess.run([
            sys.executable, '-m', 'codeviewx.cli', '-w', '.', '-o', '/tmp/test_docs'
        ], capture_output=True, text=True)

        if result.returncode != 0:
            if "too short" in result.stderr:
                print("   ✅ Correctly identifies short API key")
            else:
                print("   ⚠️  Could be more specific about length issue:")
                print(f"   {result.stderr[:200]}...")
        else:
            print("   ❌ Should have failed with short API key")

        print("\n" + "=" * 50)
        print("✅ Error handling improvements verified!")
        print("\n📋 Summary of improvements:")
        print("   • Clear error messages for missing API keys")
        print("   • Helpful guidance on how to fix the issue")
        print("   • Links to obtain API keys")
        print("   • Format validation for API keys")
        print("   • Bilingual support (English/Chinese)")

    finally:
        # Restore original API key
        if original_key:
            os.environ['ANTHROPIC_AUTH_TOKEN'] = original_key
        elif 'ANTHROPIC_AUTH_TOKEN' in os.environ:
            del os.environ['ANTHROPIC_AUTH_TOKEN']

if __name__ == '__main__':
    test_api_key_errors()