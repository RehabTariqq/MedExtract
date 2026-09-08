const API_BASE_URL = "http://127.0.0.1:8000";

export async function apiGet<T>(path: string): Promise<T> {
  const res = await fetch(`${API_BASE_URL}${path}`);
  if (!res.ok) {
    throw new Error(`API error: ${res.status}`);
  }
  return res.json();
}

export async function uploadDocument(file: File): Promise<any> {
  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch(`${API_BASE_URL}/api/v1/documents/upload`, {
    method: "POST",
    body: formData,
  });

  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.error || "Upload failed");
  }
  return res.json();
}

export interface DocumentItem {
  id: string;
  filename: string;
  status: string;
  uploaded_at: string;
}

export async function getDocuments(): Promise<DocumentItem[]> {
  return apiGet<DocumentItem[]>("/api/v1/documents/");
}

export async function getDocument(documentId: string): Promise<DocumentItem> {
  return apiGet<DocumentItem>(`/api/v1/documents/${documentId}`);
}

export interface MedicalTest {
  test_name: string;
  value: string;
  unit: string | null;
  reference_range: string | null;
  status: string;
  category: string | null;
  page_number: number;
  source_text: string;
}

export async function getDocumentTests(documentId: string): Promise<MedicalTest[]> {
  return apiGet<MedicalTest[]>(`/api/v1/documents/${documentId}/tests`);
}

export async function getDocumentSummary(documentId: string): Promise<{ summary: string }> {
  return apiGet<{ summary: string }>(`/api/v1/documents/${documentId}/summary`);
}
export interface QASource {
  document_id: string;
  page_number: number;
  source_text: string;
}

export interface QAResponse {
  answer: string;
  sources: QASource[];
}

export async function askDocumentQuestion(documentId: string, question: string): Promise<QAResponse> {
  const res = await fetch(`${API_BASE_URL}/api/v1/documents/${documentId}/ask`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question }),
  });
  if (!res.ok) {
    throw new Error("Failed to get answer");
  }
  return res.json();
}
export async function askAllDocuments(question: string): Promise<QAResponse> {
  const res = await fetch(`${API_BASE_URL}/api/v1/ask`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question }),
  });
  if (!res.ok) {
    throw new Error("Failed to get answer");
  }
  return res.json();
}
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

export async function getTestHistory(testName: string): Promise<ComparisonResponse> {
  return apiGet<ComparisonResponse>(`/api/v1/tests/${encodeURIComponent(testName)}/history`);
}
export interface SearchResults {
  keyword_results: any[];
  semantic_results: any[];
}

export async function searchAll(query: string): Promise<SearchResults> {
  return apiGet<SearchResults>(`/api/v1/search?q=${encodeURIComponent(query)}`);
}
export async function agentChat(message: string): Promise<{ answer: string }> {
  const res = await fetch(`${API_BASE_URL}/api/v1/agent/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message }),
  });
  if (!res.ok) throw new Error("Agent request failed");
  return res.json();
}