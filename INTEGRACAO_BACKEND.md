# Guia de Integração - JARVIS Web UI com Backend Python

Este documento descreve como conectar a interface web Next.js com o backend Python do JARVIS.

## 🔗 Arquitetura de Conexão

```
┌─────────────────────────────┐
│  JARVIS Web UI (Next.js)    │
│  http://localhost:3000      │
└──────────────┬──────────────┘
               │ HTTP/WebSocket
               ▼
┌─────────────────────────────┐
│  JARVIS Backend (Python)    │
│  http://localhost:5000      │
└─────────────────────────────┘
```

## 🚀 Configuração Inicial

### 1. Backend Python (Flask)

Crie um arquivo `jarvis_server.py`:

```python
from flask import Flask, jsonify
from flask_cors import CORS
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS para Next.js

# Estado simulado do sistema
SYSTEM_STATE = {
    'neural_density': 98.4,
    'sync_rate': '12ms',
    'cpu_usage': 34.2,
    'memory_pool': '1.2TB / 8TB',
    'status': 'OPTIMAL'
}

@app.route('/api/status', methods=['GET'])
def get_status():
    """Retorna status do sistema"""
    return jsonify(SYSTEM_STATE)

@app.route('/api/metrics', methods=['GET'])
def get_metrics():
    """Retorna métricas em tempo real"""
    return jsonify({
        'recognition_accuracy': 99.42,
        'processing_power': 42.1,
        'buffer_utilization': 2.1,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/logs', methods=['GET'])
def get_logs():
    """Retorna logs do sistema"""
    logs = [
        {'time': '09:42:11', 'message': 'User detected. Security handshake complete.', 'type': 'info'},
        {'time': '09:42:15', 'message': 'High-load tasks detected in Module_A.', 'type': 'warning'},
        {'time': '09:42:20', 'message': 'Neural analysis complete. Results ready.', 'type': 'success'},
    ]
    return jsonify(logs)

@app.route('/api/modules', methods=['GET'])
def get_modules():
    """Retorna módulos ativos"""
    modules = [
        {'name': 'Voice Synthesis', 'version': 'v4.2.1', 'status': 'Active', 'tasks': 14},
        {'name': 'Automation Core', 'version': 'v3.8.0', 'status': 'Active', 'tasks': 12},
        {'name': 'Node Bridge', 'version': 'v2.1.0', 'status': 'Standby', 'tasks': 0},
    ]
    return jsonify(modules)

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
```

### 2. Instale dependências Python

```bash
pip install flask flask-cors
```

### 3. Configure Next.js

Crie `.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:5000
NEXT_PUBLIC_WS_URL=ws://localhost:5000
```

## 📡 Implementando Chamadas API

### Exemplo 1: Buscar Status do Sistema

```typescript
// app/lib/api.ts
export async function getSystemStatus() {
  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/status`)
  if (!res.ok) throw new Error('Failed to fetch status')
  return res.json()
}
```

### Exemplo 2: Usar em um Componente

```typescript
'use client'

import { useEffect, useState } from 'react'
import { getSystemStatus } from '@/lib/api'

export function SystemStatus() {
  const [status, setStatus] = useState(null)

  useEffect(() => {
    getSystemStatus()
      .then(setStatus)
      .catch(console.error)
  }, [])

  if (!status) return <div>Carregando...</div>

  return (
    <div>
      <p>Neural Density: {status.neural_density}%</p>
      <p>Sync Rate: {status.sync_rate}</p>
    </div>
  )
}
```

### Exemplo 3: Atualização em Tempo Real com SWR

```typescript
'use client'

import useSWR from 'swr'

const fetcher = (url) => fetch(url).then(r => r.json())

