"use client"

import type { Message } from "@/lib/types"
import SourceCard from "./SourceCard"

type Props = {
  message: Message
}

export default function MessageBubble({ message }: Props) {
  const isUser = message.role === "user"

  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"}`}>
      <div
        className={`w-full max-w-3xl rounded-3xl border px-4 py-4 shadow-xl ${
          isUser
            ? "border-sky-400/20 bg-sky-500/15 text-sky-50"
            : "border-white/10 bg-white/5 text-slate-100"
        }`}
      >
        <div className="mb-2 flex items-center justify-between gap-3">
          <span className="text-xs font-semibold uppercase tracking-[0.16em] text-slate-400">
            {isUser ? "You" : "Assistant"}
          </span>
          <span className="text-xs text-slate-500">
            {new Date(message.createdAt).toLocaleTimeString([], {
              hour: "2-digit",
              minute: "2-digit",
            })}
          </span>
        </div>

        <div
          className={`whitespace-pre-wrap text-sm leading-7 ${
            isUser ? "" : "text-justify"
          }`}
        >
          {message.text}
        </div>

        {!isUser && message.sources?.length ? (
          <div className="mt-4 space-y-3">
            <p className="text-xs font-semibold uppercase tracking-[0.16em] text-slate-400">
              Sources
            </p>

            <div className="grid gap-3">
              {message.sources.map((source, index) => (
                <SourceCard key={`${message.id}-source-${index}`} source={source} />
              ))}
            </div>
          </div>
        ) : null}
      </div>
    </div>
  )
}