import { useState } from 'react'
import { motion } from 'framer-motion'
import { Trophy, Users, Clock, TrendingUp, Plus, Search } from 'lucide-react'
import { formatDate, cn } from '@/lib/utils'

const challenges = [
  { id: '1', title: '10K Steps Challenge', description: 'Walk 10,000 steps every day for 30 days.', type: 'steps', status: 'active', start_date: '2026-05-15', end_date: '2026-06-14', target_value: 300000, metric_unit: 'steps', reward_points: 500, participant_count: 24, is_team_challenge: false },
  { id: '2', title: 'Mindfulness Marathon', description: 'Practice meditation or mindfulness for 15 minutes daily.', type: 'mindfulness', status: 'active', start_date: '2026-05-20', end_date: '2026-06-10', target_value: 315, metric_unit: 'minutes', reward_points: 300, participant_count: 18, is_team_challenge: false },
  { id: '3', title: 'Nutrition Tracker', description: 'Log your meals and maintain a balanced diet for 14 days.', type: 'nutrition', status: 'active', start_date: '2026-05-25', end_date: '2026-06-08', target_value: 42, metric_unit: 'meals', reward_points: 200, participant_count: 31, is_team_challenge: false },
  { id: '4', title: 'Team Fitness Sprint', description: 'Team-based exercise challenge. 150 minutes per week.', type: 'exercise', status: 'draft', start_date: '2026-06-01', end_date: '2026-07-01', target_value: 600, metric_unit: 'minutes', reward_points: 400, participant_count: 0, is_team_challenge: true },
]

const statusColors: Record<string, string> = {
  active: 'bg-emerald-500/10 text-emerald-600 dark:text-emerald-400',
  draft: 'bg-amber-500/10 text-amber-600 dark:text-amber-400',
  completed: 'bg-blue-500/10 text-blue-600 dark:text-blue-400',
  cancelled: 'bg-red-500/10 text-red-600 dark:text-red-400',
}

const typeIcons: Record<string, string> = {
  steps: 'Footprints',
  exercise: 'Dumbbell',
  nutrition: 'Apple',
  mindfulness: 'Brain',
}

export default function ChallengesPage() {
  const [filter, setFilter] = useState<string>('all')
  const [search, setSearch] = useState('')

  const filtered = challenges.filter((c) => {
    const matchesFilter = filter === 'all' || c.status === filter
    const matchesSearch = c.title.toLowerCase().includes(search.toLowerCase())
    return matchesFilter && matchesSearch
  })

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="page-title">Challenges</h1>
          <p className="page-description">Join wellness challenges and compete with your team</p>
        </div>
        <button className="inline-flex items-center gap-2 px-4 py-2.5 rounded-lg bg-primary text-primary-foreground text-sm font-medium hover:bg-primary/90 transition-colors">
          <Plus className="w-4 h-4" /> Create Challenge
        </button>
      </div>

      {/* Filters */}
      <div className="flex flex-col sm:flex-row gap-4">
        <div className="relative flex-1 max-w-sm">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
          <input
            type="text" placeholder="Search challenges..."
            value={search} onChange={(e) => setSearch(e.target.value)}
            className="w-full pl-10 pr-4 py-2 rounded-lg bg-background border border-input text-sm focus:outline-none focus:ring-2 focus:ring-ring transition-colors"
          />
        </div>
        <div className="flex gap-2">
          {['all', 'active', 'draft', 'completed'].map((f) => (
            <button key={f} onClick={() => setFilter(f)}
              className={cn('px-3 py-1.5 rounded-lg text-xs font-medium transition-colors capitalize',
                filter === f ? 'bg-primary text-primary-foreground' : 'bg-accent text-muted-foreground hover:text-foreground'
              )}>
              {f}
            </button>
          ))}
        </div>
      </div>

      {/* Challenge Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {filtered.map((challenge, i) => (
          <motion.div
            key={challenge.id}
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.05 }}
            className="stat-card cursor-pointer group"
          >
            <div className="flex items-start justify-between mb-3">
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-1">
                  <h3 className="text-base font-semibold text-foreground group-hover:text-primary transition-colors">
                    {challenge.title}
                  </h3>
                  {challenge.is_team_challenge && (
                    <span className="px-1.5 py-0.5 rounded text-[10px] font-medium bg-purple-500/10 text-purple-500">
                      Team
                    </span>
                  )}
                </div>
                <p className="text-sm text-muted-foreground line-clamp-2">{challenge.description}</p>
              </div>
              <span className={cn('px-2 py-0.5 rounded-full text-xs font-medium capitalize', statusColors[challenge.status])}>
                {challenge.status}
              </span>
            </div>

            <div className="grid grid-cols-3 gap-4 mt-4 pt-4 border-t border-border/50">
              <div className="flex items-center gap-2">
                <Users className="w-3.5 h-3.5 text-muted-foreground" />
                <span className="text-xs text-muted-foreground">{challenge.participant_count} joined</span>
              </div>
              <div className="flex items-center gap-2">
                <Clock className="w-3.5 h-3.5 text-muted-foreground" />
                <span className="text-xs text-muted-foreground">{formatDate(challenge.end_date)}</span>
              </div>
              <div className="flex items-center gap-2">
                <Trophy className="w-3.5 h-3.5 text-amber-500" />
                <span className="text-xs font-medium text-amber-500">{challenge.reward_points} pts</span>
              </div>
            </div>
          </motion.div>
        ))}
      </div>
    </motion.div>
  )
}
