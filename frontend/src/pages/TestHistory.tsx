import { useState } from "react";
import { Link } from "react-router-dom";
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";
import { getTestHistory, type ComparisonResponse } from "../api/client";

function TestHistory() {
  const [testName, setTestName] = useState("");
  const [data, setData] = useState<ComparisonResponse | null>(null);
  const [loading, setLoading] = useState(false);

  const search = async () => {
    if (!testName.trim()) return;
    setLoading(true);
    try {
      const result = await getTestHistory(testName);
      setData(result);
    } finally {
      setLoading(false);
    }
  };

  const chartData = data?.history
    .map((h) => ({
      date: new Date(h.uploaded_at).toLocaleDateString(),
      value: parseFloat(h.value),
    }))
    .filter((d) => !isNaN(d.value));

  return (
    <div className="min-h-screen bg-[#FAF9F6] text-[#1C2B33]">
      <header className="border-b border-[#E3DFD6] px-8 py-5 flex items-center justify-between">
        <Link to="/" className="font-serif-display text-2xl">MedExtract</Link>
        <span className="text-sm text-[#4A7C6E]">Document Intelligence</span>
      </header>

      <main className="max-w-2xl mx-auto px-8 py-12">
        <Link to="/" className="text-sm text-[#4A7C6E] hover:underline">&larr; Back to reports</Link>
        <h2 className="font-serif-display text-3xl mt-4 mb-6">Track a test over time</h2>

        <div className="flex gap-2 mb-8">
          <input
            value={testName}
            onChange={(e) => setTestName(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && search()}
            placeholder="e.g. Hemoglobin"
            className="flex-1 border border-[#E3DFD6] rounded-sm px-3 py-2 text-sm focus:outline-none focus:border-[#4A7C6E]"
          />
          <button
            onClick={search}
            disabled={loading}
            className="bg-[#4A7C6E] text-[#FAF9F6] px-4 py-2 rounded-sm text-sm hover:bg-[#3d685c] transition-colors"
          >
            {loading ? "Searching..." : "Search"}
          </button>
        </div>

        {data && data.history.length === 0 && (
          <p className="text-sm text-[#1C2B33]/50">No history found for "{data.test_name}".</p>
        )}

        {data && data.history.length > 0 && (
          <>
            {chartData && chartData.length > 1 && (
              <div className="mb-8 h-56">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={chartData}>
                    <XAxis dataKey="date" stroke="#1C2B33" fontSize={11} />
                    <YAxis stroke="#1C2B33" fontSize={11} />
                    <Tooltip />
                    <Line type="monotone" dataKey="value" stroke="#4A7C6E" strokeWidth={2} dot={{ r: 3 }} />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            )}

            <table className="w-full text-sm border-collapse">
              <thead>
                <tr className="border-b border-[#E3DFD6] text-left text-[#1C2B33]/50">
                  <th className="py-2 pr-4 font-normal">Date</th>
                  <th className="py-2 pr-4 font-normal">Value</th>
                  <th className="py-2 pr-4 font-normal">Range</th>
                  <th className="py-2 pr-4 font-normal">Report</th>
                </tr>
              </thead>
              <tbody>
                {data.history.map((h, i) => (
                  <tr key={i} className="border-b border-[#E3DFD6]/60">
                    <td className="py-3 pr-4">{new Date(h.uploaded_at).toLocaleDateString()}</td>
                    <td className="py-3 pr-4">{h.value} {h.unit || ""}</td>
                    <td className="py-3 pr-4 text-[#1C2B33]/60">{h.reference_range || "—"}</td>
                    <td className="py-3 pr-4">
                      <Link to={`/documents/${h.document_id}`} className="text-[#4A7C6E] hover:underline">
                        {h.filename}
                      </Link>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </>
        )}
      </main>
    </div>
  );
}

export default TestHistory;