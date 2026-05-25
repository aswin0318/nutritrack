import { useNavigate } from 'react-router-dom'
import { Moon, Sun, Bell, LogOut, User, Menu } from 'lucide-react'
import { useAuthStore } from '@/stores/auth'
import { useThemeStore } from '@/stores/theme'
import { useUIStore } from '@/stores/ui'
import { getInitials } from '@/lib/utils'

export default function Topbar() {
  const navigate = useNavigate()
  const { user, logout } = useAuthStore()
  const { theme, toggleTheme } = useThemeStore()
  const { toggleSidebar } = useUIStore()

  return (
    <header className="h-16 border-b border-border bg-card/80 backdrop-blur-sm flex items-center justify-between px-6 sticky top-0 z-20">
      {/* Left: Mobile menu + breadcrumb */}
      <div className="flex items-center gap-4">
        <button
          onClick={toggleSidebar}
          className="lg:hidden p-2 rounded-lg hover:bg-accent transition-colors"
        >
          <Menu className="w-5 h-5" />
        </button>
      </div>

      {/* Right: Actions */}
      <div className="flex items-center gap-2">
        {/* Theme toggle */}
        <button
          onClick={toggleTheme}
          className="p-2 rounded-lg hover:bg-accent transition-colors text-muted-foreground hover:text-foreground"
          title={theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode'}
        >
          {theme === 'dark' ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />}
        </button>

        {/* Notifications */}
        <button className="p-2 rounded-lg hover:bg-accent transition-colors text-muted-foreground hover:text-foreground relative">
          <Bell className="w-5 h-5" />
          <span className="absolute top-1.5 right-1.5 w-2 h-2 bg-primary rounded-full" />
        </button>

        {/* Separator */}
        <div className="w-px h-8 bg-border mx-2" />

        {/* User menu */}
        <div className="flex items-center gap-3">
          <button
            onClick={() => navigate('/profile')}
            className="flex items-center gap-3 p-1.5 rounded-lg hover:bg-accent transition-colors"
          >
            <div className="w-8 h-8 rounded-full bg-primary/10 text-primary flex items-center justify-center text-sm font-semibold">
              {user ? getInitials(`${user.first_name} ${user.last_name}`) : 'U'}
            </div>
            <div className="hidden md:block text-left">
              <p className="text-sm font-medium text-foreground leading-tight">
                {user ? `${user.first_name} ${user.last_name}` : 'User'}
              </p>
              <p className="text-xs text-muted-foreground leading-tight">
                {user?.role_name?.replace('_', ' ') || 'Employee'}
              </p>
            </div>
          </button>

          <button
            onClick={logout}
            className="p-2 rounded-lg hover:bg-accent transition-colors text-muted-foreground hover:text-destructive"
            title="Sign out"
          >
            <LogOut className="w-4 h-4" />
          </button>
        </div>
      </div>
    </header>
  )
}
