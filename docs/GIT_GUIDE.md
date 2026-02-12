# Git Setup & Usage Guide

## ✅ Current Status

Your git remote is **correctly configured**:
```
origin: git@github.com:Sharunikaa/Resume_ranker.git
```

## 📝 Commit All Changes

### Step 1: Check Status
```bash
cd /Users/Sharunikaa/Desktop/Clg/llm_lab/resume_ranker
git status
```

### Step 2: Add All Files
```bash
# Add all project files
git add .

# Or add specific folders
git add backend/
git add frontend-react/
git add data/
git add docs/
git add tests/
git add utils/
git add .gitignore
git add requirements.txt
git add .env.example
```

### Step 3: Commit
```bash
git commit -m "Complete CandiSight implementation with React frontend

- Implemented modern React + TypeScript frontend with Tailwind CSS
- Added auto-scoring on resume upload with parallel processing (batch=3)
- Implemented automatic retry logic with exponential backoff
- Added LLM caching in MongoDB for faster responses
- Created toast notifications for better UX
- Added rescore functionality for individual candidates
- Implemented job description view/edit functionality
- Added settings page for secure API key management
- Created 10 sample resumes for testing (AI Engineer + Python Dev)
- Organized project structure (docs/, tests/, data/)
- Fixed async/await issues for proper event loop handling
- Added comprehensive documentation"
```

### Step 4: Push to GitHub
```bash
git push origin main
```

## 🔄 Change Git Remote (If Needed)

### Check Current Remote
```bash
git remote -v
```

### Remove Old Remote
```bash
git remote remove origin
```

### Add New Remote
```bash
# SSH (recommended)
git remote add origin git@github.com:USERNAME/REPO.git

# HTTPS
git remote add origin https://github.com/USERNAME/REPO.git
```

### Verify
```bash
git remote -v
```

### Push
```bash
git push -u origin main
```

## 🌿 Branch Management

### Create New Branch
```bash
git checkout -b feature/new-feature
```

### Switch Branch
```bash
git checkout main
git checkout feature/new-feature
```

### List Branches
```bash
git branch -a
```

### Delete Branch
```bash
git branch -d feature/old-feature
```

## 📦 Common Git Commands

### Status & Changes
```bash
git status                    # Check status
git diff                      # See changes
git log --oneline            # View commit history
```

### Adding Files
```bash
git add .                     # Add all
git add file.py              # Add specific file
git add folder/              # Add folder
```

### Committing
```bash
git commit -m "message"      # Commit with message
git commit --amend           # Amend last commit
```

### Pushing & Pulling
```bash
git push origin main         # Push to remote
git pull origin main         # Pull from remote
git fetch origin             # Fetch without merge
```

### Undoing Changes
```bash
git restore file.py          # Discard changes
git restore --staged file.py # Unstage file
git reset HEAD~1             # Undo last commit (keep changes)
git reset --hard HEAD~1      # Undo last commit (discard changes)
```

## 🔐 SSH vs HTTPS

### SSH (Recommended)
```bash
git remote add origin git@github.com:Sharunikaa/Resume_ranker.git
```
**Pros**: No password needed, more secure
**Cons**: Requires SSH key setup

### HTTPS
```bash
git remote add origin https://github.com/Sharunikaa/Resume_ranker.git
```
**Pros**: Easy to set up
**Cons**: Requires username/password or token

## 📋 .gitignore

Your `.gitignore` is configured to exclude:
- `.env` (sensitive data)
- `chroma_db/` (large vector database)
- `node_modules/` (dependencies)
- `__pycache__/` (Python cache)
- `*.pyc` (compiled Python)
- `.DS_Store` (macOS files)

## 🚀 First-Time Setup

If you need to set up a new repository:

### 1. Create GitHub Repository
- Go to https://github.com/new
- Name: `Resume_ranker`
- Don't initialize with README (you already have one)

### 2. Initialize Local Repo
```bash
cd /Users/Sharunikaa/Desktop/Clg/llm_lab/resume_ranker
git init
git add .
git commit -m "Initial commit"
git branch -M main
```

### 3. Connect to GitHub
```bash
git remote add origin git@github.com:Sharunikaa/Resume_ranker.git
git push -u origin main
```

## 🔄 Update Existing Remote

If you need to change the remote URL:

```bash
# Check current remote
git remote -v

# Update remote URL
git remote set-url origin git@github.com:Sharunikaa/NEW_REPO.git

# Or remove and re-add
git remote remove origin
git remote add origin git@github.com:Sharunikaa/NEW_REPO.git

# Verify
git remote -v

# Push
git push -u origin main
```

## 📊 Your Current Situation

Based on the terminal output:

1. ✅ **Git initialized** in `/Users/Sharunikaa/Desktop/Clg/llm_lab/resume_ranker/`
2. ✅ **Remote set correctly** to `Resume_ranker.git`
3. ✅ **Initial commit made** with README.md
4. ✅ **Pushed to GitHub** successfully
5. ⚠️ **Many untracked files** - Need to commit all your work!

## 🎯 Next Steps

### Commit All Your Work
```bash
cd /Users/Sharunikaa/Desktop/Clg/llm_lab/resume_ranker

# Add all files
git add .

# Commit
git commit -m "Complete CandiSight implementation"

# Push
git push origin main
```

### Verify on GitHub
1. Go to https://github.com/Sharunikaa/Resume_ranker
2. Check if all files are there
3. Verify README displays correctly

## 🆘 Troubleshooting

### "Permission denied (publickey)"
- Need to set up SSH key
- Or use HTTPS instead

### "Remote already exists"
```bash
git remote remove origin
git remote add origin NEW_URL
```

### "Diverged branches"
```bash
git pull origin main --rebase
git push origin main
```

### "Large files"
- Check `.gitignore` is working
- Don't commit `chroma_db/`, `node_modules/`, `.env`

## 📚 Resources

- [Git Documentation](https://git-scm.com/doc)
- [GitHub Guides](https://guides.github.com/)
- [Git Cheat Sheet](https://education.github.com/git-cheat-sheet-education.pdf)

---

**Your repository**: https://github.com/Sharunikaa/Resume_ranker
