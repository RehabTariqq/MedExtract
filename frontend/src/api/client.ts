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