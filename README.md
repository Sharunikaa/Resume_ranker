# CandiSight - AI-Powered Resume Ranking System

An intelligent resume ranking system powered by LLMs (Gemini/Groq) that automatically scores and ranks candidates based on job requirements.

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
cd frontend-react && npm install
```

### 2. Configure Environment
```bash
cp .env.example .env
# Edit .env and add your API keys:
# - MONGODB_URI
# - GEMINI_API_KEY or GROQ_API_KEY
```

### 3. Start Backend
```bash
uvicorn backend.main:app --reload --port 8000
```

### 4. Start Frontend
```bash
cd frontend-react
npm run dev
```

### 5. Open Application
Navigate to http://localhost:5173

## 📁 Project Structure

```
resume_ranker/
├── backend/              # FastAPI backend
│   ├── database/        # MongoDB & ChromaDB clients
│   ├── llm/            # LLM client (Gemini/Groq)
│   ├── models/         # Pydantic models
│   ├── routes/         # API endpoints
│   └── services/       # Business logic
├── frontend-react/      # React + TypeScript frontend
│   ├── src/
│   │   ├── components/ # UI components
│   │   ├── api.ts     # API client
│   │   └── types.ts   # TypeScript types
├── data/               # Sample resumes
│   ├── ai_engineer/   # AI Engineer resumes
│   └── python_developer/ # Python Dev resumes
├── docs/              # Documentation
├── tests/             # Test files
├── utils/             # Utility functions
├── chroma_db/         # Vector database storage
├── .env              # Environment variables
└── requirements.txt   # Python dependencies
```

## ✨ Features

### Core Features
- 🤖 **AI-Powered Scoring** - LLM-based resume analysis
- 📊 **Multi-Metric Ranking** - Project similarity, skill match, experience match
- 🔄 **Auto-Scoring** - Automatic scoring on upload
- ⚡ **Parallel Processing** - Upload 3 resumes simultaneously
- 🔁 **Auto-Retry** - 3 attempts with exponential backoff
- 💾 **LLM Caching** - MongoDB-based response caching
- 🔍 **Vector Search** - ChromaDB for semantic similarity

### Frontend Features
- 🎨 **Modern UI** - React + Tailwind CSS
- 📱 **Responsive Design** - Works on all devices
- 🔔 **Toast Notifications** - Real-time feedback
- 🔍 **Search & Filter** - Find candidates quickly
- 📈 **Analytics Dashboard** - Visualize hiring metrics
- ⚙️ **Settings Page** - Manage API keys securely
- 👁️ **Resume Viewer** - View structured resume data
- 🔄 **Rescore Feature** - Recalculate individual scores

### Backend Features
- 🚀 **FastAPI** - High-performance async API
- 🗄️ **MongoDB** - Flexible document storage
- 🧮 **ChromaDB** - Vector embeddings storage
- 🔐 **Encrypted Storage** - Secure API key storage
- 📝 **Detailed Logging** - Comprehensive error tracking
- 🔄 **Retry Logic** - Automatic failure recovery

## 📖 Documentation

All documentation is in the `docs/` folder:

### Getting Started
- [SETUP.md](docs/SETUP.md) - Complete setup guide
- [QUICK_START_GUIDE.md](docs/QUICK_START_GUIDE.md) - Quick start instructions
- [MONGODB_README.md](docs/MONGODB_README.md) - MongoDB setup

### Frontend
- [REACT_FRONTEND_GUIDE.md](docs/REACT_FRONTEND_GUIDE.md) - React frontend guide
- [START_REACT.md](docs/START_REACT.md) - Frontend quick start
- [UI_IMPROVEMENTS.md](docs/UI_IMPROVEMENTS.md) - UI features

### Features
- [FINAL_FEATURES.md](docs/FINAL_FEATURES.md) - Complete feature list
- [RESCORE_FEATURE.md](docs/RESCORE_FEATURE.md) - Rescore functionality
- [AUTO_SCORING_ON_UPLOAD.md](docs/AUTO_SCORING_ON_UPLOAD.md) - Auto-scoring
- [RETRY_AND_PARALLEL_PROCESSING.md](docs/RETRY_AND_PARALLEL_PROCESSING.md) - Performance features

### Technical
- [ASYNC_FIXES.md](docs/ASYNC_FIXES.md) - Async/await implementation
- [JD_VIEW_EDIT_UPDATE.md](docs/JD_VIEW_EDIT_UPDATE.md) - Job description editing
- [DESIGN_UPDATE.md](docs/DESIGN_UPDATE.md) - UI design updates

### Testing
- [SAMPLE_RESUMES_GUIDE.md](docs/SAMPLE_RESUMES_GUIDE.md) - Sample resumes for testing
- [UPLOAD_TROUBLESHOOTING.md](docs/UPLOAD_TROUBLESHOOTING.md) - Upload issues

## 🧪 Testing

### Sample Resumes
10 professional resumes are provided in `data/`:
- 5 AI Engineer resumes (excellent → weak)
- 5 Python Developer resumes (excellent → weak)

### Upload & Test
```bash
# 1. Start backend and frontend
# 2. Create a job (AI Engineer or Python Developer)
# 3. Upload resumes from data/ai_engineer/ or data/python_developer/
# 4. Scores calculate automatically!
```

## 🔧 Configuration

### Environment Variables
```bash
# MongoDB
MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net/
DATABASE_NAME=resume_ranker_db

# LLM APIs (at least one required)
GEMINI_API_KEY=your_gemini_key
GROQ_API_KEY=your_groq_key

# Models
GEMINI_MODEL=gemini-2.5-flash
GROQ_MODEL=llama-3.3-70b-versatile

# ChromaDB
CHROMA_PERSIST_DIR=./chroma_db
```

## 📊 Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **MongoDB** - Document database
- **ChromaDB** - Vector database
- **Sentence Transformers** - Embeddings
- **Google Gemini** - Primary LLM
- **Groq** - Fallback LLM
- **PyPDF2 / pdfplumber** - PDF parsing

### Frontend
- **React 18** - UI library
- **TypeScript** - Type safety
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **Axios** - HTTP client
- **Lucide React** - Icons
- **Recharts** - Charts

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request



## 🆘 Support

For issues or questions:
1. Check the documentation in `docs/`
2. Review test files in `tests/`
3. Check backend logs (terminal 5)
4. Check frontend console (F12)

## 🎯 Roadmap

- [ ] Bulk job operations
- [ ] Email notifications
- [ ] Interview scheduling
- [ ] Candidate comparison
- [ ] Export to PDF/Excel
- [ ] Team collaboration
- [ ] Role-based access control
- [ ] Advanced analytics
# Resume_ranker
