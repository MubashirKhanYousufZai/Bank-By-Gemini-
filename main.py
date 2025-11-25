from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# In-memory database for simplicity
db = {
    "Ali": {"balance": 5000},
    "Me": {"balance": 1000},
    "Fatima": {"balance": 2500},
}

class TransferRequest(BaseModel):
    sender: str
    receiver: str
    amount: float

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/accounts")
async def get_accounts():
    return db

@app.post("/api/transfer")
async def transfer_money(transfer: TransferRequest):
    sender = transfer.sender
    receiver = transfer.receiver
    amount = transfer.amount

    if sender not in db:
        raise HTTPException(status_code=404, detail=f"Sender '{sender}' not found.")
    if receiver not in db:
        raise HTTPException(status_code=404, detail=f"Receiver '{receiver}' not found.")
    if sender == receiver:
        raise HTTPException(status_code=400, detail="Sender and receiver cannot be the same.")
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Transfer amount must be positive.")
    if db[sender]["balance"] < amount:
        raise HTTPException(status_code=400, detail="Insufficient funds.")

    db[sender]["balance"] -= amount
    db[receiver]["balance"] += amount

    return {"message": f"Successfully transferred {amount} from {sender} to {receiver}."}
