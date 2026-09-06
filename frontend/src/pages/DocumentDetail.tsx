import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import {
  getDocument,
  getDocumentTests,
  getDocumentSummary,
  type DocumentItem,
  type MedicalTest,
} from "../api/client";

const statusStyles: Record<string, string> = {
  normal: "text-[#4A7C6E] bg-[#4A7C6E]/10",
  high: "text-[#C77D3C] bg-[#C77D3C]/10",
  low: "text-[#C77D3C] bg-[#C77D3C]/10",
  unclear: "text-[#1C2B33]/50 bg-[#1C2B33]/5",
};

function DocumentDetail() {
  const { id } = useParams<{ id: string }>();
  const [document, setDocument] = useState<DocumentItem | null>(null);
  const [tests, setTests] = useState<MedicalTest[]>([]);
  const [summary, setSummary] = useState<string>("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!id) return;
    Promise.all([getDocument(id), getDocumentTests(id), getDocumentSummary(id)])
      .then(([doc, testResults, summaryResult]) => {
        setDocument(doc);
        setTests(testResults);
        setSummary(summaryResult.summary);
      })
      .finally(() => setLoading(false));
  }, [id]);

  if (loading) {
    return <div className="max-w-3xl mx-auto px-8 py-16 text-[#1C2B33]/50">Loading...</div>;
  }

  return (
    <div className="min-h-screen bg-[#FAF9F6] text-[#1C2B33]">
      <header className="border-b border-[#E3DFD6] px-8 py-5 flex items-center justify-between">
        <Link to="/" className="font-serif-display text-2xl">MedExtract</Link>
        <span className="text-sm text-[#4A7C6E]">Document Intelligence</span>
      </header>

      <main className="max-w-3xl mx-auto px-8 py-12">
        <Link to="/" className="text-sm text-[#4A7C6E] hover:underline">&larr; Back to reports</Link>

        <h2 className="font-serif-display text-3xl mt-4 mb-1">{document?.filename}</h2>
        <p className="text-sm text-[#1C2B33]/50 mb-8">
          Status: {document?.status} &middot; {tests.length} test{tests.length !== 1 ? "s" : ""} found
        </p>

        {summary && (
          <div className="mb-10 bg-[#4A7C6E]/5 border border-[#4A7C6E]/20 rounded-sm p-5">
            <p className="text-xs uppercase tracking-wide text-[#4A7C6E] mb-2">AI Summary</p>
            <pre className="whitespace-pre-wrap font-sans text-sm text-[#1C2B33]/80 leading-relaxed">
              {summary}
            </pre>
            <p className="text-xs text-[#1C2B33]/40 mt-4 pt-3 border-t border-[#4A7C6E]/10">
              This is an informational summary, not medical advice. Always discuss results with a healthcare professional.
            </p>
          </div>
        )}

        {tests.length === 0 ? (
          <p className="text-[#1C2B33]/50 text-sm">
            No structured test data was extracted from this document.
          </p>
        ) : (
          <table className="w-full text-sm border-collapse">
            <thead>
              <tr className="border-b border-[#E3DFD6] text-left text-[#1C2B33]/50">
                <th className="py-2 pr-4 font-normal">Test</th>
                <th className="py-2 pr-4 font-normal">Value</th>
                <th className="py-2 pr-4 font-normal">Range</th>
                <th className="py-2 pr-4 font-normal">Status</th>
                <th className="py-2 pr-4 font-normal">Page</th>
              </tr>
            </thead>
            <tbody>
              {tests.map((test, i) => (
                <tr key={i} className="border-b border-[#E3DFD6]/60">
                  <td className="py-3 pr-4">{test.test_name}</td>
                  <td className="py-3 pr-4">
                    {test.value} {test.unit || ""}
                  </td>
                  <td className="py-3 pr-4 text-[#1C2B33]/60">
                    {test.reference_range || "—"}
                  </td>
                  <td className="py-3 pr-4">
                    <span className={`text-xs px-2 py-0.5 rounded-sm ${statusStyles[test.status] || statusStyles.unclear}`}>
                      {test.status}
                    </span>
                  </td>
                  <td className="py-3 pr-4 text-[#1C2B33]/40">{test.page_number}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </main>
    </div>
  );
}

export default DocumentDetail;