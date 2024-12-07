import requests

BASE_URL = "http://127.0.0.1:8000"

def test_get_root():
    response = requests.get(BASE_URL + "/")
    print("GET / Response status:", response.status_code)
    print("GET / Response content:", response.text)
    assert response.status_code == 200
    print("GET /: Passed")

def test_get_timezone():
    response = requests.get(BASE_URL + "/Europe/Moscow")
    print("Response status:", response.status_code)
    print("Response content:", response.text)
    assert response.status_code == 200
    print("GET /Europe/Moscow: Passed")

def test_post_time():
    response = requests.post(BASE_URL + "/api/v1/time", json={"tz": "Europe/Moscow"})
    print("POST /api/v1/time Response status:", response.status_code)
    print("POST /api/v1/time Response content:", response.json())
    assert response.status_code == 200
    assert "time" in response.json()
    print("POST /api/v1/time: Passed")

def test_post_date():
    response = requests.post(BASE_URL + "/api/v1/date", json={"tz": "Europe/Moscow"})
    print("POST /api/v1/date Response status:", response.status_code)
    print("POST /api/v1/date Response content:", response.json())
    assert response.status_code == 200
    assert "date" in response.json()
    print("POST /api/v1/date: Passed")

def test_post_datediff():
    payload = {
        "start": {"date": "12.20.2021 22:21:05", "tz": "Europe/Moscow"},
        "end": {"date": "12.21.2021 22:21:05", "tz": "Europe/Moscow"}
    }
    response = requests.post(BASE_URL + "/api/v1/datediff", json=payload)
    print("POST /api/v1/datediff Response status:", response.status_code)
    print("POST /api/v1/datediff Response content:", response.json())
    assert response.status_code == 200
    assert "difference" in response.json()
    print("POST /api/v1/datediff: Passed")

if __name__ == "__main__":
    test_get_root()
    test_get_timezone()
    test_post_time()
    test_post_date()
    test_post_datediff()
