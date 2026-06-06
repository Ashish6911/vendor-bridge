from fastapi import APIRouter, Form, Header, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Optional
from ..db import get_db
from .. import models, auth
from datetime import datetime

router = APIRouter()


@router.post("/invoices")
def create_invoice(po_id: int = Form(...), authorization: str = Header(None), db: Session = Depends(get_db)):
    user = auth.get_user_from_authorization_header(authorization, db)
    auth.require_roles(user, ["admin", "manager", "procurement_officer"])
    po = db.query(models.PurchaseOrder).filter(models.PurchaseOrder.id == po_id).first()
    if not po:
        raise HTTPException(status_code=404, detail="Purchase order not found")
    invoice_number = f"INV-{po_id}-{int(datetime.utcnow().timestamp())}"
    inv = models.Invoice(invoice_number=invoice_number, po_id=po_id, amount=po.amount)
    db.add(inv)
    db.commit()
    db.refresh(inv)
    return {"success": True, "invoice": {"id": inv.id, "invoice_number": inv.invoice_number}}


@router.get("/invoices")
def list_invoices(authorization: str = Header(None), db: Session = Depends(get_db)):
    user = auth.get_user_from_authorization_header(authorization, db)
    invs = db.query(models.Invoice).all()
    result = []
    for i in invs:
        result.append({
            "id": i.id,
            "invoice_number": i.invoice_number,
            "po_id": i.po_id,
            "amount": i.amount,
            "due_date": i.due_date.isoformat() if i.due_date else None,
            "status": i.status,
            "email_sent": i.email_sent,
            "created_at": i.created_at.isoformat() if i.created_at else None
        })
    return result


@router.post("/invoices/{invoice_id}/send_email")
def send_invoice_email(invoice_id: int, to_email: Optional[str] = Form(None), authorization: str = Header(None), db: Session = Depends(get_db)):
    user = auth.get_user_from_authorization_header(authorization, db)
    auth.require_roles(user, ["admin", "manager", "procurement_officer"])
    inv = db.query(models.Invoice).filter(models.Invoice.id == invoice_id).first()
    if not inv:
        raise HTTPException(status_code=404, detail="Invoice not found")
    # In this demo we only toggle email_sent and return a message
    inv.email_sent = "yes"
    db.add(inv)
    db.commit()
    return {"success": True, "message": f"Invoice {inv.invoice_number} emailed to {to_email or 'unknown'}"}
