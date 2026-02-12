import { useState } from 'react';
import { ArrowLeft, Mail, TrendingUp, Zap, Target, FileText, X, RefreshCw } from 'lucide-react';
import type { Candidate } from '../types';

interface CandidateDetailProps {
  candidate: Candidate;
  onBack: () => void;
  onRescore?: (candidateId: string) => Promise<void>;
  onShowToast?: (message: string, type: 'success' | 'error' | 'info') => void;
}

export default function CandidateDetail({ candidate, onBack, onRescore, onShowToast }: CandidateDetailProps) {
  const [showResumeViewer, setShowResumeViewer] = useState(false);
  const [rescoring, setRescoring] = useState(false);
  const scores = candidate.scores || {};
  const resume = candidate.structured_resume || {};
  const insights = candidate.career_insights || {};

  const handleRescore = async () => {
    if (!onRescore) return;
    setRescoring(true);
    try {
      await onRescore(candidate.candidate_id);
      if (onShowToast) {
        onShowToast('Candidate rescored successfully!', 'success');
      }
    } catch (error: any) {
      console.error('Failed to rescore:', error);
      if (onShowToast) {
        const errorMsg = error.message || 'Failed to rescore candidate. Please try again.';
        onShowToast(errorMsg, 'error');
      }
    } finally {
      setRescoring(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <button
            onClick={onBack}
            className="flex items-center gap-2 text-gray-600 hover:text-gray-900 mb-4"
          >
            <ArrowLeft size={20} />
            Back to Candidates
          </button>
          <div className="flex items-start justify-between">
            <div className="flex items-center gap-4">
              <div className="w-16 h-16 bg-gradient-to-br from-teal-400 to-teal-600 rounded-full flex items-center justify-center text-white font-bold text-2xl">
                {candidate.name
                  .split(' ')
                  .map((n) => n[0])
                  .join('')
                  .toUpperCase()
                  .slice(0, 2)}
              </div>
              <div>
                <h1 className="text-3xl font-bold text-gray-900">{candidate.name}</h1>
                <div className="flex items-center gap-2 text-gray-600 mt-1">
                  <Mail size={16} />
                  <span>{candidate.email}</span>
                </div>
              </div>
            </div>
            <div className="flex items-center gap-4">
              {candidate.rank && (
                <div className="text-right">
                  <div className="text-4xl font-bold text-teal-600">#{candidate.rank}</div>
                  <div className="text-sm text-gray-500">Rank</div>
                </div>
              )}
              <div className="flex gap-2">
                <button
                  onClick={handleRescore}
                  disabled={rescoring}
                  className="flex items-center gap-2 px-4 py-2 bg-white border border-teal-600 text-teal-600 rounded-lg hover:bg-teal-50 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <RefreshCw size={18} className={rescoring ? 'animate-spin' : ''} />
                  {rescoring ? 'Rescoring...' : 'Rescore'}
                </button>
                <button
                  onClick={() => setShowResumeViewer(true)}
                  className="flex items-center gap-2 px-4 py-2 bg-teal-600 text-white rounded-lg hover:bg-teal-700 transition-colors"
                >
                  <FileText size={18} />
                  View Resume
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-7xl mx-auto px-6 py-8">
        <div className="grid grid-cols-3 gap-6">
          {/* Left Column - Scores & Insights */}
          <div className="col-span-1 space-y-6">
            {/* Score Breakdown */}
            <div className="bg-white rounded-lg border border-gray-200 p-6">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">Score Breakdown</h2>
              <div className="space-y-4">
                <div>
                  <div className="flex justify-between text-sm mb-2">
                    <span className="text-gray-600">Project Similarity</span>
                    <span className="font-semibold">{((scores.project_similarity || 0) * 100).toFixed(1)}%</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div
                      className="bg-teal-600 h-2 rounded-full"
                      style={{ width: `${(scores.project_similarity || 0) * 100}%` }}
                    />
                  </div>
                </div>
                <div>
                  <div className="flex justify-between text-sm mb-2">
                    <span className="text-gray-600">Skill Match</span>
                    <span className="font-semibold">{((scores.skill_match || 0) * 100).toFixed(1)}%</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div
                      className="bg-blue-600 h-2 rounded-full"
                      style={{ width: `${(scores.skill_match || 0) * 100}%` }}
                    />
                  </div>
                </div>
                <div>
                  <div className="flex justify-between text-sm mb-2">
                    <span className="text-gray-600">Experience Match</span>
                    <span className="font-semibold">{((scores.experience_match || 0) * 100).toFixed(1)}%</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div
                      className="bg-purple-600 h-2 rounded-full"
                      style={{ width: `${(scores.experience_match || 0) * 100}%` }}
                    />
                  </div>
                </div>
                <div className="pt-4 border-t border-gray-200">
                  <div className="flex justify-between items-center">
                    <span className="text-gray-900 font-semibold">Final Score</span>
                    <span className="text-2xl font-bold text-teal-600">
                      {((scores.final_score || 0) * 100).toFixed(1)}%
                    </span>
                  </div>
                </div>
              </div>
            </div>

            {/* Career Insights */}
            <div className="bg-white rounded-lg border border-gray-200 p-6">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">Career Insights</h2>
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <TrendingUp size={20} className="text-teal-600" />
                    <span className="text-sm text-gray-600">Learning Velocity</span>
                  </div>
                  <span className="font-semibold">{insights.learning_velocity || 0}</span>
                </div>
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <Zap size={20} className="text-yellow-600" />
                    <span className="text-sm text-gray-600">Skill Evolution</span>
                  </div>
                  <span className="font-semibold capitalize">{insights.skill_evolution_rate || 'N/A'}</span>
                </div>
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <Target size={20} className="text-purple-600" />
                    <span className="text-sm text-gray-600">Adaptability</span>
                  </div>
                  <span className="font-semibold">{insights.adaptability_score || 0}</span>
                </div>
              </div>
            </div>
          </div>

          {/* Right Column - Details */}
          <div className="col-span-2 space-y-6">
            {/* Explanation */}
            {candidate.explanation && (
              <div className="bg-white rounded-lg border border-gray-200 p-6">
                <h2 className="text-lg font-semibold text-gray-900 mb-4">Explanation</h2>
                <p className="text-gray-700 whitespace-pre-wrap">{candidate.explanation}</p>
              </div>
            )}

            {/* Skills */}
            <div className="bg-white rounded-lg border border-gray-200 p-6">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">Skills</h2>
              <div className="flex flex-wrap gap-2">
                {(resume.skills || []).map((skill, index) => (
                  <span
                    key={index}
                    className="px-3 py-1 bg-teal-50 text-teal-700 rounded-full text-sm font-medium"
                  >
                    {skill}
                  </span>
                ))}
              </div>
            </div>

            {/* Skill Gaps */}
            {candidate.skill_gaps && candidate.skill_gaps.length > 0 && (
              <div className="bg-white rounded-lg border border-gray-200 p-6">
                <h2 className="text-lg font-semibold text-gray-900 mb-4">Skill Gaps</h2>
                <ul className="space-y-2">
                  {candidate.skill_gaps.map((gap, index) => (
                    <li key={index} className="flex items-start gap-2">
                      <span className="text-red-500 mt-1">•</span>
                      <span className="text-gray-700">{gap}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Experience */}
            {resume.experience && resume.experience.length > 0 && (
              <div className="bg-white rounded-lg border border-gray-200 p-6">
                <h2 className="text-lg font-semibold text-gray-900 mb-4">Experience</h2>
                <div className="space-y-4">
                  {resume.experience.map((exp, index) => (
                    <div key={index} className="border-l-2 border-teal-600 pl-4">
                      <h3 className="font-semibold text-gray-900">{exp.role}</h3>
                      <p className="text-sm text-gray-600">{exp.company} • {exp.duration}</p>
                      <p className="text-sm text-gray-700 mt-2">{exp.description}</p>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Projects */}
            {resume.projects && resume.projects.length > 0 && (
              <div className="bg-white rounded-lg border border-gray-200 p-6">
                <h2 className="text-lg font-semibold text-gray-900 mb-4">Projects</h2>
                <div className="space-y-4">
                  {resume.projects.map((project, index) => (
                    <div key={index}>
                      <h3 className="font-semibold text-gray-900">{project.title}</h3>
                      <p className="text-sm text-gray-700 mt-1">{project.description}</p>
                      {project.technologies && project.technologies.length > 0 && (
                        <div className="flex flex-wrap gap-2 mt-2">
                          {project.technologies.map((tech, techIndex) => (
                            <span
                              key={techIndex}
                              className="px-2 py-0.5 bg-gray-100 text-gray-700 rounded text-xs"
                            >
                              {tech}
                            </span>
                          ))}
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Interview Questions */}
            {candidate.interview_questions && candidate.interview_questions.length > 0 && (
              <div className="bg-white rounded-lg border border-gray-200 p-6">
                <h2 className="text-lg font-semibold text-gray-900 mb-4">Interview Questions</h2>
                <ol className="space-y-3">
                  {candidate.interview_questions.map((question, index) => (
                    <li key={index} className="flex gap-3">
                      <span className="font-semibold text-teal-600 flex-shrink-0">{index + 1}.</span>
                      <span className="text-gray-700">{question}</span>
                    </li>
                  ))}
                </ol>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Resume Viewer Modal */}
      {showResumeViewer && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg shadow-xl max-w-4xl w-full max-h-[90vh] flex flex-col">
            {/* Modal Header */}
            <div className="flex items-center justify-between p-6 border-b border-gray-200">
              <div className="flex items-center gap-3">
                <FileText size={24} className="text-teal-600" />
                <div>
                  <h2 className="text-xl font-bold text-gray-900">Resume</h2>
                  <p className="text-sm text-gray-500">{candidate.name}</p>
                </div>
              </div>
              <button
                onClick={() => setShowResumeViewer(false)}
                className="text-gray-400 hover:text-gray-600 transition-colors"
              >
                <X size={24} />
              </button>
            </div>

            {/* Modal Content */}
            <div className="flex-1 overflow-y-auto p-6">
              {/* Summary */}
              {(resume as any).summary && (
                <div className="mb-6">
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">Summary</h3>
                  <p className="text-gray-700 whitespace-pre-wrap">{(resume as any).summary}</p>
                </div>
              )}

              {/* Skills */}
              {resume.skills && resume.skills.length > 0 && (
                <div className="mb-6">
                  <h3 className="text-lg font-semibold text-gray-900 mb-3">Skills</h3>
                  <div className="flex flex-wrap gap-2">
                    {resume.skills.map((skill: string, idx: number) => (
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

              {/* Experience */}
              {resume.experience && resume.experience.length > 0 && (
                <div className="mb-6">
                  <h3 className="text-lg font-semibold text-gray-900 mb-3">Experience</h3>
                  <div className="space-y-4">
                    {resume.experience.map((exp: any, idx: number) => (
                      <div key={idx} className="border-l-2 border-teal-600 pl-4">
                        <h4 className="font-semibold text-gray-900">{exp.title}</h4>
                        <p className="text-sm text-gray-600">{exp.company}</p>
                        <p className="text-xs text-gray-500 mb-2">{exp.duration}</p>
                        {exp.description && (
                          <p className="text-sm text-gray-700 whitespace-pre-wrap">{exp.description}</p>
                        )}
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Projects */}
              {resume.projects && resume.projects.length > 0 && (
                <div className="mb-6">
                  <h3 className="text-lg font-semibold text-gray-900 mb-3">Projects</h3>
                  <div className="space-y-4">
                    {resume.projects.map((proj: any, idx: number) => (
                      <div key={idx} className="border-l-2 border-blue-600 pl-4">
                        <h4 className="font-semibold text-gray-900">{proj.name}</h4>
                        {proj.description && (
                          <p className="text-sm text-gray-700 whitespace-pre-wrap mt-1">{proj.description}</p>
                        )}
                        {proj.technologies && proj.technologies.length > 0 && (
                          <div className="flex flex-wrap gap-1 mt-2">
                            {proj.technologies.map((tech: string, techIdx: number) => (
                              <span
                                key={techIdx}
                                className="px-2 py-0.5 bg-blue-100 text-blue-700 rounded text-xs"
                              >
                                {tech}
                              </span>
                            ))}
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Education */}
              {resume.education && resume.education.length > 0 && (
                <div className="mb-6">
                  <h3 className="text-lg font-semibold text-gray-900 mb-3">Education</h3>
                  <div className="space-y-3">
                    {resume.education.map((edu: any, idx: number) => (
                      <div key={idx}>
                        <h4 className="font-semibold text-gray-900">{edu.degree}</h4>
                        <p className="text-sm text-gray-600">{edu.institution}</p>
                        {edu.year && <p className="text-xs text-gray-500">{edu.year}</p>}
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Certifications */}
              {(resume as any).certifications && (resume as any).certifications.length > 0 && (
                <div className="mb-6">
                  <h3 className="text-lg font-semibold text-gray-900 mb-3">Certifications</h3>
                  <ul className="list-disc list-inside space-y-1">
                    {(resume as any).certifications.map((cert: string, idx: number) => (
                      <li key={idx} className="text-gray-700">{cert}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>

            {/* Modal Footer */}
            <div className="flex items-center justify-end gap-3 p-6 border-t border-gray-200">
              <button
                onClick={() => setShowResumeViewer(false)}
                className="px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-lg transition-colors"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
