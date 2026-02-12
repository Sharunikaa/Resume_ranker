# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Get Gemini API Key (2 minutes)
1. Visit: https://aistudio.google.com/app/apikey
2. Sign in with Google Account
3. Click "Create API Key"
4. Copy the key (starts with `AIza...`)

### Step 2: MongoDB — choose one

**Option A: MongoDB Atlas (cloud, recommended)**  
1. Go to [mongodb.com/cloud/atlas](https://www.mongodb.com/cloud/atlas) and create a free account.  
2. Create a free cluster (e.g. M0).  
3. Create a database user (Database Access → Add New) and note username/password.  
4. In Network Access, add `0.0.0.0/0` (or your IP) so the app can connect.  
5. Click “Connect” on the cluster → “Drivers” → copy the connection string.  
6. In your `.env`, set:
   ```env
   MONGODB_URI=mongodb+srv://YOUR_USER:YOUR_PASSWORD@YOUR_CLUSTER.mongodb.net/?retryWrites=true&w=majority
   DATABASE_NAME=resume_ranker
   ```
   Replace `YOUR_USER`, `YOUR_PASSWORD`, and `YOUR_CLUSTER`. If the password has special characters, [URL-encode](https://www.w3schools.com/tags/ref_urlencode.asp) them.

**Option B: Local MongoDB (macOS with Homebrew):**
```bash
brew tap mongodb/brew
brew install mongodb-community@8.0
brew services start mongodb-community@8.0
```
Then in `.env`: `MONGODB_URI=mongodb://localhost:27017`

### Step 3: Configure Environment

```bash
cd resume_ranker
cp .env.example .env
```

Edit `.env` and add your Gemini API key:
```env
GEMINI_API_KEY=your_actual_api_key_here
```

### Step 4: Install Dependencies

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Step 5: Run the Application

**Terminal 1 - Start Backend:**
```bash
uvicorn backend.main:app --reload --port 8000
```

**Terminal 2 - Start Frontend:**
```bash
cd frontend
streamlit run app.py
```

### Step 6: Access the App

- **Frontend**: http://localhost:8501
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

---

## ✅ Verify Setup

Run this quick test:

```bash
python -c "
import os
from dotenv import load_dotenv
from pymongo import MongoClient
import google.generativeai as genai

load_dotenv()

# Test MongoDB
try:
    client = MongoClient(os.getenv('MONGODB_URI'), serverSelectionTimeoutMS=5000)
    client.admin.command('ping')
    print('✅ MongoDB: Connected')
except Exception as e:
    print(f'❌ MongoDB: {e}')

# Test Gemini
try:
    genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content('test')
    print('✅ Gemini API: Working')
except Exception as e:
    print(f'❌ Gemini API: {e}')
"
```

---

## 📚 Need More Help?

- **Detailed Setup**: See [SETUP.md](./SETUP.md)
- **MongoDB Issues**: Check MongoDB logs: `tail -f /opt/homebrew/var/log/mongodb/mongo.log`
- **API Key Issues**: Verify at https://aistudio.google.com/app/apikey

---

**That's it! You're ready to rank resumes! 🎉**
