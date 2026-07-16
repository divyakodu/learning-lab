import requests


def test_health_ok(base_url):
    resp = requests.get(f"{base_url}/api/health")
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "ok"
    assert "instance" in body
