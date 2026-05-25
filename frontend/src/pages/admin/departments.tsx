import { motion } from 'framer-motion'
import { Building2, Plus, Users, Edit2 } from 'lucide-react'

const departments = [
  { id: '1', name: 'Engineering', code: 'ENG', manager: 'Jessica Park', employees: 68, avgScore: 84 },
  { id: '2', name: 'Human Resources', code: 'HR', manager: 'Michael Thompson', employees: 18, avgScore: 90 },
  { id: '3', name: 'Marketing', code: 'MKT', manager: 'Ryan Lee', employees: 32, avgScore: 86 },
  { id: '4', name: 'Sales', code: 'SLS', manager: 'Unassigned', employees: 45, avgScore: 79 },
  { id: '5', name: 'Finance', code: 'FIN', manager: 'Unassigned', employees: 24, avgScore: 77 },
  { id: '6', name: 'Product', code: 'PRD', manager: 'Unassigned', employees: 38, avgScore: 83 },
]

export default function AdminDepartmentsPage() {
  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="page-title">Departments</h1>
          <p className="page-description">Manage organizational departments</p>
        </div>
        <button className="inline-flex items-center gap-2 px-4 py-2.5 rounded-lg bg-primary text-primary-foreground text-sm font-medium hover:bg-primary/90 transition-colors">
          <Plus className="w-4 h-4" /> Add Department
        </button>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {departments.map((dept, i) => (
          <motion.div
            key={dept.id}
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.05 }}
            className="stat-card"
          >
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-lg bg-primary/10 flex items-center justify-center">
                  <Building2 className="w-5 h-5 text-primary" />
                </div>
                <div>
                  <h3 className="text-sm font-semibold text-foreground">{dept.name}</h3>
                  <p className="text-xs text-muted-foreground">{dept.code}</p>
                </div>
              </div>
              <button className="p-1.5 rounded-lg hover:bg-accent transition-colors">
                <Edit2 className="w-3.5 h-3.5 text-muted-foreground" />
              </button>
            </div>

            <div className="space-y-2">
              <div className="flex items-center justify-between text-sm">
                <span className="text-muted-foreground">Manager</span>
                <span className="font-medium text-foreground">{dept.manager}</span>
              </div>
              <div className="flex items-center justify-between text-sm">
                <span className="text-muted-foreground">Employees</span>
                <span className="font-medium text-foreground">{dept.employees}</span>
              </div>
              <div className="flex items-center justify-between text-sm">
                <span className="text-muted-foreground">Avg. Score</span>
                <span className="font-medium text-foreground">{dept.avgScore}</span>
              </div>
            </div>
          </motion.div>
        ))}
      </div>
    </motion.div>
  )
}
