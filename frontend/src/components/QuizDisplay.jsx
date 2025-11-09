import React from "react";

export default function QuizDisplay({ quiz, data }) {
  // Accept either `quiz` prop or `data` prop (HistoryTab uses `data`).
  const qobj = quiz || data;
  if (!qobj) return null;

  // Support both `questions` and `quiz` as the list key
  const questions = Array.isArray(qobj.questions) ? qobj.questions : (Array.isArray(qobj.quiz) ? qobj.quiz : []);
  const title = qobj.title || qobj.name || qobj.article_title || "";
  const summary = qobj.summary || qobj.description || "";
  const key_entities = Array.isArray(qobj.key_entities) ? qobj.key_entities : (Array.isArray(qobj.keyEntities) ? qobj.keyEntities : []);
  const related = Array.isArray(qobj.related_topics) ? qobj.related_topics : (Array.isArray(qobj.relatedTopics) ? qobj.relatedTopics : []);

  const optionLabel = (i) => String.fromCharCode(65 + i);

  return (
    <div className="space-y-6">
      <div className="rounded-2xl bg-white p-6 shadow">
        <h2 className="text-2xl font-bold">{title}</h2>
        {summary && <p className="mt-2 text-gray-700">{summary}</p>}
        {key_entities.length > 0 && (
          <p className="mt-3 text-sm text-gray-600"><strong>Entities:</strong> {key_entities.join(", ")}</p>
        )}
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        {questions.map((q, i) => (
          <article key={i} className="rounded-2xl bg-white p-5 shadow">
            <h4 className="text-lg font-semibold">Q{i + 1}. {q.question || q.prompt}</h4>
            <div className="mt-3 grid gap-2">
              {(q.options || q.choices || []).map((opt, idx) => {
                const label = optionLabel(idx);
                const correct = (q.correct_answer || q.answer || q.correct || "").toString().trim();
                const isCorrect = correct && correct === opt.toString().trim();
                return (
                  <div key={idx} className={`flex items-start gap-3 rounded-md p-3 ${isCorrect ? 'bg-green-50 ring-1 ring-green-100' : 'bg-gray-50'}`}>
                    <div className="w-7 h-7 flex items-center justify-center rounded-full bg-white text-sm font-semibold border">{label}</div>
                    <div className="text-gray-800">{opt}</div>
                  </div>
                );
              })}
            </div>
            <div className="mt-3 text-sm text-gray-700">
              <div><strong>Answer:</strong> {q.correct_answer || q.answer || q.correct || ""}</div>
              {q.explanation && <div className="mt-1"><strong>Explanation:</strong> {q.explanation}</div>}
              {q.difficulty && <div className="mt-1"><strong>Difficulty:</strong> {q.difficulty}</div>}
            </div>
          </article>
        ))}
      </div>

      {related.length > 0 && (
        <div className="rounded-2xl bg-white p-5 shadow">
          <h3 className="text-lg font-semibold">Related Topics</h3>
          <ul className="mt-2 list-disc pl-6">
            {related.map((t, idx) => <li key={idx}>{t}</li>)}
          </ul>
        </div>
      )}
    </div>
  );
}
