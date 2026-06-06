from sqlalchemy.orm import Session
from hashlib import sha256
from . import models
from datetime import datetime, timedelta

def ensure_admin_user(db: Session):
    admin = db.query(models.User).filter(models.User.role == 'admin').first()
    if not admin:
        default_email = 'admin@vendorbridge.local'
        default_password = sha256('admin123'.encode()).hexdigest()
        existing = db.query(models.User).filter(models.User.email == default_email).first()
        if not existing:
            u = models.User(email=default_email, password=default_password, role='admin')
            db.add(u)
            db.commit()

def create_vendor(db: Session, name: str, category: str = None, gst_number: str = None, phone: str = None, contact_email: str = None, address: str = None, created_by: int = None):
    v = models.Vendor(name=name, category=category, gst_number=gst_number, phone=phone, contact_email=contact_email, address=address, created_by=created_by)
    db.add(v)
    db.commit()
    db.refresh(v)
    return v

def list_vendors(db: Session):
    return db.query(models.Vendor).all()

def create_rfq(db: Session, title: str, description: str = None, vendor_id: int = None, deadline=None, attachment_url: str = None, created_by: int = None):
    rfq = models.RFQ(title=title, description=description, vendor_id=vendor_id, deadline=deadline, attachment_url=attachment_url, created_by=created_by)
    db.add(rfq)
    db.commit()
    db.refresh(rfq)
    return rfq

def list_rfqs(db: Session):
    return db.query(models.RFQ).all()
