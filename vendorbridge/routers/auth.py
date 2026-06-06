from fastapi import APIRouter, Form, Header, HTTPException, Depends
from sqlalchemy.orm import Session
from hashlib import sha256
from ..db import get_db
from .. import models, auth

router = APIRouter()

@router.post("/signup")
def signup(new_email: str = Form(...), new_password: str = Form(...), role: str = Form(...), db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == new_email).first()
    if existing_user:
        return {"success": False, "message": "Email already exists"}

    allowed_roles = {"admin", "manager", "procurement_officer", "vendor"}
    if role not in allowed_roles:
        return {"success": False, "message": f"Invalid role. Allowed: {', '.join(allowed_roles)}"}

    hashed_password = sha256(new_password.encode()).hexdigest()
    user = models.User(email=new_email, password=hashed_password, role=role)
    db.add(user)
    db.commit()
    return {"success": True, "message": "Signup Successful"}

@router.post("/login")
def login(email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        return {"success": False, "message": "Invalid Email or Password"}
    entered_hash = sha256(password.encode()).hexdigest()
    if entered_hash != user.password:
        return {"success": False, "message": "Invalid Email or Password"}
    access_token = auth.create_access_token(user.email)
    return {"success": True, "message": "Login Successful", "access_token": access_token, "token_type": "Bearer", "role": user.role}

@router.get("/profile")
def profile(authorization: str = Header(None), db: Session = Depends(get_db)):
    user = auth.get_user_from_authorization_header(authorization, db)
    return {"success": True, "id": user.id, "email": user.email, "role": user.role}

@router.get("/users")
def list_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return [{"id": u.id, "email": u.email, "role": u.role} for u in users]
