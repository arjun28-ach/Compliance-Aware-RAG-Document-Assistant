import type { ChatResponse, UploadResponse } from "./types"

const API_BASE =
  process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000"

async function handleResponse<T>(res: Response): Promise<T> {
  if (!res.ok) {
    let message = "Request failed"
    try {
      const data = await res.json()
      message = data?.detail || data?.message || message
    } catch {
      message = await res.text()
    }
    throw new Error(message)
  }

  return res.json() as Promise<T>
}

export async function uploadPDF(file: File): Promise<UploadResponse> {
  const formData = new FormData()
  formData.append("file", file)

  const res = await fetch(`${API_BASE}/upload`, {
    method: "POST",
    body: formData,
  })

  return handleResponse<UploadResponse>(res)
}

export async function askQuestion(
  query: string,
  docId: string
): Promise<ChatResponse> {
  const res = await fetch(`${API_BASE}/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      query,
      doc_id: docId,
    }),
  })

  return handleResponse<ChatResponse>(res)
}