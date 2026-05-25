import { motion } from 'framer-motion'
import { Activity, Trophy, Calendar, Gift, TrendingUp, Users, Target, Flame } from 'lucide-react'
import { useAuthStore } from '@/stores/auth'
import { formatNumber } from '@/lib/utils'
import {
  AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
  BarChart, Bar,
} from 'recharts'

const activityData = [
  { day: 'Mon', steps: 8200, exercise: 35 },
  { day: 'Tue', steps: 11400, exercise: 45 },
  { day: 'Wed', steps: 9800, exercise: 30 },
  { day: 'Thu', steps: 12100, exercise: 60 },
  { day: 'Fri', steps: 7600, exercise: 20 },
  { day: 'Sat', steps: 14200, exercise: 50 },
  { day: 'Sun', steps: 6500, exercise: 40 },
]

const challengeProgress = [
  { name: '10K Steps', progress: 72, total: 300000, current: 216000 },
  { name: 'Mindfulness', progress: 45, total: 315, current: 142 },
  { name: 'Nutrition', progress: 28, total: 42, current: 12 },
]

const recentActivity = [
  { type: 'steps', value: '12,140 steps', time: '2 hours ago', points: 12 },
  { type: 'exercise', value: '45 min running', time: '5 hours ago', points: 7 },
  { type: 'nutrition', value: 'Logged lunch', time: '8 hours ago', points: 2 },
  { type: 'meditation', value: '15 min session', time: 'Yesterday', points: 3 },
]

const upcomingEvents = [
  { title: 'Yoga Workshop', date: 'May 28', time: '10:00 AM', location: 'Wellness Room' },
  { title: 'Nutrition Masterclass', date: 'Jun 1', time: '12:00 PM', location: 'Conf. Room A' },
  { title: 'Health Screening', date: 'Jun 8', time: '9:00 AM', location: 'Medical Suite' },
]

const teamRankings = [
  { name: 'Sophia Chen', department: 'Engineering', score: 95, points: 1100 },
  { name: 'Sarah Chen', department: 'HR', score: 92, points: 1250 },
  { name: 'Emma Davis', department: 'Sales', score: 91, points: 890 },
  { name: 'Olivia Martin', department: 'Product', score: 87, points: 710 },
  { name: 'Jessica Park', department: 'Engineering', score: 85, points: 750 },
]

const container = {
  hidden: { opacity: 0 },
  show: { opacity: 1, transition: { staggerChildren: 0.06 } },
}

const item = {
  hidden: { opacity: 0, y: 12 },
  show: { opacity: 1, y: 0, transition: { duration: 0.3 } },
}

