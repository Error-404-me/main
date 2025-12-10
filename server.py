from flask import Flask, request, jsonify, render_template
from datetime import datetime

app = Flask(__name__)

computers = {}  # stores info from all PCs

@app.route("/update", methods=["POST"])
def update():
    data = request.json
    pc = data["pc"]
    data["last"] = datetime.now().strftime("%H:%M:%S")
    computers[pc] = data
    return jsonify({"message": "ok"})

@app.route("/")
def dashboard():
    total = 30
    in_use = sum(1 for c in computers.values() if c["status"] == "in_use")
    not_used = total - in_use

    return render_template(
        "dashboard.html",
        computers=computers,
        total=total,
        in_use=in_use,
        not_used=not_used
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)