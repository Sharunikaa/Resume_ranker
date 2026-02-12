# Resume Ranker - LLM-Powered Multi-Job Resume Ranking System

A comprehensive system for ranking resumes against job descriptions using LLM-powered analysis, embeddings, and innovative career trajectory insights.

## Features

- **Job Management**: Create and manage multiple job postings
- **Resume Parsing**: Extract structured data from PDF resumes using LLM
- **Intelligent Ranking**: Multi-factor scoring (projects, skills, experience)
- **Career Insights**: Learning velocity, skill evolution, adaptability scores
- **Skill Gap Analysis**: Visual gap identification with learning suggestions
- **AI Interview Co-Pilot**: Generate personalized interview questions
- **Candidate Comparison**: Side-by-side comparison with radar charts

## Tech Stack

- **Backend**: FastAPI (async)
- **Frontend**: Streamlit (multi-page)
- **Database**: MongoDB
- **Vector DB**: ChromaDB (local persistence)
- **LLM**: Google Gemini API (gemini-pro)
- **Embeddings**: sentence-transformers (all-MiniLM-L6-v2)

## Quick Start

**🚀 New to the project?** See [QUICK_START.md](./QUICK_START.md) for a 5-minute setup guide.

**📚 Need detailed setup?** See [SETUP.md](./SETUP.md) for comprehensive MongoDB and Gemini API configuration.

**🗄️ MongoDB only?** See [MONGODB_README.md](./MONGODB_README.md) for how to create a MongoDB database (Atlas or local) and use it with this project.

## Setup Instructions

### 1. Prerequisites

- Python 3.9+
- MongoDB installed and running
- Google Gemini API key (free tier available)

### 2. Installation

```bash
# Clone or navigate to the project directory
cd resume_ranker

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your credentials
# - GEMINI_API_KEY: Get from https://aistudio.google.com/app/apikey
# - MONGODB_URI: Your MongoDB connection string (default: mongodb://localhost:27017)
# - DATABASE_NAME: Database name (default: resume_ranker)
# - CHROMA_PERSIST_DIR: Path for ChromaDB persistence
# - BACKEND_URL: Backend API URL (default: http://localhost:8000)
```

### 4. MongoDB Setup

**macOS (using Homebrew):**
```bash
brew tap mongodb/brew
brew install mongodb-community@8.0
brew services start mongodb-community@8.0
```

**Verify MongoDB is running:**
```bash
mongosh
# Type: db.adminCommand('ping')
```

For detailed MongoDB setup (including Atlas cloud), see [MONGODB_README.md](./MONGODB_README.md) or [SETUP.md](./SETUP.md#mongodb-installation--setup).

### 5. Verify Setup

Run the setup verification script:
```bash
python test_setup.py
```

This will test your MongoDB connection, Gemini API key, and all dependencies.

### 6. Run the System

#### Start Backend Server

```bash
cd resume_ranker
uvicorn backend.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`
API docs at `http://localhost:8000/docs`

#### Start Frontend

```bash
cd resume_ranker/frontend
streamlit run app.py
```

The frontend will open in your browser at `http://localhost:8501`

## Project Structure

```
resume_ranker/
├── frontend/           # Streamlit multi-page app
├── backend/            # FastAPI backend
│   ├── routes/         # API endpoints
│   ├── services/       # Business logic
│   ├── models/         # Pydantic models
│   ├── database/       # MongoDB connection
│   ├── vector_store/   # ChromaDB client
│   └── llm/            # LLM integration
├── utils/              # Utility functions
└── requirements.txt    # Python dependencies
```

## API Documentation

Once the backend is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Usage Flow

1. **Create Job**: Navigate to "Job Management" page, enter job title and description
2. **Upload Resumes**: Go to "Resume Upload" page, upload PDF resumes
3. **Rank Candidates**: Go to "Rankings" page, trigger ranking process
4. **View Details**: Click on any candidate to see detailed analysis
5. **Compare**: Select multiple candidates for side-by-side comparison

## Execution Flow

1. User creates job → LLM (Gemini) extracts requirements → store in MongoDB.
2. User uploads resumes → parse PDF (utils) → LLM extracts structured data → embeddings (sentence-transformers) → store in MongoDB + ChromaDB.
3. User triggers ranking → similarity + skill/experience scores → final score → rank → generate explanation, trajectory, skill gaps, interview questions → store.
4. User views rankings → clicks candidate → detail page (scores, resume, insights, gaps, questions).
5. User compares 2–5 candidates → side-by-side and radar chart.

## Key Endpoints

- `POST /api/jobs` - Create new job
- `GET /api/jobs` - List all jobs
- `POST /api/jobs/{job_id}/resumes` - Upload resume
- `POST /api/jobs/{job_id}/rank` - Trigger ranking
- `GET /api/jobs/{job_id}/rankings` - Get ranked candidates
- `GET /api/candidates/{candidate_id}` - Get candidate details
- `POST /api/candidates/compare` - Compare candidates

## Database Schemas

### Jobs Collection
- `job_id`, `title`, `description`
- `extracted_requirements` (skills, domain, experience_level)
- `weights` (project_weight, skill_weight, experience_weight)
- `created_at`

### Candidates Collection
- `candidate_id`, `job_id`, `name`, `email`
- `structured_resume` (skills, experience, projects, education)
- `scores` (project_similarity, skill_match, experience_match, final_score)
- `career_insights` (learning_velocity, skill_evolution_rate, adaptability_score)
- `rank`, `explanation`, `skill_gaps`, `interview_questions`
- `created_at`

## License

MIT
