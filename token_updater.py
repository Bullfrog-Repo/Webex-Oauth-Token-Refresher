"""
Webex OAuth Token Refresher Script
----------------------------------
This script reads a JSON file of Webex OAuth credentials (tokens_master.json),
refreshes each org's access token using the /v1/access_token endpoint, 
and writes the results to:

- access_tokens/tokens_<timestamp>.json (updated tokens)
- token_logs/logs_<timestamp>.json (status + responses)

Only orgs with valid client_id, client_secret, and refresh_token are processed.
"""

import json
import os
import requests
from datetime import datetime

# Load tokens from master JSON
with open("tokens_master.json", "r") as file:
    tokens_dict = json.load(file)

# Prepare for new output
new_tokens_dict = {}
token_log_entries = []
token_url = "https://webexapis.com/v1/access_token"

os.makedirs("access_tokens", exist_ok=True)
os.makedirs("token_logs", exist_ok=True)

# Timestamp for filenames
timestamp = datetime.now().strftime("%m_%d_%y_%H_%M")

for key, token_data in tokens_dict.items():
    client_id = token_data.get("client_id")
    client_secret = token_data.get("client_secret")
    refresh_token = token_data.get("refresh_token")

    if not all([client_id, client_secret, refresh_token]):
        print(f"⚠️ Skipping {key} — missing credentials")
        token_data["status"] = "skipped"
        token_data["error"] = "Missing client_id, client_secret, or refresh_token"
        new_tokens_dict[key] = token_data
        continue

    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "refresh_token",
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token,
    }

    try:
        response = requests.post(token_url, headers=headers, data=data)
        if response.status_code == 200:
            result = response.json()
            access_token = result.get("access_token")
            new_refresh_token = result.get("refresh_token")

            token_data["access_token"] = access_token
            token_data["refresh_token"] = new_refresh_token
            token_data["status"] = "success"
            token_data["error"] = None
            print(f"✅ {key} refreshed successfully.")
        else:
            token_data["status"] = "failed"
            token_data["error"] = f"HTTP {response.status_code}: {response.text}"
            print(f"❌ {key} failed: {response.status_code}")
    except requests.exceptions.RequestException as e:
        token_data["status"] = "error"
        token_data["error"] = str(e)
        print(f"❌ {key} request error: {e}")

    new_tokens_dict[key] = token_data

# Write to dated token backup
with open(os.path.join("access_tokens", f"tokens_{timestamp}.json"), "w") as output_file:
    json.dump(new_tokens_dict, output_file, indent=4)

# ✅ Overwrite the master JSON with the refreshed tokens
with open("tokens_master.json", "w") as master_file:
    json.dump(new_tokens_dict, master_file, indent=4)

print("🎉 Token refresh complete. Master and backup files updated.")
    json.dump(token_log_entries, logfile, indent=4)

print(f"\n📁 New tokens saved to: {output_file}")
print(f"📜 Token logs saved to: {log_file}")
