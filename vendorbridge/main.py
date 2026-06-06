from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from vendorbridge.db import engine, Base, SessionLocal
import vendorbridge.models as models
from vendorbridge.routers import vendors, rfqs, auth as auth_router, quotations, purchase_orders, invoices, activity, reports
from vendorbridge.crud import ensure_admin_user

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500", "http://localhost:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(vendors.router)
app.include_router(rfqs.router)
app.include_router(auth_router.router)
app.include_router(quotations.router)
app.include_router(purchase_orders.router)
app.include_router(invoices.router)
app.include_router(activity.router)
app.include_router(reports.router)

Base.metadata.create_all(bind=engine)

# Ensure admin
db = SessionLocal()
try:
    ensure_admin_user(db)
finally:
    db.close()

@app.get("/")
def root():
    return {"message": "vendorbridge API"}

