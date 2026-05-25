import { motion } from 'framer-motion'
import { Search, MoreVertical, Shield, UserCheck, UserX } from 'lucide-react'
import { cn } from '@/lib/utils'

const users = [
  { id: '1', name: 'Sarah Chen', email: 'admin@acme.com', role: 'super_admin', department: 'HR', status: 'active', wellness: 92, joined: 'Jan 15, 2025' },
  { id: '2', name: 'Michael Thompson', email: 'hr@acme.com', role: 'hr_admin', department: 'HR', status: 'active', wellness: 88, joined: 'Feb 3, 2025' },
  { id: '3', name: 'Jessica Park', email: 'manager@acme.com', role: 'department_manager', department: 'Engineering', status: 'active', wellness: 85, joined: 'Mar 12, 2025' },
  { id: '4', name: 'David Rodriguez', email: 'employee@acme.com', role: 'employee', department: 'Engineering', status: 'active', wellness: 78, joined: 'Mar 20, 2025' },
  { id: '5', name: 'Alex Wright', email: 'alex.wright@acme.com', role: 'employee', department: 'Marketing', status: 'active', wellness: 82, joined: 'Apr 5, 2025' },
  { id: '6', name: 'Emma Davis', email: 'emma.davis@acme.com', role: 'employee', department: 'Sales', status: 'active', wellness: 91, joined: 'Apr 18, 2025' },
  { id: '7', name: 'James Wilson', email: 'james.wilson@acme.com', role: 'employee', department: 'Finance', status: 'inactive', wellness: 73, joined: 'May 1, 2025' },
  { id: '8', name: 'Sophia Chen', email: 'sophia.chen@acme.com', role: 'employee', department: 'Engineering', status: 'active', wellness: 95, joined: 'May 8, 2025' },
]

const roleColors: Record<string, string> = {
  super_admin: 'bg-red-500/10 text-red-500',
  hr_admin: 'bg-purple-500/10 text-purple-500',
  department_manager: 'bg-blue-500/10 text-blue-500',
  employee: 'bg-emerald-500/10 text-emerald-500',
}

export default function AdminUsersPage() {
  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-6">
      <div>
        <h1 className="page-title">User Management</h1>
        <p className="page-description">Manage employee accounts, roles, and permissions</p>
      </div>

      {/* Search/Filter bar */}
      <div className="flex gap-4">
        <div className="relative flex-1 max-w-md">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
          <input type="text" placeholder="Search by name or email..."
            className="w-full pl-10 pr-4 py-2 rounded-lg bg-background border border-input text-sm focus:outline-none focus:ring-2 focus:ring-ring transition-colors" />
        </div>
      </div>

      {/* Table */}
      <div className="rounded-xl border border-border overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="bg-muted/50">
                <th className="text-left text-xs font-semibold text-muted-foreground px-4 py-3">User</th>
                <th className="text-left text-xs font-semibold text-muted-foreground px-4 py-3">Role</th>
                <th className="text-left text-xs font-semibold text-muted-foreground px-4 py-3">Department</th>
                <th className="text-left text-xs font-semibold text-muted-foreground px-4 py-3">Status</th>
                <th className="text-left text-xs font-semibold text-muted-foreground px-4 py-3">Wellness</th>
                <th className="text-left text-xs font-semibold text-muted-foreground px-4 py-3">Joined</th>
                <th className="text-left text-xs font-semibold text-muted-foreground px-4 py-3 w-10"></th>
              </tr>
            </thead>
            <tbody className="divide-y divide-border">
              {users.map((user) => (
                <tr key={user.id} className="hover:bg-muted/30 transition-colors">
                  <td className="px-4 py-3">
                    <div className="flex items-center gap-3">
                      <div className="w-8 h-8 rounded-full bg-primary/10 text-primary flex items-center justify-center text-xs font-semibold">
                        {user.name.split(' ').map(n => n[0]).join('')}
                      </div>
                      <div>
                        <p className="text-sm font-medium text-foreground">{user.name}</p>
                        <p className="text-xs text-muted-foreground">{user.email}</p>
                      </div>
                    </div>
                  </td>
                  <td className="px-4 py-3">
                    <span className={cn('px-2 py-0.5 rounded-full text-[10px] font-medium capitalize', roleColors[user.role])}>
                      {user.role.replace('_', ' ')}
                    </span>
                  </td>
                  <td className="px-4 py-3 text-sm text-muted-foreground">{user.department}</td>
                  <td className="px-4 py-3">
                    <span className={cn('flex items-center gap-1 text-xs font-medium',
                      user.status === 'active' ? 'text-emerald-500' : 'text-red-500'
                    )}>
                      <span className={cn('w-1.5 h-1.5 rounded-full', user.status === 'active' ? 'bg-emerald-500' : 'bg-red-500')} />
                      {user.status}
                    </span>
                  </td>
                  <td className="px-4 py-3">
                    <span className="text-sm font-medium text-foreground">{user.wellness}</span>
                  </td>
                  <td className="px-4 py-3 text-xs text-muted-foreground">{user.joined}</td>
                  <td className="px-4 py-3">
                    <button className="p-1 rounded hover:bg-accent transition-colors">
                      <MoreVertical className="w-4 h-4 text-muted-foreground" />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </motion.div>
  )
}
