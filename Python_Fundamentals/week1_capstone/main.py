from logpulse import (
    build_health_report,
    export_json_report,
    get_error_logs,
    parse_logs,
    read_log_lines,
    records_to_dicts
)


# DISPLAY HELPERS: Keep printing logic separate from menu logic

def show_summary(report: dict[str,object]) -> None:
    print("\n--- SYSTEM HEALTH SUMMARY---")
    print(f"{'System Status:':<26} {report['system_status']}")
    print(f"{'Valid Requests:':<26} {report["total_valid_requests"]}")
    print(f"{'Corrupted Lines Skipped':<26} {report["corrupted_lines_skipped"]}")
    print(f"{'Error Count':<26} {report["error_count"]}")
    print(f"{'Error Rate (%)':<26} {report["error_percent"]}%")
    print(f"{'Average Latency':<26} {report["avg_latency_ms"]}ms")


def show_errors(logs: list[dict[str, str | int | float]]) -> None:
    errors = get_error_logs(logs)
    print(f"\n---CRITICAL ERRORS ({len(errors)} found)--- ")
    for err in errors:
        print(f"[{err["timestamp"]}] {err["method"]} {err["endpoint"]} -> HTTP {err["status"]}")

def show_slow_requests(report: dict[str, object]) -> None:
    print("\n--- SLA VIOLATIONS (>250ms) ---")
    for violation in report["sla_violations"]:
        print(f"    * {violation}")


    print("\n--- TOP 3 SLOWEST REQUSTS ---")
    for req in report["top_slowest_requests"]:
        print(f"    * {req['method']} {req['endpoint']}ms (HTTP {req['status']})")

def main() -> None:
    #read raw_lines from the disk

    raw_lines = read_log_lines()
    if not raw_lines:
        print("No log lines found. Check your logs/sample_acces.log file.")
        return
    # Parse and analyze once at startup

    valid_tuples, skipped_count = parse_logs(raw_lines)
    logs = records_to_dicts(valid_tuples)
    report = build_health_report(logs, skipped_count)

    # Interctive CLI loop

    while True:
        print("\n__________________________________________")

        print("\n   LOGPULSE SERVER ANALYZER ")
        print("1. View Sysem Health Summary")
        print("2. View Critical Errors (4xx/5xx)")
        print("3. View SLA Violations & Slowest Request")
        print("4. Export Report to JSON")
        print("5. Exit")
        print("\n__________________________________________")
        choice = input("\nSelect an option (1-5): ").strip()

        if choice == "1":
            show_summary(report)
        elif choice == "2":
            show_errors(logs)
        elif choice == "3":
            show_slow_requests(report)
        elif choice == "4":
            status_msg = export_json_report(report)
            print(f"\n{status_msg}")
        elif choice == "5":
            print("Exiting LogPulse ...")
            break
        else:
            print("Invalid option. Please enter a number between 1 and 5")

if __name__ == "__main__":
    main()