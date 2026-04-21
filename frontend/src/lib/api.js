const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export async function uploadPdf(file) {
  const fd = new FormData()
  fd.append('file', file)
  const resp = await fetch(`${API_URL}/upload`, { method: 'POST', body: fd })
  if (!resp.ok) throw new Error(await resp.text())
  return resp.json()
}

export async function resetIndex() {
  const resp = await fetch(`${API_URL}/reset`, { method: 'POST' })
  if (!resp.ok) throw new Error(await resp.text())
  return resp.json()
}

export async function fetchGraph() {
  const resp = await fetch(`${API_URL}/graph`)
  if (!resp.ok) throw new Error(await resp.text())
  return resp.json()
}

export function streamAnswer({ question, top_k = 5, onContext, onToken, onDone, onError }) {
  const ctrl = new AbortController()

  fetch(`${API_URL}/query/stream`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ question, top_k }),
    signal: ctrl.signal,
  })
    .then(async (response) => {
      if (!response.ok || !response.body) {
        throw new Error(await response.text())
      }

      const reader = response.body.getReader()
      const decoder = new TextDecoder()
      let buf = ''

      while (true) {
        const { value, done } = await reader.read()
        if (done) break
        buf += decoder.decode(value, { stream: true })

        const events = buf.split('\n\n')
        buf = events.pop() || ''

        for (const evt of events) {
          const lines = evt.split('\n')
          const eventType = lines.find((l) => l.startsWith('event:'))?.replace('event:', '').trim()
          const data = lines.filter((l) => l.startsWith('data:')).map((l) => l.replace('data:', '').trim()).join('\n')

          if (!data) continue
          if (eventType === 'context') {
            onContext?.(JSON.parse(data))
          } else if (eventType === 'done') {
            onDone?.()
          } else {
            onToken?.(data)
          }
        }
      }
      onDone?.()
    })
    .catch((error) => {
      if (error.name !== 'AbortError') onError?.(error)
    })

  return () => ctrl.abort()
}
