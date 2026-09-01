"use client";

import { useState, useEffect, useCallback } from "react";

interface HealthResponse {
  status: string;
  service: string;
}

export default function Home() {
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [lastChecked, setLastChecked] = useState<string>("");

  const apiUrl =
    process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

  const checkHealth = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`${apiUrl}/health`, {
        headers: { Accept: "application/json" },
      });
      if (!res.ok) {
        throw new Error(`HTTP error! status: ${res.status}`);
      }
      const data: HealthResponse = await res.json();
      setHealth(data);
      setLastChecked(new Date().toLocaleTimeString());
    } catch (err: unknown) {
      setError(
        err instanceof Error
          ? err.message
          : "Could not connect to ClaimStream backend"
      );
      setHealth(null);
      setLastChecked(new Date().toLocaleTimeString());
    } finally {
      setLoading(false);
    }
  }, [apiUrl]);

  useEffect(() => {
    let ignore = false;

    async function fetchInitialHealth() {
      try {
        const res = await fetch(`${apiUrl}/health`, {
          headers: { Accept: "application/json" },
        });
        if (!ignore) {
          if (!res.ok) {
            throw new Error(`HTTP error! status: ${res.status}`);
          }
          const data: HealthResponse = await res.json();
          setHealth(data);
          setError(null);
          setLastChecked(new Date().toLocaleTimeString());
        }
      } catch (err: unknown) {
        if (!ignore) {
          setError(
            err instanceof Error
              ? err.message
              : "Could not connect to ClaimStream backend"
          );
          setHealth(null);
          setLastChecked(new Date().toLocaleTimeString());
        }
      } finally {
        if (!ignore) {
          setLoading(false);
        }
      }
    }

    fetchInitialHealth();

    return () => {
      ignore = true;
    };
  }, [apiUrl]);

  return (
    <main className="min-h-screen bg-gradient-to-b from-slate-950 via-slate-900 to-slate-950 text-slate-100 flex flex-col items-center justify-between p-6 sm:p-12">
      <div className="w-full max-w-6xl space-y-10">
        {/* Header Bar */}
        <header className="flex flex-col sm:flex-row items-start sm:items-center justify-between pb-6 border-b border-slate-800 gap-4">
          <div className="flex items-center gap-3">
            <div className="h-10 w-10 rounded-xl bg-gradient-to-tr from-cyan-500 to-blue-600 flex items-center justify-center font-bold text-white shadow-lg shadow-cyan-500/20 text-xl">
              ⚡
            </div>
            <div>
              <h1 className="text-2xl font-bold tracking-tight text-white flex items-center gap-2">
                ClaimStream
                <span className="text-xs uppercase px-2.5 py-0.5 rounded-full bg-cyan-950 text-cyan-400 border border-cyan-800 font-semibold">
                  v0.1.0 Ready
                </span>
              </h1>
              <p className="text-xs text-slate-400">
                AI-Powered Multi-Agent Clinical Clarification Desk
              </p>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <a
              href="http://localhost:8000/docs"
              target="_blank"
              rel="noopener noreferrer"
              className="text-xs font-medium px-3.5 py-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 transition"
            >
              API Swagger Docs ↗
            </a>
            <a
              href="https://github.com"
              target="_blank"
              rel="noopener noreferrer"
              className="text-xs font-medium px-3.5 py-2 rounded-lg bg-cyan-600 hover:bg-cyan-500 text-white shadow-md transition"
            >
              Repository
            </a>
          </div>
        </header>

        {/* Hero Banner */}
        <section className="relative overflow-hidden rounded-2xl bg-gradient-to-r from-slate-900 via-slate-800/80 to-slate-900 border border-slate-800 p-8 shadow-2xl">
          <div className="relative z-10 max-w-2xl space-y-4">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-500/10 border border-blue-500/20 text-blue-400 text-xs font-medium">
              <span className="h-2 w-2 rounded-full bg-blue-400 animate-pulse"></span>
              Hackathon Base Architecture Initialized
            </div>
            <h2 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight leading-tight">
              Clinical Clarification <br />
              <span className="bg-gradient-to-r from-cyan-400 to-blue-500 bg-clip-text text-transparent">
                Desk for TPA & Insurance
              </span>
            </h2>
            <p className="text-sm sm:text-base text-slate-300 leading-relaxed">
              Automating insurance query parsing, EHR/FHIR clinical evidence
              retrieval, medical necessity validation, and compliant response
              synthesis for hospitals.
            </p>
          </div>
        </section>

        {/* Status & Architecture Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Backend Connection Card */}
          <div className="p-6 rounded-xl bg-slate-900/80 border border-slate-800 flex flex-col justify-between space-y-4">
            <div>
              <div className="flex items-center justify-between mb-3">
                <h3 className="font-semibold text-slate-200 text-sm">
                  Backend API Health
                </h3>
                <button
                  onClick={checkHealth}
                  disabled={loading}
                  className="text-xs text-cyan-400 hover:text-cyan-300 underline disabled:opacity-50"
                >
                  {loading ? "Checking..." : "Re-check"}
                </button>
              </div>

              {health ? (
                <div className="space-y-3">
                  <div className="flex items-center gap-2 text-emerald-400 text-sm font-medium">
                    <span className="h-2.5 w-2.5 rounded-full bg-emerald-400"></span>
                    Connected: {health.status}
                  </div>
                  <div className="text-xs bg-slate-950 p-3 rounded-lg border border-slate-800/80 font-mono text-slate-300 space-y-1">
                    <div>
                      <span className="text-slate-500">Service:</span>{" "}
                      {health.service}
                    </div>
                    <div>
                      <span className="text-slate-500">Target:</span> {apiUrl}
                      /health
                    </div>
                  </div>
                </div>
              ) : (
                <div className="space-y-3">
                  <div className="flex items-center gap-2 text-amber-400 text-sm font-medium">
                    <span className="h-2.5 w-2.5 rounded-full bg-amber-400"></span>
                    Backend Standby / Disconnected
                  </div>
                  <div className="text-xs bg-slate-950 p-3 rounded-lg border border-slate-800 text-slate-400">
                    {error || "Backend not running on port 8000"}
                  </div>
                </div>
              )}
            </div>

            <div className="text-[11px] text-slate-500 border-t border-slate-800/60 pt-3">
              Last check: {lastChecked || "Just now"}
            </div>
          </div>

          {/* Tech Stack Card */}
          <div className="p-6 rounded-xl bg-slate-900/80 border border-slate-800 space-y-4">
            <h3 className="font-semibold text-slate-200 text-sm">
              Active Foundations
            </h3>
            <div className="grid grid-cols-2 gap-2 text-xs">
              <div className="p-2.5 rounded-lg bg-slate-950 border border-slate-800/70">
                <span className="text-cyan-400 font-semibold block">
                  Next.js 15
                </span>
                <span className="text-slate-400">App Router & TS</span>
              </div>
              <div className="p-2.5 rounded-lg bg-slate-950 border border-slate-800/70">
                <span className="text-emerald-400 font-semibold block">
                  FastAPI
                </span>
                <span className="text-slate-400">Python 3.12 Backend</span>
              </div>
              <div className="p-2.5 rounded-lg bg-slate-950 border border-slate-800/70">
                <span className="text-indigo-400 font-semibold block">
                  Tailwind CSS
                </span>
                <span className="text-slate-400">Responsive UI</span>
              </div>
              <div className="p-2.5 rounded-lg bg-slate-950 border border-slate-800/70">
                <span className="text-purple-400 font-semibold block">
                  Docker Ready
                </span>
                <span className="text-slate-400">Compose Configured</span>
              </div>
            </div>
          </div>

          {/* Multi-Agent Roadmap Card */}
          <div className="p-6 rounded-xl bg-slate-900/80 border border-slate-800 space-y-3">
            <h3 className="font-semibold text-slate-200 text-sm">
              Upcoming Agents
            </h3>
            <ul className="space-y-2 text-xs text-slate-300">
              <li className="flex items-center gap-2">
                <span className="h-1.5 w-1.5 rounded-full bg-cyan-400"></span>
                <span>TPA Query Parser Agent</span>
              </li>
              <li className="flex items-center gap-2">
                <span className="h-1.5 w-1.5 rounded-full bg-blue-400"></span>
                <span>EHR/FHIR Clinical Evidence Retriever</span>
              </li>
              <li className="flex items-center gap-2">
                <span className="h-1.5 w-1.5 rounded-full bg-indigo-400"></span>
                <span>Clinical Policy Matcher Agent</span>
              </li>
              <li className="flex items-center gap-2">
                <span className="h-1.5 w-1.5 rounded-full bg-teal-400"></span>
                <span>Response Synthesizer & Human Review</span>
              </li>
            </ul>
          </div>
        </div>

        {/* Quick Start Commands */}
        <section className="p-6 rounded-xl bg-slate-900/60 border border-slate-800 space-y-4">
          <h3 className="text-sm font-semibold text-slate-300">
            Quick Start Commands for Team Members
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs font-mono">
            <div className="p-4 rounded-lg bg-slate-950 border border-slate-800/80 space-y-1">
              <div className="text-slate-400 font-sans font-medium mb-1">
                Run Backend:
              </div>
              <div className="text-cyan-400">cd backend</div>
              <div className="text-cyan-400">source .venv/bin/activate</div>
              <div className="text-cyan-400">
                uvicorn app.main:app --reload --port 8000
              </div>
            </div>
            <div className="p-4 rounded-lg bg-slate-950 border border-slate-800/80 space-y-1">
              <div className="text-slate-400 font-sans font-medium mb-1">
                Run Frontend:
              </div>
              <div className="text-indigo-400">cd frontend</div>
              <div className="text-indigo-400">npm run dev</div>
            </div>
          </div>
        </section>

        {/* Footer */}
        <footer className="text-center text-xs text-slate-500 pt-4">
          ClaimStream • AI-Powered Clinical Clarification Desk • Hackathon Base
          Repository
        </footer>
      </div>
    </main>
  );
}
