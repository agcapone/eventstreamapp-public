from flask import Flask, jsonify
import redis
import json

app = Flask(__name__)
r = redis.Redis(host='redis', port=6379)

@app.route('/events', methods=['GET'])
def get_events():
    keys = r.keys("event:*")
    events = [json.loads(r.get(k)) for k in keys]
    return jsonify(events)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
