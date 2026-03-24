'use client'

import { Header } from '@/components/Header'
import { Sidebar } from '@/components/Sidebar'
import { DataRibbon } from '@/components/DataRibbon'

export default function APIBridge() {
  return (
    <div className="min-h-screen bg-background text-on-background font-body">
      <Header />
      <Sidebar />
      <DataRibbon />

      <main className="md:ml-64 pt-32 pb-20 px-6 md:px-12 min-h-screen">
        <div className="glass-panel p-8 border border-primary/20">
          <h1 className="text-2xl font-headline font-bold text-primary mb-6">API Bridge Status</h1>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {[
              { name: 'Gemini API', status: 'Connected', latency: '42ms' },
              { name: 'Vertex AI', status: 'Connected', latency: '38ms' },
              { name: 'WolframAlpha', status: 'Connected', latency: '156ms' },
            ].map((api) => (
              <div key={api.name} className="border border-outline-variant/20 p-4 rounded-sm">
                <div className="flex items-center justify-between mb-2">
                  <h3 className="font-headline text-on-surface">{api.name}</h3>
                  <div className="w-2 h-2 rounded-full bg-primary animate-pulse"></div>
                </div>
                <p className="text-[10px] text-secondary-dim mb-1">{api.status}</p>
                <p className="text-[10px] font-mono text-primary">{api.latency}</p>
              </div>
            ))}
          </div>
        </div>
      </main>
    </div>
  )
}
