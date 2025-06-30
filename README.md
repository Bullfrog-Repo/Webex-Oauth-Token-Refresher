# Webex OAuth Token Refresher

A lightweight Python automation script that refreshes Webex OAuth tokens for multiple integrations (organizations) using the Webex API. This tool handles token rotation via the `/v1/access_token` endpoint using stored `refresh_token` values and outputs refreshed tokens and logs for reuse in downstream scripts or systems.

---

## 📦 Features

- 🔁 Refreshes tokens for multiple orgs from a single config file
- 💾 Saves updated tokens to timestamped JSON files
- 🪵 Logs success/failure status per org with timestamps
- ❌ Gracefully skips orgs missing required credentials
- 🧱 Script-friendly and extensible for integration or automation

---

## 📁 Project Structure

```
webex-oauth-token-refresher/
├── token_updater.py                # Main script
├── tokens_master_template.json     # Example config file
├── access_tokens/                  # Timestamped output tokens
│   └── tokens_template.json
├── token_logs/                     # Timestamped logs
│   └── logs_template.json
├── .gitignore                      # Ignores private or generated files
└── README.md                       # You're reading it!
```

---

## 🚀 Getting Started

### 1. Clone the Repo

```bash
git clone https://github.com/YOUR_USERNAME/webex-oauth-token-refresher.git
cd webex-oauth-token-refresher
```

### 2. Install Dependencies

```bash
pip install requests
```

> Optionally add `requests` to a `requirements.txt` file for future use.

### 3. Create Your Token Config

Copy the provided template and fill in your Webex OAuth app credentials:

```bash
cp tokens_master_template.json tokens_master.json
```

**Example format:**

```json
{
  "example_org": {
    "client_id": "YOUR_CLIENT_ID",
    "client_secret": "YOUR_CLIENT_SECRET",
    "access_token": "initial_token_here",
    "refresh_token": "refresh_token_here",
    "scopes": "your_oauth_scopes_url",
    "date": "MM_DD_YY"
  }
}
```

### 4. Run the Script

```bash
python token_updater.py
```

✅ The script will:
- Refresh each org's access token
- Save updated tokens in `access_tokens/tokens_<timestamp>.json`
- Log detailed results in `token_logs/logs_<timestamp>.json`

---

## 🔐 Notes & Best Practices

- `tokens_master.json` is intentionally ignored by Git — keep this file private.
- Make sure each org entry contains a valid `client_id`, `client_secret`, and `refresh_token`.
- Webex tokens typically expire every 14 days — this script helps manage seamless rotation.

---

## 🧠 Future Improvements

- Add CLI flags for targeting specific orgs
- Integrate with secure token storage (e.g., AWS SSM, Vault)
- GitHub Actions or cron integration for scheduled runs
- Slack/email alerting for failed refreshes

---

## 👤 Author

Maintained by [Keegan] — built for personal use, automation learning, and managing Webex integrations at scale.

Feel free to fork, extend, or adapt it for your own projects.
