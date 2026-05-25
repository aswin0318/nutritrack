import { useState } from 'react'
import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Activity, ArrowLeft } from 'lucide-react'

export default function ForgotPasswordPage() {
  const [email, setEmail] = useState('')
  const [submitted, setSubmitted] = useState(false)

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    setSubmitted(true)
  }

  return (
    <div className="min-h-screen flex items-center justify-center px-6 py-12 bg-background">
      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="w-full max-w-md">
        <div className="flex items-center gap-3 mb-8">
          <div className="w-10 h-10 rounded-xl bg-primary flex items-center justify-center">
            <Activity className="w-5 h-5 text-primary-foreground" />
          </div>
          <span className="text-xl font-bold text-foreground">NutriTrack360</span>
        </div>

        {submitted ? (
          <div>
            <h2 className="text-2xl font-bold text-foreground mb-2">Check your email</h2>
            <p className="text-sm text-muted-foreground mb-8">
              If an account exists with <strong>{email}</strong>, we've sent password reset instructions.
            </p>
            <Link to="/login" className="inline-flex items-center gap-2 text-sm text-primary hover:text-primary/80 font-medium">
              <ArrowLeft className="w-4 h-4" /> Back to sign in
            </Link>
          </div>
        ) : (
          <div>
            <h2 className="text-2xl font-bold text-foreground mb-2">Reset your password</h2>
            <p className="text-sm text-muted-foreground mb-8">Enter your email and we'll send you reset instructions.</p>

            <form onSubmit={handleSubmit} className="space-y-5">
              <div>
                <label htmlFor="email" className="block text-sm font-medium text-foreground mb-1.5">Email address</label>
                <input id="email" type="email" required value={email} onChange={(e) => setEmail(e.target.value)}
                  placeholder="you@company.com"
                  className="w-full px-4 py-2.5 rounded-lg bg-background border border-input text-foreground text-sm focus:outline-none focus:ring-2 focus:ring-ring transition-colors" />
              </div>
              <button type="submit"
                className="w-full py-2.5 px-4 rounded-lg bg-primary text-primary-foreground font-medium text-sm hover:bg-primary/90 transition-colors">
                Send reset instructions
              </button>
            </form>

            <p className="mt-6 text-center text-sm text-muted-foreground">
              <Link to="/login" className="text-primary hover:text-primary/80 font-medium inline-flex items-center gap-1">
                <ArrowLeft className="w-3 h-3" /> Back to sign in
              </Link>
            </p>
          </div>
        )}
      </motion.div>
    </div>
  )
}
