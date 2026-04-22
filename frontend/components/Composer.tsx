"use client"

import { useEffect, useState } from "react"

type Props = {
  onSend: (message: string) => void
  disabled?: boolean
  draftQuestion?: string
  onDraftApplied?: () => void
}

export default function Composer({
  onSend,
  disabled = false,
  draftQuestion = "",
  onDraftApplied,
}: Props) {
  const [value, setValue] = useState("")

  useEffect(() => {
    if (draftQuestion) {
      setValue(draftQuestion)
      onDraftApplied?.()
    }
  }, [draftQuestion, onDraftApplied])

  function submit() {
    const trimmed = value.trim()
    if (!trimmed || disabled) return
    onSend(trimmed)
    setValue("")
  }

  return (
    <div className="mx-auto flex max-w-4xl items-end gap-3">
      <div className="flex-1 rounded-3xl border border-white/10 bg-black/20 px-4 py-3 shadow-inner">
        <textarea
          value={value}
          onChange={(e) => setValue(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter" && !e.shiftKey) {
              e.preventDefault()
              submit()
            }
          }}
          rows={2}
          placeholder={
            disabled
              ? "Upload a PDF before asking questions…"
              : "Ask a question about your document…"
          }
          className="max-h-40 min-h-[52px] w-full resize-y bg-transparent text-sm leading-6 text-white placeholder:text-slate-500 focus:outline-none"
        />
      </div>

      <button
        type="button"
        onClick={submit}
        disabled={disabled}
        className="rounded-2xl bg-sky-500 px-5 py-3 text-sm font-medium text-white shadow-lg shadow-sky-500/20 transition hover:bg-sky-400 disabled:cursor-not-allowed disabled:bg-slate-600"
      >
        Send
      </button>
    </div>
  )
}