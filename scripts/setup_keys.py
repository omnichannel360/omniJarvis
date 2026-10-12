#!/usr/bin/env python3
"""Store Jarvis secrets in OS credential store."""
import keyring
import sys

def setup_keys():
    """Prompt for and store secrets."""
    api_key = input("Enter ANTHROPIC_API_KEY: ").strip()
    if not api_key:
        print("Abort: API key required")
        sys.exit(1)

    keyring.set_password("jarvis", "anthropic_api_key", api_key)
    
    print("✓ Keys stored in credential store")

if __name__ == "__main__":
    setup_keys()
