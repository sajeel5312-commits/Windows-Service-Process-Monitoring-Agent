from flask import Flask, jsonify, render_template, request
from database import init_db, insert_alert, search_alerts

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

# ✅ SINGLE correct alerts route
@app.route("/api/alerts")
def alerts():
    risk = request.args.get("risk")
    query = request.args.get("query")

    data = search_alerts(risk=risk, query=query)
    return jsonify(data)

@app.route("/api/logs", methods=["POST"])
def receive_logs():
    data = request.json

    if data:
        insert_alert(data)

    return {"status": "received"}

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
