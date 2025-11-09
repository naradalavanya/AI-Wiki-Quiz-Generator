// Prefer local backend when running the frontend on localhost, otherwise use the
// deployed backend. This makes local dev work without editing this file.
const DEFAULT_REMOTE = "https://ai-wiki-quiz-generator-j8j0.onrender.com";
let BASE_URL = DEFAULT_REMOTE;
if (typeof window !== "undefined") {
  const host = window.location.hostname;
  if (host === "localhost" || host === "127.0.0.1") {
    BASE_URL = "http://127.0.0.1:8000"; // local backend default
  }
}

function normalizeQuizData(raw) {
  if (!raw) return raw;

  // If backend wrapped quiz under `quiz`, prefer it; otherwise `questions`.
  const questions = raw.questions || raw.quiz || raw.data || [];

  // Related topics may come under a couple of names
  const related = raw.related_topics || raw.relatedTopics || raw.related || [];

  // key_entities might be a dict (grouped) or already a flat list
  let key_entities = raw.key_entities || raw.keyEntities || raw.keyEntities || raw.entities || [];
  if (key_entities && !Array.isArray(key_entities)) {
    // Flatten dict values into a unique list
    const flat = [];
    if (typeof key_entities === "object") {
      Object.values(key_entities).forEach((v) => {
        if (Array.isArray(v)) flat.push(...v);
        else if (v) flat.push(v);
      });
    } else if (typeof key_entities === "string") {
      flat.push(key_entities);
    }
    // de-dupe preserving order
    const seen = new Set();
    key_entities = flat.filter((x) => {
      if (!x) return false;
      if (seen.has(x)) return false;
      seen.add(x);
      return true;
    });
  }

  // Normalize each question shape to expected fields
  const normalizedQuestions = Array.isArray(questions)
    ? questions.map((q) => ({
        question: q.question || q.q || q.prompt || "",
        options: q.options || q.choices || q.answers || [],
        correct_answer: q.correct_answer || q.answer || q.correct || "",
        explanation: q.explanation || q.explain || q.explanations || "",
        difficulty: q.difficulty || "medium",
      }))
    : [];

  return {
    ...raw,
    questions: normalizedQuestions,
    related_topics: Array.isArray(related) ? related : [related].filter(Boolean),
    key_entities: key_entities || [],
  };
}

export async function generateQuiz(url) {
  const resp = await fetch(`${BASE_URL}/generate_quiz`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ url }),
  });
  if (!resp.ok) throw new Error((await resp.json()).detail || "Failed to generate quiz");
  const raw = await resp.json();
  return normalizeQuizData(raw);
}

export async function fetchHistory() {
  const resp = await fetch(`${BASE_URL}/history`);
  if (!resp.ok) throw new Error("Failed to load history");
  const raw = await resp.json();

  // Normalize history items: ensure `date_generated` is an ISO string when
  // possible. Backend may provide `date_generated` (ISO) or
  // `date_generated_ms` (epoch ms). Prefer ISO, then ms.
  if (!Array.isArray(raw)) return [];
  return raw.map((item) => {
    const iso = item.date_generated || (item.date_generated_ms ? new Date(item.date_generated_ms).toISOString() : null);
    return {
      ...item,
      date_generated: iso,
    };
  });
}

export async function fetchQuizById(id) {
  const resp = await fetch(`${BASE_URL}/quiz/${id}`);
  if (!resp.ok) throw new Error("Failed to load quiz");
  const raw = await resp.json();
  return normalizeQuizData(raw);
}
