import { motion } from 'framer-motion'
import { Users, Trophy, Calendar, TrendingUp, Activity, Target } from 'lucide-react'
import { formatNumber } from '@/lib/utils'
import {
  AreaChart, Area, BarChart, Bar, PieChart, Pie, Cell,
  XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend,
} from 'recharts'

const stats = [
  { label: 'Total Employees', value: '248', change: '+12', icon: Users, color: 'text-blue-500', bg: 'bg-blue-500/10' },
  { label: 'Active Participants', value: '186', change: '+8', icon: Activity, color: 'text-emerald-500', bg: 'bg-emerald-500/10' },
  { label: 'Avg Wellness Score', value: '82.4', change: '+3.2', icon: Target, color: 'text-purple-500', bg: 'bg-purple-500/10' },
  { label: 'Participation Rate', value: '75%', change: '+5%', icon: TrendingUp, color: 'text-amber-500', bg: 'bg-amber-500/10' },
]

const monthlyData = [
  { month: 'Oct', activeUsers: 120, activities: 1240, challenges: 45 },
  { month: 'Nov', activeUsers: 145, activities: 1560, challenges: 52 },
  { month: 'Dec', activeUsers: 132, activities: 1380, challenges: 48 },
  { month: 'Jan', activeUsers: 158, activities: 1720, challenges: 61 },
  { month: 'Feb', activeUsers: 170, activities: 1890, challenges: 67 },
  { month: 'Mar', activeUsers: 165, activities: 1810, challenges: 64 },
  { month: 'Apr', activeUsers: 178, activities: 2050, challenges: 72 },
  { month: 'May', activeUsers: 186, activities: 2200, challenges: 78 },
]

const departmentData = [
  { department: 'Engineering', employees: 68, avgScore: 84, participations: 156 },
  { department: 'Sales', employees: 45, avgScore: 79, participations: 98 },
  { department: 'Marketing', employees: 32, avgScore: 86, participations: 87 },
  { department: 'HR', employees: 18, avgScore: 90, participations: 52 },
  { department: 'Finance', employees: 24, avgScore: 77, participations: 45 },
  { department: 'Product', employees: 38, avgScore: 83, participations: 112 },
]

const challengeCompletion = [
  { name: 'Completed', value: 234, color: 'hsl(142, 71%, 45%)' },
  { name: 'In Progress', value: 156, color: 'hsl(220, 91%, 54%)' },
  { name: 'Withdrawn', value: 42, color: 'hsl(0, 84%, 60%)' },
]

const eventAttendance = [
  { month: 'Jan', registered: 120, attended: 98 },
  { month: 'Feb', registered: 145, attended: 112 },
  { month: 'Mar', registered: 132, attended: 105 },
  { month: 'Apr', registered: 168, attended: 142 },
  { month: 'May', registered: 185, attended: 156 },
]

const container = {
  hidden: { opacity: 0 },
  show: { opacity: 1, transition: { staggerChildren: 0.06 } },
}
const item = {
  hidden: { opacity: 0, y: 12 },
  show: { opacity: 1, y: 0 },
}

