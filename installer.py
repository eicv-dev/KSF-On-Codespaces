import http.server
import json
import base64
import os
import threading
import webbrowser

PORT = 6789
DONE = threading.Event()

def get_banner_b64():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "banner.png")
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except Exception:
        return ""

HTML = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>KSF On Codespaces Installer</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    background: #0d0d0d;
    color: #f0f0f0;
    font-family: 'Segoe UI', sans-serif;
    display: flex;
    flex-direction: column;
    align-items: center;
    min-height: 100vh;
    padding: 40px 20px;
  }}
  img.banner {{
    max-width: 700px;
    width: 100%;
    margin-bottom: 40px;
    border-radius: 12px;
  }}
  h2 {{ color: #cc2222; margin-bottom: 24px; font-size: 1.4rem; }}
  .grid {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 24px;
    width: 100%;
    max-width: 860px;
    margin-bottom: 28px;
  }}
  .col h3 {{
    font-size: 0.95rem;
    color: #aaa;
    margin-bottom: 12px;
    text-transform: uppercase;
    letter-spacing: 1px;
  }}
  label {{
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 8px 10px;
    border-radius: 6px;
    cursor: pointer;
    transition: background 0.15s;
    font-size: 0.95rem;
  }}
  label:hover {{ background: #1e1e1e; }}
  input[type=checkbox] {{ accent-color: #cc2222; width: 16px; height: 16px; }}
  .de-row {{
    width: 100%;
    max-width: 860px;
    margin-bottom: 32px;
  }}
  .de-row label {{ display: block; color: #aaa; font-size: 0.85rem; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 1px; }}
  select {{
    width: 100%;
    padding: 10px 14px;
    background: #1a1a1a;
    color: #f0f0f0;
    border: 1px solid #333;
    border-radius: 8px;
    font-size: 1rem;
  }}
  button {{
    background: #cc2222;
    color: white;
    border: none;
    padding: 16px 60px;
    font-size: 1.1rem;
    font-weight: bold;
    border-radius: 10px;
    cursor: pointer;
    letter-spacing: 1px;
    transition: background 0.2s;
  }}
  button:hover {{ background: #aa1111; }}
  #done {{
    display: none;
    flex-direction: column;
    align-items: center;
    gap: 16px;
    color: #4caf50;
    font-size: 1.3rem;
    font-weight: bold;
    margin-top: 40px;
  }}
</style>
</head>
<body>
{banner_html}
<h2>SELECT YOUR OPTIONS</h2>
<form id="form">
  <div class="grid">
    <div class="col">
      <h3>Default Apps</h3>
      <label><input type="checkbox" name="defaultapps" value="0" checked> Wine</label>
      <label><input type="checkbox" name="defaultapps" value="1" checked> Chrome</label>
      <label><input type="checkbox" name="defaultapps" value="2" checked> Xarchiver</label>
      <label><input type="checkbox" name="defaultapps" value="3" checked> Discord</label>
      <label><input type="checkbox" name="defaultapps" value="4" checked> Steam</label>
      <label><input type="checkbox" name="defaultapps" value="5" checked> Minecraft</label>
    </div>
    <div class="col">
      <h3>Programming</h3>
      <label><input type="checkbox" name="programming" value="0"> OpenJDK 8 (jre)</label>
      <label><input type="checkbox" name="programming" value="1"> OpenJDK 17 (jre)</label>
      <label><input type="checkbox" name="programming" value="2"> VSCodium</label>
    </div>
    <div class="col">
      <h3>Apps</h3>
      <label><input type="checkbox" name="apps" value="0"> VLC</label>
      <label><input type="checkbox" name="apps" value="1"> LibreOffice</label>
      <label><input type="checkbox" name="apps" value="2"> Synaptic</label>
      <label><input type="checkbox" name="apps" value="3"> AQemu (VMs)</label>
      <label><input type="checkbox" name="apps" value="4"> TLauncher</label>
    </div>
  </div>
  <div class="de-row">
    <label for="de">Desktop Environment</label>
    <select id="de" name="de">
      <option>KDE Plasma (Heavy)</option>
      <option>XFCE4 (Lightweight)</option>
      <option>I3 (Very Lightweight)</option>
      <option>GNOME 42 (Very Heavy)</option>
      <option>Cinnamon</option>
      <option>LXQT</option>
    </select>
  </div>
  <button type="submit">INSTALL NOW</button>
</form>
<div id="done">
  ✓ Options saved! Return to the terminal to continue installation.
</div>
<script>
document.getElementById('form').addEventListener('submit', async function(e) {{
  e.preventDefault();
  const fd = new FormData(this);
  const data = {{
    defaultapps: fd.getAll('defaultapps').map(Number),
    programming: fd.getAll('programming').map(Number),
    apps: fd.getAll('apps').map(Number),
    enablekvm: true,
    DE: fd.get('de')
  }};
  await fetch('/install', {{method:'POST', headers:{{'Content-Type':'application/json'}}, body: JSON.stringify(data)}});
  document.getElementById('form').style.display = 'none';
  document.getElementById('done').style.display = 'flex';
}});
</script>
</body>
</html>"""

class Handler(http.server.BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def do_GET(self):
        banner_b64 = get_banner_b64()
        if banner_b64:
            banner_html = f'<img class="banner" src="data:image/png;base64,{banner_b64}">'
        else:
            banner_html = '<h1 style="color:#cc2222;margin-bottom:32px;">KSF On Codespaces</h1>'
        page = HTML.format(banner_html=banner_html)
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(page.encode())

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)
        data = json.loads(body)
        with open("options.json", "w") as f:
            json.dump(data, f)
        self.send_response(200)
        self.end_headers()
        DONE.set()

if __name__ == "__main__":
    server = http.server.HTTPServer(("0.0.0.0", PORT), Handler)
    print(f"\n>>> Opening installer in browser on port {PORT}...")
    print(f">>> If it doesn't open, go to: http://localhost:{PORT}\n")
    threading.Timer(1.5, lambda: webbrowser.open(f"http://localhost:{PORT}")).start()
    while not DONE.is_set():
        server.handle_request()
    server.server_close()
    print(">>> Options saved. Continuing installation...\n")