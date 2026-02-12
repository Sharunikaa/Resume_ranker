import { Mail } from 'lucide-react';
import type { Candidate } from '../types';

interface CandidateCardProps {
  candidate: Candidate;
  onClick: () => void;
}

export default function CandidateCard({ candidate, onClick }: CandidateCardProps) {
  const initials = candidate.name
    .split(' ')
    .map((n) => n[0])
    .join('')
    .toUpperCase()
    .slice(0, 2);

  return (
    <tr
      onClick={onClick}
      className="border-b border-gray-100 hover:bg-gray-50 cursor-pointer transition-colors"
    >
      {/* Avatar + Name */}
      <td className="py-4 px-4">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-gradient-to-br from-teal-400 to-teal-600 rounded-full flex items-center justify-center text-white font-bold text-sm flex-shrink-0">
            {initials}
          </div>
          <div className="min-w-0">
            <div className="font-medium text-gray-900 truncate">{candidate.name}</div>
            {candidate.rank && (
              <div className="text-xs text-gray-500">#{candidate.rank}</div>
            )}
          </div>
        </div>
      </td>

      {/* Email */}
      <td className="py-4 px-4">
        <div className="flex items-center gap-2 text-sm text-gray-600">
          <Mail size={14} />
          <span className="truncate">{candidate.email}</span>
        </div>
      </td>

      {/* Overall Score */}
      <td className="py-4 px-4">
        <div className="text-sm font-semibold text-gray-900">
          {((candidate.scores?.final_score || 0) * 100).toFixed(1)}%
        </div>
      </td>

      {/* Project Similarity */}
      <td className="py-4 px-4">
        <div className="text-sm font-semibold text-blue-600">
          {((candidate.scores?.project_similarity || 0) * 100).toFixed(1)}%
        </div>
      </td>

      {/* Skill Match */}
      <td className="py-4 px-4">
        <div className="text-sm font-semibold text-green-600">
          {((candidate.scores?.skill_match || 0) * 100).toFixed(1)}%
        </div>
      </td>

      {/* Experience Match */}
      <td className="py-4 px-4">
        <div className="text-sm font-semibold text-purple-600">
          {((candidate.scores?.experience_match || 0) * 100).toFixed(1)}%
        </div>
      </td>
    </tr>
  );
}
