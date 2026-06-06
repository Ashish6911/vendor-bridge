from fastapi import APIRouter, Depends, Form, Header, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from ..db import get_db
from .. import crud, auth

router = APIRouter()

@router.post("/vendors")
def create_vendor(
    name: str = Form(...),
    category: Optional[str] = Form(None),
    gst_number: Optional[str] = Form(None),
    phone: Optional[str] = Form(None),
    contact_email: Optional[str] = Form(None),
    address: Optional[str] = Form(None),
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    user = auth.get_user_from_authorization_header(authorization, db)
    auth.require_roles(user, ["admin", "manager", "procurement_officer"])
    vendor = crud.create_vendor(db, name, category, gst_number, phone, contact_email, address, created_by=user.id)
    return {"success": True, "vendor": {"id": vendor.id, "name": vendor.name}}

@router.get("/vendors")
def list_vendors(authorization: str = Header(None), db: Session = Depends(get_db)):
    user = auth.get_user_from_authorization_header(authorization, db)
    vendors = crud.list_vendors(db)
    result = []
    for v in vendors:
        result.append({
            "id": v.id,
            "name": v.name,
            "category": v.category,
            "gst_number": v.gst_number,
            "phone": v.phone,
            "contact_email": v.contact_email,
            "address": v.address,
            "created_by": v.created_by,
            "created_at": v.created_at.isoformat() if v.created_at else None
        })
    return result

@router.delete("/vendors/{vendor_id}")
def delete_vendor(vendor_id: int, authorization: str = Header(None), db: Session = Depends(get_db)):
    user = auth.get_user_from_authorization_header(authorization, db)
    auth.require_roles(user, ["admin", "manager", "procurement_officer"])
    v = db.query(auth.models.Vendor).filter(auth.models.Vendor.id == vendor_id).first()
    if not v:
        raise HTTPException(status_code=404, detail="Vendor not found")
    db.delete(v)
    db.commit()
    return {"success": True}

