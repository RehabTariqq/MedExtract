import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import "./index.css";
import App from "./App.tsx";
import DocumentDetail from "./pages/DocumentDetail.tsx";
import AskAllReports from "./pages/AskAllReports.tsx";
import TestHistory from "./pages/TestHistory.tsx";
import Search from "./pages/Search.tsx";
import AgentChat from "./pages/AgentChat.tsx";

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<App />} />
        <Route path="/documents/:id" element={<DocumentDetail />} />
        <Route path="/ask" element={<AskAllReports />} />
        <Route path="/tests/history" element={<TestHistory />} />
        <Route path="/search" element={<Search />} />
        <Route path="/agent" element={<AgentChat />} />
      </Routes>
    </BrowserRouter>
  </StrictMode>,
);
