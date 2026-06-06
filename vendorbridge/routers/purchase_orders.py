from fastapi import APIRouter, Form, Header, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Optional
from ..db import get_db
from .. import models, auth
from datetime import datetime

router = APIRouter()


@router.post("/purchase_orders")
def create_po(quotation_id: int = Form(...), authorization: str = Header(None), db: Session = Depends(get_db)):
    user = auth.get_user_from_authorization_header(authorization, db)
    # allow managers/admins/procurement to create POs; but keep it flexible
    auth.require_roles(user, ["admin", "manager", "procurement_officer"])
    q = db.query(models.Quotation).filter(models.Quotation.id == quotation_id).first()
    if not q:
        raise HTTPException(status_code=404, detail="Quotation not found")
    po_number = f"PO-{quotation_id}-{int(datetime.utcnow().timestamp())}"
    po = models.PurchaseOrder(po_number=po_number, quotation_id=quotation_id, vendor_id=q.vendor_id, amount=q.amount, created_by=user.id)
    db.add(po)
    db.commit()
    db.refresh(po)
    return {"success": True, "purchase_order": {"id": po.id, "po_number": po.po_number}}


@router.get("/purchase_orders")
def list_pos(authorization: str = Header(None), db: Session = Depends(get_db)):
    user = auth.get_user_from_authorization_header(authorization, db)
    pos = db.query(models.PurchaseOrder).all()
    result = []
    for p in pos:
        result.append({
            "id": p.id,
            "po_number": p.po_number,
            "quotation_id": p.quotation_id,
            "vendor_id": p.vendor_id,
            "amount": p.amount,
            "status": p.status,
            "created_at": p.created_at.isoformat() if p.created_at else None
        })
    return result
