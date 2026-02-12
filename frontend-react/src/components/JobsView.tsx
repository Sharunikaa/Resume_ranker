import { Briefcase, Calendar, Users } from 'lucide-react';
import { useState, useEffect } from 'react';
import type { Job } from '../types';

interface JobsViewProps {
  jobs: Job[];
  onSelectJob: (job: Job) => void;
  onCreateJob: () => void;
  getCandidateCount: (jobId: string) => Promise<number>;
}

export default function JobsView({ jobs, onSelectJob, onCreateJob, getCandidateCount }: JobsViewProps) {
  const [candidateCounts, setCandidateCounts] = useState<Record<string, number>>({});

  useEffect(() => {
    // Load candidate counts for all jobs
    const loadCounts = async () => {
      const counts: Record<string, number> = {};
      for (const job of jobs) {
        counts[job.job_id] = await getCandidateCount(job.job_id);
      }
      setCandidateCounts(counts);
    };
    loadCounts();
  }, [jobs, getCandidateCount]);
  return (
    <div className="flex-1 flex flex-col overflow-hidden">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 px-6 py-4">
        <h1 className="text-xl font-bold text-gray-900">CandiSight</h1>
      </header>

      {/* Content */}
      <div className="flex-1 overflow-y-auto p-6">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-2xl font-bold text-gray-900">All Jobs</h2>
          <button
            onClick={onCreateJob}
            className="px-4 py-2 bg-teal-600 text-white rounded-lg hover:bg-teal-700 transition-colors text-sm font-medium"
          >
            + Create New Job
          </button>
        </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {jobs.map((job) => (
          <div
            key={job.job_id}
            onClick={() => onSelectJob(job)}
            className="bg-white rounded-lg border border-gray-200 p-5 hover:shadow-lg transition-shadow cursor-pointer"
          >
            <div className="flex items-start gap-3 mb-3">
              <div className="w-10 h-10 bg-teal-100 rounded-lg flex items-center justify-center flex-shrink-0">
                <Briefcase size={20} className="text-teal-600" />
              </div>
              <div className="flex-1 min-w-0">
                <h3 className="font-semibold text-gray-900 truncate">{job.title}</h3>
                <p className="text-xs text-gray-500 mt-0.5">
                  {job.extracted_requirements?.domain || 'General'}
                </p>
              </div>
            </div>

            <p className="text-sm text-gray-600 line-clamp-3 mb-4">
              {job.description}
            </p>

            <div className="flex items-center gap-4 text-xs text-gray-500">
              <div className="flex items-center gap-1">
                <Calendar size={14} />
                <span>
                  {job.created_at
                    ? new Date(job.created_at).toLocaleDateString()
                    : 'N/A'}
                </span>
              </div>
              <div className="flex items-center gap-1">
                <Users size={14} />
                <span>{candidateCounts[job.job_id] || 0} candidates</span>
              </div>
            </div>

            {job.extracted_requirements?.required_skills && (
              <div className="mt-3 flex flex-wrap gap-1">
                {job.extracted_requirements.required_skills.slice(0, 3).map((skill, idx) => (
                  <span
                    key={idx}
                    className="px-2 py-0.5 bg-gray-100 text-gray-700 rounded text-xs"
                  >
                    {skill}
                  </span>
                ))}
                {job.extracted_requirements.required_skills.length > 3 && (
                  <span className="px-2 py-0.5 bg-gray-100 text-gray-500 rounded text-xs">
                    +{job.extracted_requirements.required_skills.length - 3}
                  </span>
                )}
              </div>
            )}
          </div>
        ))}
      </div>

      {jobs.length === 0 && (
        <div className="text-center py-12">
          <Briefcase size={48} className="mx-auto text-gray-400 mb-4" />
          <h3 className="text-lg font-semibold text-gray-700 mb-2">No Jobs Yet</h3>
          <p className="text-gray-500 mb-4">Create your first job to start ranking candidates</p>
          <button
            onClick={onCreateJob}
            className="px-6 py-3 bg-teal-600 text-white rounded-lg hover:bg-teal-700 transition-colors"
          >
            Create Your First Job
          </button>
        </div>
      )}
      </div>
    </div>
  );
}
