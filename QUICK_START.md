# ⚡ Quick Start - JARVIS Web UI

Comece a usar o JARVIS Web UI em menos de 5 minutos!

## 1️⃣ Instalação (1 minuto)

```bash
# Instale as dependências
npm install
```

## 2️⃣ Iniciar Servidor (30 segundos)

```bash
npm run dev
```

## 3️⃣ Abrir no Navegador (30 segundos)

Clique aqui: [http://localhost:3000](http://localhost:3000)

## 4️⃣ Explorar as Páginas

| Página | URL | Descrição |
|--------|-----|-----------|
| 🏠 Dashboard | `http://localhost:3000` | Visualizar status do sistema |
| 👁️ Visualizer | `http://localhost:3000/visualizer` | Análise visual com HUD |
| ⚙️ Config | `http://localhost:3000/configs` | Configurações do sistema |
| 📦 Modules | `http://localhost:3000/modules` | Módulos ativos |

## 🎨 Personalizações Rápidas

### Mudar Cor Primária

Abra `tailwind.config.js` e procure por:

```js
'primary': '#8ff5ff',  // Cyan
```

Troque para sua cor (ex: `'#00ff00'` para verde)

### Mudar Logo

Edite `components/Header.tsx`:

```tsx
<h1 className="...">SEU_NOME_AQUI</h1>
```

### Adicionar Nova Página

1. Crie pasta: `app/nova-pagina/`
2. Crie arquivo: `app/nova-pagina/page.tsx`
3. Adicione o link no `components/Sidebar.tsx`

## 📡 Conectar ao Backend Python

Leia: `INTEGRACAO_BACKEND.md`

Quick example:

```typescript
// app/lib/api.ts
export async function getStatus() {
  const res = await fetch('http://localhost:5000/api/status')
  return res.json()
}
```

## 🚀 Deploy em Produção

### Opção 1: Vercel (Recomendado)

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel
```

### Opção 2: Heroku

```bash
heroku create jarvis-ui
git push heroku main
```

### Opção 3: Seu Servidor

```bash
npm run build
npm start
```

## 🐛 Problemas Comuns

**P: Porta 3000 já está em uso**
```bash
npm run dev -- -p 3001
```

**P: Erros de CORS ao conectar Python**
```python
# No backend Flask adicione:
from flask_cors import CORS
CORS(app)
```

**P: Estilos não aparecem**
```bash
rm -rf .next
npm run dev
```

## 📚 Próximos Passos

1. ✅ Customizar cores e logo
2. ✅ Conectar backend Python
3. ✅ Adicionar mais páginas
4. ✅ Deploy em produção

## 📖 Documentação Completa

- **JARVIS_WEB_UI_README.md** - Guia detalhado
- **INTEGRACAO_BACKEND.md** - Backend Python
- **IMPLEMENTACAO_COMPLETADA.md** - Overview técnico

## 💡 Dicas Úteis

- Use DevTools (F12) para debugar
- Tailwind IntelliSense para auto-complete CSS
- Next.js Fast Refresh atualiza sem reload
- Server Components por padrão (mais rápido)

## 🆘 Precisa de Ajuda?

1. Verifique a documentação acima
2. Procure por comentários `TODO` no código
3. Verifique `JARVIS_WEB_UI_README.md`
4. Leia o erro no console

---

**Pronto para começar? Execute:**

```bash
npm install && npm run dev
```

**Boa sorte! 🚀**
