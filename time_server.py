import wsgiref.simple_server
import json
from datetime import datetime
from pytz import timezone, all_timezones, utc

# Укажите временную зону сервера
SERVER_TIMEZONE = "UTC"

def application(environ, start_response):
    path = environ["PATH_INFO"]
    method = environ["REQUEST_METHOD"]

    if method == "GET":
        if path == "/":
            current_time = datetime.now(timezone(SERVER_TIMEZONE)).strftime("%Y-%m-%d %H:%M:%S")
            start_response("200 OK", [("Content-Type", "text/html")])
            return [f"<h1>Current server time: {current_time}</h1>".encode("utf-8")]
        elif path.startswith("/") and path[1:] in all_timezones:
            tz_name = path[1:]
            current_time = datetime.now(timezone(tz_name)).strftime("%Y-%m-%d %H:%M:%S")
            start_response("200 OK", [("Content-Type", "text/html")])
            return [f"<h1>Current time in {tz_name}: {current_time}</h1>".encode("utf-8")]
        else:
            start_response("404 Not Found", [("Content-Type", "text/plain")])
            return [b"Timezone not found"]

    elif method == "POST":
        try:
            content_length = int(environ.get("CONTENT_LENGTH", 0))
            request_body = environ["wsgi.input"].read(content_length).decode("utf-8")
            data = json.loads(request_body)
        except (ValueError, json.JSONDecodeError):
            start_response("400 Bad Request", [("Content-Type", "application/json")])
            return [json.dumps({"error": "Invalid JSON input"}).encode("utf-8")]

        if path == "/api/v1/time":
            tz_name = data.get("tz", SERVER_TIMEZONE)
            if tz_name not in all_timezones:
                start_response("400 Bad Request", [("Content-Type", "application/json")])
                return [json.dumps({"error": "Invalid timezone"}).encode("utf-8")]
            current_time = datetime.now(timezone(tz_name)).strftime("%Y-%m-%d %H:%M:%S")
            start_response("200 OK", [("Content-Type", "application/json")])
            return [json.dumps({"time": current_time}).encode("utf-8")]

        elif path == "/api/v1/date":
            tz_name = data.get("tz", SERVER_TIMEZONE)
            if tz_name not in all_timezones:
                start_response("400 Bad Request", [("Content-Type", "application/json")])
                return [json.dumps({"error": "Invalid timezone"}).encode("utf-8")]
            current_date = datetime.now(timezone(tz_name)).strftime("%Y-%m-%d")
            start_response("200 OK", [("Content-Type", "application/json")])
            return [json.dumps({"date": current_date}).encode("utf-8")]

        elif path == "/api/v1/datediff":
            try:
                start_data = data["start"]
                end_data = data["end"]
                start_date = datetime.strptime(start_data["date"], "%m.%d.%Y %H:%M:%S")
                end_date = datetime.strptime(end_data["date"], "%m.%d.%Y %H:%M:%S")
                start_tz = timezone(start_data.get("tz", SERVER_TIMEZONE))
                end_tz = timezone(end_data.get("tz", SERVER_TIMEZONE))
                start_date = start_tz.localize(start_date).astimezone(utc)
                end_date = end_tz.localize(end_date).astimezone(utc)
                diff = end_date - start_date
                start_response("200 OK", [("Content-Type", "application/json")])
                return [json.dumps({"difference": str(diff)}).encode("utf-8")]
            except (KeyError, ValueError):
                start_response("400 Bad Request", [("Content-Type", "application/json")])
                return [json.dumps({"error": "Invalid date format"}).encode("utf-8")]

    start_response("404 Not Found", [("Content-Type", "text/plain")])
    return [b"Not found"]

if __name__ == "__main__":
    with wsgiref.simple_server.make_server("", 8000, application) as server:
        print("Serving on port 8000...")
        server.serve_forever()
