import { Outlet } from 'react-router-dom'
import Sidebar from './sidebar'
import Topbar from './topbar'
import { useUIStore } from '@/stores/ui'
import { cn } from '@/lib/utils'

export default function AppLayout() {
  const { sidebarCollapsed } = useUIStore()

  return (
    <div className="flex h-screen overflow-hidden bg-background">
      <Sidebar />
      <div className={cn(
        'flex-1 flex flex-col overflow-hidden transition-all duration-300',
        sidebarCollapsed ? 'lg:ml-[72px]' : 'lg:ml-[260px]'
      )}>
        <Topbar />
        <main className="flex-1 overflow-y-auto">
          <div className="container mx-auto px-6 py-8 max-w-7xl">
            <Outlet />
          </div>
        </main>
      </div>
    </div>
  )
}
