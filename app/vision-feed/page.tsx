'use client'

import { Header } from '@/components/Header'
import { Sidebar } from '@/components/Sidebar'
import { DataRibbon } from '@/components/DataRibbon'

export default function VisionFeed() {
  return (
    <div className="min-h-screen bg-background text-on-background font-body">
      <Header />
      <Sidebar />
      <DataRibbon />

      <main className="md:ml-64 pt-32 pb-20 px-6 md:px-12 min-h-screen">
        <div className="aspect-video bg-surface-container-lowest border border-outline-variant/30 rounded-sm overflow-hidden flex items-center justify-center">
          <div className="text-center">
            <div className="w-16 h-16 rounded-full border-2 border-primary/20 mx-auto mb-4 flex items-center justify-center">
              <span className="material-symbols-outlined text-primary text-4xl">visibility</span>
            </div>
            <h2 className="text-xl font-headline text-on-surface mb-2">Vision Feed Offline</h2>
            <p className="text-secondary-dim text-sm">Camera connection not established</p>
          </div>
        </div>
      </main>
    </div>
  )
}
