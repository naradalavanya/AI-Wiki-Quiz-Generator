import React from "react";

export default function QuizDisplay({ data }) {
  if (!data) return null;
  const { title, summary, key_entities = [], related_topics = [], questions = [] } = data;

  return (
    <div className="space-y-4">
      <div className="rounded-2xl bg-white p-5 shadow">
        <h2 className="text-2xl font-bold">{title}</h2>
        <p className="mt-2 text-gray-700">{summary}</p>
        <div className="mt-3 flex flex-wrap gap-2 text-sm">
          {key_entities.length > 0 && (
            <div className="rounded-full bg-indigo-50 px-3 py-1">Entities: {key_entities.join(", ")}</div>
          )}
          {related_topics.length > 0 && (
            <div className="rounded-full bg-emerald-50 px-3 py-1">Related: {related_topics.join(", ")}</div>
          )}
        </div>
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        {questions.map((q, idx) => (
          <div key={idx} className="rounded-2xl bg-white p-5 shadow">
            <h4 className="text-lg font-semibold">Q{idx + 1}. {q.question}</h4>
            <ul className="mt-2 list-disc space-y-1 pl-6 text-gray-700">
              {q.options.map((opt, i) => (
                <li key={i}>{opt}</li>
              ))}
            </ul>
            <div className="mt-3 rounded-md bg-gray-50 p-3 text-sm">
              <strong>Answer:</strong> {q.correct_answer}
              {q.explanation && <p className="mt-1 text-gray-600">{q.explanation}</p>}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
