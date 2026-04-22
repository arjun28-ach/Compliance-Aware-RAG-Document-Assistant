export default function Header() {
  return (
    <header className="flex flex-col gap-3 rounded-3xl border border-white/10 bg-white/5 px-5 py-5 shadow-2xl backdrop-blur-xl sm:flex-row sm:items-end sm:justify-between">
      <div>
        <p className="text-xs font-semibold uppercase tracking-[0.22em] text-sky-300">
          Compliance-aware RAG
        </p>
        <h1 className="mt-2 text-3xl font-semibold tracking-tight text-white sm:text-4xl">
          PDF Question Answering Assistant
        </h1>
        <p className="mt-2 max-w-2xl text-sm leading-7 text-justify text-slate-300 sm:text-base">
          Upload a PDF, ask natural-language questions, and get grounded answers
          with supporting source snippets from your document.
        </p>
      </div>

      <div className="rounded-2xl border border-emerald-400/20 bg-emerald-400/10 px-4 py-3 text-sm text-emerald-200">
        Backend connected via FastAPI + Qdrant
      </div>
    </header>
  )
}