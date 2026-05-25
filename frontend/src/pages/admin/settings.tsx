import { motion } from 'framer-motion'
import { Save } from 'lucide-react'

export default function AdminSettingsPage() {
  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-6">
      <div>
        <h1 className="page-title">Platform Settings</h1>
        <p className="page-description">Configure organization-wide settings</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* General */}
        <div className="stat-card">
          <h3 className="text-base font-semibold text-foreground mb-4">General Settings</h3>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-foreground mb-1.5">Organization Name</label>
              <input type="text" defaultValue="Acme Corporation"
                className="w-full px-4 py-2.5 rounded-lg bg-background border border-input text-foreground text-sm focus:outline-none focus:ring-2 focus:ring-ring" />
            </div>
            <div>
              <label className="block text-sm font-medium text-foreground mb-1.5">Industry</label>
              <input type="text" defaultValue="Technology"
                className="w-full px-4 py-2.5 rounded-lg bg-background border border-input text-foreground text-sm focus:outline-none focus:ring-2 focus:ring-ring" />
            </div>
            <div>
              <label className="block text-sm font-medium text-foreground mb-1.5">Timezone</label>
              <select className="w-full px-4 py-2.5 rounded-lg bg-background border border-input text-foreground text-sm focus:outline-none focus:ring-2 focus:ring-ring">
                <option>US/Eastern</option>
                <option>US/Central</option>
                <option>US/Pacific</option>
                <option>UTC</option>
              </select>
            </div>
          </div>
        </div>

        {/* Wellness */}
        <div className="stat-card">
          <h3 className="text-base font-semibold text-foreground mb-4">Wellness Configuration</h3>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-foreground mb-1.5">Default Daily Step Goal</label>
              <input type="number" defaultValue={10000}
                className="w-full px-4 py-2.5 rounded-lg bg-background border border-input text-foreground text-sm focus:outline-none focus:ring-2 focus:ring-ring" />
            </div>
            <div>
              <label className="block text-sm font-medium text-foreground mb-1.5">Points per 1000 Steps</label>
              <input type="number" defaultValue={1}
                className="w-full px-4 py-2.5 rounded-lg bg-background border border-input text-foreground text-sm focus:outline-none focus:ring-2 focus:ring-ring" />
            </div>
            <div>
              <label className="block text-sm font-medium text-foreground mb-1.5">Points per 30 min Exercise</label>
              <input type="number" defaultValue={5}
                className="w-full px-4 py-2.5 rounded-lg bg-background border border-input text-foreground text-sm focus:outline-none focus:ring-2 focus:ring-ring" />
            </div>
          </div>
        </div>

        {/* Notifications */}
        <div className="stat-card">
          <h3 className="text-base font-semibold text-foreground mb-4">Notification Preferences</h3>
          <div className="space-y-4">
            {[
              { label: 'Challenge reminders', checked: true },
              { label: 'Event notifications', checked: true },
              { label: 'Weekly wellness reports', checked: true },
              { label: 'Achievement alerts', checked: false },
              { label: 'Leaderboard updates', checked: false },
            ].map((item) => (
              <label key={item.label} className="flex items-center justify-between cursor-pointer">
                <span className="text-sm text-foreground">{item.label}</span>
                <div className={`w-10 h-6 rounded-full transition-colors ${item.checked ? 'bg-primary' : 'bg-muted'} relative`}>
                  <div className={`w-4 h-4 rounded-full bg-white absolute top-1 transition-transform ${item.checked ? 'translate-x-5' : 'translate-x-1'}`} />
                </div>
              </label>
            ))}
          </div>
        </div>

        {/* Security */}
        <div className="stat-card">
          <h3 className="text-base font-semibold text-foreground mb-4">Security Settings</h3>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-foreground mb-1.5">Session Timeout (minutes)</label>
              <input type="number" defaultValue={30}
                className="w-full px-4 py-2.5 rounded-lg bg-background border border-input text-foreground text-sm focus:outline-none focus:ring-2 focus:ring-ring" />
            </div>
            <div>
              <label className="block text-sm font-medium text-foreground mb-1.5">Password Min Length</label>
              <input type="number" defaultValue={8}
                className="w-full px-4 py-2.5 rounded-lg bg-background border border-input text-foreground text-sm focus:outline-none focus:ring-2 focus:ring-ring" />
            </div>
            <label className="flex items-center justify-between cursor-pointer">
              <span className="text-sm text-foreground">Enforce MFA</span>
              <div className="w-10 h-6 rounded-full bg-muted relative">
                <div className="w-4 h-4 rounded-full bg-white absolute top-1 translate-x-1" />
              </div>
            </label>
          </div>
        </div>
      </div>

      <div className="flex justify-end">
        <button className="inline-flex items-center gap-2 px-6 py-2.5 rounded-lg bg-primary text-primary-foreground text-sm font-medium hover:bg-primary/90 transition-colors">
          <Save className="w-4 h-4" /> Save Changes
        </button>
      </div>
    </motion.div>
  )
}
