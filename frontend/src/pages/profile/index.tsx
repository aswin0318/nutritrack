import { motion } from 'framer-motion'
import { useAuthStore } from '@/stores/auth'
import { User, Mail, Phone, Building2, Shield, Calendar } from 'lucide-react'
import { formatDate, getInitials } from '@/lib/utils'

export default function ProfilePage() {
  const user = useAuthStore((s) => s.user)

  if (!user) return null

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-6 max-w-3xl">
      <div>
        <h1 className="page-title">Profile</h1>
        <p className="page-description">Manage your personal information</p>
      </div>

      {/* Profile header */}
      <div className="stat-card">
        <div className="flex items-center gap-6">
          <div className="w-20 h-20 rounded-full bg-primary/10 text-primary flex items-center justify-center text-2xl font-bold">
            {getInitials(`${user.first_name} ${user.last_name}`)}
          </div>
          <div>
            <h2 className="text-xl font-bold text-foreground">{user.first_name} {user.last_name}</h2>
            <p className="text-sm text-muted-foreground">{user.title || 'Employee'}</p>
            <p className="text-xs text-muted-foreground mt-1">{user.role_name?.replace('_', ' ')}</p>
          </div>
        </div>
      </div>

      {/* Profile details */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="stat-card">
          <h3 className="text-base font-semibold text-foreground mb-4">Personal Information</h3>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-foreground mb-1.5">First Name</label>
              <input type="text" defaultValue={user.first_name}
                className="w-full px-4 py-2.5 rounded-lg bg-background border border-input text-foreground text-sm focus:outline-none focus:ring-2 focus:ring-ring" />
            </div>
            <div>
              <label className="block text-sm font-medium text-foreground mb-1.5">Last Name</label>
              <input type="text" defaultValue={user.last_name}
                className="w-full px-4 py-2.5 rounded-lg bg-background border border-input text-foreground text-sm focus:outline-none focus:ring-2 focus:ring-ring" />
            </div>
            <div>
              <label className="block text-sm font-medium text-foreground mb-1.5">Email</label>
              <input type="email" defaultValue={user.email} disabled
                className="w-full px-4 py-2.5 rounded-lg bg-muted border border-input text-muted-foreground text-sm cursor-not-allowed" />
            </div>
          </div>
        </div>

        <div className="stat-card">
          <h3 className="text-base font-semibold text-foreground mb-4">Work Information</h3>
          <div className="space-y-3">
            <div className="flex items-center gap-3 py-2">
              <Building2 className="w-4 h-4 text-muted-foreground" />
              <div>
                <p className="text-xs text-muted-foreground">Organization</p>
                <p className="text-sm font-medium text-foreground">{user.organization_name || 'Acme Corporation'}</p>
              </div>
            </div>
            <div className="flex items-center gap-3 py-2">
              <User className="w-4 h-4 text-muted-foreground" />
              <div>
                <p className="text-xs text-muted-foreground">Department</p>
                <p className="text-sm font-medium text-foreground">{user.department_name || 'Unassigned'}</p>
              </div>
            </div>
            <div className="flex items-center gap-3 py-2">
              <Shield className="w-4 h-4 text-muted-foreground" />
              <div>
                <p className="text-xs text-muted-foreground">Role</p>
                <p className="text-sm font-medium text-foreground capitalize">{user.role_name?.replace('_', ' ') || 'Employee'}</p>
              </div>
            </div>
            <div className="flex items-center gap-3 py-2">
              <Mail className="w-4 h-4 text-muted-foreground" />
              <div>
                <p className="text-xs text-muted-foreground">Employee ID</p>
                <p className="text-sm font-medium text-foreground">{user.employee_id || 'N/A'}</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="flex justify-end">
        <button className="px-6 py-2.5 rounded-lg bg-primary text-primary-foreground text-sm font-medium hover:bg-primary/90 transition-colors">
          Save Changes
        </button>
      </div>
    </motion.div>
  )
}
