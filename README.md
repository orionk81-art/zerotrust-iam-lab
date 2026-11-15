# ZeroTrust IAM Security Lab

An educational FastAPI demonstration of identity authentication, role-based access control (RBAC), audit logging, and automated authorization tests.

> **Security notice:** This first version uses hard-coded demonstration bearer tokens and an in-memory audit log. It is **not production-ready** and does **not** implement OAuth2 or OpenID Connect yet. Do not expose it to the public internet or use real credentials/data.

## Quick start (Windows PowerShell)

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m pytest -q
python -m uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000/docs for interactive API documentation.

## Demonstrate access control

```powershell
# Unauthenticated: 401
Invoke-WebRequest http://127.0.0.1:8000/documents

# Viewer reads: 200
Invoke-RestMethod http://127.0.0.1:8000/documents -Headers @{Authorization='Bearer demo-viewer-token'}

# Viewer writes: 403
Invoke-WebRequest http://127.0.0.1:8000/documents -Method Post -ContentType 'application/json' -Body '{"title":"test"}' -Headers @{Authorization='Bearer demo-viewer-token'}

# Admin writes: 201
Invoke-RestMethod http://127.0.0.1:8000/documents -Method Post -ContentType 'application/json' -Body '{"title":"approved"}' -Headers @{Authorization='Bearer demo-admin-token'}
```

## Architecture

Client -> Bearer token check -> RBAC policy -> Authorized endpoint or 403 + audit event

## Roadmap
- Replace demo tokens with standards-compliant OIDC identity provider and JWT verification
- Add persistent, tamper-resistant audit events
- Add least-privilege scopes and resource-level authorization
- Add security scans, dependency pinning, threat modeling, and AWS deployment

## Resume-ready description (after testing)
Built a FastAPI-based identity and access-control demonstration with role-based authorization, audit event capture, and automated tests for denied and permitted access paths.
