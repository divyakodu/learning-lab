import requests


def test_list_resumes_contains_known_slug(base_url, known_slug):
    resp = requests.get(f"{base_url}/api/resumes")
    assert resp.status_code == 200
    items = resp.json()
    assert isinstance(items, list)
    assert any(r["slug"] == known_slug for r in items)


def test_list_resumes_summary_shape(base_url):
    resp = requests.get(f"{base_url}/api/resumes")
    for r in resp.json():
        assert set(r.keys()) == {"slug", "name", "headline"}


def test_get_resume_detail(base_url, known_slug):
    resp = requests.get(f"{base_url}/api/resumes/{known_slug}")
    assert resp.status_code == 200
    body = resp.json()
    assert body["slug"] == known_slug
    for field in ("name", "headline", "contact", "summary", "skills", "experience"):
        assert field in body


def test_get_resume_not_found(base_url):
    resp = requests.get(f"{base_url}/api/resumes/does-not-exist")
    assert resp.status_code == 404
