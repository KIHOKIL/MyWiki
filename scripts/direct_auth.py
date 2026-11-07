import os
import sys
import json
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = [
    "https://www.googleapis.com/auth/tasks",
    "https://www.googleapis.com/auth/calendar.events",
]

cred_path = Path.home() / ".google_todo_sync" / "credentials.json"
token_path = Path.home() / ".google_todo_sync" / "token.json"

flow = InstalledAppFlow.from_client_secrets_file(str(cred_path), SCOPES, redirect_uri="http://localhost:8088/")
auth_url, _ = flow.authorization_url(prompt="consent", access_type="offline")

auth_code = None

class OAuthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global auth_code
        parsed = urllib.parse.urlparse(self.path)
        qs = urllib.parse.parse_qs(parsed.query)
        if "code" in qs:
            auth_code = qs["code"][0]
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            html = """
            <html>
            <body style="font-family:sans-serif; text-align:center; padding-top:50px; background:#0d1117; color:#3fb950;">
                <h2>🎉 Google 계정 인증이 완료되었습니다!</h2>
                <p style="color:#e6edf3;">이 창을 닫고 Antigravity 대화창으로 돌아가셔도 좋습니다.</p>
            </body>
            </html>
            """
            self.wfile.write(html.encode("utf-8"))
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"No code found")

    def log_message(self, format, *args):
        pass

server = HTTPServer(("localhost", 8088), OAuthHandler)
print(f"AUTH_READY_URL: {auth_url}", flush=True)

# Open browser via OS command
os.system(f'start "" "{auth_url}"')

while not auth_code:
    server.handle_request()

flow.fetch_token(code=auth_code)
token_path.write_text(flow.credentials.to_json(), encoding="utf-8")
print("TOKEN_SAVED_SUCCESSFULLY", flush=True)
