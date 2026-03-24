'use client'

import { Header } from '@/components/Header'
import { Sidebar } from '@/components/Sidebar'
import { DataRibbon } from '@/components/DataRibbon'

export default function System() {
  return (
    <div className="min-h-screen bg-background text-on-background font-body">
      <Header />
      <Sidebar />
      <DataRibbon />

      <main className="md:ml-64 pt-32 pb-20 px-6 md:px-12 min-h-screen">
        <h1 className="text-3xl font-headline font-bold text-on-surface mb-8">System Settings</h1>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {[
            { title: 'Neural Processing', items: ['Core Clock: 3.2 GHz', 'Memory: 64GB', 'Cache: 32MB'] },
            { title: 'Network Stack', items: ['Upload: 1000 Mbps', 'Download: 1000 Mbps', 'Ping: 4ms'] },
            { title: 'Security', items: ['Encryption: AES-256', 'Auth: MFA Enabled', 'Firewall: Active'] },
            { title: 'Maintenance', items: ['Last Backup: 2 hours ago', 'Defrag: Complete', 'Updates: Current'] },
          ].map((section) => (
            <div key={section.title} className="glass-panel p-6 border border-outline-variant/20">
              <h2 className="font-headline text-lg font-bold text-primary mb-4">{section.title}</h2>
              <ul className="space-y-2">
                {section.items.map((item) => (
                  <li key={item} className="text-[10px] text-secondary-dim border-b border-outline-variant/10 pb-2">
                    {item}
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      </main>
    </div>
  )
}
