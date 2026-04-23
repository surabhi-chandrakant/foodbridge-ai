from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
import google.generativeai as genai
import json
import os
from datetime import datetime
import uvicorn

app = FastAPI(title="FoodBridge AI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Configure Gemini ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY_HERE")
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

# --- In-memory store (replace with DB in production) ---
donations = []
ngo_requests = []
matches = []

# --- Models ---
class DonationEntry(BaseModel):
    restaurant_name: str
    food_type: str
    quantity_kg: float
    prepared_at: str       # e.g. "2024-01-15 14:00"
    location: str
    contact: str

class NGORequest(BaseModel):
    ngo_name: str
    people_count: int
    location: str
    contact: str
    food_preference: Optional[str] = "any"

class BotpressWebhook(BaseModel):
    ngo_name: str
    people_count: int
    location: str
    contact: str
    food_preference: Optional[str] = "any"

# --- Helper: Ask Gemini ---
def ask_gemini(prompt: str) -> str:
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"AI unavailable: {str(e)}"

# --- Routes ---

@app.get("/")
def root():
    return {"status": "FoodBridge AI is running"}

@app.post("/donate")
def add_donation(entry: DonationEntry):
    donation = entry.dict()
    donation["id"] = len(donations) + 1
    donation["timestamp"] = datetime.now().isoformat()
    donation["status"] = "available"

    # AI: predict spoilage risk
    prompt = f"""
    A restaurant donated food with these details:
    - Food type: {entry.food_type}
    - Quantity: {entry.quantity_kg} kg
    - Prepared at: {entry.prepared_at}
    - Current time: {datetime.now().strftime('%Y-%m-%d %H:%M')}

    Give a SHORT response (3 lines max):
    1. Spoilage risk: LOW / MEDIUM / HIGH
    2. Safe consumption window (hours from now)
    3. One handling tip
    """
    donation["ai_spoilage_analysis"] = ask_gemini(prompt)
    donations.append(donation)

    # Auto-match with pending NGO requests
    _auto_match()

    return {"success": True, "donation_id": donation["id"], "analysis": donation["ai_spoilage_analysis"]}

@app.post("/request")
def add_ngo_request(req: NGORequest):
    request = req.dict()
    request["id"] = len(ngo_requests) + 1
    request["timestamp"] = datetime.now().isoformat()
    request["status"] = "pending"
    ngo_requests.append(request)

    _auto_match()

    return {"success": True, "request_id": request["id"]}

@app.get("/donations")
def get_donations():
    return donations

@app.get("/requests")
def get_requests():
    return ngo_requests

@app.get("/matches")
def get_matches():
    return matches

@app.get("/predict-waste")
def predict_waste(restaurant: str, day: str, meal_type: str):
    prompt = f"""
    Predict food waste for a restaurant in India:
    - Restaurant: {restaurant}
    - Day: {day}
    - Meal: {meal_type}

    Respond ONLY with valid JSON like this (no markdown):
    {{
      "predicted_waste_kg": 12,
      "confidence": "high",
      "peak_hours": "2pm-4pm",
      "suggestion": "Contact NGO by 1pm"
    }}
    """
    raw = ask_gemini(prompt)
    try:
        # Strip markdown code blocks if present
        clean = raw.strip().strip("```json").strip("```").strip()
        return json.loads(clean)
    except:
        return {"raw_response": raw}

@app.post("/botpress-webhook")
def botpress_webhook(data: BotpressWebhook):
    """
    Called by Botpress when NGO submits a food request via chatbot.
    Returns matched donations for the bot to display.
    """
    req = NGORequest(**data.dict())
    result = add_ngo_request(req)

    # Find available donations near them
    available = [d for d in donations if d["status"] == "available"]

    if not available:
        return {
            "matched": False,
            "message": "No donations available right now. We'll notify you when food is listed.",
            "request_id": result["request_id"]
        }

    # Use Gemini to pick the best match
    donation_list = "\n".join([
        f"- ID {d['id']}: {d['food_type']} ({d['quantity_kg']}kg) from {d['restaurant_name']} at {d['location']}"
        for d in available
    ])

    prompt = f"""
    An NGO needs food:
    - NGO: {data.ngo_name}
    - People to feed: {data.people_count}
    - Location: {data.location}
    - Preference: {data.food_preference}

    Available donations:
    {donation_list}

    Pick the BEST donation ID. Reply ONLY with the donation ID number, nothing else.
    """
    best_id_raw = ask_gemini(prompt).strip()
    try:
        best_id = int(best_id_raw)
        match = next((d for d in available if d["id"] == best_id), available[0])
    except:
        match = available[0]

    return {
        "matched": True,
        "donation_id": match["id"],
        "restaurant": match["restaurant_name"],
        "food": match["food_type"],
        "quantity_kg": match["quantity_kg"],
        "location": match["location"],
        "contact": match["contact"],
        "message": f"Great news! {match['restaurant_name']} has {match['quantity_kg']}kg of {match['food_type']} available at {match['location']}. Contact: {match['contact']}"
    }

@app.get("/dashboard-stats")
def dashboard_stats():
    total_donations = len(donations)
    total_kg = sum(d["quantity_kg"] for d in donations)
    matched_count = len(matches)
    pending_requests = len([r for r in ngo_requests if r["status"] == "pending"])
    meals_saved = int(total_kg * 4)  # ~250g per meal

    return {
        "total_donations": total_donations,
        "total_kg_donated": total_kg,
        "matches_made": matched_count,
        "pending_requests": pending_requests,
        "meals_saved_estimate": meals_saved,
        "active_restaurants": len(set(d["restaurant_name"] for d in donations)),
        "active_ngos": len(set(r["ngo_name"] for r in ngo_requests))
    }

def _auto_match():
    """Simple matching: pair available donations with pending requests."""
    for req in ngo_requests:
        if req["status"] == "pending":
            for don in donations:
                if don["status"] == "available":
                    don["status"] = "matched"
                    req["status"] = "matched"
                    matches.append({
                        "match_id": len(matches) + 1,
                        "donation_id": don["id"],
                        "request_id": req["id"],
                        "restaurant": don["restaurant_name"],
                        "ngo": req["ngo_name"],
                        "food": don["food_type"],
                        "quantity_kg": don["quantity_kg"],
                        "timestamp": datetime.now().isoformat()
                    })
                    break

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
