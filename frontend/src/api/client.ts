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