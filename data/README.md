# Sample Resumes for Testing

This folder contains 10 sample resumes (5 for each role) ranging from most suited to least suited candidates.

## AI Engineer Resumes

Located in `ai_engineer/` folder:

1. **ai_engineer_excellent.pdf** - Dr. Aisha Patel
   - PhD in CS, 8+ years experience
   - Expert in PyTorch, TensorFlow, LLMs, RAG, MLOps
   - Published papers, fine-tuning experience
   - **Expected Rank: #1**

2. **ai_engineer_strong.pdf** - Raj Kumar
   - M.Tech, 5 years experience
   - Strong in PyTorch, LLMs, RAG, FastAPI
   - Production LLM systems experience
   - **Expected Rank: #2**

3. **ai_engineer_good.pdf** - Emily Chen
   - M.S. Data Science, 3 years experience
   - ML Engineer with PyTorch, scikit-learn
   - Some deep learning experience
   - **Expected Rank: #3**

4. **ai_engineer_moderate.pdf** - Michael Brown
   - B.S. CS, 2 years experience
   - Software Engineer learning ML
   - Basic ML knowledge
   - **Expected Rank: #4**

5. **ai_engineer_weak.pdf** - Sarah Johnson
   - Recent graduate, minimal experience
   - Basic Python, completed online courses
   - No professional AI experience
   - **Expected Rank: #5**

## Senior Python Developer Resumes

Located in `python_developer/` folder:

1. **python_dev_excellent.pdf** - David Martinez
   - M.S. CS, 10+ years experience
   - Expert in FastAPI, Django, Flask, microservices
   - System design, Docker, Kubernetes, AWS
   - **Expected Rank: #1**

2. **python_dev_strong.pdf** - Priya Sharma
   - B.Tech, 6 years experience
   - Strong in Django, Flask, FastAPI, PostgreSQL
   - Microservices and cloud deployment
   - **Expected Rank: #2**

3. **python_dev_good.pdf** - Alex Thompson
   - B.S. CS, 3 years experience
   - Flask, Django, PostgreSQL
   - Web development and APIs
   - **Expected Rank: #3**

4. **python_dev_moderate.pdf** - Lisa Wang
   - B.S. IS, 1 year experience
   - Junior developer learning Python
   - Basic Flask and SQL
   - **Expected Rank: #4**

5. **python_dev_weak.pdf** - Tom Anderson
   - Bootcamp graduate, minimal experience
   - Basic Python, completed online courses
   - No professional experience
   - **Expected Rank: #5**

## How to Use

### Upload via Frontend

1. Open the CandiSight frontend at http://localhost:5173
2. Select the job (AI Engineer or Senior Python Developer)
3. Click "Upload Resumes"
4. Navigate to the appropriate folder:
   - For AI Engineer job: `data/ai_engineer/`
   - For Python Developer job: `data/python_developer/`
5. Select all 5 PDFs and upload
6. Click "Refresh Rankings" (🔄) to calculate scores
7. Candidates should appear ranked from best to worst match

### Expected Results

After ranking, you should see:
- **Excellent** candidates: 85-95% overall score
- **Strong** candidates: 75-85% overall score
- **Good** candidates: 65-75% overall score
- **Moderate** candidates: 50-65% overall score
- **Weak** candidates: 30-50% overall score

The system will also provide:
- Skill gaps analysis
- Career insights
- Interview questions
- Detailed explanations for rankings

## Testing Different Scenarios

1. **Upload all at once**: Test bulk upload functionality
2. **Upload one by one**: Test incremental uploads
3. **Mix roles**: Upload AI resumes to Python job (should rank lower)
4. **Re-score**: Use the "Rescore" button to recalculate rankings

## Regenerating Resumes

If you need to regenerate these resumes:

```bash
cd /Users/Sharunikaa/Desktop/Clg/llm_lab/resume_ranker
python3 generate_sample_resumes.py
```

This will recreate all 10 PDFs with the same content.
