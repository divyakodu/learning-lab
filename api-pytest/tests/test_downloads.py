import requests


def test_pdf_download(base_url, known_slug):
    resp = requests.get(f"{base_url}/api/resumes/{known_slug}/pdf")
    assert resp.status_code == 200
    assert resp.headers["content-type"] == "application/pdf"
    assert resp.content[:4] == b"%PDF"


def test_docx_download(base_url, known_slug):
    resp = requests.get(f"{base_url}/api/resumes/{known_slug}/docx")
    assert resp.status_code == 200
    assert (
        resp.headers["content-type"]
        == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
    assert resp.content[:2] == b"PK"  # docx is a zip container


def test_pdf_download_unknown_slug_is_404(base_url):
    resp = requests.get(f"{base_url}/api/resumes/does-not-exist/pdf")
    assert resp.status_code == 404
