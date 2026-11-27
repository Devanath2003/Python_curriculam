# Instead of writing four seperate import lines in main.py
# re-export our main package functions inside logpulse/__init__.py

from logpulse.analyzer import(
    build_health_report,
    get_error_logs,
    get_sla_violations,
    records_to_dicts
)

from logpulse.storage import export_json_report, read_log_lines
from logpulse.parser import parse_logs

__all__ = [
    "build_health_report",
    "export_json_report",
    "get_error_logs",
    "get_sla_violations",
    "parse_logs",
    "read_log_lines",
    "records_to_dicts",
]

# This is a standard Python list of strings that tells VS code and Python
# as These are the official public functions this package exposes


