from fastapi import APIRouter, Header, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..db import get_db
from .. import models, auth

router = APIRouter()


@router.get("/reports")
def reports(authorization: str = Header(None), db: Session = Depends(get_db)):
    user = auth.get_user_from_authorization_header(authorization, db)
    total_vendors = db.query(func.count(models.Vendor.id)).scalar() or 0
    total_rfqs = db.query(func.count(models.RFQ.id)).scalar() or 0
    total_quotations = db.query(func.count(models.Quotation.id)).scalar() or 0
    total_pos = db.query(func.count(models.PurchaseOrder.id)).scalar() or 0
    total_invoices = db.query(func.count(models.Invoice.id)).scalar() or 0

    approved_quotations = db.query(func.count(models.Quotation.id)).filter(models.Quotation.status == 'approved').scalar() or 0
    rejected_quotations = db.query(func.count(models.Quotation.id)).filter(models.Quotation.status == 'rejected').scalar() or 0

    # top vendor by quote count
    vendor_counts = db.query(models.Vendor.name, func.count(models.Quotation.id).label('c')).join(models.Quotation, models.Quotation.vendor_id == models.Vendor.id).group_by(models.Vendor.id).order_by(func.count(models.Quotation.id).desc()).first()
    top_vendor = vendor_counts[0] if vendor_counts else None

    return {
        "total_vendors": total_vendors,
        "total_rfqs": total_rfqs,
        "total_quotations": total_quotations,
        "total_pos": total_pos,
        "total_invoices": total_invoices,
        "approved_quotations": approved_quotations,
        "rejected_quotations": rejected_quotations,
        "top_vendor_by_quotes": top_vendor
    }
