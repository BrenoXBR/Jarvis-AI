'use client'

import { Header } from '@/components/Header'
import { Sidebar } from '@/components/Sidebar'
import { DataRibbon } from '@/components/DataRibbon'

export default function NeuralLink() {
  return (
    <div className="min-h-screen bg-background text-on-background font-body">
      <Header />
      <Sidebar />
      <DataRibbon />

      <main className="md:ml-64 pt-32 pb-20 px-6 md:px-12 min-h-screen flex items-center justify-center">
        <div className="text-center">
          <span className="material-symbols-outlined text-6xl text-primary/20 block mb-4">neurology</span>
          <h1 className="text-3xl font-headline font-bold text-on-surface mb-2">Neural Link Interface</h1>
          <p className="text-secondary-dim max-w-md">Direct neural pathway connection to JARVIS core system. Status: OPTIMAL</p>
        </div>
      </main>
    </div>
  )
}
