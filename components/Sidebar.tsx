'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'

const navItems = [
  { href: '/neural-link', label: 'Neural Link', icon: 'psychology' },
  { href: '/log-stream', label: 'Log Stream', icon: 'terminal' },
  { href: '/vision-feed', label: 'Vision Feed', icon: 'visibility' },
  { href: '/api-bridge', label: 'API Bridge', icon: 'api' },
  { href: '/system', label: 'System', icon: 'settings_slow_motion' },
]

export function Sidebar() {
  const pathname = usePathname()

  const isActive = (href: string) => {
    return pathname === href
  }

  return (
    <aside className="fixed left-0 top-0 h-full w-64 z-40 bg-slate-950/60 backdrop-blur-md border-r border-cyan-500/10 flex flex-col h-full pt-24 pb-8 hidden md:flex">
      <div className="px-6 mb-8">
        <h2 className="text-cyan-400 font-black font-headline text-lg">JARVIS_OS</h2>
        <p className="text-[10px] text-cyan-400/60 tracking-[0.2em] font-headline uppercase">STATUS: OPTIMAL</p>
      </div>

      <nav className="flex-1 space-y-1">
        {navItems.map((item) => (
          <Link
            key={item.href}
            href={item.href}
            className={`flex items-center gap-3 px-6 py-4 font-headline text-sm uppercase transition-all duration-200 ease-in-out ${
              isActive(item.href)
                ? 'text-cyan-400 bg-cyan-950/30 border-l-4 border-cyan-400'
                : 'text-slate-400 hover:bg-slate-900/50 hover:text-cyan-300'
            }`}
          >
            <span className="material-symbols-outlined">{item.icon}</span>
            {item.label}
          </Link>
        ))}
      </nav>

      <div className="px-6 mt-auto space-y-2">
        <button className="w-full bg-primary text-on-primary text-[10px] font-headline font-bold py-2 rounded-sm hover:opacity-90 transition-opacity">
          INITIALIZE_UPGRADE
        </button>
        <div className="pt-4 border-t border-cyan-500/10">
          <a href="#" className="flex items-center gap-3 text-slate-500 py-2 hover:text-cyan-300 transition-colors">
            <span className="material-symbols-outlined text-sm">help_center</span>
            <span className="text-[10px] font-headline uppercase">Support</span>
          </a>
          <a href="#" className="flex items-center gap-3 text-slate-500 py-2 hover:text-error transition-colors">
            <span className="material-symbols-outlined text-sm">power_settings_new</span>
            <span className="text-[10px] font-headline uppercase">Logout</span>
          </a>
        </div>
      </div>
    </aside>
  )
}
