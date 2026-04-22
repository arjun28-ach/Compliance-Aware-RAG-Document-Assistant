"use client"

import { useEffect, useRef } from "react"
import type { Message } from "@/lib/types"
import MessageBubble from "./MessageBubble"
import Composer from "./Composer"

type Props = {
  messages: Message[]
  isLoading: boolean
  onSend: (message: string) => void
  emptyState: boolean
  disabled?: boolean
  hasUploadedDocument?: boolean
  uploadedFileName?: string
  onStartNewChat?: () => void
  draftQuestion?: string
  onDraftApplied?: () => void
  onSuggestionClick?: (question: string) => void
}

const SUGGESTIONS = [
  "What is this document about?",
  "Summarize the main points",
  "What are the key sections?",
  "What are the main findings?",
  "Give me a short summary",
  "What important details should I know?",
]

export default function ChatPanel({
  messages,
  isLoading,
  onSend,
  emptyState,
  disabled = false,
  hasUploadedDocument = false,
  uploadedFileName = "",
  onStartNewChat,
  draftQuestion = "",
  onDraftApplied,
  onSuggestionClick,
}: Props) {
  const bottomRef = useRef<HTMLDivElement | null>(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [messages, isLoading])

  return (
    <div className="flex h-full min-h-[70vh] flex-col">
      <div className="border-b border-white/10 px-5 py-4">
        <div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
          <div>
            <p className="text-sm font-semibold text-white">Document chat</p>
            <p className="mt-1 text-sm leading-6 text-slate-400">
              Ask questions about the uploaded PDF and review the source snippets used.
            </p>
          </div>

          <button
            type="button"
            onClick={onStartNewChat}
            className="rounded-2xl border border-white/10 bg-white/5 px-4 py-2 text-sm text-slate-200 transition hover:bg-white/10 disabled:cursor-not-allowed disabled:opacity-50"
            disabled={!hasUploadedDocument && messages.length === 0}
          >
            Start new chat
          </button>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto px-4 py-5 sm:px-5">
        {emptyState ? (
          hasUploadedDocument ? (
            <div className="mx-auto flex h-full max-w-2xl flex-col items-center justify-center rounded-3xl border border-white/10 bg-black/15 px-6 py-12 text-center">
              <div className="rounded-full border border-emerald-400/20 bg-emerald-400/10 px-4 py-2 text-sm text-emerald-200">
                Thank you for uploading your PDF
              </div>

              <h2 className="mt-5 text-2xl font-semibold text-white">
                Start asking questions
              </h2>

              <p className="mt-3 max-w-xl break-words text-sm leading-6 text-slate-400">
                Your document{" "}
                <span className="font-medium text-slate-200 break-all">
                  {uploadedFileName || "PDF"}
                </span>{" "}
                is ready.
              </p>

              <div className="mt-6 grid w-full max-w-xl grid-cols-1 gap-3 sm:grid-cols-2">
                {SUGGESTIONS.map((question) => (
                  <button
                    key={question}
                    type="button"
                    onClick={() => onSuggestionClick?.(question)}
                    className="rounded-2xl border border-white/10 bg-white/5 px-4 py-3 text-left text-sm leading-6 text-slate-200 transition hover:bg-white/10"
                  >
                    {question}
                  </button>
                ))}
              </div>

              <p className="mt-4 text-xs leading-5 text-slate-500">
                Click a suggestion to place it in the chat box, then press Send.
              </p>
            </div>
          ) : (
            <div className="mx-auto flex h-full max-w-2xl flex-col items-center justify-center rounded-3xl border border-white/10 bg-black/15 px-6 py-12 text-center">
              <div className="rounded-full border border-sky-400/20 bg-sky-400/10 px-4 py-2 text-sm text-sky-200">
                Ask grounded questions over your PDF
              </div>
              <h2 className="mt-5 text-2xl font-semibold text-white">
                Upload first, then start chatting
              </h2>
              <p className="mt-3 max-w-xl text-sm leading-6 text-slate-400">
                Try questions like “What is this document about?”, “Summarize the
                main points”, or “What date is mentioned in this file?”
              </p>
            </div>
          )
        ) : (
          <div className="mx-auto flex max-w-4xl flex-col gap-4">
            {messages.map((message) => (
              <MessageBubble key={message.id} message={message} />
            ))}

            {isLoading ? (
              <div className="max-w-2xl rounded-3xl border border-white/10 bg-white/5 px-4 py-4 text-sm text-slate-300">
                Thinking…
              </div>
            ) : null}

            <div ref={bottomRef} />
          </div>
        )}
      </div>

      <div className="border-t border-white/10 px-4 py-4 sm:px-5">
        <Composer
          onSend={onSend}
          disabled={disabled || isLoading}
          draftQuestion={draftQuestion}
          onDraftApplied={onDraftApplied}
        />
      </div>
    </div>
  )
}