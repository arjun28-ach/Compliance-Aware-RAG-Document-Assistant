export type SourceItem = {
  text: string
  score?: number
  source?: string
  rerank_score?: number
}

export type ChatResponse = {
  doc_id?: string
  query: string
  answer: string
  sources: SourceItem[]
}

export type UploadResponse = {
  doc_id: string
  filename: string
  chunks: number
  status: string
}

export type Message = {
  id: string
  role: "user" | "assistant"
  text: string
  sources?: SourceItem[]
  createdAt: string
}
