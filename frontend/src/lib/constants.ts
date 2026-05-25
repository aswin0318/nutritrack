export const APP_NAME = 'NutriTrack360'

export const ROLES = {
  SUPER_ADMIN: 'super_admin',
  HR_ADMIN: 'hr_admin',
  DEPARTMENT_MANAGER: 'department_manager',
  EMPLOYEE: 'employee',
} as const

export const CHALLENGE_STATUS = {
  DRAFT: 'draft',
  ACTIVE: 'active',
  COMPLETED: 'completed',
  CANCELLED: 'cancelled',
} as const

export const EVENT_STATUS = {
  UPCOMING: 'upcoming',
  ONGOING: 'ongoing',
  COMPLETED: 'completed',
  CANCELLED: 'cancelled',
} as const

export const ACTIVITY_TYPES = [
  { value: 'steps', label: 'Steps', unit: 'steps' },
  { value: 'exercise', label: 'Exercise', unit: 'minutes' },
  { value: 'meditation', label: 'Meditation', unit: 'minutes' },
  { value: 'nutrition', label: 'Nutrition', unit: 'meals' },
  { value: 'sleep', label: 'Sleep', unit: 'hours' },
] as const

export const NAV_ITEMS = [
  { path: '/dashboard', label: 'Dashboard', icon: 'LayoutDashboard' },
  { path: '/challenges', label: 'Challenges', icon: 'Trophy' },
  { path: '/events', label: 'Events', icon: 'Calendar' },
  { path: '/rewards', label: 'Rewards', icon: 'Gift' },
  { path: '/analytics', label: 'Analytics', icon: 'BarChart3' },
] as const

export const ADMIN_NAV_ITEMS = [
  { path: '/admin/users', label: 'User Management', icon: 'Users' },
  { path: '/admin/departments', label: 'Departments', icon: 'Building2' },
  { path: '/admin/settings', label: 'Settings', icon: 'Settings' },
  { path: '/admin/audit-logs', label: 'Audit Logs', icon: 'FileText' },
] as const
