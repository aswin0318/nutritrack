import { useState } from 'react'
import { motion } from 'framer-motion'
import { Calendar, MapPin, Clock, Users, ExternalLink, Plus, Search } from 'lucide-react'
import { formatDateTime, cn } from '@/lib/utils'

const events = [
  { id: '1', title: 'Yoga and Stretching Workshop', description: 'Rejuvenating session focused on flexibility and stress relief.', type: 'fitness_class', status: 'upcoming', start_time: '2026-05-28T10:00:00Z', end_time: '2026-05-28T11:00:00Z', location: 'Wellness Room, Floor 2', capacity: 30, registered_count: 18, reward_points: 50 },
  { id: '2', title: 'Nutrition Masterclass: Meal Prep', description: 'Efficient meal prep techniques from our nutrition expert.', type: 'workshop', status: 'upcoming', start_time: '2026-06-01T12:00:00Z', end_time: '2026-06-01T13:30:00Z', location: 'Conference Room A', capacity: 25, registered_count: 12, reward_points: 40 },
  { id: '3', title: 'Annual Health Screening', description: 'Blood pressure, cholesterol, and BMI assessment.', type: 'health_screening', status: 'upcoming', start_time: '2026-06-08T09:00:00Z', end_time: '2026-06-08T17:00:00Z', location: 'Medical Suite, Floor 1', capacity: 100, registered_count: 45, reward_points: 100 },
  { id: '4', title: 'Stress Management Webinar', description: 'Managing workplace stress and maintaining work-life balance.', type: 'webinar', status: 'upcoming', start_time: '2026-05-30T14:00:00Z', end_time: '2026-05-30T15:00:00Z', virtual_link: 'https://meet.nutritrack360.in/stress-mgmt', capacity: 200, registered_count: 67, reward_points: 30 },
]

const typeLabels: Record<string, string> = {
  fitness_class: 'Fitness Class',
  workshop: 'Workshop',
  health_screening: 'Health Screening',
  webinar: 'Webinar',
  seminar: 'Seminar',
}

export default function EventsPage() {
  const [view, setView] = useState<'grid' | 'list'>('grid')

  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="page-title">Events</h1>
          <p className="page-description">Discover and register for corporate wellness events</p>
        </div>
        <button className="inline-flex items-center gap-2 px-4 py-2.5 rounded-lg bg-primary text-primary-foreground text-sm font-medium hover:bg-primary/90 transition-colors">
          <Plus className="w-4 h-4" /> Create Event
        </button>
      </div>

      {/* Event Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {events.map((event, i) => (
          <motion.div
            key={event.id}
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.05 }}
            className="stat-card group cursor-pointer"
          >
            <div className="flex items-start justify-between mb-2">
              <span className="px-2 py-0.5 rounded-full text-[10px] font-medium bg-blue-500/10 text-blue-500 capitalize">
                {typeLabels[event.type] || event.type}
              </span>
              <span className="text-xs font-medium text-emerald-500">+{event.reward_points} pts</span>
            </div>

            <h3 className="text-base font-semibold text-foreground mb-1 group-hover:text-primary transition-colors">
              {event.title}
            </h3>
            <p className="text-sm text-muted-foreground line-clamp-2 mb-4">{event.description}</p>

            <div className="space-y-2 text-xs text-muted-foreground">
              <div className="flex items-center gap-2">
                <Clock className="w-3.5 h-3.5" />
                <span>{formatDateTime(event.start_time)}</span>
              </div>
              <div className="flex items-center gap-2">
                {event.location ? (
                  <>
                    <MapPin className="w-3.5 h-3.5" />
                    <span>{event.location}</span>
                  </>
                ) : (
                  <>
                    <ExternalLink className="w-3.5 h-3.5" />
                    <span>Virtual Event</span>
                  </>
                )}
              </div>
              <div className="flex items-center gap-2">
                <Users className="w-3.5 h-3.5" />
                <span>{event.registered_count} / {event.capacity} registered</span>
              </div>
            </div>

            {/* Capacity bar */}
            <div className="mt-4">
              <div className="w-full h-1.5 rounded-full bg-muted">
                <div
                  className="h-full rounded-full bg-primary transition-all"
                  style={{ width: `${(event.registered_count / (event.capacity || 1)) * 100}%` }}
                />
              </div>
            </div>

            <button className="mt-4 w-full py-2 rounded-lg bg-primary/10 text-primary text-sm font-medium hover:bg-primary/20 transition-colors">
              Register
            </button>
          </motion.div>
        ))}
      </div>
    </motion.div>
  )
}
