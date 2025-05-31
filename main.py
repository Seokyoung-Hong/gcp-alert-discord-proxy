import os
import requests
from functions_framework import http

@http
def gcp_alert_handler(request):
    data = request.get_json()
    incident = data.get("incident", {})
    severity = incident.get("severity", "WARNING").upper()

    webhook = os.environ["DISCORD_CRITICAL_WEBHOOK"] if severity == "CRITICAL" else os.environ["DISCORD_WARNING_WEBHOOK"]

    embed = {
        "title": f"🚨 {incident.get('policy_name')}",
        "description": incident.get("summary"),
        "color": 16711680 if severity == "CRITICAL" else 16753920,
        "fields": [
            {"name": "상태", "value": incident.get("state", "-")},
            {"name": "타입", "value": incident.get("condition_name", "-")},
        ],
    }

    requests.post(webhook, json={"embeds": [embed]})
    return "OK"
