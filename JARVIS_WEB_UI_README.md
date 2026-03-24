# KINETIC_INTEL_V2.0 - JARVIS Web Interface

Uma interface web moderna e sofisticada para o JARVIS OS, baseada no design system "The Ethereal Command Deck". Construída com Next.js, React e Tailwind CSS.

## 🚀 Características

- **Dashboard Neural** - Visualização central do status do sistema com orbe dinâmico e métricas em tempo real
- **Visualizer** - Análise visual com overlays HUD, detecções de objetos e logs neurais
- **System Config** - Configuração de API bridges, parâmetros de voz e automação
- **Módulos Ativos** - Monitoramento de módulos do sistema (Voice Synthesis, Automation Core, Node Bridge)
- **Design HUD Futurista** - Glassmorphism, cores luminescentes cyan/purple, animações sophisticadas
- **Responsivo** - Interface adaptável para desktop e mobile

## 📋 Requisitos

- Node.js 18.0 ou superior
- npm, yarn, pnpm ou bun

## 🛠️ Instalação

1. Clone o repositório:
```bash
git clone https://github.com/BrenoXBR/Jarvis-AI.git
cd Jarvis-AI
```

2. Instale as dependências:
```bash
npm install
# ou
yarn install
# ou
pnpm install
```

3. Inicie o servidor de desenvolvimento:
```bash
npm run dev
# ou
yarn dev
# ou
pnpm dev
```

4. Abra [http://localhost:3000](http://localhost:3000) no seu navegador

## 📁 Estrutura do Projeto

```
├── app/
│   ├── layout.tsx              # Layout raiz
│   ├── globals.css             # Estilos globais
│   ├── page.tsx                # Dashboard (Neural Link)
│   ├── visualizer/
│   │   └── page.tsx            # Página Visualizer
│   ├── configs/
│   │   └── page.tsx            # Página System Config
│   ├── modules/
│   │   └── page.tsx            # Página Módulos
│   ├── neural-link/
│   ├── log-stream/
│   ├── vision-feed/
│   ├── api-bridge/
│   └── system/
├── components/
│   ├── Header.tsx              # Navegação superior
│   ├── Sidebar.tsx             # Menu lateral
│   └── DataRibbon.tsx          # Fita de dados em tempo real
├── tailwind.config.js          # Configuração Tailwind
├── next.config.js              # Configuração Next.js
└── package.json
```

## 🎨 Design System

### Cores Principais
- **Primary (Cyan)**: `#8ff5ff` - Elementos principais, glows
- **Primary Dim**: `#00deec` - Interações micro
- **Tertiary (Purple)**: `#ac89ff` - Acentos secundários
- **Background**: `#050f16` - Fundo noir absoluto
- **Surface Container**: `#0e1b23` - Camadas de interface

### Tipografia
- **Headlines**: Space Grotesk (engineered, technical)
- **Body**: Manrope (readable, humanized)
- **Labels**: Space Grotesk com tracking amplo (monospace feel)

### Componentes
- Glass panels com `backdrop-blur: 20px`
- Orbes gradientes radiais
- Animações de scan e pulsação
- Bordas luminescentes (sem linhas sólidas)
- Overlays HUD com detecções visuais

## 🔌 Integração com Python/Backend

Para conectar com o backend Python do JARVIS:

1. Configure as variáveis de ambiente em `.env.local`:
```env
NEXT_PUBLIC_API_URL=http://localhost:5000
NEXT_PUBLIC_WS_URL=ws://localhost:5000
```

2. Crie um arquivo `/app/api/` para rotas API (Server Actions ou Route Handlers)

3. Use SWR ou fetch para comunicação com o backend:
```typescript
import useSWR from 'swr'

export function useSystemStatus() {
  const { data, error } = useSWR('/api/status', fetch)
  return { status: data, isLoading: !error && !data, error }
}
```

## 📱 Páginas Disponíveis

### Dashboard (/)
- Orbe neural central com aura brilhante
- Métricas de Density e Sync Rate
- Visualização de frequência
- Stream de logs do sistema

### Visualizer (/visualizer)
- Feed central com overlays HUD
- Bounding boxes com detecções
- Métricas analíticas em painel lateral
- Logs neurais coloridos por tipo

### Configs (/configs)
- API Secure Bridge (Gemini, WolframAlpha, Stable Diffusion)
- Voice Output (volume, velocidade, wake word)
- Automation (PyAutoGUI, mouse smoothing)
- System Diagnostics

### Modules (/modules)
- Cards dos módulos ativos
- Voice Synthesis, Automation Core, Node Bridge
- Status e runtime tasks

### Seções Secundárias
- Neural Link: Interface de conexão neural
- Log Stream: Logs do sistema em tempo real
- Vision Feed: Feed da câmera
- API Bridge: Status das APIs
- System: Configurações do sistema

## 🚀 Build para Produção

```bash
npm run build
npm start
```

## 📝 Customização

### Alterar Cores
Edite `tailwind.config.js` na seção `colors`:
```js
'primary': '#SEU_HEX_AQUI',
'tertiary': '#PURPLE_AQUI',
```

### Adicionar Novas Páginas
1. Crie um diretório em `app/nova-pagina/`
2. Adicione `page.tsx` com o layout
3. O Next.js fará o roteamento automaticamente

### Atualizar Dados em Tempo Real
Use Server Components ou SWR para sincronizar dados:
```typescript
'use client'
import useSWR from 'swr'

export function RealtimeMetric() {
  const { data } = useSWR('/api/metric', fetch, { 
    refreshInterval: 1000 
  })
  return <div>{data?.value}</div>
}
```

## 🔐 Segurança

- Variáveis de ambiente para APIs sensíveis
- Server Components por padrão
- CORS configurado no Next.js
- Validação de entrada em formulários

## 📊 Performance

- Server-Side Rendering onde possível
- Image Optimization automática
- Code splitting por rota
- Streaming CSS com Tailwind
- Animações GPU-accelerated

## 🐛 Troubleshooting

**Problema**: Imagens não carregam
- Solução: Verifique as permissões do domínio em `next.config.js`

**Problema**: Estilos não aplicados
- Solução: Limpe `.next/` e execute `npm run dev` novamente

**Problema**: Animações lentas
- Solução: Desabilite efeitos visuais em navegadores lentos

## 📖 Documentação do Design

Veja os arquivos DESIGN-*.md para especificações completas do design system.

## 🤝 Integração com JARVIS Python

Este projeto é um frontend para o JARVIS OS desenvolvido em Python. Configure a comunicação:

```python
# jarvis_backend.py
from flask import Flask
app = Flask(__name__)

@app.route('/api/status')
def status():
    return {'neural_density': 98.4, 'sync_rate': '12ms'}
```

```typescript
// Dentro de um Server Action do Next.js
async function fetchStatus() {
  const res = await fetch('http://localhost:5000/api/status')
  return res.json()
}
```

## 📄 Licença

MIT License - Veja LICENSE file para detalhes

## 👤 Autor

Breno Speretta
- GitHub: [@BrenoXBR](https://github.com/BrenoXBR)

---

**Status**: ✨ Em desenvolvimento ativo  
**Versão**: 2.0.0  
**Data da Última Atualização**: Março 2025