export default function AnalyticsPage() {
  return (
    <motion.div variants={container} initial="hidden" animate="show" className="space-y-8">
      <motion.div variants={item}>
        <h1 className="page-title">HR Analytics</h1>
        <p className="page-description">Comprehensive wellness engagement insights</p>
      </motion.div>

      {/* Stats */}
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
            <span className="text-xs text-emerald-500 font-medium">{stat.change} vs last month</span>
          </div>
        ))}
      </motion.div>

      {/* Charts Row 1 */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Participation Trends */}
        <motion.div variants={item} className="stat-card">
          <h3 className="text-base font-semibold text-foreground mb-1">Participation Trends</h3>
          <p className="text-xs text-muted-foreground mb-6">Active users over the past 8 months</p>
          <div className="h-[280px]">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={monthlyData} margin={{ top: 0, right: 0, left: -20, bottom: 0 }}>
                <defs>
                  <linearGradient id="grad1" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="hsl(220, 91%, 54%)" stopOpacity={0.2} />
                    <stop offset="95%" stopColor="hsl(220, 91%, 54%)" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
                <XAxis dataKey="month" tick={{ fontSize: 12 }} stroke="hsl(var(--muted-foreground))" />
                <YAxis tick={{ fontSize: 12 }} stroke="hsl(var(--muted-foreground))" />
                <Tooltip contentStyle={{ backgroundColor: 'hsl(var(--card))', border: '1px solid hsl(var(--border))', borderRadius: '8px', fontSize: '12px' }} />
                <Area type="monotone" dataKey="activeUsers" stroke="hsl(220, 91%, 54%)" fill="url(#grad1)" strokeWidth={2} name="Active Users" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </motion.div>

        {/* Department Engagement */}
        <motion.div variants={item} className="stat-card">
          <h3 className="text-base font-semibold text-foreground mb-1">Department Engagement</h3>
          <p className="text-xs text-muted-foreground mb-6">Average wellness score by department</p>
          <div className="h-[280px]">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={departmentData} margin={{ top: 0, right: 0, left: -20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
                <XAxis dataKey="department" tick={{ fontSize: 11 }} stroke="hsl(var(--muted-foreground))" />
                <YAxis tick={{ fontSize: 12 }} stroke="hsl(var(--muted-foreground))" domain={[60, 100]} />
                <Tooltip contentStyle={{ backgroundColor: 'hsl(var(--card))', border: '1px solid hsl(var(--border))', borderRadius: '8px', fontSize: '12px' }} />
                <Bar dataKey="avgScore" fill="hsl(220, 91%, 54%)" radius={[4, 4, 0, 0]} name="Avg Score" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </motion.div>
      </div>

      {/* Charts Row 2 */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Challenge Completion */}
        <motion.div variants={item} className="stat-card">
          <h3 className="text-base font-semibold text-foreground mb-1">Challenge Completion</h3>
          <p className="text-xs text-muted-foreground mb-4">Overall challenge outcomes</p>
          <div className="h-[200px]">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie data={challengeCompletion} cx="50%" cy="50%" innerRadius={50} outerRadius={75} dataKey="value" stroke="none">
                  {challengeCompletion.map((entry, i) => (
                    <Cell key={i} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip contentStyle={{ backgroundColor: 'hsl(var(--card))', border: '1px solid hsl(var(--border))', borderRadius: '8px', fontSize: '12px' }} />
              </PieChart>
            </ResponsiveContainer>
          </div>
          <div className="flex justify-center gap-4 mt-2">
            {challengeCompletion.map((entry) => (
              <div key={entry.name} className="flex items-center gap-1.5">
                <div className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: entry.color }} />
                <span className="text-xs text-muted-foreground">{entry.name}</span>
              </div>
            ))}
          </div>
        </motion.div>

        {/* Event Attendance */}
        <motion.div variants={item} className="stat-card lg:col-span-2">
          <h3 className="text-base font-semibold text-foreground mb-1">Event Attendance</h3>
          <p className="text-xs text-muted-foreground mb-6">Registered vs actual attendance</p>
          <div className="h-[220px]">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={eventAttendance} margin={{ top: 0, right: 0, left: -20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
                <XAxis dataKey="month" tick={{ fontSize: 12 }} stroke="hsl(var(--muted-foreground))" />
                <YAxis tick={{ fontSize: 12 }} stroke="hsl(var(--muted-foreground))" />
                <Tooltip contentStyle={{ backgroundColor: 'hsl(var(--card))', border: '1px solid hsl(var(--border))', borderRadius: '8px', fontSize: '12px' }} />
                <Legend wrapperStyle={{ fontSize: '12px' }} />
                <Bar dataKey="registered" fill="hsl(220, 91%, 54%)" radius={[4, 4, 0, 0]} name="Registered" />
                <Bar dataKey="attended" fill="hsl(142, 71%, 45%)" radius={[4, 4, 0, 0]} name="Attended" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </motion.div>
      </div>
    </motion.div>
  )
}
