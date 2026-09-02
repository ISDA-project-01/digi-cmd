"""
PyWebView Dashboard Launcher
"""

import webview

def launch_webview():
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>DigiShell Web Interface</title>
        <style>
            body { background-color: #121212; color: #00ff66; font-family: monospace; padding: 20px; }
            h1 { color: #ffffff; }
            #output { border: 1px solid #333; padding: 10px; height: 300px; overflow-y: scroll; background: #000; }
            input { width: 100%; padding: 10px; background: #222; color: #fff; border: 1px solid #444; }
        </style>
    </head>
    <body>
        <h1>DigiShell AI Control Panel</h1>
        <p>Local Ollama Engine: qwen2.5:3b</p>
        <div id="output">DigiShell Web Dashboard Loaded.<br>Ready for instructions...</div>
        <br>
        <input type="text" placeholder="Enter command or natural language instruction..." />
    </body>
    </html>
    """
    webview.create_window('DigiShell AI Dashboard', html=html_content, width=900, height=600)
    webview.start()
