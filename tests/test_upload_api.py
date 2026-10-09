
from fastapi.testclient import TestClient

from backend.config import MAX_UPLOAD_SIZE
from backend.main import app
from backend.routes import reports


client = TestClient(app)


def test_upload_report_succeeds(
    isolated_database,
    tmp_path,
    monkeypatch,
):
    def fake_save_file(content, extension):
        path = tmp_path / f"stored{extension}"
        path.write_bytes(content)
        return path

    monkeypatch.setattr(
        reports.storage,
        "save_file",
        fake_save_file,
    )

    content = b"%PDF-1.4 test report"

    response = client.post(
        "/api/v1/reports/upload",
        files={
            "file": (
                "report.pdf",
                content,
                "application/pdf",
            )
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["filename"] == "report.pdf"
    assert data["file_type"] == "pdf"
    assert data["size_bytes"] == len(content)
    assert data["status"] == "uploaded"


def test_upload_rejects_unsupported_extension(
    isolated_database,
):
    response = client.post(
        "/api/v1/reports/upload",
        files={
            "file": (
                "report.txt",
                b"report content",
                "text/plain",
            )
        },
    )

    assert response.status_code == 400
    assert "Unsupported file type" in response.json()["detail"]


def test_upload_rejects_empty_file(
    isolated_database,
):
    response = client.post(
        "/api/v1/reports/upload",
        files={
            "file": (
                "report.pdf",
                b"",
                "application/pdf",
            )
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Uploaded file is empty."


def test_upload_rejects_oversized_file(
    isolated_database,
    monkeypatch,
):
    def unexpected_save(*args, **kwargs):
        raise AssertionError("Oversized file must not be saved.")

    monkeypatch.setattr(
        reports.storage,
        "save_file",
        unexpected_save,
    )

    response = client.post(
        "/api/v1/reports/upload",
        files={
            "file": (
                "large-report.pdf",
                b"x" * (MAX_UPLOAD_SIZE + 1),
                "application/pdf",
            )
        },
    )

    assert response.status_code == 400
    assert "10 MB size limit" in response.json()["detail"]
