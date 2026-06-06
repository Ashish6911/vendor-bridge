from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from datetime import datetime
from .db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False, default="vendor")

class Vendor(Base):
    __tablename__ = "vendors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    category = Column(String, nullable=True)
    gst_number = Column(String, nullable=True)
    contact_email = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    address = Column(Text, nullable=True)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class RFQ(Base):
    __tablename__ = "rfqs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    vendor_id = Column(Integer, ForeignKey("vendors.id"), nullable=True)
    deadline = Column(DateTime, nullable=True)
    attachment_url = Column(String, nullable=True)
    status = Column(String, default="open")
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Quotation(Base):
    __tablename__ = "quotations"

    id = Column(Integer, primary_key=True, index=True)
    rfq_id = Column(Integer, ForeignKey("rfqs.id"), nullable=False)
    vendor_id = Column(Integer, ForeignKey("vendors.id"), nullable=False)
    amount = Column(Float, nullable=False)
    details = Column(Text, nullable=True)
    delivery_timeline = Column(String, nullable=True)
    comments = Column(Text, nullable=True)
    status = Column(String, default="submitted")
    submitted_at = Column(DateTime, default=datetime.utcnow)

class Approval(Base):
    __tablename__ = "approvals"

    id = Column(Integer, primary_key=True, index=True)
    quotation_id = Column(Integer, ForeignKey("quotations.id"), nullable=False)
    approver_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    decision = Column(String, nullable=False)
    comments = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

class PurchaseOrder(Base):
    __tablename__ = "purchase_orders"

    id = Column(Integer, primary_key=True, index=True)
    po_number = Column(String, unique=True, nullable=False)
    quotation_id = Column(Integer, ForeignKey("quotations.id"), nullable=False)
    vendor_id = Column(Integer, ForeignKey("vendors.id"), nullable=False)
    amount = Column(Float, nullable=False)
    status = Column(String, default="issued")
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)
    invoice_number = Column(String, unique=True, nullable=False)
    po_id = Column(Integer, ForeignKey("purchase_orders.id"), nullable=False)
    amount = Column(Float, nullable=False)
    due_date = Column(DateTime, nullable=True)
    status = Column(String, default="unpaid")
    email_sent = Column(String, default="no")
    created_at = Column(DateTime, default=datetime.utcnow)