export default function DashboardPage() {
  const user = useAuthStore((s) => s.user)

  const stats = [
    { label: 'Wellness Score', value: user?.wellness_score || 78, icon: Activity, color: 'text-blue-500', bg: 'bg-blue-500/10' },
    { label: 'Reward Points', value: formatNumber(user?.reward_points || 620), icon: Gift, color: 'text-amber-500', bg: 'bg-amber-500/10' },
    { label: 'Active Challenges', value: 3, icon: Trophy, color: 'text-emerald-500', bg: 'bg-emerald-500/10' },
    { label: 'Events Attended', value: 7, icon: Calendar, color: 'text-purple-500', bg: 'bg-purple-500/10' },
  ]

  return (
    <motion.div variants={container} initial="hidden" animate="show" className="space-y-8">
      {/* Header */}
      <motion.div variants={item}>
        <h1 className="page-title">
          Welcome back, {user?.first_name || 'User'}
        </h1>
        <p className="page-description">Here's your wellness overview for this week</p>
      </motion.div>

      {/* Stats Grid */}
      <motion.div variants={item} className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {stats.map((stat) => (
          <div key={stat.label} className="stat-card">
            <div className="flex items-center justify-between mb-3">
              <span className="text-sm text-muted-foreground">{stat.label}</span>
              <div className={`w-9 h-9 rounded-lg ${stat.bg} flex items-center justify-center`}>
                <stat.icon className={`w-4 h-4 ${stat.color}`} />
              </div>
            </div>
            <p className="text-2xl font-bold text-foreground">{stat.value}</p>
          </div>
        ))}
      </motion.div>

      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Activity Chart */}
        <motion.div variants={item} className="stat-card">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h3 className="text-base font-semibold text-foreground">Activity Overview</h3>
              <p className="text-xs text-muted-foreground mt-0.5">Steps and exercise this week</p>
            </div>
            <div className="flex items-center gap-1 text-xs text-emerald-500 bg-emerald-500/10 px-2 py-1 rounded-full">
              <TrendingUp className="w-3 h-3" />
              <span>+12%</span>
            </div>
          </div>
          <div className="h-[220px]">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={activityData} margin={{ top: 0, right: 0, left: -20, bottom: 0 }}>
                <defs>
                  <linearGradient id="stepsGrad" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="hsl(220, 91%, 54%)" stopOpacity={0.2} />
                    <stop offset="95%" stopColor="hsl(220, 91%, 54%)" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
                <XAxis dataKey="day" tick={{ fontSize: 12 }} stroke="hsl(var(--muted-foreground))" />
                <YAxis tick={{ fontSize: 12 }} stroke="hsl(var(--muted-foreground))" />
                <Tooltip
                  contentStyle={{
                    backgroundColor: 'hsl(var(--card))',
                    border: '1px solid hsl(var(--border))',
                    borderRadius: '8px',
                    fontSize: '12px',
                  }}
                />
                <Area type="monotone" dataKey="steps" stroke="hsl(220, 91%, 54%)" fill="url(#stepsGrad)" strokeWidth={2} />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </motion.div>

        {/* Challenge Progress */}
        <motion.div variants={item} className="stat-card">
          <div className="mb-6">
            <h3 className="text-base font-semibold text-foreground">Challenge Progress</h3>
            <p className="text-xs text-muted-foreground mt-0.5">Your active challenges</p>
          </div>
          <div className="space-y-5">
            {challengeProgress.map((challenge) => (
              <div key={challenge.name}>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm font-medium text-foreground">{challenge.name}</span>
                  <span className="text-xs text-muted-foreground">{challenge.progress}%</span>
                </div>
                <div className="w-full h-2 rounded-full bg-muted">
                  <motion.div
                    initial={{ width: 0 }}
                    animate={{ width: `${challenge.progress}%` }}
                    transition={{ duration: 0.8, delay: 0.2 }}
                    className="h-full rounded-full bg-primary"
                  />
                </div>
                <p className="text-xs text-muted-foreground mt-1">
                  {formatNumber(challenge.current)} / {formatNumber(challenge.total)}
                </p>
              </div>
            ))}
          </div>
        </motion.div>
      </div>

      {/* Bottom Row */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Recent Activity */}
        <motion.div variants={item} className="stat-card">
          <h3 className="text-base font-semibold text-foreground mb-4">Recent Activity</h3>
          <div className="space-y-4">
            {recentActivity.map((activity, i) => (
              <div key={i} className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className="w-8 h-8 rounded-lg bg-primary/10 flex items-center justify-center">
                    <Flame className="w-4 h-4 text-primary" />
                  </div>
                  <div>
                    <p className="text-sm font-medium text-foreground">{activity.value}</p>
                    <p className="text-xs text-muted-foreground">{activity.time}</p>
                  </div>
                </div>
                <span className="text-xs font-medium text-emerald-500">+{activity.points} pts</span>
              </div>
            ))}
          </div>
        </motion.div>

        {/* Upcoming Events */}
        <motion.div variants={item} className="stat-card">
          <h3 className="text-base font-semibold text-foreground mb-4">Upcoming Events</h3>
          <div className="space-y-4">
            {upcomingEvents.map((event, i) => (
              <div key={i} className="flex items-start gap-3">
                <div className="w-12 h-12 rounded-lg bg-accent flex flex-col items-center justify-center shrink-0">
                  <span className="text-xs font-semibold text-foreground">{event.date.split(' ')[0]}</span>
                  <span className="text-sm font-bold text-primary">{event.date.split(' ')[1]}</span>
                </div>
                <div>
                  <p className="text-sm font-medium text-foreground">{event.title}</p>
                  <p className="text-xs text-muted-foreground">{event.time} - {event.location}</p>
                </div>
              </div>
            ))}
          </div>
        </motion.div>

        {/* Team Rankings */}
        <motion.div variants={item} className="stat-card">
          <h3 className="text-base font-semibold text-foreground mb-4">Team Rankings</h3>
          <div className="space-y-3">
            {teamRankings.map((person, i) => (
              <div key={i} className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <span className="w-6 h-6 rounded-full bg-accent flex items-center justify-center text-xs font-bold text-foreground">
                    {i + 1}
                  </span>
                  <div>
                    <p className="text-sm font-medium text-foreground">{person.name}</p>
                    <p className="text-xs text-muted-foreground">{person.department}</p>
                  </div>
                </div>
                <div className="text-right">
                  <p className="text-sm font-semibold text-foreground">{person.score}</p>
                  <p className="text-xs text-muted-foreground">{person.points} pts</p>
                </div>
              </div>
            ))}
          </div>
        </motion.div>
      </div>
    </motion.div>
  )
}
