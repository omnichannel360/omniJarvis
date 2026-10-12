#!/usr/bin/env python3
"""Setup device token for PC-to-brain auth."""
import keyring
import uuid
import sys

def setup_device_token():
    """Generate and store device token."""
    token = f"jarvis-{uuid.uuid4()}"
    keyring.set_password("jarvis", "device_token", token)
    print(f"Device token stored: {token}")
    return token

if __name__ == "__main__":
    setup_device_token()
