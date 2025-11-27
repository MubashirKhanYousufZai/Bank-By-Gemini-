from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import database as db_utils

app = FastAPI()

# Initialize the database
db_utils.init_db()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

class TransferRequest(BaseModel):
    sender: str
    receiver: str
    amount: float

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/accounts")
async def get_accounts():
    return db_utils.get_accounts()

@app.post("/api/transfer")
async def transfer_money(transfer: TransferRequest):
    sender = transfer.sender
    receiver = transfer.receiver
    amount = transfer.amount

    if sender == receiver:
        raise HTTPException(status_code=400, detail="Sender and receiver cannot be the same.")
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Transfer amount must be positive.")

    try:
        db_utils.update_balances(sender, receiver, amount)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {"message": f"Successfully transferred {amount} from {sender} to {receiver}."}
