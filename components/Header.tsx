'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'

export function Header() {
  const pathname = usePathname()

  const isActive = (href: string) => {
    return pathname === href
  }

  return (
    <header className="fixed top-0 w-full z-50 bg-slate-950/40 backdrop-blur-xl border-b border-cyan-500/20 shadow-[0_4px_30px_rgba(0,0,0,0.1)]">
      <div className="flex justify-between items-center px-8 py-4">
        <div className="flex items-center gap-6">
          <h1 className="text-xl font-bold tracking-tighter text-cyan-400 drop-shadow-[0_0_8px_rgba(0,240,255,0.5)] font-headline">
            KINETIC_INTEL_V2.0
          </h1>
          <nav className="hidden md:flex gap-8">
            <Link
              href="/"
              className={`font-headline uppercase tracking-widest text-xs transition-all duration-300 ${
                isActive('/') ? 'text-cyan-400 border-b-2 border-cyan-400 pb-1' : 'text-slate-500 hover:text-cyan-200'
              }`}
            >
              DASHBOARD
            </Link>
            <Link
              href="/visualizer"
              className={`font-headline uppercase tracking-widest text-xs transition-all duration-300 ${
                isActive('/visualizer') ? 'text-cyan-400 border-b-2 border-cyan-400 pb-1' : 'text-slate-500 hover:text-cyan-200'
              }`}
            >
              VISUALIZER
            </Link>
            <Link
              href="/modules"
              className={`font-headline uppercase tracking-widest text-xs transition-all duration-300 ${
                isActive('/modules') ? 'text-cyan-400 border-b-2 border-cyan-400 pb-1' : 'text-slate-500 hover:text-cyan-200'
              }`}
            >
              MODULES
            </Link>
            <Link
              href="/configs"
              className={`font-headline uppercase tracking-widest text-xs transition-all duration-300 ${
                isActive('/configs') ? 'text-cyan-400 border-b-2 border-cyan-400 pb-1' : 'text-slate-500 hover:text-cyan-200'
              }`}
            >
              CONFIGS
            </Link>
          </nav>
        </div>
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2">
            <span className="material-symbols-outlined text-cyan-400">settings_input_antenna</span>
            <span className="material-symbols-outlined text-cyan-400">security</span>
            <span className="material-symbols-outlined text-cyan-400">memory</span>
          </div>
          <div className="w-8 h-8 rounded-sm bg-primary/20 flex items-center justify-center border border-primary/40">
            <span className="material-symbols-outlined text-xs text-primary">bolt</span>
          </div>
        </div>
      </div>
    </header>
  )
}
