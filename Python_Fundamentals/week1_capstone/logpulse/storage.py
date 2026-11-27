# File storage

from pathlib import Path

import json

BASE_DIR = Path(__file__).resolve().parent.parent

def write_log(logs: str, folder_name: str = "logs", file_name: str = "sample_access.log") -> str :

    log_dir = Path(f"{BASE_DIR}/{folder_name}")  # .. - is the parent folder
    log_dir.mkdir(parents=True, exist_ok=True) # Parents = True is for safety if parents also missing   
    
    log_file = log_dir/file_name # File creation path


    try :

        with log_file.open(mode="a",encoding="utf-8") as f:
            f.write(f"{logs}\n")
    except FileNotFoundError as e:
        return f"Warning : {e} - Log updation failed"

    else:
        return "Log updation completed"

def clear_log(folder_name: str = "logs", file_name : str = "sample_access.log") -> str:

    log_file = Path(f"{BASE_DIR}/{folder_name}/{file_name}")

    try:
        with log_file.open(mode="w") as f:
            f.write("")
    except FileNotFoundError as e:
        return f"Error: {e}"
    else:
        return "Log Cleared"

def read_log_lines(folder_name: str = "logs", file_name : str = "sample_access.log") -> list[str]:

    log_file = Path(f"{BASE_DIR}/{folder_name}/{file_name}")
    log_data = []

    try:
        with log_file.open(mode="r", encoding="utf-8") as f:
            for line in f:
                clean_line = line.strip()
                if clean_line:
                    log_data.append(clean_line)
    except FileNotFoundError as e:
        print(f"Error : File missing - {e}")
        return []

    else:
        return log_data


def export_json_report(report_data: dict[str, object], folder_name: str = "reports", file_name : str = "report_output.json",):

    report_dir = BASE_DIR/ folder_name
    report_dir.mkdir(parents=True, exist_ok=True)

    report_file = report_dir / file_name
    try:
        with report_file.open(mode="w", encoding="utf-8") as f:
            json.dump(report_data,f, indent=2)
    except OSError or TypeError:
        print("Got issues with the report_data writing")

    else:
        return f"Report exported successfully to {report_file}"


    



if __name__ == "__main__":

    data_logs = """2026-11-19T09:00:01 | GET | /api/v1/health | 200 | 12.4
2026-11-19T09:01:15 | POST | /api/v1/login | 200 | 145.0
2026-11-19T09:02:30 | POST | /api/v1/login | 401 | 88.2
2026-11-19T09:03:10 | GET | /api/v1/users | 200 | 310.5
CORRUPTED_LINE_MISSING_FIELDS
2026-11-19T09:05:00 | GET | /api/v1/orders | 500 | 640.8
2026-11-19T09:06:22 | PUT | /api/v1/users | 200 | 190.0
2026-11-19T09:07:45 | GET | /api/v1/products | 200 | 95.3
2026-11-19T09:08:12 | DELETE | /api/v1/orders | 403 | 42.1
2026-11-19T09:09:00 | GET | /api/v1/orders | NOT_A_NUMBER | 120.0
2026-11-19T09:10:18 | GET | /api/v1/reports | 200 | 480.2
2026-11-19T09:11:05 | POST | /api/v1/orders | 201 | 215.6
"""

    print(write_log(data_logs))
    # print(clear_log())

    print(read_log_lines())



    













