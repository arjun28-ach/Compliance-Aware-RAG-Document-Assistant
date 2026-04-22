"use client"

import type { SourceItem } from "@/lib/types"

type Props = {
  source: SourceItem
}

function cleanText(text: string) {
  return text.replace(/\s+/g, " ").trim()
}

function extractSourceHeading(text: string) {
  const cleaned = cleanText(text)

  const lines = text
    .split("\n")
    .map((line) => line.trim())
    .filter(Boolean)

  const headingLike =
    lines.find((line) => {
      if (line.length < 4 || line.length > 90) return false

      const upperRatio =
        line.replace(/[^A-Z]/g, "").length / Math.max(line.replace(/[^A-Za-z]/g, "").length, 1)

      return (
        upperRatio > 0.55 ||
        /^[A-Z][A-Za-z0-9\s\-,:/&()]+$/.test(line) ||
        /section|chapter|conclusion|introduction|monitoring|detection|forecasting|analysis|growth/i.test(
          line
        )
      )
    }) || ""

  if (headingLike) return headingLike

  const sentence = cleaned.split(/[.!?]/).map((s) => s.trim()).find(Boolean)
  if (sentence) return sentence.slice(0, 90)

  return cleaned.slice(0, 90)
}

function extractSnippet(text: string) {
  const cleaned = cleanText(text)
  return cleaned.length > 180 ? `${cleaned.slice(0, 180)}…` : cleaned
}

export default function SourceCard({ source }: Props) {
  const heading = extractSourceHeading(source.text || "")
  const snippet = extractSnippet(source.text || "")

  return (
    <div className="rounded-2xl border border-white/10 bg-black/20 p-4">
      <div className="flex flex-wrap items-center gap-2 text-xs text-slate-400">
        <span className="rounded-full border border-white/10 bg-white/5 px-2 py-1">
          {source.source || "Unknown source"}
        </span>

        {typeof source.score === "number" ? (
          <span className="rounded-full border border-emerald-400/20 bg-emerald-400/10 px-2 py-1 text-emerald-300">
            score {source.score.toFixed(3)}
          </span>
        ) : null}

        {typeof source.rerank_score === "number" ? (
          <span className="rounded-full border border-sky-400/20 bg-sky-400/10 px-2 py-1 text-sky-300">
            rerank {source.rerank_score.toFixed(3)}
          </span>
        ) : null}
      </div>

      <div className="mt-3">
        <p className="text-sm font-semibold leading-6 text-slate-100">
          {heading || "Relevant section"}
        </p>

        <p className="mt-2 text-justify text-sm leading-6 text-slate-300">
          {snippet}
        </p>
      </div>
    </div>
  )
}