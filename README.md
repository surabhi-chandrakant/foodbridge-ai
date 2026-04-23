# 🍱 FoodBridge AI — Smart Food Waste Redistribution System

### 🌍 SDG 12: Responsible Consumption | 🤖 Powered by Gemini AI

---

## 🚀 Overview

**FoodBridge AI** is a full-stack AI-powered platform that reduces food waste by connecting **restaurants with surplus food** to **NGOs in need**.

The system uses **Google Gemini AI** to:

* Predict food waste before it happens
* Analyze spoilage risk
* Suggest optimal donation timing

---

## 🎯 Key Features

* 🍽️ **Food Donation System** — Restaurants register surplus food
* 🤝 **NGO Request System** — NGOs request food based on need
* 🔄 **Auto Matching Engine** — Smart pairing of donors & NGOs
* 🤖 **AI Waste Prediction** — Predict surplus using Gemini
* 📊 **Live Dashboard** — Real-time stats & activity tracking
* 💬 **Botpress Chatbot Integration** — NGO requests via chat

---

## 🧠 System Architecture

```
Frontend (Vercel)
        ↓
Backend API (Render - FastAPI)
        ↓
Gemini AI (Google)
        ↓
Matching Engine + Prediction Logic
```

---

## 🛠️ Tech Stack

| Layer        | Technology                          |
| ------------ | ----------------------------------- |
| Frontend     | HTML, CSS, JavaScript               |
| Backend      | FastAPI (Python)                    |
| AI Engine    | Google Gemini 1.5 Flash             |
| Deployment   | Vercel (Frontend), Render (Backend) |
| Chatbot      | Botpress Cloud                      |
| Data Storage | In-memory (Demo)                    |

---

## 📁 Project Structure

```
foodwaste/
├── backend/
│   ├── main.py              # FastAPI backend + AI integration
│   └── requirements.txt
├── frontend/
│   └── index.html           # Interactive dashboard UI
└── README.md
```

---

## 🌐 Live Demo

* 🔗 Frontend: https://foodbridge-ai-flame.vercel.app/
* 🔗 Backend API: https://foodbridge-backend-o9ng.onrender.com/docs

---

## ⚙️ Setup Instructions (Local)

### 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/foodbridge-ai.git
cd foodbridge-ai
```

---

### 2️⃣ Install Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
```

---

### 3️⃣ Set Gemini API Key

**Windows:**

```bash
set GEMINI_API_KEY=your_api_key
```

**Mac/Linux:**

```bash
export GEMINI_API_KEY=your_api_key
```

---

### 4️⃣ Run Backend

```bash
python main.py
```

* API: http://127.0.0.1:8000
* Docs: http://127.0.0.1:8000/docs

---

### 5️⃣ Run Frontend

Open:

```bash
frontend/index.html
```

---

## 📡 API Endpoints

| Method | Endpoint            | Description            |
| ------ | ------------------- | ---------------------- |
| POST   | `/donate`           | Register food donation |
| POST   | `/request`          | NGO request            |
| GET    | `/donations`        | List donations         |
| GET    | `/requests`         | List requests          |
| GET    | `/matches`          | View matches           |
| GET    | `/predict-waste`    | AI prediction          |
| GET    | `/dashboard-stats`  | Dashboard data         |
| POST   | `/botpress-webhook` | Chatbot integration    |

---

## 🤖 Botpress Integration

### Flow:

```
User → Botpress → Webhook → FastAPI → Gemini → Match → Response
```

### Sample Code (Botpress Execute Node)

```javascript
const response = await axios.post(
  "https://your-backend-url/botpress-webhook",
  {
    ngo_name: workflow.ngoName,
    people_count: parseInt(workflow.peopleCount),
    location: workflow.location,
    contact: workflow.contact,
    food_preference: "any"
  }
);

workflow.result = response.data;
```

---



---

## ⚠️ Known Limitations

* Data stored in-memory (resets on restart)
* No authentication (can add OAuth/JWT)
* AI prediction is prompt-based (not ML-trained model)
* No route optimization (future Maps API integration)

---

## 🌍 SDG Impact

* **SDG 12.3** → Reduce food waste
* **SDG 2** → Zero Hunger
* **SDG 11** → Sustainable Cities

---

## 👩‍💻 Author

**Surabhi Chandrakant Bhor**
🔗 LinkedIn: https://www.linkedin.com/in/surabhi-chandrakant/
💻 GitHub: https://github.com/surabhi-chandrakant

---

## ⭐ Final Note

This project demonstrates a **real-world AI-powered system** combining:

* LLMs (Gemini)
* Backend APIs (FastAPI)
* Deployment (Render + Vercel)
* Chatbot integration (Botpress)

👉 Built with focus on **impact, scalability, and practical AI application**
