import { useState } from "react";
import { Link } from "react-router-dom";
import { searchAll, type SearchResults } from "../api/client";

function Search() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<SearchResults | null>(null);
  const [loading, setLoading] = useState(false);

  const doSearch = async () => {
    if (!query.trim()) return;
    setLoading(true);
    try {
      setResults(await searchAll(query));
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
        <h2 className="font-serif-display text-3xl mt-4 mb-6">Search your reports</h2>

        <div className="flex gap-2 mb-8">
          <input
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && doSearch()}
            placeholder="Search by test, date, document, or question"
            className="flex-1 border border-[#E3DFD6] rounded-sm px-3 py-2 text-sm focus:outline-none focus:border-[#4A7C6E]"
          />
          <button onClick={doSearch} disabled={loading} className="bg-[#4A7C6E] text-[#FAF9F6] px-4 py-2 rounded-sm text-sm hover:bg-[#3d685c] transition-colors">
            {loading ? "..." : "Search"}
          </button>
        </div>

        {results && (
          <div className="space-y-8">
            <div>
              <h3 className="text-sm uppercase tracking-wide text-[#1C2B33]/50 mb-2">Exact matches</h3>
              {results.keyword_results.length === 0 ? (
                <p className="text-sm text-[#1C2B33]/40">None found.</p>
              ) : (
                results.keyword_results.map((r, i) => (
                  <Link key={i} to={`/documents/${r.document_id}`} className="block py-2 text-sm hover:text-[#4A7C6E]">
                    {r.filename} {r.matched_tests.length > 0 && `— ${r.matched_tests.join(", ")}`}
                  </Link>
                ))
              )}
            </div>
            <div>
              <h3 className="text-sm uppercase tracking-wide text-[#1C2B33]/50 mb-2">Related content</h3>
              {results.semantic_results.length === 0 ? (
                <p className="text-sm text-[#1C2B33]/40">None found.</p>
              ) : (
                results.semantic_results.map((r, i) => (
                  <Link key={i} to={`/documents/${r.document_id}`} className="block py-2 text-sm hover:text-[#4A7C6E]">
                    Page {r.page_number}: "{r.text}..."
                  </Link>
                ))
              )}
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default Search;