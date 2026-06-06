from fastapi import APIRouter, Form, Header, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Optional
from ..db import get_db
from .. import models, auth

router = APIRouter()


@router.post("/quotations")
def create_quotation(
    rfq_id: int = Form(...),
    vendor_id: int = Form(...),
    amount: float = Form(...),
    delivery_timeline: Optional[str] = Form(None),
    comments: Optional[str] = Form(None),
    details: Optional[str] = Form(None),
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    user = auth.get_user_from_authorization_header(authorization, db)
    q = models.Quotation(rfq_id=rfq_id, vendor_id=vendor_id, amount=amount, delivery_timeline=delivery_timeline, comments=comments, details=details)
    db.add(q)
    db.commit()
    db.refresh(q)
    return {"success": True, "quotation": {"id": q.id, "rfq_id": q.rfq_id, "vendor_id": q.vendor_id, "amount": q.amount, "status": q.status}}


@router.get("/quotations")
def list_quotations(authorization: str = Header(None), db: Session = Depends(get_db)):
    user = auth.get_user_from_authorization_header(authorization, db)
    qs = db.query(models.Quotation).all()
    result = []
    for q in qs:
        result.append({
            "id": q.id,
            "rfq_id": q.rfq_id,
            "vendor_id": q.vendor_id,
            "amount": q.amount,
            "details": q.details,
            "delivery_timeline": q.delivery_timeline,
            "comments": q.comments,
            "status": q.status,
            "submitted_at": q.submitted_at.isoformat() if q.submitted_at else None
        })
    return result


@router.post("/quotations/{quotation_id}/approve")
def approve_quotation(quotation_id: int, comments: Optional[str] = Form(None), authorization: str = Header(None), db: Session = Depends(get_db)):
    user = auth.get_user_from_authorization_header(authorization, db)
    auth.require_roles(user, ["admin", "manager", "procurement_officer"])
    q = db.query(models.Quotation).filter(models.Quotation.id == quotation_id).first()
    if not q:
        raise HTTPException(status_code=404, detail="Quotation not found")
    q.status = "approved"
    db.add(q)
    appr = models.Approval(quotation_id=quotation_id, approver_id=user.id, decision="approved", comments=comments)
    db.add(appr)
    db.commit()
    return {"success": True}


@router.post("/quotations/{quotation_id}/reject")
def reject_quotation(quotation_id: int, comments: Optional[str] = Form(None), authorization: str = Header(None), db: Session = Depends(get_db)):
    user = auth.get_user_from_authorization_header(authorization, db)
    auth.require_roles(user, ["admin", "manager", "procurement_officer"])
    q = db.query(models.Quotation).filter(models.Quotation.id == quotation_id).first()
    if not q:
        raise HTTPException(status_code=404, detail="Quotation not found")
    q.status = "rejected"
    db.add(q)
    appr = models.Approval(quotation_id=quotation_id, approver_id=user.id, decision="rejected", comments=comments)
    db.add(appr)
    db.commit()
    return {"success": True}
