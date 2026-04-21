import { useEffect, useRef, useState } from 'react'

export default function ChatPanel({ onAsk, answer, loading, contexts, onVoiceInput }) {
  const [question, setQuestion] = useState('')
  const [displayAnswer, setDisplayAnswer] = useState('')
  const iRef = useRef(0)

  useEffect(() => {
    if (!answer) {
      setDisplayAnswer('')
      iRef.current = 0
      return
    }

    const t = setInterval(() => {
      iRef.current += 2
      setDisplayAnswer(answer.slice(0, iRef.current))
      if (iRef.current >= answer.length) clearInterval(t)
    }, 12)

    return () => clearInterval(t)
  }, [answer])

  return (
    <div className="panel chat-panel">
      <h3>Ask your document</h3>
      <div className="row">
        <input
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Ask anything from uploaded PDFs..."
          onKeyDown={(e) => e.key === 'Enter' && onAsk(question)}
        />
        <button onClick={() => onAsk(question)} disabled={loading || !question.trim()}>
          Ask
        </button>
        <button className="ghost" onClick={onVoiceInput}>🎙️</button>
      </div>
      {loading && <div className="thinking">AI is thinking<span>.</span><span>.</span><span>.</span></div>}
      <pre className="answer">{displayAnswer}</pre>

      <h4>Retrieved Chunks</h4>
      <div className="chunk-list">
        {contexts.map((c) => (
          <article key={c.chunk_id} className="chunk-item">
            <strong>{c.chunk_id}</strong>
            <small>score: {c.score.toFixed(3)}</small>
            <p>{c.text}</p>
          </article>
        ))}
      </div>
    </div>
  )
}
