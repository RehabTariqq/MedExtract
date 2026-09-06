import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { uploadDocument, getDocuments, type DocumentItem } from "./api/client";

const NOTES = [
  "Reference ranges vary by lab — always compare your result to the range printed on that specific report.",
  "A single out-of-range value often means less than a trend across several reports.",
  "Hemoglobin, glucose, and lipid panels are among the most commonly tracked values over time.",
  "Units matter: the same test can be reported in different units depending on the lab.",
];

function App() {
  const [documents, setDocuments] = useState<DocumentItem[]>([]);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [dragOver, setDragOver] = useState(false);
  const [noteIndex, setNoteIndex] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setNoteIndex((i) => (i + 1) % NOTES.length);
    }, 6000);
    return () => clearInterval(interval);
  }, []);

  const loadDocuments = async () => {
    try {
      const docs = await getDocuments();
      setDocuments(docs);
    } catch {
      setError("Could not load documents");
    }
  };

  useEffect(() => {
    loadDocuments();
  }, []);

  const doUpload = async (file: File) => {
    setUploading(true);
    setError(null);
    try {
      await uploadDocument(file);
      await loadDocuments();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Upload failed");
    } finally {
      setUploading(false);
    }
  };

  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) await doUpload(file);
    e.target.value = "";
  };

  const handleDrop = async (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setDragOver(false);
    const file = e.dataTransfer.files?.[0];
    if (file) await doUpload(file);
  };

  return (
    <div className="min-h-screen bg-[#FAF9F6] text-[#1C2B33]">
      <header className="border-b border-[#E3DFD6] px-8 py-5 flex items-baseline justify-between">
        <div className="flex items-center gap-2">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#4A7C6E" strokeWidth="1.6">
            <path d="M4 4h16v16H4z" strokeLinejoin="round" />
            <path d="M8 9h8M8 13h5" strokeLinecap="round" />
            <circle cx="16" cy="16" r="2.4" />
          </svg>
          <h1 className="font-serif-display text-2xl">MedExtract</h1>
        </div>
        <span className="text-sm text-[#4A7C6E]">Document Intelligence</span>
      </header>

      <main className="max-w-2xl mx-auto px-8 py-16">
        <h2 className="font-serif-display text-4xl leading-tight mb-4">
          Read your medical reports like someone explained them to you.
        </h2>
        <p className="text-[#1C2B33]/70 leading-relaxed mb-10">
          Upload a report, and MedExtract pulls out the values, tracks them over time,
          and answers questions grounded in what your documents actually say.
        </p>

        <div
          onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
          onDragLeave={() => setDragOver(false)}
          onDrop={handleDrop}
          className={`relative border rounded-sm px-6 py-10 text-center transition-all duration-200 ${
            dragOver
              ? "border-[#4A7C6E] bg-[#4A7C6E]/5 scale-[1.01]"
              : "border-dashed border-[#E3DFD6]"
          }`}
        >
          <svg
            className={`mx-auto mb-3 transition-transform duration-300 ${dragOver ? "-translate-y-1" : ""}`}
            width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="#4A7C6E" strokeWidth="1.5"
          >
            <path d="M12 3v12" strokeLinecap="round" />
            <path d="M7 8l5-5 5 5" strokeLinecap="round" strokeLinejoin="round" />
            <path d="M4 17v2a2 2 0 002 2h12a2 2 0 002-2v-2" strokeLinecap="round" />
          </svg>
          <p className="text-sm text-[#1C2B33]/60 mb-4">
            Drag a PDF report here, or
          </p>
          <label className="inline-block bg-[#4A7C6E] text-[#FAF9F6] px-5 py-2.5 rounded-sm hover:bg-[#3d685c] transition-colors cursor-pointer text-sm">
            {uploading ? "Uploading..." : "Choose a file"}
            <input
              type="file"
              accept="application/pdf"
              className="hidden"
              onChange={handleFileChange}
              disabled={uploading}
            />
          </label>
        </div>

        {error && <p className="text-[#C77D3C] text-sm mt-3">{error}</p>}

        <div className="mt-6 text-xs text-[#1C2B33]/50 leading-relaxed border-l-2 border-[#E3DFD6] pl-3 min-h-[2.5rem] transition-opacity duration-500">
          {NOTES[noteIndex]}
        </div>

        <div className="mt-12">
          <h3 className="text-sm uppercase tracking-wide text-[#1C2B33]/50 mb-3">
            Your reports
          </h3>
          {documents.length === 0 ? (
            <p className="text-[#1C2B33]/50 text-sm">No reports uploaded yet.</p>
          ) : (
            <ul className="divide-y divide-[#E3DFD6]">
              {documents.map((doc) => (
                <Link to={`/documents/${doc.id}`} key={doc.id}>
                  <li className="py-3 flex items-center justify-between hover:bg-[#4A7C6E]/5 px-2 -mx-2 rounded-sm transition-colors cursor-pointer">
                    <span className="flex items-center gap-2">
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#1C2B33" strokeOpacity="0.4" strokeWidth="1.6">
                        <path d="M6 3h9l4 4v14a1 1 0 01-1 1H6a1 1 0 01-1-1V4a1 1 0 011-1z" />
                        <path d="M15 3v4h4" />
                      </svg>
                      {doc.filename}
                    </span>
                    <span
                      className={`text-xs px-2 py-0.5 rounded-sm ${
                        doc.status === "processed"
                          ? "text-[#4A7C6E] bg-[#4A7C6E]/10"
                          : "text-[#C77D3C] bg-[#C77D3C]/10"
                      }`}
                    >
                      {doc.status}
                    </span>
                  </li>
                </Link>
              ))}
            </ul>
          )}
        </div>
      </main>
    </div>
  );
}

export default App;