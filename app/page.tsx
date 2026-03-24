'use client'

import { Header } from '@/components/Header'
import { Sidebar } from '@/components/Sidebar'
import { DataRibbon } from '@/components/DataRibbon'

export default function Dashboard() {
  return (
    <div className="min-h-screen bg-background text-on-background font-body overflow-hidden">
      <Header />
      <Sidebar />
      <DataRibbon />

      <main className="md:ml-64 pt-32 pb-20 md:pb-0 h-full relative overflow-hidden px-8">
        <div className="absolute inset-0 pointer-events-none">
          <div className="scan-line w-full h-1/2 absolute"></div>
        </div>

        {/* Central Core Pulse */}
        <div className="flex flex-col items-center justify-center h-full max-w-6xl mx-auto space-y-12">
          <div className="relative group">
            {/* Outer Reactive Rings */}
            <div className="absolute -inset-12 border border-primary/20 rounded-full animate-spin-slow"></div>
            <div className="absolute -inset-8 border-2 border-primary/10 rounded-full animate-reverse-spin border-dashed"></div>

            {/* Main Core Orb */}
            <div className="relative w-48 h-48 rounded-full orb-gradient flex items-center justify-center shadow-[0_0_80px_rgba(143,245,255,0.4)]">
              <div className="w-32 h-32 rounded-full bg-slate-950/80 backdrop-blur-md flex items-center justify-center border border-primary/40">
                <div className="w-4 h-4 rounded-full bg-primary animate-ping"></div>
                <span className="material-symbols-outlined text-primary absolute text-5xl opacity-20">neurology</span>
              </div>
            </div>

            {/* Data Callouts */}
            <div className="absolute -right-48 top-0 glass-panel border-l-2 border-primary p-4 min-w-[180px]">
              <p className="font-label text-[10px] text-primary-dim tracking-widest uppercase mb-1">Neural_Density</p>
              <p className="font-headline text-2xl text-on-surface">
                98.4<span className="text-sm opacity-50 ml-1">%</span>
              </p>
              <div className="w-full bg-surface-container-highest h-1 mt-2">
                <div className="bg-primary w-[98%] h-full"></div>
              </div>
            </div>

            <div className="absolute -left-48 bottom-0 glass-panel border-r-2 border-primary p-4 min-w-[180px] text-right">
              <p className="font-label text-[10px] text-primary-dim tracking-widest uppercase mb-1">Sync_Rate</p>
              <p className="font-headline text-2xl text-on-surface">12ms</p>
              <p className="text-[8px] text-primary-dim/60 font-label mt-1">SATELLITE_UPLINK_01</p>
            </div>
          </div>

          {/* Voice Visualization / Frequency Bar */}
          <div className="w-full max-w-xl flex items-end justify-center gap-1 h-12">
            {[0.2, 0.4, 0.6, 0.8, 1, 0.8, 0.6, 0.4, 0.2, 0.4, 0.8, 0.4].map((opacity, i) => (
              <div key={i} className="w-1 bg-primary h-12" style={{ opacity }}></div>
            ))}
          </div>

          {/* Terminal Area */}
          <div className="w-full max-w-3xl glass-panel p-6 border border-primary/10 rounded-sm">
            <div className="flex items-center gap-2 mb-4">
              <div className="w-2 h-2 rounded-full bg-error animate-pulse"></div>
              <span className="font-label text-[10px] tracking-widest text-primary/60 uppercase">System_Output_Stream</span>
            </div>
            <div className="space-y-3 font-mono text-sm">
              <p className="text-on-surface/80 leading-relaxed">
                <span className="text-primary-dim">[09:42:11]</span> JARVIS: User detected. Security handshake complete. Initializing environment variables...
              </p>
              <p className="text-on-surface/80 leading-relaxed">
                <span className="text-primary-dim">[09:42:15]</span> SYSTEM: High-load tasks detected in Module_A. Re-routing computational power from sub-sector 4.
              </p>
              <p className="text-primary font-bold">
                <span className="text-primary-dim">[09:42:20]</span> JARVIS: &quot;Good morning. I&apos;ve analyzed the telemetry from last night&apos;s simulation. Results are ready for your review.&quot;
              </p>
              <div className="flex items-center gap-2 pt-2">
                <span className="text-primary-dim animate-pulse">_</span>
                <input
                  className="bg-transparent border-none focus:ring-0 p-0 text-sm text-on-surface placeholder:text-surface-container-highest w-full"
                  placeholder="Command input required..."
                  type="text"
                />
              </div>
            </div>
          </div>
        </div>

        {/* Floating Telemetry Ribbons */}
        <div className="absolute bottom-8 left-8 right-8 flex justify-between items-end pointer-events-none">
          {/* System Stats Cluster */}
          <div className="space-y-4">
            <div className="flex items-center gap-4 bg-surface-container-low/40 p-2 border-l border-primary/40">
              <div className="p-2 bg-primary/10 rounded-sm">
                <span className="material-symbols-outlined text-primary text-lg">memory</span>
              </div>
              <div>
                <p className="text-[9px] font-label text-slate-500 uppercase">CPU_USAGE</p>
                <p className="text-xs font-headline text-on-surface">34.2%</p>
              </div>
            </div>
            <div className="flex items-center gap-4 bg-surface-container-low/40 p-2 border-l border-primary/40">
              <div className="p-2 bg-primary/10 rounded-sm">
                <span className="material-symbols-outlined text-primary text-lg">database</span>
              </div>
              <div>
                <p className="text-[9px] font-label text-slate-500 uppercase">MEMORY_POOL</p>
                <p className="text-xs font-headline text-on-surface">1.2TB / 8TB</p>
              </div>
            </div>
          </div>

          {/* Latency / Network Cluster */}
          <div className="text-right">
            <div className="bg-surface-container-highest/20 p-4 border border-outline-variant/20 rounded-sm">
              <div className="flex items-center justify-end gap-2 mb-2">
                <span className="text-[9px] font-label text-primary uppercase">API_CONNECTIVITY</span>
                <div className="flex gap-1">
                  <div className="w-1 h-2 bg-primary"></div>
                  <div className="w-1 h-3 bg-primary"></div>
                  <div className="w-1 h-4 bg-primary"></div>
                </div>
              </div>
              <p className="text-[10px] font-label text-slate-400">LATENCY: 4MS</p>
              <p className="text-[10px] font-label text-slate-400">PACKET_LOSS: 0.000%</p>
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}
