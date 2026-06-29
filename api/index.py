from fastapi import FastAPI, Request, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware

EMAIL = "23f2000085@ds.study.iitm.ac.in"
API_KEY = "ak_0o36tbq7udcsxf005czvlks2"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "ok"}

@app.post("/analytics")
async def analytics(request: Request, x_api_key: str = Header(default=None, alias="X-API-Key")):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    body = await request.json()
    events = body.get("events", [])

    total_events = len(events)

    users = set()

    revenue = 0.0

    totals = {}

    for event in events:
        user = str(event.get("user", ""))
        amount = float(event.get("amount", 0))

        users.add(user)

        if amount > 0:
            revenue += amount
            totals[user] = totals.get(user, 0) + amount

    top_user = max(totals, key=totals.get) if totals else ""

    return {
        "email": EMAIL,
        "total_events": total_events,
        "unique_users": len(users),
        "revenue": revenue,
        "top_user": top_user
    }
