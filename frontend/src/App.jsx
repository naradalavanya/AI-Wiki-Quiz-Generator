import React, { useState } from "react";
import GenerateQuizTab from "./tabs/GenerateQuizTab";
import HistoryTab from "./tabs/HistoryTab";

export default function App() {
  const [tab, setTab] = useState("generate");
  const [historyTrigger, setHistoryTrigger] = useState(0);

  return (
    <div className="mx-auto max-w-6xl p-4 md:p-8">
      <header className="mb-8 rounded-3xl bg-gradient-to-r from-indigo-600 to-purple-600 p-8 text-white shadow-lg">
        <div className="flex items-center justify-between gap-4">
          <div>
            <h1 className="text-4xl font-extrabold drop-shadow">AI Wiki Quiz Generator</h1>
            <p className="mt-2 max-w-xl text-indigo-100">Turn any Wikipedia article into a short multiple-choice quiz — great for study, teaching, or quick practice.</p>
            
          </div>
          <div className="hidden md:block text-6xl" aria-hidden>🧠</div>
        </div>
      </header>

      <div className="mb-6 flex gap-2">
        <button
          onClick={() => setTab("generate")}
          className={`rounded-xl px-4 py-2 ${tab === "generate" ? "bg-indigo-600 text-white" : "bg-white text-gray-800 shadow"}`}
        >
          Generate Quiz
        </button>
        <button
          onClick={() => { setTab("history"); setHistoryTrigger((t) => t + 1); }}
          className={`rounded-xl px-4 py-2 ${tab === "history" ? "bg-indigo-600 text-white" : "bg-white text-gray-800 shadow"}`}
        >
          History
        </button>
      </div>

  {tab === "generate" ? <GenerateQuizTab /> : <HistoryTab animateTrigger={historyTrigger} />}

      
    </div>
  );
}
