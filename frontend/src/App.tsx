import { useEffect, useState } from "react";
import { apiGet } from "./api/client";

function App() {
  const [status, setStatus] = useState<string>("checking...");

  useEffect(() => {
    apiGet<{ status: string; service: string }>("/health")
      .then((data) => setStatus(data.status))
      .catch(() => setStatus("unreachable"));
  }, []);

  return (
    <div className="min-h-screen bg-[#FAF9F6] text-[#1C2B33]">
      <header className="border-b border-[#E3DFD6] px-8 py-5 flex items-baseline justify-between">
        <h1 className="font-serif-display text-2xl">MedExtract</h1>
        <span className="text-sm text-[#4A7C6E]">Document Intelligence</span>
      </header>

      <main className="max-w-2xl mx-auto px-8 py-16">
        <h2 className="font-serif-display text-4xl leading-tight mb-4">
          Read your medical reports like someone explained them to you.
        </h2>
        <p className="text-[#1C2B33]/70 leading-relaxed mb-8">
          Upload a report, and MedExtract pulls out the values, tracks them over time,
          and answers questions grounded in what your documents actually say.
        </p>
        <button className="bg-[#4A7C6E] text-[#FAF9F6] px-5 py-2.5 rounded-sm hover:bg-[#3d685c] transition-colors">
          Upload a report
        </button>
        <p className="text-xs text-[#1C2B33]/40 mt-8">
          Backend status: {status}
        </p>
      </main>
    </div>
  );
}

export default App;