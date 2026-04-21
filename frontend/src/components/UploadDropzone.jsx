import { useRef } from 'react'

export default function UploadDropzone({ onFile, loading }) {
  const inputRef = useRef(null)

  const handleFiles = (files) => {
    const file = files?.[0]
    if (file && file.type === 'application/pdf') {
      onFile(file)
    }
  }

  return (
    <div
      className="panel dropzone"
      onDragOver={(e) => e.preventDefault()}
      onDrop={(e) => {
        e.preventDefault()
        handleFiles(e.dataTransfer.files)
      }}
      onClick={() => inputRef.current?.click()}
    >
      <input
        ref={inputRef}
        type="file"
        accept="application/pdf"
        hidden
        onChange={(e) => handleFiles(e.target.files)}
      />
      <h3>Upload PDF</h3>
      <p>Drag & drop or click to select a document.</p>
      {loading && <span className="pill">Indexing...</span>}
    </div>
  )
}
