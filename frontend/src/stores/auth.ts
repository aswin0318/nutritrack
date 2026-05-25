import { create } from 'zustand'
import api from '@/lib/api'
import type { User, TokenResponse } from '@/types'

interface AuthState {
  user: User | null
  isAuthenticated: boolean
  isLoading: boolean
  login: (email: string, password: string) => Promise<void>
  register: (data: { email: string; password: string; first_name: string; last_name: string; organization_name?: string }) => Promise<void>
  logout: () => void
  fetchUser: () => Promise<void>
  setUser: (user: User) => void
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  isAuthenticated: !!localStorage.getItem('access_token'),
  isLoading: false,

  login: async (email: string, password: string) => {
    set({ isLoading: true })
    try {
      const { data } = await api.post<TokenResponse>('/auth/login', { email, password })
      localStorage.setItem('access_token', data.access_token)
      localStorage.setItem('refresh_token', data.refresh_token)
      set({ isAuthenticated: true })

      // Fetch user profile
      const { data: user } = await api.get<User>('/users/me')
      set({ user, isLoading: false })
    } catch (error) {
      set({ isLoading: false })
      throw error
    }
  },

  register: async (data) => {
    set({ isLoading: true })
    try {
      const { data: tokens } = await api.post<TokenResponse>('/auth/register', data)
      localStorage.setItem('access_token', tokens.access_token)
      localStorage.setItem('refresh_token', tokens.refresh_token)
      set({ isAuthenticated: true })

      const { data: user } = await api.get<User>('/users/me')
      set({ user, isLoading: false })
    } catch (error) {
      set({ isLoading: false })
      throw error
    }
  },

  logout: () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    set({ user: null, isAuthenticated: false })
    window.location.href = '/login'
  },

  fetchUser: async () => {
    try {
      set({ isLoading: true })
      const { data: user } = await api.get<User>('/users/me')
      set({ user, isAuthenticated: true, isLoading: false })
    } catch {
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      set({ user: null, isAuthenticated: false, isLoading: false })
    }
  },

  setUser: (user: User) => set({ user }),
}))
