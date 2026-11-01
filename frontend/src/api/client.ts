// Set VITE_API_URL in frontend/.env.local (local) or in your Render build settings (production).
const API_BASE_URL: string =
  import.meta.env.VITE_API_URL ?? "https://medextract-backend-mjjf.onrender.com";

async function errorMessage(res: Response, fallback: string): Promise<string> {
  try {
    const body = await res.json();
    if (typeof body?.error === "string") return body.error;
    if (typeof body?.detail === "string") return body.detail;
  } catch {
    /* response was not JSON */
  }
  return `${fallback} (HTTP ${res.status})`;
}

export async function apiGet<T>(path: string): Promise<T> {
  const res = await fetch(`${API_BASE_URL}${path}`);
  if (!res.ok) throw new Error(await errorMessage(res, "Request failed"));
  return res.json();
}

async function apiPost<T>(path: string, body?: unknown): Promise<T> {
  const res = await fetch(`${API_BASE_URL}${path}`, {
    method: "POST",
    headers: body ? { "Content-Type": "application/json" } : undefined,
    body: body ? JSON.stringify(body) : undefined,
  });
  if (!res.ok) throw new Error(await errorMessage(res, "Request failed"));
  return res.json();
}

/* ---------- documents ---------- */

export interface DocumentItem {
  id: string;
  filename: string;
  status: "uploaded" | "processing" | "processed" | "failed" | string;
  uploaded_at: string;
  error?: string | null;
}

export async function uploadDocument(file: File): Promise<DocumentItem> {
  const formData = new FormData();
  formData.append("file", file);
  const res = await fetch(`${API_BASE_URL}/api/v1/documents/upload`, {
    method: "POST",
    body: formData,
  });
  if (!res.ok) throw new Error(await errorMessage(res, "Upload failed"));
  return res.json();
}

export const getDocuments = () => apiGet<DocumentItem[]>("/api/v1/documents/");
export const getDocument = (id: string) => apiGet<DocumentItem>(`/api/v1/documents/${id}`);
export const reprocessDocument = (id: string) =>
  apiPost<DocumentItem>(`/api/v1/documents/${id}/reprocess`);

export interface MedicalTest {
  test_name: string;
  value: string;
  unit: string | null;
  reference_range: string | null;
  status: string;
  category: string | null;
  page_number: number | null;
  source_text: string;
}

export const getDocumentTests = (id: string) =>
  apiGet<MedicalTest[]>(`/api/v1/documents/${id}/tests`);
export const getDocumentSummary = (id: string) =>
  apiGet<{ summary: string }>(`/api/v1/documents/${id}/summary`);

/* ---------- Q&A ---------- */

export interface QASource {
  document_id: string;
  page_number: number;
  source_text: string;
}

export interface QAResponse {
  answer: string;
  sources: QASource[];
}

export const askDocumentQuestion = (documentId: string, question: string) =>
  apiPost<QAResponse>(`/api/v1/documents/${documentId}/ask`, { question });
export const askAllDocuments = (question: string) =>
  apiPost<QAResponse>("/api/v1/ask", { question });

/* ---------- test history ---------- */

export interface TestHistoryItem {
  document_id: string;
  filename: string;
  uploaded_at: string;
  value: string;
  unit: string | null;
  reference_range: string | null;
  status: string;
}

export interface ComparisonResponse {
  test_name: string;
  history: TestHistoryItem[];
  comparisons: { from: TestHistoryItem; to: TestHistoryItem; difference: number | null }[];
}

export const getTestHistory = (testName: string) =>
  apiGet<ComparisonResponse>(`/api/v1/tests/${encodeURIComponent(testName)}/history`);

/* ---------- search ---------- */

export interface SearchResults {
  keyword_results: any[];
  semantic_results: any[];
}

export const searchAll = (query: string) =>
  apiGet<SearchResults>(`/api/v1/search?q=${encodeURIComponent(query)}`);

/* ---------- agent ---------- */

function getSessionId(): string {
  try {
    let id = localStorage.getItem("medextract_session");
    if (!id) {
      id = crypto.randomUUID();
      localStorage.setItem("medextract_session", id);
    }
    return id;
  } catch {
    return "default";
  }
}

export const agentChat = (message: string) =>
  apiPost<{ answer: string }>("/api/v1/agent/chat", { message, session_id: getSessionId() });
