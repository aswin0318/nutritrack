import { useEffect } from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import { useAuthStore } from '@/stores/auth'
import { ProtectedRoute } from '@/routes/protected-route'
import AppLayout from '@/components/layout/app-layout'
import LoginPage from '@/pages/auth/login'
import SignupPage from '@/pages/auth/signup'
import ForgotPasswordPage from '@/pages/auth/forgot-password'
import DashboardPage from '@/pages/dashboard'
import ChallengesPage from '@/pages/challenges'
import EventsPage from '@/pages/events'
import RewardsPage from '@/pages/rewards'
import AnalyticsPage from '@/pages/analytics'
import AdminUsersPage from '@/pages/admin/users'
import AdminDepartmentsPage from '@/pages/admin/departments'
import AdminSettingsPage from '@/pages/admin/settings'
import AdminAuditLogsPage from '@/pages/admin/audit-logs'
import ProfilePage from '@/pages/profile'
import NotFoundPage from '@/pages/not-found'

function App() {
  const { isAuthenticated, fetchUser } = useAuthStore()

  useEffect(() => {
    if (isAuthenticated) {
      fetchUser()
    }
  }, [isAuthenticated, fetchUser])

  return (
    <Routes>
      {/* Public routes */}
      <Route path="/login" element={isAuthenticated ? <Navigate to="/dashboard" /> : <LoginPage />} />
      <Route path="/signup" element={isAuthenticated ? <Navigate to="/dashboard" /> : <SignupPage />} />
      <Route path="/forgot-password" element={<ForgotPasswordPage />} />

      {/* Protected routes */}
      <Route element={<ProtectedRoute />}>
        <Route element={<AppLayout />}>
          <Route path="/dashboard" element={<DashboardPage />} />
          <Route path="/challenges" element={<ChallengesPage />} />
          <Route path="/events" element={<EventsPage />} />
          <Route path="/rewards" element={<RewardsPage />} />
          <Route path="/analytics" element={<AnalyticsPage />} />
          <Route path="/profile" element={<ProfilePage />} />
          <Route path="/admin/users" element={<AdminUsersPage />} />
          <Route path="/admin/departments" element={<AdminDepartmentsPage />} />
          <Route path="/admin/settings" element={<AdminSettingsPage />} />
          <Route path="/admin/audit-logs" element={<AdminAuditLogsPage />} />
        </Route>
      </Route>

      {/* Default & 404 */}
      <Route path="/" element={<Navigate to="/dashboard" replace />} />
      <Route path="*" element={<NotFoundPage />} />
    </Routes>
  )
}

export default App
