import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi.testclient import TestClient

from app.main import app
from app.database.session import get_db
from tests.test_auth_and_users import override_get_db, setup_db

# Use same DB session overrides
app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture
def auth_headers():
    # Register and login a user to get auth headers
    reg_payload = {
        "email": "endpoint_user@example.com",
        "password": "secretpassword",
        "full_name": "Endpoint Tester"
    }
    client.post("/api/v1/auth/register", json=reg_payload)
    login_response = client.post("/api/v1/auth/login", json={
        "email": "endpoint_user@example.com",
        "password": "secretpassword"
    })
    token = login_response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_files_endpoints(auth_headers):
    # 1. Upload file (simulate multipart)
    file_content = b"Python developer with 5 years experience."
    files = {"file": ("resume.txt", file_content, "text/plain")}
    response = client.post("/api/v1/files/upload", files=files, headers=auth_headers)
    assert response.status_code == 201
    file_id = response.json()["id"]
    assert file_id is not None

    # 2. Get file metadata
    get_response = client.get(f"/api/v1/files/{file_id}", headers=auth_headers)
    assert get_response.status_code == 200
    assert get_response.json()["data"]["filename"] == "resume.txt"

    # 3. List files
    list_response = client.get("/api/v1/files", headers=auth_headers)
    assert list_response.status_code == 200
    assert len(list_response.json()["data"]["files"]) >= 1

    # 4. Delete file
    del_response = client.delete(f"/api/v1/files/{file_id}", headers=auth_headers)
    assert del_response.status_code == 200
    assert del_response.json()["data"]["deleted"] is True


def test_resume_endpoints(auth_headers):
    # 1. Upload raw resume
    payload = {"payload": {"resume_text": "Experienced engineer"}}
    response = client.post("/api/v1/resume/upload", json=payload, headers=auth_headers)
    assert response.status_code == 201
    resume_id = response.json()["id"]

    # 2. Parse resume
    parse_payload = {"resume_text": "Python, FastAPI, AWS", "metadata": {}}
    parse_response = client.post("/api/v1/resume/parse", json=parse_payload, headers=auth_headers)
    assert parse_response.status_code == 200
    assert "skills" in parse_response.json()["data"]["sections"]

    # 3. Get resume
    get_response = client.get(f"/api/v1/resume/{resume_id}", headers=auth_headers)
    assert get_response.status_code == 200

    # 4. Update resume
    update_payload = {"payload": {"resume_text": "Updated resume text"}}
    up_response = client.put(f"/api/v1/resume/{resume_id}", json=update_payload, headers=auth_headers)
    assert up_response.status_code == 200

    # 5. List resumes
    list_response = client.get("/api/v1/resume", headers=auth_headers)
    assert list_response.status_code == 200

    # 6. Delete resume
    del_response = client.delete(f"/api/v1/resume/{resume_id}", headers=auth_headers)
    assert del_response.status_code == 200


def test_job_endpoints(auth_headers):
    # 1. Upload job description
    payload = {"payload": {"description": "React Developer role"}}
    response = client.post("/api/v1/job/upload", json=payload, headers=auth_headers)
    assert response.status_code == 201
    job_id = response.json()["id"]

    # 2. Parse job
    parse_payload = {"job_description": "React, TypeScript, 3 years experience", "metadata": {}}
    parse_response = client.post("/api/v1/job/parse", json=parse_payload, headers=auth_headers)
    assert parse_response.status_code == 200

    # 3. Get job
    get_response = client.get(f"/api/v1/job/{job_id}", headers=auth_headers)
    assert get_response.status_code == 200

    # 4. List jobs
    list_response = client.get("/api/v1/job", headers=auth_headers)
    assert list_response.status_code == 200

    # 5. Delete job
    del_response = client.delete(f"/api/v1/job/{job_id}", headers=auth_headers)
    assert del_response.status_code == 200


