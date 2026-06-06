from fastapi import APIRouter, Depends, Form, Header, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from ..db import get_db
from .. import crud, auth

router = APIRouter()


@router.post("/rfqs")
def create_rfq(
    title: str = Form(...),
    description: Optional[str] = Form(None),
    vendor_id: Optional[int] = Form(None),
    deadline: Optional[str] = Form(None),
    attachment_url: Optional[str] = Form(None),
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    user = auth.get_user_from_authorization_header(authorization, db)
    auth.require_roles(user, ["admin", "manager", "procurement_officer"])
    deadline_value = None
    if deadline:
        try:
            from datetime import datetime
            deadline_value = datetime.fromisoformat(deadline)
        except ValueError:
            deadline_value = None
    rfq = crud.create_rfq(db, title, description, vendor_id, deadline_value, attachment_url, created_by=user.id)
    return {"success": True, "rfq": {"id": rfq.id, "title": rfq.title}}


@router.get("/rfqs")
def list_rfqs(authorization: str = Header(None), db: Session = Depends(get_db)):
    _ = auth.get_user_from_authorization_header(authorization, db)
    rfqs = crud.list_rfqs(db)
    result = []
    for r in rfqs:
        result.append({
            "id": r.id,
            "title": r.title,
            "description": r.description,
            "vendor_id": r.vendor_id,
            "deadline": r.deadline.isoformat() if r.deadline else None,
            "attachment_url": r.attachment_url,
            "status": r.status,
            "created_by": r.created_by,
            "created_at": r.created_at.isoformat() if r.created_at else None
        })
    return result
