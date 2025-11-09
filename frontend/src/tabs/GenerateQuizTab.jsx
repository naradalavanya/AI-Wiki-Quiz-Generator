import React, { useState } from "react";
import { generateQuiz } from "../services/api";
import QuizDisplay from "../components/QuizDisplay";

export default function GenerateQuizTab() {
  const [url, setUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState(null);
  const [error, setError] = useState("");

  const onSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setData(null);
    if (!/^https?:\/\//.test(url)) {
      setError("Please enter a valid http(s) Wikipedia URL.");
      return;
    }
    setLoading(true);
    try {
      const result = await generateQuiz(url);
      setData(result);
    } catch (err) {
      setError(err.message || "Failed to generate quiz.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <form onSubmit={onSubmit} className="rounded-2xl bg-white p-5 shadow animate-fade-up">
        <label className="block text-sm font-medium">Wikipedia URL</label>
        <input
          type="url"
          id="wiki-url-input"
          placeholder="Enter Wikipedia article URL"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          className="mt-2 w-full rounded-lg border px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
          required
        />
        <button
          type="submit"
          disabled={loading}
          className="mt-3 rounded-lg bg-indigo-600 px-4 py-2 text-white hover:bg-indigo-700 disabled:opacity-60"
        >
          {loading ? "Generating…" : "Generate Quiz"}
        </button>
        {error && <p className="mt-2 text-sm text-red-600">{error}</p>}
      </form>

      {loading && (
        <div className="rounded-2xl bg-white p-5 text-center shadow">
          Processing the article…
        </div>
      )}

      {data && <QuizDisplay data={data} />}
    </div>
  );
}
