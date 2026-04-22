export type SourceItem = {
  text: string
  score?: number
  source?: string
  rerank_score?: number
}

export type ChatResponse = {
  query: string
  answer: string
  sources: SourceItem[]
}

export type UploadResponse = {
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