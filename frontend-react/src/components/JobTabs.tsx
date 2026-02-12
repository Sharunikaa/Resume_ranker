import { Lock } from 'lucide-react';
import type { Job } from '../types';

interface JobTabsProps {
  jobs: Job[];
  selectedJob: Job | null;
  onSelectJob: (job: Job) => void;
}

export default function JobTabs({ jobs, selectedJob, onSelectJob }: JobTabsProps) {
  return (
    <div className="bg-white border-b border-gray-200 px-6">
      <div className="flex items-center gap-1 overflow-x-auto">
        {jobs.map((job, index) => (
          <button
            key={job.job_id}
            onClick={() => onSelectJob(job)}
            className={`flex items-center gap-2 px-4 py-3 border-b-2 transition-colors whitespace-nowrap ${
              selectedJob?.job_id === job.job_id
                ? 'border-teal-600 text-teal-600 font-medium'
                : 'border-transparent text-gray-600 hover:text-gray-900'
            }`}
          >
            {index > 0 && <Lock size={14} className="text-gray-400" />}
            <span className="text-sm truncate max-w-[200px]">{job.title}</span>
          </button>
        ))}
      </div>
    </div>
  );
}
