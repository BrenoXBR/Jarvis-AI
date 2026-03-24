'use client'

export function DataRibbon() {
  const data = [
    'L: 256/1024',
    'CORE_TEMP: 42°C',
    'ENTROPY: 0.00342',
    'PACKET_LOSS: 0.00%',
    'ACTIVE_SOCKETS: 882',
    'UPTIME: 14:22:01',
    'ENCRYPTION: AES-512',
    'NEURAL_ENGINE: OPTIMAL',
  ]

  return (
    <div className="fixed top-20 left-0 w-full bg-surface-container-highest/40 border-y border-primary/5 py-1 z-30 overflow-hidden">
      <div className="whitespace-nowrap flex gap-12 font-label text-[9px] tracking-[0.3em] text-primary/40 uppercase animate-marquee">
        {[...data, ...data].map((item, i) => (
          <span key={i}>{item}</span>
        ))}
      </div>
    </div>
  )
}
