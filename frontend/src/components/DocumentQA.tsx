import { useState } from "react";
import { askDocumentQuestion, type QAResponse } from "../api/client";

function DocumentQA({ documentId }: { documentId: string }) {
  const [question, setQuestion] = useState("");
  const [history, setHistory] = useState<{ question: string; result: QAResponse }[]>([]);
  const [loading, setLoading] = useState(false);

  const handleAsk = async () => {
    if (!question.trim()) return;
    setLoading(true);
    try {
      const result = await askDocumentQuestion(documentId, question);
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
    <div className="mt-10 border-t border-[#E3DFD6] pt-8">
      <h3 className="text-sm uppercase tracking-wide text-[#1C2B33]/50 mb-4">
        Ask about this report
      </h3>

      <div className="space-y-6 mb-6">
        {history.map((entry, i) => (
          <div key={i}>
            <p className="text-sm font-medium mb-1">{entry.question}</p>
            <p className="text-sm text-[#1C2B33]/80 leading-relaxed">{entry.result.answer}</p>
            {entry.result.sources.length > 0 && (
              <div className="mt-2 space-y-1">
                {entry.result.sources.map((s, j) => (
                  <p key={j} className="text-xs text-[#4A7C6E]">
                    Source: Page {s.page_number} &mdash; "{s.source_text.slice(0, 100)}..."
                  </p>
                ))}
              </div>
            )}
          </div>
        ))}
      </div>

      <div className="flex gap-2">
        <input
          type="text"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleAsk()}
          placeholder="e.g. What was my hemoglobin level?"
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
    </div>
  );
}

export default DocumentQA;