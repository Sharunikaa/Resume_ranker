# Resume Ranker - React Frontend

Modern React frontend for the AI-powered Resume Ranker application.

## Features

- 🎨 Modern UI with Tailwind CSS
- ⚡ Fast development with Vite
- 📱 Responsive design
- 🔄 Real-time candidate ranking
- 📊 Interactive score visualizations
- 📄 PDF resume upload
- 🤖 AI-powered job description parsing

## Getting Started

### Prerequisites

- Node.js 18+ and npm
- Backend API running on http://localhost:8000

### Installation

```bash
cd frontend-react
npm install
```

### Development

```bash
npm run dev
```

The app will be available at http://localhost:5173

### Build for Production

```bash
npm run build
npm run preview  # Preview the production build
```

## Project Structure

```
src/
├── components/          # React components
│   ├── Sidebar.tsx
│   ├── CandidateCard.tsx
│   ├── CandidateDetail.tsx
│   ├── CreateJobModal.tsx
│   └── UploadResumesModal.tsx
├── types.ts            # TypeScript interfaces
├── api.ts              # API client
├── App.tsx             # Main app component
└── main.tsx            # Entry point
```

## Environment Variables

Create a `.env` file:

```
VITE_API_URL=http://localhost:8000/api
```

## Usage

1. **Create a Job**: Click "Create Job" button in the top right
2. **Upload Resumes**: Select a job and click "Upload Resumes"
3. **Trigger Ranking**: Click "Trigger Ranking" to analyze and rank candidates
4. **View Details**: Click on any candidate card to see detailed analysis

## Tech Stack

- React 18
- TypeScript
- Vite
- Tailwind CSS
- Axios
- Lucide React (icons)
