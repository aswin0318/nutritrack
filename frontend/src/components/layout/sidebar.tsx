import { NavLink, useLocation } from 'react-router-dom'
import { motion } from 'framer-motion'
import {
  LayoutDashboard, Trophy, Calendar, Gift, BarChart3,
  Users, Building2, Settings, FileText, ChevronLeft, Activity,
} from 'lucide-react'
import { cn } from '@/lib/utils'
import { useUIStore } from '@/stores/ui'
import { useAuthStore } from '@/stores/auth'
import { ROLES } from '@/lib/constants'

const iconMap: Record<string, React.ElementType> = {
  LayoutDashboard, Trophy, Calendar, Gift, BarChart3,
  Users, Building2, Settings, FileText,
}

const mainNav = [
  { path: '/dashboard', label: 'Dashboard', icon: 'LayoutDashboard' },
  { path: '/challenges', label: 'Challenges', icon: 'Trophy' },
  { path: '/events', label: 'Events', icon: 'Calendar' },
  { path: '/rewards', label: 'Rewards', icon: 'Gift' },
  { path: '/analytics', label: 'Analytics', icon: 'BarChart3' },
]

const adminNav = [
  { path: '/admin/users', label: 'Users', icon: 'Users' },
  { path: '/admin/departments', label: 'Departments', icon: 'Building2' },
  { path: '/admin/settings', label: 'Settings', icon: 'Settings' },
  { path: '/admin/audit-logs', label: 'Audit Logs', icon: 'FileText' },
]

export default function Sidebar() {
  const location = useLocation()
  const { sidebarCollapsed, toggleSidebarCollapse } = useUIStore()
  const user = useAuthStore((s) => s.user)
  const isAdmin = user?.role_name === ROLES.SUPER_ADMIN || user?.role_name === ROLES.HR_ADMIN

  return (
    <aside className={cn(
      'hidden lg:flex flex-col fixed inset-y-0 left-0 z-30 bg-card border-r border-border transition-all duration-300',
      sidebarCollapsed ? 'w-[72px]' : 'w-[260px]'
    )}>
      {/* Logo */}
      <div className="flex items-center h-16 px-4 border-b border-border">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-lg bg-primary flex items-center justify-center">
            <Activity className="w-4 h-4 text-primary-foreground" />
          </div>
          {!sidebarCollapsed && (
            <motion.span
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="font-bold text-base text-foreground tracking-tight"
            >
              NutriTrack360
            </motion.span>
          )}
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 overflow-y-auto py-4 px-3 space-y-1">
        <div className="mb-2">
          {!sidebarCollapsed && (
            <span className="px-3 text-xs font-semibold text-muted-foreground uppercase tracking-wider">
              Main
            </span>
          )}
        </div>
        {mainNav.map((item) => {
          const Icon = iconMap[item.icon]
          const isActive = location.pathname === item.path

          return (
            <NavLink
              key={item.path}
              to={item.path}
              className={cn(
                'sidebar-link',
                isActive && 'sidebar-link-active'
              )}
              title={sidebarCollapsed ? item.label : undefined}
            >
              <Icon className="w-5 h-5 shrink-0" />
              {!sidebarCollapsed && <span>{item.label}</span>}
            </NavLink>
          )
        })}

        {isAdmin && (
          <>
            <div className="mt-6 mb-2">
              {!sidebarCollapsed && (
                <span className="px-3 text-xs font-semibold text-muted-foreground uppercase tracking-wider">
                  Administration
                </span>
              )}
            </div>
            {adminNav.map((item) => {
              const Icon = iconMap[item.icon]
              const isActive = location.pathname === item.path

              return (
                <NavLink
                  key={item.path}
                  to={item.path}
                  className={cn(
                    'sidebar-link',
                    isActive && 'sidebar-link-active'
                  )}
                  title={sidebarCollapsed ? item.label : undefined}
                >
                  <Icon className="w-5 h-5 shrink-0" />
                  {!sidebarCollapsed && <span>{item.label}</span>}
                </NavLink>
              )
            })}
          </>
        )}
      </nav>

      {/* Collapse toggle */}
      <div className="border-t border-border p-3">
        <button
          onClick={toggleSidebarCollapse}
          className="sidebar-link w-full justify-center"
        >
          <ChevronLeft className={cn(
            'w-5 h-5 transition-transform duration-200',
            sidebarCollapsed && 'rotate-180'
          )} />
          {!sidebarCollapsed && <span>Collapse</span>}
        </button>
      </div>
    </aside>
  )
}
