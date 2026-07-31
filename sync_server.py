import http.server
import socketserver
import threading
import json
import os
import time

PORT = 5000

class SyncHandler(http.server.SimpleHTTPRequestHandler):
    save_file_path = "expeditions.json"

    @classmethod
    sende_config(cls, path):
        cls.save_file_path = path

    def do_GET(self):
        if self.path == "/sync":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()

            if os.path.exists(self.save_file_path):
                with open(self.save_file_path, "r", encoding="utf-8") as f:
                    content = f.read()
            else:
                # Fallback, falls Datei noch nicht existiert
                default_data = {"last_modified": int(time.time()), "expeditions": []}
                content = json.dumps(default_data, ensure_ascii=False, indent=4)

            self.wfile.write(content.encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == "/sync":
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)

            try:
                incoming_data = json.loads(post_data.decode("utf-8"))
                incoming_time = incoming_data.get("last_modified", 0)

                # Lokalen Stand laden und Zeitstempel prüfen
                local_time = 0
                if os.path.exists(self.save_file_path):
                    with open(self.save_file_path, "r", encoding="utf-8") as f:
                        local_data = json.load(f)
                        local_time = local_data.get("last_modified", 0)

                # Smart Sync Logik: Wer den neueren Zeitstempel hat, gewinnt
                if incoming_time > local_time:
                    with open(self.save_file_path, "w", encoding="utf-8") as f:
                        json.dump(incoming_data, f, ensure_ascii=False, indent=4)
                    response_msg = {"status": "updated_local_from_mobile", "server_time": int(time.time())}
                else:
                    response_msg = {"status": "desktop_is_newer_or_equal", "server_time": local_time}

                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(response_msg).encode("utf-8"))
            except Exception as e:
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        # Unterdrückt standardmäßige Konsolen-Logs im HTTP-Server (optional, hält das Terminal sauber)
        return

def start_sync_server(save_file_path="expeditions.json"):
    SyncHandler.save_file_path = save_file_path

    def run_server():
        try:
            with socketserver.TCPServer(("", PORT), SyncHandler) as httpd:
                print(f"[SyncServer] Läuft im Hintergrund auf Port {PORT}...")
                httpd.serve_forever()
        except Exception as e:
            print(f"[SyncServer Fehler] Konnte Server nicht starten: {e}")

    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
