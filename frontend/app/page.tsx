"use client"

import { useMemo, useState } from "react"
import Header from "@/components/Header"
import UploadPanel from "@/components/UploadPanel"
import ChatPanel from "@/components/ChatPanel"
import type { Message, SourceItem } from "@/lib/types"
import { askQuestion } from "@/lib/api"

function createId() {
  return `${Date.now()}-${Math.random().toString(36).slice(2, 9)}`
}

export default function HomePage() {
  const [docId, setDocId] = useState<string>("")
  const [uploadedFileName, setUploadedFileName] = useState<string>("")
  const [chunksCount, setChunksCount] = useState<number | null>(null)
  const [messages, setMessages] = useState<Message[]>([])
  const [isAsking, setIsAsking] = useState(false)
  const [error, setError] = useState<string>("")
  const [draftQuestion, setDraftQuestion] = useState("")

  const hasUploadedDocument = Boolean(docId)
  const emptyState = useMemo(() => messages.length === 0, [messages.length])

  async function handleAsk(question: string) {
    const trimmed = question.trim()

    if (!trimmed || isAsking) return

    if (!docId) {
      setError("Please upload a document first.")
      return
    }

    setError("")

    const userMessage: Message = {
      id: createId(),
      role: "user",
      text: trimmed,
      createdAt: new Date().toISOString(),
    }

    setMessages((prev) => [...prev, userMessage])
    setIsAsking(true)

    try {
      const res = await askQuestion(trimmed, docId)

      const assistantMessage: Message = {
        id: createId(),
        role: "assistant",
        text: res.answer,
        sources: res.sources as SourceItem[],
        createdAt: new Date().toISOString(),
      }

      setMessages((prev) => [...prev, assistantMessage])
    } catch (err) {
      const message =
        err instanceof Error ? err.message : "Something went wrong."

      setError(message)

      const assistantMessage: Message = {
        id: createId(),
        role: "assistant",
        text: `I couldn’t complete that request.\n\n${message}`,
        createdAt: new Date().toISOString(),
      }

      setMessages((prev) => [...prev, assistantMessage])
    } finally {
      setIsAsking(false)
    }
  }

  function handleStartNewChat() {
    setDocId("")
    setUploadedFileName("")
    setChunksCount(null)
    setMessages([])
    setError("")
    setIsAsking(false)
    setDraftQuestion("")
  }

  return (
    <main className="min-h-screen bg-[radial-gradient(circle_at_top,_#1e293b_0%,_#0f172a_35%,_#020617_100%)] text-slate-100">
      <div className="mx-auto flex min-h-screen max-w-7xl flex-col px-4 py-6 sm:px-6 lg:px-8">
        <Header />

        <div className="mt-6 grid flex-1 grid-cols-1 gap-6 lg:grid-cols-[360px_minmax(0,1fr)]">
          <aside className="rounded-3xl border border-white/10 bg-white/5 p-4 shadow-2xl backdrop-blur-xl">
            <UploadPanel
              uploadedFileName={uploadedFileName}
              chunksCount={chunksCount}
              onUploaded={(data) => {
                setDocId(data.doc_id)
                setUploadedFileName(data.filename)
                setChunksCount(data.chunks)
                setMessages([])
                setDraftQuestion("")
                setError("")
              }}
              onError={(message) => setError(message)}
            />

            <div className="mt-6 rounded-2xl border border-white/10 bg-black/20 p-4">
              <p className="text-xs font-semibold uppercase tracking-[0.18em] text-slate-400">
                Session
              </p>

              <div className="mt-3 space-y-3">
                <div className="rounded-2xl border border-white/10 bg-white/5 p-3">
                  <p className="text-xs text-slate-400">Document</p>
                  <p className="mt-1 break-words text-sm font-medium leading-6 text-slate-100">
                    {uploadedFileName || "No file uploaded yet"}
                  </p>
                </div>

                <div className="rounded-2xl border border-white/10 bg-white/5 p-3">
                  <p className="text-xs text-slate-400">Indexed chunks</p>
                  <p className="mt-1 text-sm font-medium text-slate-100">
                    {chunksCount ?? "—"}
                  </p>
                </div>

                <div className="rounded-2xl border border-white/10 bg-white/5 p-3">
                  <p className="text-xs text-slate-400">Status</p>
                  <p className="mt-1 text-sm font-medium text-emerald-300">
                    {docId ? "Ready for questions" : "Upload a PDF first"}
                  </p>
                </div>
              </div>

              {error ? (
                <div className="mt-4 rounded-2xl border border-rose-400/20 bg-rose-400/10 p-3 text-sm text-rose-200">
                  {error}
                </div>
              ) : null}
            </div>
          </aside>

          <section className="min-h-[70vh] rounded-3xl border border-white/10 bg-white/5 shadow-2xl backdrop-blur-xl">
            <ChatPanel
              messages={messages}
              isLoading={isAsking}
              onSend={handleAsk}
              emptyState={emptyState}
              disabled={!hasUploadedDocument}
              hasUploadedDocument={hasUploadedDocument}
              uploadedFileName={uploadedFileName}
              onStartNewChat={handleStartNewChat}
              draftQuestion={draftQuestion}
              onDraftApplied={() => setDraftQuestion("")}
              onSuggestionClick={(question) => setDraftQuestion(question)}
            />
          </section>
        </div>
      </div>
    </main>
  )
}