from logpulse.storage import export_json_report

def records_to_dicts(records: list[tuple[str, str, str, int, float]]) -> list[dict[str, str | int | float]] :
    LOG_COLUMNS = ("timestamp", "method", "endpoint", "status", "latency_ms")

    dict_records = list(map(lambda row: dict(zip(LOG_COLUMNS, row, strict=True)),records))

    return dict_records


def get_error_logs(logs: list[dict[str, str | int | float]]) -> list[dict[str, str | int | float]]:

    error_logs = list(filter(lambda l : l["status"] >= 400,logs))

    return error_logs







def calculate_avg_latency(logs: list[dict[str, str | int | float]]) -> float:

    if not logs:
        return 0.0

    latency_values = list(map(lambda d : d["latency_ms"], logs))

    return round(sum(latency_values) / len(latency_values),2)


def get_slowest_requests( logs: list[dict[str, str | int | float]], top_n: int = 3) -> list[dict[str, str | int | float]]:
    slowest = sorted(logs, key = lambda la : la["latency_ms"],reverse=True)
    return slowest[:top_n]


def get_sla_violations (logs: list[dict[str, str | int | float]], threshold_ms: float = 250.0) -> list[str]:
    return [f"{log["method"]} {log["endpoint"].removeprefix('/api/v1')} ({log["latency_ms"]} ms)"for log in logs if log["latency_ms"] > threshold_ms]


def build_health_report(logs: list[dict[str, str | int | float]], corrupted_count: int) -> dict[str, object] :
    unique_endpoints = {log["endpoint"] for log in logs}

    unique_endpoints = sorted(unique_endpoints)

    endpoint_hit_counts = {ep: sum(1 for log in logs if log["endpoint"] == ep) for ep in unique_endpoints}

    errors = get_error_logs(logs)
    error_rate = round((len(errors)/len(logs))* 100,2) if logs else 0.0

    #check for 5xx server crashes and classify system_status

    has_server_error = any(err["status"] >=500 for err in errors)

    if error_rate >= 25.0 or has_server_error:
        system_status = "CRITICAL"
    elif error_rate > 0.0:
        system_status = "DEGRADED"
    else:
        system_status = "HEALTHY"

    return {
        "system_status" : system_status,
        "total_valid_requests" : len(logs),
        "corrupted_lines_skipped" : corrupted_count,
        "error_count" : len(errors),
        "error_percent" : error_rate,
        "avg_latency_ms": calculate_avg_latency(logs),
        "unique_endpoints" : unique_endpoints,
        "endpoint_hit_counts" : endpoint_hit_counts,
        "sla_violations" : get_sla_violations(logs),
        "top_slowest_requests" : get_slowest_requests(logs)
    }

if __name__ == "__main__":
    d = [('2026-11-19T09:00:01', 'GET', '/api/v1/health', 200, 12.4), ('2026-11-19T09:01:15', 'POST', '/api/v1/login', 200, 145.0), ('2026-11-19T09:02:30', 'POST', '/api/v1/login', 401, 88.2), ('2026-11-19T09:03:10', 'GET', '/api/v1/users', 200, 310.5), ('2026-11-19T09:05:00', 'GET', '/api/v1/orders', 500, 640.8), ('2026-11-19T09:06:22', 'PUT', '/api/v1/users', 200, 190.0), ('2026-11-19T09:07:45', 'GET', '/api/v1/products', 200, 95.3), ('2026-11-19T09:08:12', 'DELETE', '/api/v1/orders', 403, 42.1), ('2026-11-19T09:10:18', 'GET', '/api/v1/reports', 200, 480.2), ('2026-11-19T09:11:05', 'POST', '/api/v1/orders', 201, 215.6)]

    dict_vals = records_to_dicts(d)
    info = get_error_logs(dict_vals)
    print(info)
    print("\n")
    print(calculate_avg_latency(dict_vals))
    print()
    print(get_slowest_requests(dict_vals))
    print()
    print(get_sla_violations(dict_vals))
    print()
    report = build_health_report(dict_vals,2)
    print(report)
    print(export_json_report(report))

