'use client'

import { Header } from '@/components/Header'
import { Sidebar } from '@/components/Sidebar'

export default function Configs() {
  return (
    <div className="min-h-screen bg-background text-on-background font-body">
      <Header />
      <Sidebar />

      <main className="md:ml-64 pt-24 pb-20 px-6 md:px-12 min-h-screen">
        <header className="mb-12">
          <div className="inline-flex items-center gap-2 px-3 py-1 bg-primary/10 border border-primary/20 text-primary text-[10px] font-headline tracking-widest uppercase mb-4">
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-primary opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2 w-2 bg-primary"></span>
            </span>
            Configuration Terminal_v4.2
          </div>
          <h1 className="text-4xl md:text-5xl font-headline font-bold tracking-tight text-on-surface mb-2">System Config</h1>
          <p className="text-secondary-dim font-body max-w-2xl opacity-80">
            Adjust neural processing parameters, interface responsiveness, and secure API bridges for the Kinetic Intelligence layer.
          </p>
        </header>

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
          <section className="lg:col-span-8 space-y-8">
            {/* API Secure Bridge */}
            <div className="glass-panel p-8 border-l-2 border-primary/40">
              <div className="flex justify-between items-center mb-8">
                <div>
                  <h3 className="text-xl font-headline font-bold text-primary tracking-tight">API Secure Bridge</h3>
                  <p className="text-xs text-secondary-dim/60 font-label uppercase tracking-widest">Access Tokens & Neural Pathways</p>
                </div>
                <span className="material-symbols-outlined text-primary/40">api</span>
              </div>
              <div className="space-y-6">
                <div className="space-y-2">
                  <label className="block text-[10px] font-label text-secondary-dim uppercase tracking-wider">
                    Gemini Enterprise API
                  </label>
                  <div className="relative">
                    <input
                      className="w-full bg-surface-container-highest border-b border-outline-variant/30 py-3 px-4 text-primary font-mono text-sm focus:outline-none focus:border-primary transition-all pr-12"
                      type="password"
                      defaultValue="sk-ai-gemini-77x-alpha-omega-9921"
                    />
                    <span className="material-symbols-outlined absolute right-4 top-1/2 -translate-y-1/2 text-outline-variant cursor-pointer hover:text-primary transition-colors">
                      visibility_off
                    </span>
                  </div>
                  <p className="text-[10px] text-outline-variant">
                    Connected to: <span className="text-secondary-dim">vertex-ai-us-east1</span>
                  </p>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="space-y-2">
                    <label className="block text-[10px] font-label text-secondary-dim uppercase tracking-wider">WolframAlpha ID</label>
                    <div className="relative">
                      <input
                        className="w-full bg-surface-container-highest border-b border-outline-variant/30 py-3 px-4 text-primary font-mono text-sm focus:outline-none focus:border-primary transition-all pr-12"
                        type="password"
                        defaultValue="WA-XXXX-YYYY"
                      />
                      <span className="material-symbols-outlined absolute right-4 top-1/2 -translate-y-1/2 text-outline-variant">lock</span>
                    </div>
                  </div>
                  <div className="space-y-2">
                    <label className="block text-[10px] font-label text-secondary-dim uppercase tracking-wider">Stable Diffusion Hub</label>
                    <div className="relative">
                      <input
                        className="w-full bg-surface-container-highest border-b border-outline-variant/30 py-3 px-4 text-primary font-mono text-sm focus:outline-none focus:border-primary transition-all pr-12"
                        type="password"
                        defaultValue="sd-local-host-7812"
                      />
                      <span className="material-symbols-outlined absolute right-4 top-1/2 -translate-y-1/2 text-outline-variant">lock</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Voice Output and Automation */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              {/* Voice Output */}
              <div className="glass-panel p-6 border-l-2 border-tertiary/40">
                <div className="flex items-center gap-3 mb-6">
                  <span className="material-symbols-outlined text-tertiary">record_voice_over</span>
                  <h3 className="text-lg font-headline font-bold text-on-surface">Voice Output</h3>
                </div>
                <div className="space-y-8">
                  <div className="space-y-3">
                    <div className="flex justify-between text-[10px] font-label uppercase tracking-wider">
                      <span className="text-secondary-dim">Master Volume</span>
                      <span className="text-tertiary">85%</span>
                    </div>
                    <input className="w-full accent-tertiary" type="range" defaultValue="85" />
                  </div>
                  <div className="space-y-3">
                    <div className="flex justify-between text-[10px] font-label uppercase tracking-wider">
                      <span className="text-secondary-dim">Speech Velocity</span>
                      <span className="text-tertiary">1.2x</span>
                    </div>
                    <input className="w-full accent-tertiary" type="range" defaultValue="60" />
                  </div>
                  <div className="pt-2 flex items-center justify-between">
                    <span className="text-xs font-label uppercase tracking-widest text-secondary-dim">Wake Word: &quot;JARVIS&quot;</span>
                    <div className="w-10 h-5 bg-tertiary/20 rounded-full relative cursor-pointer">
                      <div className="absolute right-1 top-1 w-3 h-3 bg-tertiary rounded-full shadow-[0_0_8px_rgba(172,137,255,0.6)]"></div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Automation */}
              <div className="glass-panel p-6 border-l-2 border-primary-dim/40">
                <div className="flex items-center gap-3 mb-6">
                  <span className="material-symbols-outlined text-primary-dim">smart_toy</span>
                  <h3 className="text-lg font-headline font-bold text-on-surface">Automation</h3>
                </div>
                <div className="space-y-8">
                  <div className="space-y-3">
                    <div className="flex justify-between text-[10px] font-label uppercase tracking-wider">
                      <span className="text-secondary-dim">PyAutoGUI Interval</span>
                      <span className="text-primary-dim">0.05s</span>
                    </div>
                    <input className="w-full accent-primary-dim" type="range" defaultValue="20" />
                  </div>
                  <div className="space-y-3">
                    <div className="flex justify-between text-[10px] font-label uppercase tracking-wider">
                      <span className="text-secondary-dim">Mouse Glide Smoothing</span>
                      <span className="text-primary-dim">High</span>
                    </div>
                    <input className="w-full accent-primary-dim" type="range" defaultValue="90" />
                  </div>
                  <div className="pt-2 flex items-center justify-between">
                    <span className="text-xs font-label uppercase tracking-widest text-secondary-dim">Safe-Fail Shutdown</span>
                    <div className="w-10 h-5 bg-surface-container-highest rounded-full relative cursor-pointer border border-outline-variant/30">
                      <div className="absolute left-1 top-1 w-3 h-3 bg-outline-variant rounded-full"></div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </section>

          {/* System Diagnostics Sidebar */}
          <aside className="lg:col-span-4 space-y-8">
            <div className="bg-surface-container p-6 rounded-sm border border-outline-variant/10 shadow-xl">
              <h3 className="text-sm font-headline font-bold text-primary mb-6 flex items-center gap-2 uppercase tracking-tighter">
                <span className="material-symbols-outlined text-sm">health_metrics</span>
                System Diagnostics
              </h3>
              <div className="space-y-5">
                {[
                  { label: 'Neural Core', status: 'STABLE', color: 'bg-primary' },
                  { label: 'API Gateway', status: 'CONNECTED', color: 'bg-primary', badge: '42ms' },
                  { label: 'Memory Buffer', status: '94% LOAD', color: 'bg-error', statusColor: 'text-error' },
                  { label: 'I/O Bridge', status: 'OPTIMAL', color: 'bg-primary' },
                ].map((item, i) => (
                  <div key={i} className="flex items-center justify-between p-3 bg-surface-container-low rounded-sm">
                    <div className="flex items-center gap-3">
                      <div className={`w-2 h-2 rounded-full ${item.color} shadow-[0_0_8px_${item.color === 'bg-error' ? 'rgba(255,113,108,0.6)' : 'rgba(143,245,255,0.6)'}]`}></div>
                      <span className="text-xs font-label uppercase text-on-surface/80">{item.label}</span>
                      {item.badge && (
                        <span className="text-[8px] bg-primary/10 text-primary px-1 border border-primary/20">
                          {item.badge}
                        </span>
                      )}
                    </div>
                    <span className={`text-[10px] font-mono ${item.statusColor || (item.color === 'bg-error' ? 'text-error' : 'text-primary')}`}>
                      {item.status}
                    </span>
                  </div>
                ))}
              </div>

              <div className="mt-8 pt-6 border-t border-outline-variant/10">
                <div className="bg-black/40 p-4 font-mono text-[10px] text-primary/60 rounded-sm">
                  <p className="mb-1">&gt; SCANNING_NETWORKS...</p>
                  <p className="mb-1">&gt; AUTH_TOKEN_VALIDATED</p>
                  <p className="mb-1 text-primary">&gt; CORE_READY_FOR_UPGRADE</p>
                  <p className="animate-pulse">_</p>
                </div>
              </div>
            </div>

            {/* Privacy Protocol */}
            <div className="bg-primary/5 p-6 border border-primary/20 relative overflow-hidden group">
              <div className="absolute top-0 right-0 p-2 opacity-10 group-hover:opacity-20 transition-opacity">
                <span className="material-symbols-outlined text-6xl">verified_user</span>
              </div>
              <h4 className="text-xs font-headline font-bold text-primary mb-2 uppercase tracking-widest">Privacy Protocol</h4>
              <p className="text-[11px] text-secondary-dim font-body leading-relaxed mb-4">
                All API keys and biometric data are encrypted locally using AES-256 before transmission. No data is stored on cloud nodes without neural sharding.
              </p>
              <button className="text-[10px] font-headline text-primary border-b border-primary/40 pb-0.5 hover:text-white hover:border-white transition-all uppercase tracking-widest">
                Learn More
              </button>
            </div>
          </aside>
        </div>
      </main>
    </div>
  )
}
