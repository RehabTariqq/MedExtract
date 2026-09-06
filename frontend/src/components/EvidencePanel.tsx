import type { QASource } from "../api/client";

function EvidencePanel({ sources }: { sources: QASource[] }) {
  if (sources.length === 0) return null;

  return (
    <div className="mt-3 space-y-2">
      <p className="text-xs uppercase tracking-wide text-[#1C2B33]/40">Evidence</p>
      {sources.map((s, i) => (
        <div
          key={i}
          className="border-l-2 border-[#4A7C6E]/40 pl-3 py-1 text-xs text-[#1C2B33]/70"
        >
          <span className="text-[#4A7C6E] font-medium">Page {s.page_number}</span>
          <span className="mx-1">&middot;</span>
          <span className="italic">"{s.source_text.slice(0, 140)}{s.source_text.length > 140 ? "..." : ""}"</span>
        </div>
      ))}
    </div>
  );
}

export default EvidencePanel;