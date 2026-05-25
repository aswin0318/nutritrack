import { motion } from 'framer-motion'
import { Gift, Star, ShoppingBag, Heart, CreditCard } from 'lucide-react'
import { useAuthStore } from '@/stores/auth'
import { formatNumber, cn } from '@/lib/utils'

const rewards = [
  { id: '1', name: 'Premium Gym Membership (1 Month)', description: 'One month pass to any partner gym facility.', category: 'experience', points_required: 500, quantity_available: 20 },
  { id: '2', name: 'Wellness Gift Box', description: 'Curated box with aromatherapy, snacks, and fitness accessories.', category: 'merchandise', points_required: 300, quantity_available: 50 },
  { id: '3', name: 'Charity Donation', description: 'Donate your points to a health-related charity.', category: 'donation', points_required: 100, quantity_available: null },
  { id: '4', name: 'Extra PTO Day', description: 'Earn an additional paid time off day.', category: 'experience', points_required: 1000, quantity_available: 10 },
  { id: '5', name: 'Healthy Meal Delivery (1 Week)', description: 'One week of healthy meal deliveries.', category: 'gift_card', points_required: 400, quantity_available: 30 },
  { id: '6', name: 'Fitness Tracker Device', description: 'Premium fitness tracking wristband.', category: 'merchandise', points_required: 800, quantity_available: 15 },
]

const categoryIcons: Record<string, React.ElementType> = {
  experience: Star,
  merchandise: ShoppingBag,
  donation: Heart,
  gift_card: CreditCard,
}

const categoryColors: Record<string, string> = {
  experience: 'text-purple-500 bg-purple-500/10',
  merchandise: 'text-blue-500 bg-blue-500/10',
  donation: 'text-rose-500 bg-rose-500/10',
  gift_card: 'text-amber-500 bg-amber-500/10',
}

const achievements = [
  { name: 'First Steps', description: 'Complete your first activity', icon: '🏃', unlocked: true },
  { name: 'Week Warrior', description: '7-day activity streak', icon: '🔥', unlocked: true },
  { name: 'Challenge Champion', description: 'Complete 5 challenges', icon: '🏆', unlocked: false },
  { name: 'Social Butterfly', description: 'Attend 3 events', icon: '👥', unlocked: true },
  { name: 'Point Master', description: 'Earn 1000 points', icon: '⭐', unlocked: false },
]

export default function RewardsPage() {
  const user = useAuthStore((s) => s.user)
  const userPoints = user?.reward_points || 620

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-8">
      <div>
        <h1 className="page-title">Rewards</h1>
        <p className="page-description">Redeem your wellness points for exciting rewards</p>
      </div>

      {/* Points summary */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div className="stat-card">
          <p className="text-sm text-muted-foreground mb-1">Available Points</p>
          <p className="text-3xl font-bold text-foreground">{formatNumber(userPoints)}</p>
        </div>
        <div className="stat-card">
          <p className="text-sm text-muted-foreground mb-1">Total Earned</p>
          <p className="text-3xl font-bold text-emerald-500">{formatNumber(1840)}</p>
        </div>
        <div className="stat-card">
          <p className="text-sm text-muted-foreground mb-1">Redeemed</p>
          <p className="text-3xl font-bold text-foreground">{formatNumber(1220)}</p>
        </div>
      </div>

      {/* Achievements */}
      <div>
        <h2 className="text-lg font-semibold text-foreground mb-4">Achievements</h2>
        <div className="flex gap-3 overflow-x-auto pb-2">
          {achievements.map((a) => (
            <div
              key={a.name}
              className={cn(
                'flex flex-col items-center gap-2 p-4 rounded-xl border min-w-[120px] transition-all',
                a.unlocked
                  ? 'border-primary/30 bg-primary/5'
                  : 'border-border bg-card opacity-50 grayscale'
              )}
            >
              <span className="text-2xl">{a.icon}</span>
              <span className="text-xs font-semibold text-foreground text-center">{a.name}</span>
              <span className="text-[10px] text-muted-foreground text-center">{a.description}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Reward catalog */}
      <div>
        <h2 className="text-lg font-semibold text-foreground mb-4">Reward Catalog</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {rewards.map((reward, i) => {
            const Icon = categoryIcons[reward.category] || Gift
            const colorClass = categoryColors[reward.category] || 'text-gray-500 bg-gray-500/10'
            const canRedeem = userPoints >= reward.points_required

            return (
              <motion.div
                key={reward.id}
                initial={{ opacity: 0, y: 12 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.05 }}
                className="stat-card flex flex-col"
              >
                <div className="flex items-center justify-between mb-3">
                  <div className={cn('w-9 h-9 rounded-lg flex items-center justify-center', colorClass)}>
                    <Icon className="w-4 h-4" />
                  </div>
                  <span className="text-xs font-medium capitalize text-muted-foreground">{reward.category.replace('_', ' ')}</span>
                </div>
                <h3 className="text-sm font-semibold text-foreground mb-1">{reward.name}</h3>
                <p className="text-xs text-muted-foreground mb-4 flex-1">{reward.description}</p>
                <div className="flex items-center justify-between mt-auto pt-3 border-t border-border/50">
                  <div>
                    <span className="text-lg font-bold text-foreground">{formatNumber(reward.points_required)}</span>
                    <span className="text-xs text-muted-foreground ml-1">pts</span>
                  </div>
                  <button
                    disabled={!canRedeem}
                    className={cn(
                      'px-4 py-1.5 rounded-lg text-xs font-medium transition-colors',
                      canRedeem
                        ? 'bg-primary text-primary-foreground hover:bg-primary/90'
                        : 'bg-muted text-muted-foreground cursor-not-allowed'
                    )}
                  >
                    {canRedeem ? 'Redeem' : 'Insufficient'}
                  </button>
                </div>
              </motion.div>
            )
          })}
        </div>
      </div>
    </motion.div>
  )
}
