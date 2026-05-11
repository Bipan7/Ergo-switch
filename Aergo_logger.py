import csv
import os
from datetime import datetime

# Log file path
LOG_FILE = "inspection_log.csv"


# -------------------------------
# INIT LOG FILE (CREATE HEADER)
# -------------------------------
def init_log():
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, mode="w", newline="") as file:
            writer = csv.writer(file)

            writer.writerow([
                "Timestamp",
                "Selected_Type",
                "Final_Result",
                "Switch",
                "Button1",
                "Button2",
                "Button3",
                "Symbol1",
                "Symbol2",
                "Symbol3"
            ])


# -------------------------------
# SAVE LOG ENTRY
# -------------------------------
def save_log(selected_type, final, roi_status):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(LOG_FILE, mode="a", newline="") as file:
        writer = csv.writer(file)

        writer.writerow([
            timestamp,
            selected_type,
            final,
            roi_status.get("switch"),
            roi_status.get("button1"),
            roi_status.get("button2"),
            roi_status.get("button3"),
            roi_status.get("symbol1"),
            roi_status.get("symbol2"),
            roi_status.get("symbol3"),
        ])