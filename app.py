from flask import Flask, request, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import re

app = Flask(__name__)
sched = BackgroundScheduler(); sched.start()
DB = []

def remind(user, med):
    print(f"[MED-REMINDER] @{user}: Take {med['name']} dose {med['dose']}")

@app.post("/meds")
def add_med():
    data = request.json   # {user,name,dose,time:"2025-08-16T19:30:00"}
    DB.append(data)
    t = datetime.fromisoformat(data["time"])
    sched.add_job(remind,'date',run_date=t,args=[data["user"],data])
    return {"ok":True}

@app.post("/info")
def info():
    q = request.json.get("q","")
    # Very simple, static info map
    if re.search(r"headache|migraine",q, re.I):
        return jsonify({"info":"Stay hydrated, rest; if persistent or severe, consult a doctor."})
    return jsonify({"info":"I can offer general wellness info and reminders—not medical diagnosis."})

if __name__ == "__main__":
    app.run(port=5052)
