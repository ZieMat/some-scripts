import os
import sys
import json
import requests
from pathlib import Path
from pypac import PACSession

# Constants
VAULT_ADDR = "https://active.fe.vault.tech.orange"
VAULT_TOKEN_TTL = "10m"
SERVICE = "secgov"

# Environment configurations
ENV_CONFIGS = {
    "di": {
        "ROLE_ID": os.getenv("VAULT_ROLE_ID"),
        "SECRET_ID": os.getenv("VAULT_SECRET_ID")
    },
    # pr to be adjusted
    "pr": {
        "ROLE_ID": "some_role_id",
        "SECRET_ID": "some_secret_id"
    }
}
# Proxy config (comment if you don't use proxy)
session = PACSession(pac_file_url='http://proxy.tepenet/opl.pac') 

def parse_arguments():
    """Parse command line arguments"""
    if len(sys.argv) != 2 or sys.argv[1] not in ENV_CONFIGS:
        print(f"Usage: python {os.path.basename(__file__)} env")
        print("env = di or pr")
        sys.exit(1)
    return sys.argv[1]

def authenticate_vault(env):
    """Authenticate to Vault using requests and return token"""
    role_id = ENV_CONFIGS[env]["ROLE_ID"]
    secret_id = ENV_CONFIGS[env]["SECRET_ID"]
    
    auth_url = f"{VAULT_ADDR}/v1/auth/approle/login"
    payload = {
        "role_id": role_id,
        "secret_id": secret_id
    }
    
    try:
        response = session.post(auth_url, json=payload) # With proxy
        #response = requests.post(auth_url, json=payload) # Without proxy
        response.raise_for_status()  # Raise exception for HTTP errors
        
        auth_data = response.json()
        return auth_data["auth"]["client_token"]
    except requests.exceptions.RequestException as e:
        print(f"Error authenticating to Vault: {e}")
        sys.exit(1)

### SECRET LIST ###
def list_vault_secrets(token, path):
    """List secrets at the given path using requests"""
    headers = {"X-Vault-Token": token}
    list_url = f"{VAULT_ADDR}/v1/{path}?list=true"
    
    try:
        response = session.get(list_url, headers=headers) # With proxy 
        # response = requests.get(list_url, headers=headers) # Without proxy
        response.raise_for_status()
        
        data = response.json()
        return data.get("data", {}).get("keys", [])
    except requests.exceptions.RequestException as e:
        print(f"Error listing secrets at {path}: {e}")
        return []

def main():
    """Main function"""
    env = parse_arguments()
    
    # Authenticate to Vault
    vault_token = authenticate_vault(env)
    
    # Remove JSON file if it exists
    json_file = Path(f"{env}{SERVICE}.json")
    if json_file.exists():
        json_file.unlink()
    
    # List secrets
    base_path = f"diod/{env}/{SERVICE}"
    protected_path = f"{base_path}/protected"
    
    print(f"Secrets in {base_path}:")
    for key in list_vault_secrets(vault_token, base_path):
        print(f"  {key}")
    
    print(f"Secrets in {protected_path}:")
    for key in list_vault_secrets(vault_token, protected_path):
        print(f"  {key}")
    
    # Print token
    print(f"Vault Token: {vault_token}")

if __name__ == "__main__":
    main()