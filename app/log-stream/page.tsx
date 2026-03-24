'use client'

import { Header } from '@/components/Header'
import { Sidebar } from '@/components/Sidebar'
import { DataRibbon } from '@/components/DataRibbon'

export default function LogStream() {
  return (
    <div className="min-h-screen bg-background text-on-background font-body">
      <Header />
      <Sidebar />
      <DataRibbon />

      <main className="md:ml-64 pt-32 pb-20 px-6 md:px-12 min-h-screen">
        <div className="glass-panel p-8 border border-primary/20 rounded-sm">
          <h1 className="text-2xl font-headline font-bold text-on-surface mb-4">System Log Stream</h1>
          <div className="space-y-2 font-mono text-sm max-h-96 overflow-y-auto">
            {Array.from({ length: 20 }).map((_, i) => (
              <p key={i} className="text-primary/60">
                <span className="text-primary-dim">[{String(9 + Math.floor(i / 5)).padStart(2, '0')}:{String(42 + i).padStart(2, '0')}:{String(i * 3).padStart(2, '0')}]</span> System
                process executed successfully
              </p>
            ))}
          </div>
        </div>
      </main>
    </div>
  )
}
