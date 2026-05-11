import json
import os
import urllib.request
import urllib.error
import ast

script_dir = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(script_dir, 'issue_output.json')

with open(json_path, 'r', encoding='utf-8') as f:
    issue_data = json.load(f)

title = issue_data.get('title', '')
body = issue_data.get('body', issue_data.get('content', ''))

if not title or not body:
    print("Error: Missing title or body in issue_output.json")
    exit(1)

payload = json.dumps({
    "title": title,
    "body": body
}).encode('utf-8')

headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

# Optional webhook secret for authentication
webhook_secret = os.environ.get('WEBHOOK_SECRET')
if webhook_secret:
    headers['X-Webhook-Secret'] = webhook_secret

webhook_url = os.environ.get('WEBHOOK_URL', 'http://42.193.17.157:8081/webhook')

req = urllib.request.Request(
    webhook_url,
    data=payload,
    headers=headers,
    method='POST'
)

try:
    with urllib.request.urlopen(req) as response:
        result = response.read().decode('utf-8')
        print("Issue created successfully via webhook server: " + ast.literal_eval(result)['html_url'])
except urllib.error.HTTPError as e:
    error_body = e.read().decode('utf-8')
    print(f"Error {e.code}: {error_body}")
    exit(1)
except Exception as e:
    print(f"Error: {e}")
    exit(1)