export function LiveMetrics() {
  const { data, error } = useSWR(
    `${process.env.NEXT_PUBLIC_API_URL}/api/metrics`,
    fetcher,
    { refreshInterval: 1000 } // Atualiza a cada 1 segundo
  )

  if (error) return <div>Erro ao carregar</div>
  if (!data) return <div>Carregando...</div>

  return (
    <div>
      <p>Accuracy: {data.recognition_accuracy}%</p>
      <p>Power: {data.processing_power} TFLOPS</p>
    </div>
  )
}
```

## 🔄 WebSocket para Real-Time Updates

### Backend (Python com Flask-SocketIO)

```bash
pip install python-socketio python-engineio
```

```python
from flask_socketio import SocketIO, emit
import threading
import time

socketio = SocketIO(app, cors_allowed_origins="*")

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

def broadcast_metrics():
    """Envia métricas a cada 1 segundo"""
    while True:
        time.sleep(1)
        socketio.emit('metrics_update', SYSTEM_STATE, broadcast=True)

# Inicie thread de broadcast
thread = threading.Thread(target=broadcast_metrics, daemon=True)
thread.start()

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5000)
```

### Frontend (Next.js com Socket.IO)

```bash
npm install socket.io-client
```

```typescript
'use client'

import { useEffect, useState } from 'react'
import { io } from 'socket.io-client'

export function RealtimeUpdates() {
  const [metrics, setMetrics] = useState(null)

  useEffect(() => {
    const socket = io(process.env.NEXT_PUBLIC_WS_URL)

    socket.on('metrics_update', (data) => {
      setMetrics(data)
    })

    return () => socket.disconnect()
  }, [])

  return (
    <div>
      {metrics && (
        <>
          <p>Neural Density: {metrics.neural_density}%</p>
          <p>Status: {metrics.status}</p>
        </>
      )}
    </div>
  )
}
```

## 🔐 Autenticação

### Backend

```python
from functools import wraps
import jwt

SECRET_KEY = 'sua-chave-secreta-aqui'

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization', '').split(' ')[1]
        if not token:
            return {'message': 'Token is missing'}, 401
        try:
            jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        except:
            return {'message': 'Token is invalid'}, 401
        return f(*args, **kwargs)
    return decorated

@app.route('/api/protected', methods=['GET'])
@token_required
def protected_route():
    return jsonify({'message': 'Access granted'})
```

### Frontend

```typescript
async function fetchProtected() {
  const token = localStorage.getItem('auth_token')
  
  const res = await fetch(`${API_URL}/api/protected`, {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  })
  
  return res.json()
}
```

## 📊 Estrutura de Dados Esperada

### Status do Sistema

```json
{
  "neural_density": 98.4,
  "sync_rate": "12ms",
  "cpu_usage": 34.2,
  "memory_pool": "1.2TB / 8TB",
  "status": "OPTIMAL"
}
```

### Métricas

```json
{
  "recognition_accuracy": 99.42,
  "processing_power": 42.1,
  "buffer_utilization": 2.1,
  "timestamp": "2025-03-23T14:22:01Z"
}
```

### Logs

```json
[
  {
    "time": "09:42:11",
    "message": "User detected. Security handshake complete.",
    "type": "info"
  },
  {
    "time": "09:42:15",
    "message": "High-load tasks detected in Module_A.",
    "type": "warning"
  }
]
```

## 🚀 Deployment

### Local Development

```bash
# Terminal 1: Backend Python
python jarvis_server.py

# Terminal 2: Frontend Next.js
npm run dev
```

### Production (Vercel + Cloud Python)

1. Deploy Next.js no Vercel
2. Deploy backend Python em plataforma como Render, Railway ou AWS
3. Atualize `NEXT_PUBLIC_API_URL` com URL de produção

## 🐛 Troubleshooting

**CORS Error**: Adicione `CORS(app)` no backend Flask

**Conexão recusada**: Certifique-se de que backend está rodando na porta 5000

**Timeout**: Aumente o timeout em requisições:
```typescript
fetch(url, { 
  signal: AbortSignal.timeout(5000) // 5 segundos
})
```

## 📖 Recursos Úteis

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Next.js Data Fetching](https://nextjs.org/docs/app/building-your-application/data-fetching)
- [Socket.IO](https://socket.io/)
- [SWR](https://swr.vercel.app/)

---

Para mais informações, consulte a documentação do projeto principal.
