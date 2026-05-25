import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Activity } from 'lucide-react'
import { useAuthStore } from '@/stores/auth'

export default function SignupPage() {
  const navigate = useNavigate()
  const { register, isLoading } = useAuthStore()
  const [form, setForm] = useState({ email: '', password: '', first_name: '', last_name: '', organization_name: '' })
  const [error, setError] = useState('')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    try {
      await register(form)
      navigate('/dashboard')
    } catch (err: any) {
      setError(err.response?.data?.message || 'Registration failed')
    }
  }

  const update = (field: string, value: string) => setForm({ ...form, [field]: value })

  return (
    <div className="min-h-screen flex items-center justify-center px-6 py-12 bg-background">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="w-full max-w-md"
      >
        <div className="flex items-center gap-3 mb-8">
          <div className="w-10 h-10 rounded-xl bg-primary flex items-center justify-center">
            <Activity className="w-5 h-5 text-primary-foreground" />
          </div>
          <span className="text-xl font-bold text-foreground">NutriTrack360</span>
        </div>

        <h2 className="text-2xl font-bold text-foreground mb-2">Create your account</h2>
        <p className="text-sm text-muted-foreground mb-8">Get started with corporate wellness tracking</p>

        {error && (
          <div className="mb-6 p-3 rounded-lg bg-destructive/10 border border-destructive/20 text-sm text-destructive">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label htmlFor="first_name" className="block text-sm font-medium text-foreground mb-1.5">First name</label>
              <input id="first_name" type="text" required value={form.first_name} onChange={(e) => update('first_name', e.target.value)}
                className="w-full px-4 py-2.5 rounded-lg bg-background border border-input text-foreground text-sm focus:outline-none focus:ring-2 focus:ring-ring transition-colors" />
            </div>
            <div>
              <label htmlFor="last_name" className="block text-sm font-medium text-foreground mb-1.5">Last name</label>
              <input id="last_name" type="text" required value={form.last_name} onChange={(e) => update('last_name', e.target.value)}
                className="w-full px-4 py-2.5 rounded-lg bg-background border border-input text-foreground text-sm focus:outline-none focus:ring-2 focus:ring-ring transition-colors" />
            </div>
          </div>

          <div>
            <label htmlFor="email" className="block text-sm font-medium text-foreground mb-1.5">Email</label>
            <input id="email" type="email" required value={form.email} onChange={(e) => update('email', e.target.value)}
              placeholder="you@company.com"
              className="w-full px-4 py-2.5 rounded-lg bg-background border border-input text-foreground text-sm focus:outline-none focus:ring-2 focus:ring-ring transition-colors" />
          </div>

          <div>
            <label htmlFor="org" className="block text-sm font-medium text-foreground mb-1.5">Organization name</label>
            <input id="org" type="text" value={form.organization_name} onChange={(e) => update('organization_name', e.target.value)}
              placeholder="Your company name"
              className="w-full px-4 py-2.5 rounded-lg bg-background border border-input text-foreground text-sm focus:outline-none focus:ring-2 focus:ring-ring transition-colors" />
          </div>

          <div>
            <label htmlFor="password" className="block text-sm font-medium text-foreground mb-1.5">Password</label>
            <input id="password" type="password" required minLength={8} value={form.password} onChange={(e) => update('password', e.target.value)}
              placeholder="Min. 8 characters"
              className="w-full px-4 py-2.5 rounded-lg bg-background border border-input text-foreground text-sm focus:outline-none focus:ring-2 focus:ring-ring transition-colors" />
          </div>

          <button type="submit" disabled={isLoading}
            className="w-full py-2.5 px-4 rounded-lg bg-primary text-primary-foreground font-medium text-sm hover:bg-primary/90 focus:ring-2 focus:ring-ring transition-colors disabled:opacity-50">
            {isLoading ? 'Creating account...' : 'Create account'}
          </button>
        </form>

        <p className="mt-6 text-center text-sm text-muted-foreground">
          Already have an account?{' '}
          <Link to="/login" className="text-primary hover:text-primary/80 font-medium">Sign in</Link>
        </p>
      </motion.div>
    </div>
  )
}
