'use client'

import Image from 'next/image'
import { Header } from '@/components/Header'
import { Sidebar } from '@/components/Sidebar'
import { DataRibbon } from '@/components/DataRibbon'

export default function Visualizer() {
  return (
    <div className="min-h-screen bg-background text-on-background font-body">
      <Header />
      <Sidebar />
      <DataRibbon />

      <main className="md:ml-64 pt-32 pb-20 px-6 lg:px-12 min-h-screen">
        <div className="grid grid-cols-12 gap-6">
          {/* Central Visualizer */}
          <div className="col-span-12 lg:col-span-8 space-y-6">
            <div className="relative aspect-video bg-surface-container-lowest border border-outline-variant/30 overflow-hidden group">
              {/* Glass Texture Overlay */}
              <div className="absolute inset-0 bg-gradient-to-tr from-primary/5 to-transparent pointer-events-none"></div>
              <div className="absolute inset-0 wireframe-grid pointer-events-none opacity-20"></div>

              {/* The Main Feed Image */}
              <Image
                src="https://lh3.googleusercontent.com/aida-public/AB6AXuAcI-V3Zb7_AyCI27icv2nPxW_ZxHFjirBmBnvLDRGrJZcf2EPNUpjIqcGabq3C1j4f8y2TRudh6Ky55A9iB2QK_ppxF7rdoNJxXhq48cHq_nJ6xmPkyiUydDhoI_KbDhtVDYGAFbHVlcEn6SloOtjPt_VEVWszm3I90xoC9NRLBmytEAjZaAnBxhGXKd6YMC3zKheXxdLqq-wgnqm5NTFYuX0dQ0np5kLKT9dNpxib0mWkN-nB0RXeEgRKPJi4_sV3EIjlq7Se08g"
                alt="Vision feed"
                fill
                className="w-full h-auto object-cover opacity-60 grayscale brightness-50 contrast-125"
              />

              {/* Scanning Line */}
              <div className="scanning-line"></div>

              {/* HUD Overlays (Bounding Boxes) */}
              <div className="absolute inset-0 pointer-events-none p-12">
                {/* Box 1: AI Core */}
                <div className="absolute top-[15%] left-[20%] w-[120px] h-[80px] border border-primary/60 bg-primary/5">
                  <div className="absolute -top-6 left-0 flex items-center gap-1">
                    <span className="bg-primary text-on-primary text-[10px] px-1 font-label">OBJECT: CORE_NODE</span>
                    <span className="text-primary text-[8px] font-label">CONF: 99.8%</span>
                  </div>
                  <div className="absolute -bottom-6 right-0 text-[8px] font-label text-primary/40 uppercase">x: 442 | y: 129</div>
                  <div className="absolute top-0 left-0 w-2 h-2 border-t border-l border-primary"></div>
                  <div className="absolute top-0 right-0 w-2 h-2 border-t border-r border-primary"></div>
                  <div className="absolute bottom-0 left-0 w-2 h-2 border-b border-l border-primary"></div>
                  <div className="absolute bottom-0 right-0 w-2 h-2 border-b border-r border-primary"></div>
                </div>

                {/* Box 2: Potential Error */}
                <div className="absolute bottom-[25%] right-[30%] w-[180px] h-[120px] border border-error/60 bg-error/5">
                  <div className="absolute -top-6 left-0 flex items-center gap-1">
                    <span className="bg-error text-on-error text-[10px] px-1 font-label">ALERT: ANOMALY_DETECTED</span>
                    <span className="text-error text-[8px] font-label">CONF: 84.1%</span>
                  </div>
                  <div className="absolute inset-0 flex items-center justify-center">
                    <div className="w-full h-px bg-error/20 rotate-45"></div>
                    <div className="w-full h-px bg-error/20 -rotate-45"></div>
                  </div>
                </div>

                {/* Box 3: Data Stream */}
                <div className="absolute top-[40%] right-[10%] w-[60px] h-[200px] border border-tertiary/60 bg-tertiary/5">
                  <div className="absolute -top-6 right-0 flex items-center gap-1">
                    <span className="bg-tertiary text-on-tertiary text-[10px] px-1 font-label">TYPE: DATA_PIPE</span>
                  </div>
                </div>
              </div>

              {/* Screen Corners Metadata */}
              <div className="absolute top-4 left-4 font-label text-[10px] text-primary space-y-1">
                <div>REC [●] LIVE_FEED</div>
                <div className="text-white/40">FR: 120 FPS</div>
              </div>
              <div className="absolute bottom-4 right-4 font-label text-[10px] text-primary text-right space-y-1">
                <div>COORD: 34° 03&apos; 08&quot; N</div>
                <div>ELEV: 12,442 FT</div>
              </div>
            </div>

            {/* Action Controls */}
            <div className="grid grid-cols-4 gap-4">
              <div className="bg-surface-container-high p-4 border-l-2 border-primary/40 hover:bg-surface-container-highest transition-colors cursor-pointer">
                <div className="text-[10px] font-label text-primary-dim mb-1">ZOOM_LEVEL</div>
                <div className="text-xl font-headline font-bold">4.2X</div>
              </div>
              <div className="bg-surface-container-high p-4 border-l-2 border-primary/40 hover:bg-surface-container-highest transition-colors cursor-pointer">
                <div className="text-[10px] font-label text-primary-dim mb-1">FILTER_STRENGTH</div>
                <div className="text-xl font-headline font-bold">88%</div>
              </div>
              <div className="bg-surface-container-high p-4 border-l-2 border-primary/40 hover:bg-surface-container-highest transition-colors cursor-pointer">
                <div className="text-[10px] font-label text-primary-dim mb-1">OBJECT_COUNT</div>
                <div className="text-xl font-headline font-bold">14</div>
              </div>
              <div className="bg-surface-container-high p-4 border-l-2 border-error/40 hover:bg-surface-container-highest transition-colors cursor-pointer">
                <div className="text-[10px] font-label text-error-dim mb-1">ANOMALIES</div>
                <div className="text-xl font-headline font-bold">03</div>
              </div>
            </div>
          </div>

          {/* Side Intelligence Panel */}
          <div className="col-span-12 lg:col-span-4 space-y-6">
            {/* Analysis Card */}
            <div className="bg-surface-container p-6 border border-outline-variant/20 relative overflow-hidden">
              <div className="absolute top-0 right-0 p-2">
                <span className="material-symbols-outlined text-primary/20 text-4xl">query_stats</span>
              </div>
              <h3 className="font-headline text-lg font-bold mb-4 flex items-center gap-2">
                <span className="w-2 h-4 bg-primary"></span> ANALYTIC_METRICS
              </h3>
              <div className="space-y-4">
                <div className="space-y-2">
                  <div className="flex justify-between text-[10px] font-label">
                    <span>RECOGNITION_ACCURACY</span>
                    <span>99.42%</span>
                  </div>
                  <div className="h-1 bg-surface-container-highest w-full">
                    <div className="h-full bg-primary shadow-[0_0_8px_#8ff5ff]" style={{ width: '99.42%' }}></div>
                  </div>
                </div>
                <div className="space-y-2">
                  <div className="flex justify-between text-[10px] font-label">
                    <span>PROCESSING_POWER</span>
                    <span>42.1 TFLOPS</span>
                  </div>
                  <div className="h-1 bg-surface-container-highest w-full">
                    <div className="h-full bg-tertiary shadow-[0_0_8px_#ac89ff]" style={{ width: '65%' }}></div>
                  </div>
                </div>
                <div className="space-y-2">
                  <div className="flex justify-between text-[10px] font-label">
                    <span>BUFFER_UTILIZATION</span>
                    <span>2.1GB / 8GB</span>
                  </div>
                  <div className="h-1 bg-surface-container-highest w-full">
                    <div className="h-full bg-primary shadow-[0_0_8px_#8ff5ff]" style={{ width: '25%' }}></div>
                  </div>
                </div>
              </div>
            </div>

            {/* Recent Detections List */}
            <div className="bg-surface-container p-6 border border-outline-variant/20">
              <h3 className="font-headline text-lg font-bold mb-4">NEURAL_LOGS</h3>
              <div className="space-y-3">
                {[
                  { time: 'T+14:22:01.4', label: 'UI_ELEMENT: BUTTON_PRIMARY', color: 'bg-primary', status: 'normal' },
                  { time: 'T+14:21:58.2', label: 'ERR_VOID: MEMORY_LEAK_04', color: 'bg-error', status: 'error' },
                  { time: 'T+14:21:55.9', label: 'META_DATA: CACHE_FLUSH', color: 'bg-slate-500', status: 'faded' },
                  { time: 'T+14:21:52.1', label: 'IO_EVENT: KEYBOARD_IN', color: 'bg-slate-500', status: 'faded' },
                ].map((log, i) => (
                  <div key={i} className={`flex items-center gap-4 group cursor-pointer ${log.status === 'faded' ? 'opacity-60' : 'opacity-80'}`}>
                    <div className={`w-1 h-8 ${log.color}`}></div>
                    <div className="flex-grow">
                      <div className={`text-[10px] font-label ${log.color === 'bg-error' ? 'text-error-dim' : log.color === 'bg-slate-500' ? 'text-slate-500' : 'text-primary/60'}`}>
                        {log.time}
                      </div>
                      <div className="text-sm font-headline text-on-surface">{log.label}</div>
                    </div>
                    <span className="material-symbols-outlined text-primary/40 group-hover:text-primary">chevron_right</span>
                  </div>
                ))}
              </div>
              <button className="w-full mt-6 py-2 text-[10px] font-label text-primary/60 hover:text-primary border-t border-outline-variant/10 transition-colors uppercase">
                View Full Traceback
              </button>
            </div>

            {/* Heartbeat Monitor */}
            <div className="bg-surface-container p-6 border border-outline-variant/20 flex flex-col items-center">
              <div className="relative w-32 h-32 flex items-center justify-center">
                <svg className="absolute w-full h-full -rotate-90">
                  <circle cx="64" cy="64" fill="transparent" r="58" stroke="currentColor" strokeWidth="2" className="text-primary/10"></circle>
                  <circle cx="64" cy="64" fill="transparent" r="58" stroke="currentColor" strokeDasharray="364" strokeDashoffset="100" strokeWidth="2" className="text-primary"></circle>
                </svg>
                <svg className="absolute w-20 h-20 -rotate-90">
                  <circle cx="40" cy="40" fill="transparent" r="34" stroke="currentColor" strokeWidth="2" className="text-tertiary/10"></circle>
                  <circle cx="40" cy="40" fill="transparent" r="34" stroke="currentColor" strokeDasharray="213" strokeDashoffset="150" strokeWidth="2" className="text-tertiary"></circle>
                </svg>
                <div className="text-center">
                  <div className="text-xs font-label text-primary">CORE</div>
                  <div className="text-xl font-headline font-black">88%</div>
                </div>
              </div>
              <div className="mt-4 text-center">
                <div className="text-[10px] font-label tracking-widest text-primary/60 uppercase">NEURAL_STABILITY: HIGH</div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}
