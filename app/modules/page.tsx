'use client'

import { Header } from '@/components/Header'
import { Sidebar } from '@/components/Sidebar'
import { DataRibbon } from '@/components/DataRibbon'

export default function Modules() {
  const modules = [
    {
      name: 'Voice Synthesis',
      version: 'v4.2.1-stable',
      status: 'Active',
      uptime: '14 Tasks',
      color: 'text-primary',
      icon: 'mic',
    },
    {
      name: 'Automation Core',
      version: 'v3.8.0',
      status: 'Active',
      uptime: '12 Tasks',
      color: 'text-primary-dim',
      icon: 'smart_toy',
    },
    {
      name: 'Node Bridge',
      version: 'v2.1.0',
      status: 'Standby',
      uptime: 'Idle',
      color: 'text-slate-400',
      icon: 'sitemap',
    },
  ]

  return (
    <div className="min-h-screen bg-background text-on-background font-body">
      <Header />
      <Sidebar />
      <DataRibbon />

      <main className="md:ml-64 pt-32 pb-20 px-6 md:px-12 min-h-screen">
        <header className="mb-12">
          <h1 className="text-4xl font-headline font-bold tracking-tight text-on-surface mb-2">Active Modules</h1>
          <p className="text-secondary-dim font-body max-w-2xl opacity-80">
            Monitor and manage active neural processing modules and subsystems.
          </p>
        </header>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {modules.map((module) => (
            <div key={module.name} className="glass-panel p-6 border border-outline-variant/20">
              <div className="flex items-start justify-between mb-4">
                <div>
                  <h3 className={`text-lg font-headline font-bold ${module.color}`}>{module.name}</h3>
                  <p className="text-[10px] text-secondary-dim uppercase tracking-widest">{module.version}</p>
                </div>
                <span className={`material-symbols-outlined ${module.color}`}>{module.icon}</span>
              </div>

              <div className="space-y-3">
                <div className="flex justify-between items-center text-[10px]">
                  <span className="text-secondary-dim uppercase">Status</span>
                  <span className={`font-headline ${module.color}`}>{module.status}</span>
                </div>
                <div className="flex justify-between items-center text-[10px]">
                  <span className="text-secondary-dim uppercase">Runtime Tasks</span>
                  <span className={`font-headline ${module.color}`}>{module.uptime}</span>
                </div>
              </div>

              <div className="mt-4 pt-4 border-t border-outline-variant/10">
                <button className="w-full text-[10px] font-label text-primary/60 hover:text-primary uppercase tracking-widest transition-colors">
                  View Details
                </button>
              </div>
            </div>
          ))}
        </div>
      </main>
    </div>
  )
}
