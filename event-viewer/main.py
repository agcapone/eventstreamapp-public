from flask import Flask, jsonify, request, render_template_string
import redis
import json

app = Flask(__name__)

from flask import redirect

@app.route('/')
def index():
    return redirect('/events', code=302)

# Conexión a Redis
r = redis.Redis(host='redis', port=6379)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Eventos recientes</title>
    <style>
        body { font-family: sans-serif; padding: 20px; }
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #ccc; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
    </style>
</head>
<body>
    <h2>Últimos {{ count }} eventos (cambio3)</h2>
    <table>
        <thead>
            <tr>
                {% for key in keys %}
                    <th>{{ key }}</th>
                {% endfor %}
            </tr>
        </thead>
        <tbody>
            {% for event in events %}
                <tr>
                    {% for key in keys %}
                        <td>{{ event.get(key, '') }}</td>
                    {% endfor %}
                </tr>
            {% endfor %}
        </tbody>
    </table>
</body>
</html>
"""

@app.route('/events', methods=['GET'])
def get_events():
    count = int(request.args.get('count', 10))
    raw_events = r.zrevrange('event_log', 0, count - 1)
    events = [json.loads(e.decode()) for e in raw_events]

    # Si acepta JSON, devolver JSON
    if "application/json" in request.headers.get("Accept", "") or request.args.get("format") == "json":
        return jsonify(events)

    # Si no, renderizar HTML
    keys = sorted({k for event in events for k in event.keys()})
    return render_template_string(HTML_TEMPLATE, events=events, keys=keys, count=len(events))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
