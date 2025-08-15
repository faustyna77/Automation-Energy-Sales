# --- backend/main.py ---
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import requests
import os
from datetime import datetime
from jose import jwt, JWTError

app = FastAPI()

# CORS dla frontendu NiceGUI/Streamlit
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_API_KEY = os.getenv("SUPABASE_API_KEY")
SUPABASE_JWT_SECRET = os.getenv("SUPABASE_JWT_SECRET")

security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SUPABASE_JWT_SECRET, algorithms=["HS256"])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Nieprawidłowy token")
        return user_id
    except JWTError:
        raise HTTPException(status_code=403, detail="Błąd autoryzacji")

# ---------------------- MODELE ---------------------- #
class AuthData(BaseModel):
    email: str
    password: str

class Decision(BaseModel):
    action: str
    reason: str
    price: float
    volume: float

class FileUpload(BaseModel):
    filename: str
    raw_data: dict

class AnalyzeRequest(BaseModel):
    price: float
    thresholds: dict

# ---------------------- ENDPOINTY AUTH ---------------------- #

@app.post("/register")
def register(data: AuthData):
    response = requests.post(
        f"{SUPABASE_URL}/auth/v1/signup",
        headers={
            "apikey": SUPABASE_API_KEY,
            "Content-Type": "application/json"
        },
        json={"email": data.email, "password": data.password}
    )
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())
    return response.json()

@app.post("/login")
def login(data: AuthData):
    response = requests.post(
        f"{SUPABASE_URL}/auth/v1/token?grant_type=password",
        headers={
            "apikey": SUPABASE_API_KEY,
            "Content-Type": "application/json"
        },
        json={"email": data.email, "password": data.password}
    )
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())
    return response.json()

@app.get("/me")
def get_profile(user_id: str = Depends(get_current_user)):
    return {"user_id": user_id}

# ---------------------- ENDPOINTY DECYZYJNE ---------------------- #

@app.post("/decision")
def add_decision(data: Decision, user_id: str = Depends(get_current_user)):
    response = requests.post(
        f"{SUPABASE_URL}/rest/v1/decisions",
        headers={
            "apikey": SUPABASE_API_KEY,
            "Authorization": f"Bearer {SUPABASE_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "user_id": user_id,
            "timestamp": datetime.utcnow().isoformat(),
            "action": data.action,
            "reason": data.reason,
            "price": data.price,
            "volume": data.volume
        }
    )
    if response.status_code != 201:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    return {"status": "decision saved"}

@app.get("/decisions")
def get_user_decisions(user_id: str = Depends(get_current_user)):
    response = requests.get(
        f"{SUPABASE_URL}/rest/v1/decisions?user_id=eq.{user_id}&order=timestamp.desc",
        headers={
            "apikey": SUPABASE_API_KEY,
            "Authorization": f"Bearer {SUPABASE_API_KEY}"
        }
    )
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    return response.json()

# ---------------------- ENDPOINT ANALITYCZNY ---------------------- #

@app.post("/analyze")
def analyze_price(data: AnalyzeRequest):
    if data.price < data.thresholds.get("buy", 200):
        return {"action": "buy", "reason": "Cena ponizej progu zakupu"}
    elif data.price > data.thresholds.get("sell", 600):
        return {"action": "sell", "reason": "Cena powyzej progu sprzedazy"}
    else:
        return {"action": "wait", "reason": "Cena neutralna"}

# ---------------------- ENDPOINTY IMPORTU DANYCH ---------------------- #

@app.post("/upload")
def upload_data(data: FileUpload, user_id: str = Depends(get_current_user)):
    response = requests.post(
        f"{SUPABASE_URL}/rest/v1/uploads",
        headers={
            "apikey": SUPABASE_API_KEY,
            "Authorization": f"Bearer {SUPABASE_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "user_id": user_id,
            "uploaded_at": datetime.utcnow().isoformat(),
            "filename": data.filename,
            "raw_data": data.raw_data
        }
    )
    if response.status_code != 201:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    return {"status": "upload saved"}

@app.get("/uploads")
def get_user_uploads(user_id: str = Depends(get_current_user)):
    response = requests.get(
        f"{SUPABASE_URL}/rest/v1/uploads?user_id=eq.{user_id}&order=uploaded_at.desc",
        headers={
            "apikey": SUPABASE_API_KEY,
            "Authorization": f"Bearer {SUPABASE_API_KEY}"
        }
    )
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    return response.json()



if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=7860)
