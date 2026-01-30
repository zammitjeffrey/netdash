from flask import Flask, request, render_template_string
import socket

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>NetDash</title>
    <style>
        body { font-family: sans-serif; text-align: center; padding-top: 50px; background-color: #f0f2f5; }
        .card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); display: inline-block; }
        h1 { color: #333; }
        p { color: #666; font-size: 1.2em; }
    </style>
</head>
<body>
    <div class="card">
        <h1>🌐 NetDash Network Info</h1>
        <p>Your IP Address: <strong>{{ user_ip }}</strong></p>
        <p>Server Hostname: <strong>{{ hostname }}</strong></p>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    user_ip = request.remote_addr
    hostname = socket.gethostname()
    return render_template_string(HTML_TEMPLATE, user_ip=user_ip, hostname=hostname)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)