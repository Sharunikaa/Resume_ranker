import { useState, useEffect } from 'react';
import { Plus, Upload, RefreshCw, User, Briefcase, Eye, Edit } from 'lucide-react';
import { jobsApi, candidatesApi, rankingApi } from './api';
import type { Job, Candidate } from './types';
import CreateJobModal from './components/CreateJobModal';
import UploadResumesModal from './components/UploadResumesModal';
import CandidateCard from './components/CandidateCard';
import CandidateDetail from './components/CandidateDetail';
import Sidebar from './components/Sidebar';
import JobsView from './components/JobsView';
import ViewEditJDModal from './components/ViewEditJDModal';
import AnalyticsView from './components/AnalyticsView';
import SettingsView from './components/SettingsView';
import Toast from './components/Toast';

function App() {
  const [jobs, setJobs] = useState<Job[]>([]);
  const [selectedJob, setSelectedJob] = useState<Job | null>(null);
  const [candidates, setCandidates] = useState<Candidate[]>([]);
  const [selectedCandidate, setSelectedCandidate] = useState<Candidate | null>(null);
  const [showCreateJob, setShowCreateJob] = useState(false);
  const [showUploadResumes, setShowUploadResumes] = useState(false);
  const [loading, setLoading] = useState(false);
  const [ranking, setRanking] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [currentView, setCurrentView] = useState<'jobs' | 'candidates' | 'analytics' | 'settings'>('candidates');
  const [showJDModal, setShowJDModal] = useState(false);
  const [jdModalMode, setJDModalMode] = useState<'view' | 'edit'>('view');
  const [toast, setToast] = useState<{ message: string; type: 'success' | 'error' | 'info' } | null>(null);

  useEffect(() => {
    loadJobs();
    
    // Restore view from URL on page load
    const params = new URLSearchParams(window.location.search);
    const view = params.get('view') as 'jobs' | 'candidates' | 'analytics' | 'settings' | null;
    if (view) {
      setCurrentView(view);
    }
  }, []);

  useEffect(() => {
    if (selectedJob) {
      console.log('Selected job changed, loading candidates for:', selectedJob.job_id);
      loadCandidates(selectedJob.job_id);
      
      // Update URL when job changes
      const url = new URL(window.location.href);
      url.searchParams.set('job', selectedJob.job_id);
      if (currentView === 'candidates') {
        url.searchParams.set('view', 'candidates');
      }
      window.history.replaceState({}, '', url);
    }
  }, [selectedJob]);

  const loadJobs = async () => {
    try {
      const response = await jobsApi.list();
      setJobs(response.data);
      
      // Check if there's a job ID in the URL
      const params = new URLSearchParams(window.location.search);
      const jobId = params.get('job');
      
      if (jobId) {
        // Find and select the job from URL
        const job = response.data.find(j => j.job_id === jobId);
        if (job) {
          setSelectedJob(job);
          return;
        }
      }
      
      // Otherwise select first job if none selected
      if (response.data.length > 0 && !selectedJob) {
        setSelectedJob(response.data[0]);
        // Update URL with first job
        const url = new URL(window.location.href);
        url.searchParams.set('job', response.data[0].job_id);
        window.history.replaceState({}, '', url);
      }
    } catch (error) {
      console.error('Failed to load jobs:', error);
    }
  };

  const loadCandidates = async (jobId: string) => {
    try {
      setLoading(true);
      console.log('Loading candidates for job:', jobId);
      // Use candidates endpoint to get ALL candidates (including unranked ones)
      const response = await candidatesApi.list(jobId);
      console.log('Candidates loaded:', response.data.length, 'candidates');
      console.log('Candidate data:', response.data);
      
      // Force state update by creating a new array
      const newCandidates = [...response.data];
      setCandidates(newCandidates);
      console.log('State updated with candidates:', newCandidates.length);
    } catch (error) {
      console.error('Failed to load candidates:', error);
      // Fallback to rankings endpoint if candidates endpoint fails
      try {
        console.log('Trying fallback rankings endpoint...');
        const response = await rankingApi.getRankings(jobId);
        console.log('Fallback rankings loaded:', response.data.length, 'candidates');
        const newCandidates = [...response.data];
        setCandidates(newCandidates);
      } catch (fallbackError) {
        console.error('Fallback also failed:', fallbackError);
        setCandidates([]);
      }
    } finally {
      setLoading(false);
    }
  };

  const handleCreateJob = async (title: string, description: string) => {
    try {
      const response = await jobsApi.create({ title, description });
      setJobs([response.data, ...jobs]);
      setSelectedJob(response.data);
      setShowCreateJob(false);
      setToast({ message: 'Job created successfully!', type: 'success' });
    } catch (error) {
      console.error('Failed to create job:', error);
      setToast({ message: 'Failed to create job. Check console for details.', type: 'error' });
    }
  };

  const handleUploadResumes = async (files: File[]) => {
    if (!selectedJob) {
      console.error('No job selected');
      return;
    }
    
    console.log('Uploading resumes...', { jobId: selectedJob.job_id, fileCount: files.length });
    
    try {
      const response = await candidatesApi.uploadResumes(selectedJob.job_id, files);
      console.log('Upload response:', response.data);
      console.log('Uploaded candidates:', response.data.uploaded);
      console.log('Upload errors:', response.data.errors);
      
      const uploadedCount = response.data.uploaded?.length || 0;
      const errorCount = response.data.errors?.length || 0;
      
      setShowUploadResumes(false);
      
      if (uploadedCount > 0) {
        // Show upload success message
        if (errorCount === 0) {
          setToast({ 
            message: `Successfully uploaded ${uploadedCount} resume(s)! Calculating scores...`, 
            type: 'success' 
          });
        } else {
          setToast({ 
            message: `Uploaded ${uploadedCount} resume(s), but ${errorCount} failed. Calculating scores...`, 
            type: 'info' 
          });
        }
        
        // Reload candidates to show them immediately (with 0% scores)
        console.log('Reloading candidates after upload...');
        await loadCandidates(selectedJob.job_id);
        console.log('Candidates reloaded, current count:', candidates.length);
        
        // Automatically trigger ranking
        console.log('Auto-triggering ranking...');
        setRanking(true);
        try {
          await rankingApi.trigger(selectedJob.job_id);
          await loadCandidates(selectedJob.job_id);
          setToast({ 
            message: `All ${uploadedCount} candidate(s) scored successfully!`, 
            type: 'success' 
          });
        } catch (rankError) {
          console.error('Auto-ranking failed:', rankError);
          setToast({ 
            message: 'Upload successful, but scoring failed. Click Refresh Rankings to retry.', 
            type: 'error' 
          });
        } finally {
          setRanking(false);
        }
      } else if (errorCount > 0) {
        const firstError = response.data.errors[0];
        setToast({ 
          message: `Failed to upload resumes: ${firstError}`, 
          type: 'error' 
        });
      }
    } catch (error: any) {
      console.error('Failed to upload resumes:', error);
      console.error('Error details:', error.response?.data);
      setToast({ 
        message: `Failed to upload resumes: ${error.response?.data?.detail || error.message}`, 
        type: 'error' 
      });
    }
  };

  const handleTriggerRanking = async () => {
    if (!selectedJob) return;
    try {
      setRanking(true);
      await rankingApi.trigger(selectedJob.job_id);
      await loadCandidates(selectedJob.job_id);
      setToast({ message: 'Ranking completed successfully!', type: 'success' });
    } catch (error) {
      console.error('Failed to trigger ranking:', error);
      setToast({ message: 'Failed to trigger ranking. Check console for details.', type: 'error' });
    } finally {
      setRanking(false);
    }
  };

  const handleUpdateJD = async (jobId: string, description: string) => {
    try {
      await jobsApi.update(jobId, { description });
      await loadJobs();
      setToast({ message: 'Job description updated! Click Refresh Rankings to update scores.', type: 'success' });
    } catch (error) {
      console.error('Failed to update job:', error);
      setToast({ message: 'Failed to update job description.', type: 'error' });
      throw error;
    }
  };

  const handleRescore = async (candidateId: string) => {
    if (!selectedJob) return;
    
    try {
      // Trigger rescore for this candidate (will re-rank all candidates in the job)
      await rankingApi.rescore(candidateId);
      // Reload all candidates to get updated scores
      await loadCandidates(selectedJob.job_id);
      // Update the selected candidate with new data
      const response = await rankingApi.getRankings(selectedJob.job_id);
      const updatedCandidate = response.data.find(c => c.candidate_id === candidateId);
      if (updatedCandidate) {
        setSelectedCandidate(updatedCandidate);
      }
    } catch (error: any) {
      console.error('Failed to rescore:', error);
      const errorMsg = error.response?.data?.detail || error.message || 'Failed to rescore candidate';
      throw new Error(errorMsg);
    }
  };

  if (selectedCandidate) {
    return (
      <CandidateDetail
        candidate={selectedCandidate}
        onBack={() => setSelectedCandidate(null)}
        onRescore={handleRescore}
        onShowToast={(message, type) => setToast({ message, type })}
      />
    );
  }

  const handleViewChange = (view: 'jobs' | 'candidates' | 'analytics' | 'settings') => {
    setCurrentView(view);
    if (view === 'candidates' && !selectedJob && jobs.length > 0) {
      setSelectedJob(jobs[0]);
    }
    
    // Update URL when switching views
    const url = new URL(window.location.href);
    url.searchParams.set('view', view);
    if (view === 'candidates' && selectedJob) {
      url.searchParams.set('job', selectedJob.job_id);
    }
    window.history.replaceState({}, '', url);
  };

  const handleSaveAPIKeys = async (geminiKey: string, groqKey: string) => {
    const response = await fetch(`${import.meta.env.VITE_API_URL || 'http://localhost:8000/api'}/settings/api-keys`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ gemini_api_key: geminiKey, groq_api_key: groqKey }),
    });
    if (!response.ok) throw new Error('Failed to save API keys');
  };

  const handleLoadAPIKeys = async () => {
    const response = await fetch(`${import.meta.env.VITE_API_URL || 'http://localhost:8000/api'}/settings/api-keys`);
    if (!response.ok) return {};
    return await response.json();
  };

  return (
    <div className="flex h-screen bg-gray-50">
      {/* Toast Notifications */}
      {toast && (
        <Toast
          message={toast.message}
          type={toast.type}
          onClose={() => setToast(null)}
        />
      )}

      {/* Sidebar */}
      <Sidebar currentView={currentView} onViewChange={handleViewChange} />

      {/* Main Content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Show Jobs View */}
        {currentView === 'jobs' && (
          <JobsView
            jobs={jobs}
            onSelectJob={(job) => {
              setSelectedJob(job);
              setCurrentView('candidates');
            }}
            onCreateJob={() => setShowCreateJob(true)}
            getCandidateCount={async (jobId) => {
              try {
                const response = await rankingApi.getRankings(jobId);
                return response.data.length;
              } catch {
                return 0;
              }
            }}
          />
        )}

        {/* Show Analytics View */}
        {currentView === 'analytics' && (
          <AnalyticsView 
            jobs={jobs}
            selectedJob={selectedJob}
            candidates={candidates}
          />
        )}

        {/* Show Settings View */}
        {currentView === 'settings' && (
          <SettingsView 
            onSave={handleSaveAPIKeys}
            onLoad={handleLoadAPIKeys}
          />
        )}

        {/* Show Candidates View */}
        {currentView === 'candidates' && (
          <>
            {/* Header with App Name */}
            <header className="bg-white border-b border-gray-200 px-6 py-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-4 flex-1">
                  {/* App Name */}
                  <div className="flex-1">
                    <h1 className="text-xl font-bold text-gray-900">
                      CandiSight
                    </h1>
                  </div>
                  
                  {/* JD Action Icons with Tooltips */}
                  {selectedJob && (
                    <div className="flex items-center gap-2">
                      <div className="relative group">
                        <button
                          onClick={() => {
                            setJDModalMode('view');
                            setShowJDModal(true);
                          }}
                          className="p-2 text-gray-600 hover:bg-gray-100 rounded-lg transition-colors"
                        >
                          <Eye size={20} />
                        </button>
                        <div className="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 px-3 py-1.5 bg-gray-900 text-white text-xs rounded-lg opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap pointer-events-none">
                          View Job Description
                          <div className="absolute top-full left-1/2 -translate-x-1/2 -mt-1 border-4 border-transparent border-t-gray-900"></div>
                        </div>
                      </div>
                      <div className="relative group">
                        <button
                          onClick={() => {
                            setJDModalMode('edit');
                            setShowJDModal(true);
                          }}
                          className="p-2 text-gray-600 hover:bg-gray-100 rounded-lg transition-colors"
                        >
                          <Edit size={20} />
                        </button>
                        <div className="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 px-3 py-1.5 bg-gray-900 text-white text-xs rounded-lg opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap pointer-events-none">
                          Edit Job Description
                          <div className="absolute top-full left-1/2 -translate-x-1/2 -mt-1 border-4 border-transparent border-t-gray-900"></div>
                        </div>
                      </div>
                      <div className="relative group">
                        <button
                          onClick={handleTriggerRanking}
                          disabled={ranking || candidates.length === 0}
                          className="p-2 text-gray-600 hover:bg-gray-100 rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                        >
                          <RefreshCw size={20} className={ranking ? 'animate-spin' : ''} />
                        </button>
                        <div className="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 px-3 py-1.5 bg-gray-900 text-white text-xs rounded-lg opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap pointer-events-none">
                          {ranking ? 'Ranking...' : 'Refresh Rankings'}
                          <div className="absolute top-full left-1/2 -translate-x-1/2 -mt-1 border-4 border-transparent border-t-gray-900"></div>
                        </div>
                      </div>
                    </div>
                  )}
                </div>
            <div className="flex items-center gap-3 ml-4">
              {selectedJob && (
                <>
                  <button
                    onClick={() => setShowUploadResumes(true)}
                    className="flex items-center gap-2 px-4 py-2 bg-teal-600 text-white rounded-lg hover:bg-teal-700 transition-colors text-sm"
                  >
                    <Upload size={18} />
                    Upload Resumes
                  </button>
                </>
              )}
              <button
                onClick={() => setShowCreateJob(true)}
                className="flex items-center gap-2 px-4 py-2 bg-teal-600 text-white rounded-lg hover:bg-teal-700 transition-colors text-sm font-medium"
              >
                <Plus size={18} />
                Create Job
              </button>
            </div>
          </div>
        </header>

        {/* Candidates Table */}
        <main className="flex-1 overflow-auto p-6">
          {!selectedJob ? (
            <div className="flex items-center justify-center h-full">
              <div className="text-center">
                <Briefcase size={64} className="mx-auto text-gray-400 mb-4" />
                <h2 className="text-xl font-semibold text-gray-700 mb-2">No Job Selected</h2>
                <p className="text-gray-500 mb-4">Create a new job or select one from the sidebar</p>
                <button
                  onClick={() => setShowCreateJob(true)}
                  className="px-6 py-3 bg-teal-600 text-white rounded-lg hover:bg-teal-700 transition-colors"
                >
                  Create Your First Job
                </button>
              </div>
            </div>
          ) : (
            <>
              {/* Job Title in Center */}
              <div className="mb-6 text-center">
                <h2 className="text-2xl font-bold text-gray-900">{selectedJob.title}</h2>
              </div>

              {loading ? (
            <div className="flex items-center justify-center h-full">
              <RefreshCw size={48} className="animate-spin text-teal-600" />
            </div>
          ) : candidates.length === 0 ? (
            <div className="flex items-center justify-center h-full">
              <div className="text-center">
                <User size={64} className="mx-auto text-gray-400 mb-4" />
                <h2 className="text-xl font-semibold text-gray-700 mb-2">No Candidates Yet</h2>
                <p className="text-gray-500 mb-4">Upload resumes to start ranking candidates</p>
                <button
                  onClick={() => setShowUploadResumes(true)}
                  className="px-6 py-3 bg-teal-600 text-white rounded-lg hover:bg-teal-700 transition-colors"
                >
                  Upload Resumes
                </button>
              </div>
            </div>
          ) : (
            <div className="bg-white rounded-lg border border-gray-200 overflow-hidden">
              {/* Search Bar */}
              <div className="p-4 border-b border-gray-200">
                <div className="relative">
                  <input
                    type="text"
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    placeholder="Search candidates by name or email..."
                    className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-transparent"
                  />
                  <div className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400">
                    <svg width="16" height="16" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24">
                      <circle cx="11" cy="11" r="8"/>
                      <path d="m21 21-4.35-4.35"/>
                    </svg>
                  </div>
                </div>
              </div>

              {/* Table */}
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead className="bg-gray-50 border-b border-gray-200">
                    <tr>
                      <th className="py-3 px-4 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Candidate
                      </th>
                      <th className="py-3 px-4 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Email
                      </th>
                      <th className="py-3 px-4 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Overall Score
                      </th>
                      <th className="py-3 px-4 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Project Similarity
                      </th>
                      <th className="py-3 px-4 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Skill Match
                      </th>
                      <th className="py-3 px-4 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Experience Match
                      </th>
                    </tr>
                  </thead>
                  <tbody>
                    {candidates
                      .filter((c) => {
                        if (!searchQuery) return true;
                        const query = searchQuery.toLowerCase();
                        return (
                          c.name.toLowerCase().includes(query) ||
                          c.email.toLowerCase().includes(query)
                        );
                      })
                      .sort((a, b) => (a.rank || 999) - (b.rank || 999))
                      .map((candidate) => (
                        <CandidateCard
                          key={candidate.candidate_id}
                          candidate={candidate}
                          onClick={() => setSelectedCandidate(candidate)}
                        />
                      ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}
          </>
        )}
        </main>
          </>
        )}
      </div>

      {/* Modals */}
      {showCreateJob && (
        <CreateJobModal
          onClose={() => setShowCreateJob(false)}
          onCreate={handleCreateJob}
        />
      )}
      {showUploadResumes && selectedJob && (
        <UploadResumesModal
          onClose={() => setShowUploadResumes(false)}
          onUpload={handleUploadResumes}
        />
      )}
      {showJDModal && selectedJob && (
        <ViewEditJDModal
          job={selectedJob}
          mode={jdModalMode}
          onClose={() => setShowJDModal(false)}
          onUpdate={handleUpdateJD}
          onShowToast={(message, type) => setToast({ message, type })}
        />
      )}
    </div>
  );
}

export default App;
