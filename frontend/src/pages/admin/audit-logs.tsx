import { motion } from 'framer-motion'
import { Search, Filter } from 'lucide-react'
import { cn } from '@/lib/utils'

const logs = [
  { id: '1', action: 'user.login', resource_type: 'user', description: 'User login successful', ip: '192.168.1.45', user: 'Sarah Chen', time: '2 min ago' },
  { id: '2', action: 'challenge.created', resource_type: 'challenge', description: 'Created "10K Steps Challenge"', ip: '192.168.1.48', user: 'Michael Thompson', time: '15 min ago' },
  { id: '3', action: 'user.updated', resource_type: 'user', description: 'Updated profile settings', ip: '192.168.1.52', user: 'Jessica Park', time: '1 hour ago' },
  { id: '4', action: 'event.created', resource_type: 'event', description: 'Created "Yoga Workshop"', ip: '192.168.1.48', user: 'Michael Thompson', time: '2 hours ago' },
  { id: '5', action: 'reward.redeemed', resource_type: 'reward', description: 'Redeemed "Wellness Gift Box"', ip: '192.168.1.61', user: 'Emma Davis', time: '3 hours ago' },
  { id: '6', action: 'user.login', resource_type: 'user', description: 'User login successful', ip: '192.168.1.55', user: 'David Rodriguez', time: '4 hours ago' },
  { id: '7', action: 'challenge.joined', resource_type: 'challenge', description: 'Joined "Mindfulness Marathon"', ip: '192.168.1.62', user: 'Alex Wright', time: '5 hours ago' },
  { id: '8', action: 'department.updated', resource_type: 'department', description: 'Updated Engineering department', ip: '192.168.1.45', user: 'Sarah Chen', time: '6 hours ago' },
]

const actionColors: Record<string, string> = {
  'user': 'bg-blue-500/10 text-blue-500',
  'challenge': 'bg-emerald-500/10 text-emerald-500',
  'event': 'bg-purple-500/10 text-purple-500',
  'reward': 'bg-amber-500/10 text-amber-500',
  'department': 'bg-rose-500/10 text-rose-500',
}

export default function AdminAuditLogsPage() {
  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-6">
      <div>
        <h1 className="page-title">Audit Logs</h1>
        <p className="page-description">Track all system activities and changes</p>
      </div>

      <div className="flex gap-4">
        <div className="relative flex-1 max-w-md">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
          <input type="text" placeholder="Search audit logs..."
            className="w-full pl-10 pr-4 py-2 rounded-lg bg-background border border-input text-sm focus:outline-none focus:ring-2 focus:ring-ring" />
        </div>
      </div>

      <div className="rounded-xl border border-border overflow-hidden">
        <table className="w-full">
          <thead>
            <tr className="bg-muted/50">
              <th className="text-left text-xs font-semibold text-muted-foreground px-4 py-3">Action</th>
              <th className="text-left text-xs font-semibold text-muted-foreground px-4 py-3">Description</th>
              <th className="text-left text-xs font-semibold text-muted-foreground px-4 py-3">User</th>
              <th className="text-left text-xs font-semibold text-muted-foreground px-4 py-3">IP Address</th>
              <th className="text-left text-xs font-semibold text-muted-foreground px-4 py-3">Time</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-border">
            {logs.map((log) => (
              <tr key={log.id} className="hover:bg-muted/30 transition-colors">
                <td className="px-4 py-3">
                  <span className={cn('px-2 py-0.5 rounded-full text-[10px] font-medium', actionColors[log.resource_type])}>
                    {log.action}
                  </span>
                </td>
                <td className="px-4 py-3 text-sm text-foreground">{log.description}</td>
                <td className="px-4 py-3 text-sm text-muted-foreground">{log.user}</td>
                <td className="px-4 py-3 text-xs font-mono text-muted-foreground">{log.ip}</td>
                <td className="px-4 py-3 text-xs text-muted-foreground">{log.time}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </motion.div>
  )
}
