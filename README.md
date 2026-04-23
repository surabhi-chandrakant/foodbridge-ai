# FoodBridge AI — Food Waste Redistribution System
### SDG 12: Responsible Consumption | Powered by Gemini AI + Botpress

---

## What This System Does

- **Restaurants** log surplus food via a dashboard
- **Gemini AI** analyzes spoilage risk and predicts future waste
- **NGOs** request food via dashboard OR via Botpress chatbot
- **Matching engine** auto-pairs donors with NGOs
- **Botpress webhook** lets the chatbot trigger real-time matching

---

## Project Structure

```
foodwaste/
├── backend/
│   ├── main.py              # FastAPI backend + Gemini integration
│   └── requirements.txt
├── frontend/
│   └── index.html           # Full dashboard (single file, no build needed)
└── README.md
```

---

## Setup Instructions

### Step 1: Get Gemini API Key
1. Go to https://aistudio.google.com/
2. Click "Get API Key" → Create key
3. Copy the key

### Step 2: Install Backend
```bash
cd backend
pip install -r requirements.txt
```

### Step 3: Set API Key
**Windows:**
```cmd
set GEMINI_API_KEY=your_key_here
```

**Mac/Linux:**
```bash
export GEMINI_API_KEY=your_key_here
```

OR directly in `main.py` line 18:
```python
GEMINI_API_KEY = "your_actual_key_here"
```

### Step 4: Run Backend
```bash
cd backend
python main.py
```
Backend runs at: http://localhost:8000
API docs at: http://localhost:8000/docs

### Step 5: Open Frontend
Just open `frontend/index.html` in your browser.
(No build step needed — it's a single HTML file)

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /donate | Register surplus food |
| POST | /request | NGO food request |
| GET | /donations | List all donations |
| GET | /requests | List all requests |
| GET | /matches | List all matches |
| GET | /predict-waste | AI waste prediction |
| GET | /dashboard-stats | Stats for dashboard |
| POST | /botpress-webhook | **Botpress integration endpoint** |

---

## Botpress Integration

### Architecture
```
NGO → Botpress Chatbot → Webhook → Your FastAPI → Gemini → Match → Response → Bot
```

### Steps in Botpress Cloud

1. Create a new bot at https://app.botpress.cloud
2. In Flow builder, create this conversation flow:
   - Ask: "What is your NGO name?"
   - Ask: "How many people do you need to feed?"
   - Ask: "What area are you in?"
   - Ask: "Your contact number?"
   - Execute Code node (see below)
   - Text node: Show `{{workflow.result.message}}`

3. **Execute Code node:**
```javascript
const axios = require('axios');

const response = await axios.post('https://YOUR_BACKEND_URL/botpress-webhook', {
  ngo_name: workflow.ngoName,
  people_count: parseInt(workflow.peopleCount),
  location: workflow.location,
  contact: workflow.contact,
  food_preference: "any"
});

workflow.result = response.data;
```

4. **Condition node after:**
   - If `workflow.result.matched == true` → Show match details
   - If `workflow.result.matched == false` → Show "We'll notify you"

### Making Backend Public (for Botpress to reach it)

**Option A: ngrok (for testing/demo)**
```bash
# Install ngrok from https://ngrok.com
ngrok http 8000
# Copy the https://xxxx.ngrok.io URL
# Use that as your Botpress webhook URL
```

**Option B: Deploy to Railway (free tier)**
```bash
# Push to GitHub, connect Railway at https://railway.app
# Set env var GEMINI_API_KEY in Railway dashboard
```

**Option C: Deploy to Render (free tier)**
```bash
# Push to GitHub, connect Render at https://render.com
# Create a Web Service → Python
# Build command: pip install -r requirements.txt
# Start command: uvicorn main:app --host 0.0.0.0 --port $PORT
```

---

## Demo Flow for Hackathon

1. Open dashboard → show stats (all 0)
2. Go to "AI Predict" tab → enter a restaurant name + day + meal → show Gemini prediction
3. Go to "Donate Food" → enter surplus food → show Gemini spoilage analysis
4. Go to "NGO Request" → submit request → show auto-match
5. Go to "Matches" tab → show matched pair
6. Open Botpress chatbot → show same flow via chat interface
7. Show live stats updating on Dashboard

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| AI Brain | Gemini 1.5 Flash (Google) |
| Backend | FastAPI (Python) |
| Frontend | Vanilla HTML/CSS/JS (no build) |
| Chatbot Platform | Botpress Cloud |
| ML (Prediction) | Gemini-powered (prompt-based) |
| Database | In-memory (demo) → swap for PostgreSQL |

---

## SDG Alignment

- **SDG 12.3**: Halve per-capita food waste globally by 2030
- **SDG 2**: Zero Hunger — connecting surplus food with those who need it
- **SDG 11**: Sustainable Cities — local redistribution networks

---

## Known Limitations (be honest in your demo)

- In-memory storage resets on restart (production would use a database)
- Gemini prediction is LLM-based, not a trained regression model
- No authentication on endpoints (add OAuth2 for production)
- Route optimization is not implemented (Maps API integration point marked in code)
