"use client"

import { useRef, useState } from "react"
import { uploadPDF } from "@/lib/api"
import type { UploadResponse } from "@/lib/types"

type Props = {
  uploadedFileName: string
  chunksCount: number | null
  onUploaded: (data: UploadResponse) => void
  onError: (message: string) => void
}

export default function UploadPanel({
  uploadedFileName,
  chunksCount,
  onUploaded,
  onError,
}: Props) {
  const inputRef = useRef<HTMLInputElement | null>(null)
  const [dragging, setDragging] = useState(false)
  const [uploading, setUploading] = useState(false)

  async function handleFile(file?: File) {
    if (!file) return

    if (file.type !== "application/pdf") {
      onError("Please upload a PDF file.")
      return
    }

    setUploading(true)
    onError("")

    try {
      const data = await uploadPDF(file)
      onUploaded(data)
    } catch (err) {
      const message = err instanceof Error ? err.message : "Upload failed."
      onError(message)
    } finally {
      setUploading(false)
    }
  }

  return (
    <div>
      <p className="text-xs font-semibold uppercase tracking-[0.18em] text-slate-400">
        Upload document
      </p>

      <button
        type="button"
        onClick={() => inputRef.current?.click()}
        onDragOver={(e) => {
          e.preventDefault()
          setDragging(true)
        }}
        onDragLeave={() => setDragging(false)}
        onDrop={(e) => {
          e.preventDefault()
          setDragging(false)
          const file = e.dataTransfer.files?.[0]
          void handleFile(file)
        }}
        className={`mt-3 flex w-full flex-col items-center justify-center rounded-3xl border border-dashed px-4 py-10 text-center transition ${
          dragging
            ? "border-sky-400 bg-sky-400/10"
            : "border-white/15 bg-white/5 hover:border-sky-400/40 hover:bg-white/10"
        }`}
      >
        <div className="rounded-2xl bg-sky-400/10 px-3 py-2 text-sm text-sky-200">
          {uploading ? "Uploading PDF..." : "Drop PDF here or click to upload"}
        </div>

        <p className="mt-3 text-sm leading-6 text-slate-300">
          One PDF at a time. The backend will extract, chunk, embed, and index it.
        </p>

        <p className="mt-2 text-xs text-slate-500">Supported format: .pdf</p>
      </button>

      <input
        ref={inputRef}
        type="file"
        accept="application/pdf"
        className="hidden"
        onChange={(e) => {
          const file = e.target.files?.[0]
          void handleFile(file)
        }}
      />

      <div className="mt-4 rounded-2xl border border-white/10 bg-black/20 p-4">
        <p className="text-sm font-medium text-slate-100">Latest upload</p>

        <p className="mt-2 break-words text-sm leading-6 text-slate-300">
          {uploadedFileName || "No file uploaded"}
        </p>

        <p className="mt-1 text-xs text-slate-500">
          {chunksCount !== null ? `${chunksCount} chunks indexed` : "No indexing yet"}
        </p>
      </div>
    </div>
  )
}