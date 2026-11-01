# MedExtract

An AI-powered medical document intelligence system. Upload medical reports (PDF), extract structured test data, and ask grounded questions about your results using RAG and an AI agent.

This project is being built on Ubuntu Linux, using Python, FastAPI, MongoDB, React, and modern AI/RAG tooling.

## Status
In active development, following a structured build roadmap.




## Development Environment
- OS: Ubuntu Linux (24.04)
- Backend: Python, FastAPI, MongoDB
- Frontend: React, TypeScript, Vite, Tailwind CSS
- AI: LLM (OpenAI/Gemini), RAG, Qdrant vector database, LangGraph agents
- DevOps: Docker, Docker Compose

## Disclaimer
MedExtract is an informational document-analysis tool. It does not diagnose conditions, recommend treatment, or replace professional medical advice.

## Running locally (Docker)

1. Copy the env template and fill in your keys:
   - `GROQ_API_KEY` from https://console.groq.com
   - `COHERE_API_KEY` from https://dashboard.cohere.com
   - `JWT_SECRET_KEY`: any long random text
2. Start everything:
3. Open http://localhost:5173 and upload a PDF lab report.

Uploads are processed in the background. The report page shows `processing`, then `processed`, or `failed` with the reason and a "Try again" button.
