import psutil
import wmi
import time
import datetime
import requests

# Track seen processes
SEEN_PIDS = set()

# -------- RISK RULES -------- #
SUSPICIOUS_NAMES = ["powershell.exe", "cmd.exe"]
SAFE_NAMES = ["chrome.exe", "msedge.exe", "explorer.exe", "code.exe"]

# -------- SEND ALERT -------- #
def send_alert(alert):
    try:
        requests.post("http://127.0.0.1:5000/api/logs", json=alert)
    except Exception as e:
        print("Error sending alert:", e)

# -------- GET PROCESSES -------- #
def get_processes():
    processes = {}
    for p in psutil.process_iter(['pid', 'ppid', 'name', 'exe']):
        try:
            processes[p.info['pid']] = p.info
        except:
            continue
    return processes

# -------- DETECT ALL APPS -------- #
def detect_all_processes(processes):
    alerts = []

    for pid, info in processes.items():
        if pid in SEEN_PIDS:
            continue

        SEEN_PIDS.add(pid)

        name = (info['name'] or "").lower()
        path = (info.get('exe') or "").lower()

        risk = "LOW"

        # HIGH risk
        if any(x in name for x in SUSPICIOUS_NAMES):
            risk = "HIGH"

        # MEDIUM risk
        elif "temp" in path or "appdata" in path:
            risk = "MEDIUM"

        # LOW risk (default)
        elif name in SAFE_NAMES:
            risk = "LOW"

        alerts.append({
            "type": "process",
            "message": name,
            "risk": risk,
            "timestamp": str(datetime.datetime.now())
        })

    return alerts

# -------- MAIN LOOP -------- #
def monitor():
    print("Monitoring started...\n")

    while True:
        processes = get_processes()

        alerts = detect_all_processes(processes)

        for alert in alerts:
            send_alert(alert)
            print(f"[{alert['risk']}] {alert['message']}")

        time.sleep(5)

# -------- RUN -------- #
if __name__ == "__main__":
    monitor()
