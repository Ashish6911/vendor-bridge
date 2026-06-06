from fastapi import APIRouter, Header, Depends
from sqlalchemy.orm import Session
from ..db import get_db
from .. import models, auth

router = APIRouter()


@router.get("/activity_logs")
def activity_logs(authorization: str = Header(None), db: Session = Depends(get_db)):
    user = auth.get_user_from_authorization_header(authorization, db)
    events = []
    # recent RFQs
    rfqs = db.query(models.RFQ).order_by(models.RFQ.created_at.desc()).limit(10).all()
    for r in rfqs:
        events.append({"message": f"RFQ ready: {r.title} (id:{r.id})", "timestamp": r.created_at.isoformat() if r.created_at else None})
    # recent quotations
    qs = db.query(models.Quotation).order_by(models.Quotation.submitted_at.desc()).limit(10).all()
    for q in qs:
        events.append({"message": f"Quotation submitted for RFQ {q.rfq_id} — {q.amount}", "timestamp": q.submitted_at.isoformat() if q.submitted_at else None})
    # recent POs
    pos = db.query(models.PurchaseOrder).order_by(models.PurchaseOrder.created_at.desc()).limit(10).all()
    for p in pos:
        events.append({"message": f"PO generated: {p.po_number}", "timestamp": p.created_at.isoformat() if p.created_at else None})
    # recent invoices
    invs = db.query(models.Invoice).order_by(models.Invoice.created_at.desc()).limit(10).all()
    for i in invs:
        events.append({"message": f"Invoice created: {i.invoice_number}", "timestamp": i.created_at.isoformat() if i.created_at else None})

    # return most recent 20
    events_sorted = sorted(events, key=lambda e: e.get("timestamp") or "", reverse=True)
    return events_sorted[:20]
