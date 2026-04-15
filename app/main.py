import json
import sys
import copy
from parser import classify_logs

import time
from parser import classify_single_log

from ai_engine import generate_insight

# --------------------for real time monitoring--------------------
def monitor_logs(file_path):
    counts = {
        "ERROR": 0,
        "WARNING": 0,
        "INFO": 0,
        "OTHER": 0
    }

    alert_triggered = False  # ✅ prevent spam

    with open(file_path, "r") as file:
        file.seek(0, 2)

        print("🔄 Monitoring logs in real-time...\n")

        while True:
            line = file.readline()

            if not line:
                time.sleep(1)
                continue

            line = line.strip()
            if not line:
                continue

            log_type = classify_single_log(line)
            counts[log_type] += 1

            # 🔥 PRINT LOG
            print(f"[{log_type}] {line.replace(log_type + ': ', '').strip()}")

            # 🔥 ADD AI HERE (THIS IS THE CHANGE)
            insight = generate_insight(line)
            print(f"💡 AI Insight: {insight}")

            # 🚨 Alert logic
            if counts["ERROR"] >= 2:
                print("🚨 CRITICAL ALERT: Multiple errors detected!")
                counts["ERROR"] = 0


def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <log_file> [--realtime]")
        return

    log_file = sys.argv[1]

    # 🔥 NEW: mode selection
    if len(sys.argv) == 3 and sys.argv[2] == "--realtime":
        monitor_logs(log_file)
        return

    logs = classify_logs(log_file)

    # 🔹 Build report (single source of truth)
    report = "\n--------- LOG ANALYSIS ---------\n"

    # 1. Add log details
    for level, messages in logs.items():
        report += f"\n{level}:\n"
        for msg in messages:
            report += msg + "\n"

    # 2. Add summary
    report += "\n--------- SUMMARY ---------\n"
    for level, messages in logs.items():
        report += f"{level}: {len(messages)}\n"

    # 3. Add alert logic
    error_count = len(logs["ERROR"])
    warning_count = len(logs["WARNING"])

    if error_count >= 2:
        alert = "🚨 CRITICAL ALERT: Multiple errors detected!"
        report += "\n" + alert + "\n"
    elif error_count > 0:
        alert = "⚠️ WARNING: Errors detected."
        report += "\n" + alert + "\n"
    elif warning_count >= 2:
        alert = "⚠️ WARNING: Multiple warnings detected."
        report += "\n" + alert + "\n"
    else:
        alert = "✅ System looks stable."
        report += "\n" + alert + "\n"

    # 🔹 Print to terminal
    print(report)

    # 🔹 Save to file
    with open("report.txt", "w", encoding="utf-8") as file:
        file.write(report)

    print("Report saved as report.txt")

    summary = {}
    for level, messages in logs.items():
        summary[level] = len(messages)

    json_data = copy.deepcopy(logs)
    json_data["SUMMARY"] = summary

    with open("report.json", "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=4)

if __name__ == "__main__":
    main()

