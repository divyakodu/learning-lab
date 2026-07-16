import requests


def test_health_round_robins_across_both_backends(base_url):
    instances = {requests.get(f"{base_url}/api/health").json()["instance"] for _ in range(10)}
    assert instances == {"backend1", "backend2"}


def test_served_by_header_present(base_url):
    resp = requests.get(f"{base_url}/api/health")
    assert "X-Served-By" in resp.headers