def test_company_endpoints(auth_headers):
    # 1. Analyze company
    payload = {"payload": {"company_name": "Google", "job_description": "SRE Role"}}
    response = client.post("/api/v1/company/analyze", json=payload, headers=auth_headers)
    assert response.status_code == 201
    company_id = response.json()["id"]

    # 2. Get company
    get_response = client.get(f"/api/v1/company/{company_id}", headers=auth_headers)
    assert get_response.status_code == 200


def test_match_endpoints(auth_headers):
    payload = {"payload": {"resume_text": "Python, FastAPI", "job_description": "FastAPI engineer"}}

    # Skills matching
    response = client.post("/api/v1/match/skills", json=payload, headers=auth_headers)
    assert response.status_code == 200

    # Experience matching
    response = client.post("/api/v1/match/experience", json=payload, headers=auth_headers)
    assert response.status_code == 200

    # Overall matching
    response = client.post("/api/v1/match/overall", json=payload, headers=auth_headers)
    assert response.status_code == 200


def test_public_actions(auth_headers):
    # Rank projects
    response = client.post(
        "/api/v1/projects/rank",
        json={"payload": {"projects": ["projectA", "projectB"], "job_description": "React Developer"}},
        headers=auth_headers
    )
    assert response.status_code == 200

    # Write resume
    response = client.post(
        "/api/v1/writer/resume",
        json={"payload": {"profile": {"skills": ["Python"]}, "target_role": "Backend Engineer"}},
        headers=auth_headers
    )
    assert response.status_code == 200


@patch("app.workflows.candidate_screening.get_gemini_chat")
def test_workflows_and_history(mock_get_gemini, auth_headers):
    # Mock the LLM return value for candidate screening
    mock_chat = MagicMock()
    mock_chat.ainvoke = AsyncMock(return_value=MagicMock(content="Candidate is an excellent match."))
    mock_get_gemini.return_value = mock_chat

    # 1. Candidate screening workflow
    screen_payload = {
        "candidate_text": "Python senior engineer with FastAPI expertise.",
        "job_description": "Looking for Senior FastAPI developer."
    }
    response = client.post("/api/v1/workflows/candidate-screening", json=screen_payload, headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["fit_summary"] == "Candidate is an excellent match."
    assert response.json()["recommendation"] == "shortlist"

    # 2. Resume optimization workflow
    opt_payload = {
        "resume_text": "SRE engineer, Docker, Kubernetes.",
        "job_description": "Kubernetes admin.",
        "company_name": "Tech Corp",
        "candidate_name": "John Doe",
        "target_role": "DevOps Lead",
        "max_rewrites": 1
    }
    opt_response = client.post("/api/v1/workflows/resume-optimization", json=opt_payload, headers=auth_headers)
    assert opt_response.status_code == 200
    assert opt_response.json()["final_resume"] is not None

    # 3. List history to verify records are created
    hist_response = client.get("/api/v1/history", headers=auth_headers)
    assert hist_response.status_code == 200
    assert hist_response.json()["data"]["total"] >= 2
    history_id = hist_response.json()["data"]["history"][0]["id"]

    # 4. Get history item
    get_hist = client.get(f"/api/v1/history/{history_id}", headers=auth_headers)
    assert get_hist.status_code == 200

    # 5. Delete history item
    del_hist = client.delete(f"/api/v1/history/{history_id}", headers=auth_headers)
    assert del_hist.status_code == 200


def test_dashboard_endpoint(auth_headers):
    response = client.get("/api/v1/dashboard", headers=auth_headers)
    assert response.status_code == 200
    assert "stats" in response.json()["data"]


def test_agents_endpoints(auth_headers):
    # List agents
    response = client.get("/api/v1/agents", headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json()["agents"]) > 0

    # Get info
    response = client.get("/api/v1/agents/resume-parser", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["alias"] == "resume-parser"

    # Run agent
    response = client.post(
        "/api/v1/agents/resume-parser/run",
        json={"payload": {"resume_text": "My resume skills: Python, SQL"}},
        headers=auth_headers
    )
    assert response.status_code == 200
    assert "sections" in response.json()["result"]
