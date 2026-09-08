import { useState } from "react";
import { Link } from "react-router-dom";
import { agentChat } from "../api/client";

function AgentChat() {
  const [message, setMessage] = useState("");
  const [history, setHistory] = useState<{ role: "user" | "assistant"; text: string }[]>([]);
  const [loading, setLoading] = useState(false);

  const send = async () => {
    if (!message.trim()) return;
    const userMsg = message;
    setHistory((prev) => [...prev, { role: "user", text: userMsg }]);
    setMessage("");
    setLoading(true);
    try {
      const result = await agentChat(userMsg);
      setHistory((prev) => [...prev, { role: "assistant", text: result.answer }]);
    } catch {
      setHistory((prev) => [...prev, { role: "assistant", text: "Something went wrong." }]);
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
        <h2 className="font-serif-display text-3xl mt-4 mb-6">Ask the assistant</h2>

        <div className="space-y-4 mb-6 min-h-[200px]">
          {history.map((m, i) => (
            <div key={i} className={m.role === "user" ? "font-medium" : "text-[#1C2B33]/80"}>
              {m.text}
            </div>
          ))}
        </div>

        <div className="flex gap-2">
          <input
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && send()}
            placeholder="e.g. Compare my last two CBC reports"
            className="flex-1 border border-[#E3DFD6] rounded-sm px-3 py-2 text-sm focus:outline-none focus:border-[#4A7C6E]"
            disabled={loading}
          />
          <button onClick={send} disabled={loading} className="bg-[#4A7C6E] text-[#FAF9F6] px-4 py-2 rounded-sm text-sm hover:bg-[#3d685c] transition-colors">
            {loading ? "..." : "Send"}
          </button>
        </div>
      </main>
    </div>
  );
}

export default AgentChat;