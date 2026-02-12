import { useState, useEffect } from 'react';
import { Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer, Legend, Tooltip } from 'recharts';
import { TrendingUp, Users, Briefcase, Award } from 'lucide-react';
import type { Job, Candidate } from '../types';

interface AnalyticsViewProps {
  jobs: Job[];
  selectedJob: Job | null;
  candidates: Candidate[];
}

export default function AnalyticsView({ jobs, selectedJob, candidates }: AnalyticsViewProps) {
  const [radarData, setRadarData] = useState<any[]>([]);
  const [topCandidates, setTopCandidates] = useState<Candidate[]>([]);

  useEffect(() => {
    if (candidates.length > 0) {
      // Get top 5 candidates
      const sorted = [...candidates]
        .filter(c => c.scores)
        .sort((a, b) => (b.scores?.final_score || 0) - (a.scores?.final_score || 0))
        .slice(0, 5);
      
      setTopCandidates(sorted);

      // Prepare radar chart data - compare top candidates
      const data = [
        {
          metric: 'Overall Score',
          ...sorted.reduce((acc, c) => {
            acc[c.name] = ((c.scores?.final_score || 0) * 100).toFixed(1);
            return acc;
          }, {} as any)
        },
        {
          metric: 'Project Similarity',
          ...sorted.reduce((acc, c) => {
            acc[c.name] = ((c.scores?.project_similarity || 0) * 100).toFixed(1);
            return acc;
          }, {} as any)
        },
        {
          metric: 'Skill Match',
          ...sorted.reduce((acc, c) => {
            acc[c.name] = ((c.scores?.skill_match || 0) * 100).toFixed(1);
            return acc;
          }, {} as any)
        },
        {
          metric: 'Experience Match',
          ...sorted.reduce((acc, c) => {
            acc[c.name] = ((c.scores?.experience_match || 0) * 100).toFixed(1);
            return acc;
          }, {} as any)
        },
      ];

      setRadarData(data);
    }
  }, [candidates]);

  const colors = ['#0d9488', '#3b82f6', '#8b5cf6', '#f59e0b', '#ef4444'];

  const avgScore = candidates.length > 0
    ? (candidates.reduce((sum, c) => sum + (c.scores?.final_score || 0), 0) / candidates.length * 100).toFixed(1)
    : '0.0';

  const topScore = candidates.length > 0
    ? (Math.max(...candidates.map(c => c.scores?.final_score || 0)) * 100).toFixed(1)
    : '0.0';

  return (
    <div className="flex-1 flex flex-col overflow-hidden">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 px-6 py-4">
        <h1 className="text-xl font-bold text-gray-900">CandiSight</h1>
      </header>

      {/* Content */}
      <div className="flex-1 overflow-y-auto p-6 bg-gray-50">
        <div className="max-w-7xl mx-auto">
          {/* Page Header */}
          <div className="mb-6">
            <h2 className="text-2xl font-bold text-gray-900 mb-2">Analytics Dashboard</h2>
            <p className="text-gray-600">
              {selectedJob ? `Insights for ${selectedJob.title}` : 'Select a job to view analytics'}
            </p>
          </div>

        {!selectedJob || candidates.length === 0 ? (
          <div className="flex items-center justify-center h-96">
            <div className="text-center">
              <Briefcase size={48} className="mx-auto text-gray-400 mb-4" />
              <h3 className="text-lg font-semibold text-gray-700 mb-2">No Data Available</h3>
              <p className="text-gray-500">
                {!selectedJob 
                  ? 'Select a job to view analytics' 
                  : 'Upload and rank candidates to see insights'}
              </p>
            </div>
          </div>
        ) : (
          <>
            {/* Stats Cards */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
              <div className="bg-white rounded-lg p-5 border border-gray-200">
                <div className="flex items-center gap-3">
                  <div className="w-12 h-12 bg-teal-100 rounded-lg flex items-center justify-center">
                    <Users size={24} className="text-teal-600" />
                  </div>
                  <div>
                    <p className="text-sm text-gray-600">Total Candidates</p>
                    <p className="text-2xl font-bold text-gray-900">{candidates.length}</p>
                  </div>
                </div>
              </div>

              <div className="bg-white rounded-lg p-5 border border-gray-200">
                <div className="flex items-center gap-3">
                  <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
                    <TrendingUp size={24} className="text-blue-600" />
                  </div>
                  <div>
                    <p className="text-sm text-gray-600">Average Score</p>
                    <p className="text-2xl font-bold text-gray-900">{avgScore}%</p>
                  </div>
                </div>
              </div>

              <div className="bg-white rounded-lg p-5 border border-gray-200">
                <div className="flex items-center gap-3">
                  <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center">
                    <Award size={24} className="text-purple-600" />
                  </div>
                  <div>
                    <p className="text-sm text-gray-600">Top Score</p>
                    <p className="text-2xl font-bold text-gray-900">{topScore}%</p>
                  </div>
                </div>
              </div>

              <div className="bg-white rounded-lg p-5 border border-gray-200">
                <div className="flex items-center gap-3">
                  <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
                    <Briefcase size={24} className="text-green-600" />
                  </div>
                  <div>
                    <p className="text-sm text-gray-600">Total Jobs</p>
                    <p className="text-2xl font-bold text-gray-900">{jobs.length}</p>
                  </div>
                </div>
              </div>
            </div>

            {/* Radar Chart */}
            <div className="bg-white rounded-lg p-6 border border-gray-200 mb-6">
              <h2 className="text-lg font-bold text-gray-900 mb-4">
                Top 5 Candidates Comparison
              </h2>
              <ResponsiveContainer width="100%" height={500}>
                <RadarChart data={radarData}>
                  <PolarGrid stroke="#e5e7eb" />
                  <PolarAngleAxis 
                    dataKey="metric" 
                    tick={{ fill: '#6b7280', fontSize: 12 }}
                  />
                  <PolarRadiusAxis 
                    angle={90} 
                    domain={[0, 100]}
                    tick={{ fill: '#6b7280', fontSize: 10 }}
                  />
                  {topCandidates.map((candidate, idx) => (
                    <Radar
                      key={candidate.candidate_id}
                      name={candidate.name}
                      dataKey={candidate.name}
                      stroke={colors[idx]}
                      fill={colors[idx]}
                      fillOpacity={0.2}
                      strokeWidth={2}
                    />
                  ))}
                  <Legend 
                    wrapperStyle={{ paddingTop: '20px' }}
                    iconType="circle"
                  />
                  <Tooltip 
                    contentStyle={{ 
                      backgroundColor: '#fff', 
                      border: '1px solid #e5e7eb',
                      borderRadius: '8px',
                      padding: '8px 12px'
                    }}
                    formatter={(value: any) => `${value}%`}
                  />
                </RadarChart>
              </ResponsiveContainer>
            </div>

            {/* Top Candidates List */}
            <div className="bg-white rounded-lg p-6 border border-gray-200">
              <h2 className="text-lg font-bold text-gray-900 mb-4">Top Candidates</h2>
              <div className="space-y-3">
                {topCandidates.map((candidate, idx) => (
                  <div 
                    key={candidate.candidate_id}
                    className="flex items-center justify-between p-4 bg-gray-50 rounded-lg"
                  >
                    <div className="flex items-center gap-4">
                      <div 
                        className="w-10 h-10 rounded-full flex items-center justify-center text-white font-bold"
                        style={{ backgroundColor: colors[idx] }}
                      >
                        #{idx + 1}
                      </div>
                      <div>
                        <p className="font-semibold text-gray-900">{candidate.name}</p>
                        <p className="text-sm text-gray-600">{candidate.email}</p>
                      </div>
                    </div>
                    <div className="text-right">
                      <p className="text-lg font-bold text-gray-900">
                        {((candidate.scores?.final_score || 0) * 100).toFixed(1)}%
                      </p>
                      <p className="text-xs text-gray-500">Overall Score</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </>
        )}
        </div>
      </div>
    </div>
  );
}
