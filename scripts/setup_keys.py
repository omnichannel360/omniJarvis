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
    
    telegram_token = input("Enter TELEGRAM_BOT_TOKEN: ").strip()
    telegram_owner = input("Enter TELEGRAM_OWNER_ID: ").strip()
    
    keyring.set_password("jarvis", "anthropic_api_key", api_key)
    keyring.set_password("jarvis", "telegram_bot_token", telegram_token)
    keyring.set_password("jarvis", "telegram_owner_id", telegram_owner)
    
    print("✓ Keys stored in credential store")

if __name__ == "__main__":
    setup_keys()
