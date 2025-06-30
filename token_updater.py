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
        token_log_entries.append({
            "org": key,
            "timestamp": datetime.utcnow().isoformat(),
            "status": "skipped",
            "error": "Missing credentials"
        })
        continue

    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "refresh_token",
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token
    }

    try:
        response = requests.post(token_url, data=data, headers=headers)
        response.raise_for_status()
        new_data = response.json()

        # Store new tokens
        token_data["access_token"] = new_data.get("access_token", "")
        token_data["refresh_token"] = new_data.get("refresh_token", "")
        token_data["date"] = datetime.now().strftime("%B %d, %Y")
        token_data["status"] = "success"
        token_data.pop("error", None)

        print(f"✅ {key} token refreshed successfully")

        token_log_entries.append({
            "org": key,
            "timestamp": datetime.utcnow().isoformat(),
            "status": "success",
            "response": new_data
        })

    except requests.exceptions.RequestException as e:
        token_data["status"] = "failed"
        token_data["error"] = str(e)
        print(f"❌ {key} failed to refresh: {e}")

        token_log_entries.append({
            "org": key,
            "timestamp": datetime.utcnow().isoformat(),
            "status": "failed",
            "error": str(e)
        })

    new_tokens_dict[key] = token_data

# Save to timestamped JSON
output_file = f"access_tokens/tokens_{timestamp}.json"
log_file = f"token_logs/logs_{timestamp}.json"

with open(output_file, "w") as outfile:
    json.dump(new_tokens_dict, outfile, indent=4)

with open(log_file, "w") as logfile:
    json.dump(token_log_entries, logfile, indent=4)

print(f"\n📁 New tokens saved to: {output_file}")
print(f"📜 Token logs saved to: {log_file}")
