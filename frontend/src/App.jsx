import { useEffect, useMemo, useState } from 'react'
import UploadDropzone from './components/UploadDropzone'
import ChatPanel from './components/ChatPanel'
import ThreeGraph from './components/ThreeGraph'
import { fetchGraph, resetIndex, streamAnswer, uploadPdf } from './lib/api'

export default function App() {
  const [uploading, setUploading] = useState(false)
  const [thinking, setThinking] = useState(false)
  const [points, setPoints] = useState([])
  const [answer, setAnswer] = useState('')
  const [contexts, setContexts] = useState([])

  const highlightedIds = useMemo(() => contexts.map((c) => c.chunk_id), [contexts])

  const reloadGraph = async () => {
    const res = await fetchGraph()
    setPoints(res.points)
  }

  useEffect(() => {
    reloadGraph().catch(console.error)
  }, [])

  const handleUpload = async (file) => {
    setUploading(true)
    try {
      await uploadPdf(file)
      await reloadGraph()
    } finally {
      setUploading(false)
    }
  }

  const handleAsk = async (question) => {
    if (!question?.trim()) return
    setThinking(true)
    setAnswer('')
    setContexts([])

    streamAnswer({
      question,
      onContext: (ctx) => setContexts(ctx),
      onToken: (token) => setAnswer((prev) => prev + token),
      onDone: () => setThinking(false),
      onError: (err) => {
        console.error(err)
        setThinking(false)
      },
    })
  }

  const handleVoiceInput = () => {
    const SR = window.SpeechRecognition || window.webkitSpeechRecognition
    if (!SR) {
      alert('Speech Recognition is not supported in this browser')
      return
    }
    const recognition = new SR()
    recognition.lang = 'en-US'
    recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript
      handleAsk(transcript)
    }
    recognition.start()
  }

  return (
    <main className="layout">
      <header className="hero">
        <h1>Neural RAG 3D Studio</h1>
        <button className="ghost" onClick={async () => { await resetIndex(); setAnswer(''); setContexts([]); await reloadGraph(); }}>
          Reset Index
        </button>
      </header>

      <section className="left-col">
        <UploadDropzone onFile={handleUpload} loading={uploading} />
        <ChatPanel
          onAsk={handleAsk}
          answer={answer}
          loading={thinking}
          contexts={contexts}
          onVoiceInput={handleVoiceInput}
        />
      </section>

      <section className="right-col">
        <ThreeGraph points={points} highlightedIds={highlightedIds} />
      </section>
    </main>
  )
}
