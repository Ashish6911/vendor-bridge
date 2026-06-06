from fastapi import FastAPI, Form, Header
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
from hashlib import sha256
from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =====================================
# JWT SETTINGS
# =====================================

SECRET_KEY = "etdstrfkfytfvkytfvktgvtkgygygiygygygygtvktgvkuygiygiygiygiygiygiygiygiygiyg"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# =====================================
# DATABASE
# =====================================

DATABASE_URL = "sqlite:///users.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

# =====================================
# USER TABLE
# =====================================

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

Base.metadata.create_all(bind=engine)

# =====================================
# TOKEN CREATION
# =====================================

def create_access_token(email: str):

    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": email,
        "exp": expire
    }

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token

# =====================================
# HOME
# =====================================

@app.get("/")
def home():
    return {
        "message": "JWT Authentication Running"
    }

# =====================================
# SIGNUP
# =====================================

@app.post("/signup")
def signup(
    new_email: str = Form(...),
    new_password: str = Form(...)
):
    db = SessionLocal()

    existing_user = db.query(User).filter(
        User.email == new_email
    ).first()

    if existing_user:
        db.close()

        return {
            "success": False,
            "message": "Email already exists"
        }

    hashed_password = sha256(
        new_password.encode()
    ).hexdigest()

    user = User(
        email=new_email,
        password=hashed_password
    )

    db.add(user)
    db.commit()

    db.close()

    return {
        "success": True,
        "message": "Signup Successful"
    }

# =====================================
# LOGIN
# =====================================

@app.post("/login")
def login(
    email: str = Form(...),
    password: str = Form(...)
):
    db = SessionLocal()

    user = db.query(User).filter(
        User.email == email
    ).first()

    if not user:
        db.close()

        return {
            "success": False,
            "message": "Invalid Email or Password"
        }

    entered_hash = sha256(
        password.encode()
    ).hexdigest()

    if entered_hash != user.password:
        db.close()

        return {
            "success": False,
            "message": "Invalid Email or Password"
        }

    access_token = create_access_token(
        user.email
    )

    db.close()

    return {
        "success": True,
        "message": "Login Successful",
        "access_token": access_token,
        "token_type": "Bearer"
    }

# =====================================
# PROTECTED PROFILE
# =====================================

@app.get("/profile")
def profile(
    authorization: str = Header(None)
):

    if not authorization:
        return {
            "success": False,
            "message": "Authorization Header Missing"
        }

    try:

        token = authorization.replace(
            "Bearer ",
            ""
        )

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        email = payload["sub"]

        db = SessionLocal()

        user = db.query(User).filter(
            User.email == email
        ).first()

        db.close()

        if not user:
            return {
                "success": False,
                "message": "User Not Found"
            }

        return {
            "success": True,
            "id": user.id,
            "email": user.email
        }

    except JWTError:

        return {
            "success": False,
            "message": "Invalid or Expired Token"
        }

# =====================================
# TEST USERS
# =====================================

@app.get("/users")
def show_users():

    db = SessionLocal()

    users = db.query(User).all()

    result = []

    for user in users:
        result.append({
            "id": user.id,
            "email": user.email
        })

    db.close()

    return result