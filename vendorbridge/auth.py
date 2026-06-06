from fastapi import Header, HTTPException, Depends
from jose import jwt, JWTError
from .config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from .db import get_db
from sqlalchemy.orm import Session
from . import models
from datetime import datetime, timedelta


def create_access_token(email: str, expires_minutes: int = None):
    exp_minutes = expires_minutes or ACCESS_TOKEN_EXPIRE_MINUTES
    expire = datetime.utcnow() + timedelta(minutes=exp_minutes)
    payload = {"sub": email, "exp": expire}
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token


def get_user_from_authorization_header(authorization: str = Header(None), db: Session = Depends(get_db)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization Header Missing")
    try:
        token = authorization.replace("Bearer ", "")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if not email:
            raise HTTPException(status_code=401, detail="Invalid Token")
        user = db.query(models.User).filter(models.User.email == email).first()
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or Expired Token")


def require_roles(user: models.User, allowed_roles: list):
    if user.role not in allowed_roles:
        raise HTTPException(status_code=403, detail="Insufficient role permissions")
