import http.server
import socketserver
import threading
import json
import os
import time

PORT = 5000
httpd_instance = None
server_thread = None

class SyncHandler(http.server.SimpleHTTPRequestHandler):
    save_file_path = "expeditions.json"
    sync_mode = "smart"  # "smart" (Neueste gewinnt), "pc_to_android", "android_to_pc"

    @classmethod
    def set_config(cls, path, mode="smart"):
        cls.save_file_path = path
        cls.sync_mode = mode

    def do_GET(self):
        if self.path == "/sync":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()

            if os.path.exists(self.save_file_path):
                with open(self.save_file_path, "r", encoding="utf-8") as f:
                    content = f.read()
            else:
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

                local_time = 0
                if os.path.exists(self.save_file_path):
                    with open(self.save_file_path, "r", encoding="utf-8") as f:
                        local_data = json.load(f)
                        local_time = local_data.get("last_modified", 0)

                # --- SYNC-LOGIK AUSWERTEN ---
                should_update = False

                if self.sync_mode == "pc_to_android":
                    # PC ist Master: Android darf den PC niemals überschreiben
                    should_update = False
                    response_msg = {"status": "rejected_pc_is_master", "server_time": local_time}

                elif self.sync_mode == "android_to_pc":
                    # Android ist Master: Android überschreibt den PC immer
                    should_update = True

                else:  # "smart" (Neueste gewinnt)
                    if incoming_time > local_time:
                        should_update = True
                    else:
                        should_update = False

                if should_update:
                    with open(self.save_file_path, "w", encoding="utf-8") as f:
                        json.dump(incoming_data, f, ensure_ascii=False, indent=4)
                    response_msg = {"status": "updated_local_from_mobile", "server_time": int(time.time())}
                elif self.sync_mode != "pc_to_android":
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
        return

class ThreadingHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True
    allow_reuse_address = True

def start_sync_server(save_file_path="expeditions.json", sync_mode="smart"):
    global httpd_instance, server_thread
    if httpd_instance is not None:
        # Falls er schon läuft, nur den Modus aktualisieren
        SyncHandler.set_config(save_file_path, sync_mode)
        return

    SyncHandler.set_config(save_file_path, sync_mode)

    try:
        httpd_instance = ThreadingHTTPServer(("", PORT), SyncHandler)
        server_thread = threading.Thread(target=httpd_instance.serve_forever, daemon=True)
        server_thread.start()
        print(f"[SyncServer] Läuft im Hintergrund auf Port {PORT} (Modus: {sync_mode})...")
    except Exception as e:
        print(f"[SyncServer Fehler] Konnte Server nicht starten: {e}")
        httpd_instance = None

def stop_sync_server():
    global httpd_instance
    if httpd_instance is not None:
        try:
            httpd_instance.shutdown()
            httpd_instance.server_close()
            print("[SyncServer] Gestoppt.")
        except Exception as e:
            print(f"[SyncServer Fehler beim Stoppen]: {e}")
        finally:
            httpd_instance = None

def is_server_running():
    return httpd_instance is not None
