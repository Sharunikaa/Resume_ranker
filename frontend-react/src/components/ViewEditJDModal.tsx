import { X } from 'lucide-react';
import { useState } from 'react';
import type { Job } from '../types';

interface ViewEditJDModalProps {
  job: Job;
  onClose: () => void;
  onUpdate: (jobId: string, description: string) => Promise<void>;
  mode: 'view' | 'edit';
  onShowToast?: (message: string, type: 'success' | 'error' | 'info') => void;
}

export default function ViewEditJDModal({ job, onClose, onUpdate, mode: initialMode, onShowToast }: ViewEditJDModalProps) {
  const [mode, setMode] = useState<'view' | 'edit'>(initialMode);
  const [description, setDescription] = useState(job.description);
  const [updating, setUpdating] = useState(false);

  const handleUpdate = async () => {
    setUpdating(true);
    try {
      await onUpdate(job.job_id, description);
      onClose();
    } catch (error) {
      console.error('Failed to update job:', error);
      if (onShowToast) {
        onShowToast('Failed to update job description', 'error');
      }
    } finally {
      setUpdating(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg shadow-xl max-w-3xl w-full max-h-[90vh] flex flex-col">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-gray-200">
          <div>
            <h2 className="text-xl font-bold text-gray-900">
              {mode === 'view' ? 'View' : 'Edit'} Job Description
            </h2>
            <p className="text-sm text-gray-500 mt-1">{job.title}</p>
          </div>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 transition-colors"
          >
            <X size={24} />
          </button>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-y-auto p-6">
          {mode === 'view' ? (
            <div className="prose max-w-none">
              <p className="text-gray-700 whitespace-pre-wrap">{job.description}</p>
              
              {job.extracted_requirements && (
                <div className="mt-6 space-y-4">
                  {job.extracted_requirements.required_skills && (
                    <div>
                      <h3 className="text-sm font-semibold text-gray-900 mb-2">Required Skills</h3>
                      <div className="flex flex-wrap gap-2">
                        {job.extracted_requirements.required_skills.map((skill, idx) => (
                          <span
                            key={idx}
                            className="px-3 py-1 bg-teal-100 text-teal-700 rounded-full text-sm"
                          >
                            {skill}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}
                  
                  {job.extracted_requirements.experience_level && (
                    <div>
                      <h3 className="text-sm font-semibold text-gray-900 mb-1">Experience Level</h3>
                      <p className="text-gray-700">{job.extracted_requirements.experience_level}</p>
                    </div>
                  )}
                  
                  {job.extracted_requirements.domain && (
                    <div>
                      <h3 className="text-sm font-semibold text-gray-900 mb-1">Domain</h3>
                      <p className="text-gray-700">{job.extracted_requirements.domain}</p>
                    </div>
                  )}
                </div>
              )}
            </div>
          ) : (
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Job Description
              </label>
              <textarea
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                className="w-full h-96 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-teal-500 focus:border-transparent resize-none"
                placeholder="Enter job description..."
              />
              <p className="text-xs text-gray-500 mt-2">
                Note: Updating the job description will re-extract requirements and may affect candidate rankings.
              </p>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="flex items-center justify-end gap-3 p-6 border-t border-gray-200">
          {mode === 'view' ? (
            <>
              <button
                onClick={onClose}
                className="px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-lg transition-colors"
              >
                Close
              </button>
              <button
                onClick={() => setMode('edit')}
                className="px-4 py-2 bg-teal-600 text-white rounded-lg hover:bg-teal-700 transition-colors"
              >
                Edit Description
              </button>
            </>
          ) : (
            <>
              <button
                onClick={() => {
                  setDescription(job.description);
                  setMode('view');
                }}
                className="px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-lg transition-colors"
                disabled={updating}
              >
                Cancel
              </button>
              <button
                onClick={handleUpdate}
                disabled={updating || description === job.description}
                className="px-4 py-2 bg-teal-600 text-white rounded-lg hover:bg-teal-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {updating ? 'Updating...' : 'Save Changes'}
              </button>
            </>
          )}
        </div>
      </div>
    </div>
  );
}
