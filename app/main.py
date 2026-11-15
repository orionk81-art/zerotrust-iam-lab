import os
from datetime import datetime, timezone
from fastapi import FastAPI, Depends, HTTPException, Header
from pydantic import BaseModel

app = FastAPI(title="ZeroTrust IAM Security Lab", version="1.0.0")
# Demo tokens only; never deploy these sample values to production.
TOKENS = {"demo-viewer-token": ("viewer", "viewer"), "demo-admin-token": ("admin", "admin")}
AUDIT_EVENTS = []

class Document(BaseModel):
    title: str


def principal(authorization: str | None = Header(default=None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Bearer token required")
    token = authorization.removeprefix("Bearer ")
    user = TOKENS.get(token)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user


def authorize(required: str):
    def dependency(user=Depends(principal)):
        name, role = user
        allowed = role == "admin" or required == "read"
        AUDIT_EVENTS.append({"timestamp": datetime.now(timezone.utc).isoformat(), "user": name, "role": role, "action": required, "allowed": allowed})
        if not allowed:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return user
    return dependency

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/documents")
def list_documents(user=Depends(authorize("read"))):
    return {"documents": [{"id": 1, "title": "Demo security report"}]}

@app.post("/documents", status_code=201)
def create_document(document: Document, user=Depends(authorize("write"))):
    return {"id": 2, "title": document.title, "created_by": user[0]}

@app.get("/audit")
def audit(user=Depends(authorize("write"))):
    return {"events": AUDIT_EVENTS}
