import { useState } from "react";
import { Link } from "react-router-dom";
import { askAllDocuments, type QAResponse } from "../api/client";
import EvidencePanel from "../components/EvidencePanel";

function AskAllReports() {
  const [question, setQuestion] = useState("");
  const [history, setHistory] = useState<{ question: string; result: QAResponse }[]>([]);
  const [loading, setLoading] = useState(false);

  const handleAsk = async () => {
    if (!question.trim()) return;
    setLoading(true);
    try {
      const result = await askAllDocuments(question);
      setHistory((prev) => [...prev, { question, result }]);
      setQuestion("");
    } catch {
      setHistory((prev) => [
        ...prev,
        { question, result: { answer: "Something went wrong. Please try again.", sources: [] } },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#FAF9F6] text-[#1C2B33]">
      <header className="border-b border-[#E3DFD6] px-8 py-5 flex items-center justify-between">
        <Link to="/" className="font-serif-display text-2xl">MedExtract</Link>
        <span className="text-sm text-[#4A7C6E]">Document Intelligence</span>
      </header>

      <main className="max-w-2xl mx-auto px-8 py-12">
        <Link to="/" className="text-sm text-[#4A7C6E] hover:underline">&larr; Back to reports</Link>

        <h2 className="font-serif-display text-3xl mt-4 mb-2">Ask across all your reports</h2>
        <p className="text-sm text-[#1C2B33]/60 mb-8">
          Questions here search every report you've uploaded, not just one.
        </p>

        <div className="space-y-6 mb-6">
          {history.map((entry, i) => (
            <div key={i}>
              <p className="text-sm font-medium mb-1">{entry.question}</p>
              <p className="text-sm text-[#1C2B33]/80 leading-relaxed">{entry.result.answer}</p>
              <EvidencePanel sources={entry.result.sources} />
            </div>
          ))}
        </div>

        <div className="flex gap-2">
          <input
            type="text"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleAsk()}
            placeholder="e.g. Which report had the highest glucose?"
            className="flex-1 border border-[#E3DFD6] rounded-sm px-3 py-2 text-sm focus:outline-none focus:border-[#4A7C6E]"
            disabled={loading}
          />
          <button
            onClick={handleAsk}
            disabled={loading}
            className="bg-[#4A7C6E] text-[#FAF9F6] px-4 py-2 rounded-sm text-sm hover:bg-[#3d685c] transition-colors disabled:opacity-50"
          >
            {loading ? "Thinking..." : "Ask"}
          </button>
        </div>
      </main>
    </div>
  );
}

export default AskAllReports;