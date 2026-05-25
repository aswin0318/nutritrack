export interface User {
  id: string
  email: string
  first_name: string
  last_name: string
  employee_id?: string
  phone?: string
  title?: string
  avatar_url?: string
  wellness_score: number
  reward_points: number
  is_active: boolean
  organization_id: string
  department_id?: string
  role_id: string
  role_name?: string
  department_name?: string
  organization_name?: string
  created_at: string
  updated_at: string
}

export interface Challenge {
  id: string
  title: string
  description?: string
  type: string
  status: string
  start_date: string
  end_date: string
  target_value: number
  metric_unit: string
  reward_points: number
  max_participants?: number
  is_team_challenge: boolean
  image_url?: string
  organization_id: string
  created_by?: string
  creator_name?: string
  participant_count: number
  created_at: string
}

export interface Event {
  id: string
  title: string
  description?: string
  type: string
  status: string
  start_time: string
  end_time: string
  location?: string
  virtual_link?: string
  capacity?: number
  registered_count: number
  image_url?: string
  reward_points: number
  organization_id: string
  is_registered: boolean
  created_at: string
}

export interface Reward {
  id: string
  name: string
  description?: string
  category: string
  points_required: number
  quantity_available?: number
  image_url?: string
  is_active: boolean
  organization_id: string
  created_at: string
}

export interface Department {
  id: string
  name: string
  code: string
  description?: string
  is_active: boolean
  organization_id: string
  manager_id?: string
  manager_name?: string
  employee_count: number
  created_at: string
}

export interface ActivityLog {
  id: string
  activity_type: string
  activity_date: string
  value: number
  unit: string
  duration_minutes?: number
  calories_burned?: number
  notes?: string
  points_earned: number
  user_id: string
  created_at: string
}

export interface LeaderboardEntry {
  rank: number
  user_id: string
  user_name: string
  department_name?: string
  progress_value: number
  progress_percentage: number
  points_earned: number
}

export interface PaginatedResponse<T> {
  items: T[]
  total: number
  page: number
  page_size: number
  total_pages: number
  has_next: boolean
  has_previous: boolean
}

export interface DashboardStats {
  total_employees: number
  active_employees: number
  total_challenges: number
  active_challenges: number
  total_events: number
  total_departments: number
  avg_wellness_score: number
  participation_rate: number
}

export interface PointsSummary {
  total_earned: number
  total_redeemed: number
  current_balance: number
  this_month_earned: number
}

export interface TokenResponse {
  access_token: string
  refresh_token: string
  token_type: string
  expires_in: number
}
