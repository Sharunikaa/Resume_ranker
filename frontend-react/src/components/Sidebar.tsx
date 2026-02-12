import { Briefcase, Users, BarChart3, Settings } from 'lucide-react';

interface SidebarProps {
  currentView: 'jobs' | 'candidates' | 'analytics' | 'settings';
  onViewChange: (view: 'jobs' | 'candidates' | 'analytics' | 'settings') => void;
}

export default function Sidebar({ currentView, onViewChange }: SidebarProps) {
  return (
    <div className="w-16 bg-white border-r border-gray-200 flex flex-col items-center py-4">
      {/* Logo */}
      <div className="mb-8">
        <div className="w-10 h-10 bg-teal-600 rounded-lg flex items-center justify-center">
          <Briefcase size={24} className="text-white" />
        </div>
      </div>

      {/* Navigation Icons */}
      <nav className="flex-1 flex flex-col gap-4">
        <div className="relative group">
          <button
            onClick={() => onViewChange('jobs')}
            className={`p-3 rounded-lg transition-colors ${
              currentView === 'jobs'
                ? 'bg-teal-100 text-teal-600'
                : 'text-gray-600 hover:bg-gray-100'
            }`}
          >
            <Briefcase size={20} />
          </button>
          <div className="absolute left-full ml-2 top-1/2 -translate-y-1/2 px-3 py-1.5 bg-gray-900 text-white text-xs rounded-lg opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap pointer-events-none z-50">
            Jobs
            <div className="absolute right-full top-1/2 -translate-y-1/2 mr-[-4px] border-4 border-transparent border-r-gray-900"></div>
          </div>
        </div>

        <div className="relative group">
          <button
            onClick={() => onViewChange('candidates')}
            className={`p-3 rounded-lg transition-colors ${
              currentView === 'candidates'
                ? 'bg-teal-100 text-teal-600'
                : 'text-gray-600 hover:bg-gray-100'
            }`}
          >
            <Users size={20} />
          </button>
          <div className="absolute left-full ml-2 top-1/2 -translate-y-1/2 px-3 py-1.5 bg-gray-900 text-white text-xs rounded-lg opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap pointer-events-none z-50">
            Candidates
            <div className="absolute right-full top-1/2 -translate-y-1/2 mr-[-4px] border-4 border-transparent border-r-gray-900"></div>
          </div>
        </div>

        <div className="relative group">
          <button
            onClick={() => onViewChange('analytics')}
            className={`p-3 rounded-lg transition-colors ${
              currentView === 'analytics'
                ? 'bg-teal-100 text-teal-600'
                : 'text-gray-600 hover:bg-gray-100'
            }`}
          >
            <BarChart3 size={20} />
          </button>
          <div className="absolute left-full ml-2 top-1/2 -translate-y-1/2 px-3 py-1.5 bg-gray-900 text-white text-xs rounded-lg opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap pointer-events-none z-50">
            Analytics
            <div className="absolute right-full top-1/2 -translate-y-1/2 mr-[-4px] border-4 border-transparent border-r-gray-900"></div>
          </div>
        </div>
      </nav>

      {/* Bottom Icons */}
      <div className="flex flex-col gap-4 mt-auto">
        <div className="relative group">
          <button
            onClick={() => onViewChange('settings')}
            className={`p-3 rounded-lg transition-colors ${
              currentView === 'settings'
                ? 'bg-teal-100 text-teal-600'
                : 'text-gray-600 hover:bg-gray-100'
            }`}
          >
            <Settings size={20} />
          </button>
          <div className="absolute left-full ml-2 top-1/2 -translate-y-1/2 px-3 py-1.5 bg-gray-900 text-white text-xs rounded-lg opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap pointer-events-none z-50">
            Settings
            <div className="absolute right-full top-1/2 -translate-y-1/2 mr-[-4px] border-4 border-transparent border-r-gray-900"></div>
          </div>
        </div>

        <div className="relative group">
          <button
            className="w-8 h-8 bg-orange-500 rounded-full flex items-center justify-center text-white font-bold text-sm"
          >
            S
          </button>
          <div className="absolute left-full ml-2 top-1/2 -translate-y-1/2 px-3 py-1.5 bg-gray-900 text-white text-xs rounded-lg opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap pointer-events-none z-50">
            Profile
            <div className="absolute right-full top-1/2 -translate-y-1/2 mr-[-4px] border-4 border-transparent border-r-gray-900"></div>
          </div>
        </div>
      </div>
    </div>
  );
}
