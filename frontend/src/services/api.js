const BASE_URL ="https://ai-wiki-quiz-generator-j8j0.onrender.com";

export async function generateQuiz(url) {
  const resp = await fetch(`${BASE_URL}/generate_quiz`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ url }),
  });
  if (!resp.ok) throw new Error((await resp.json()).detail || "Failed to generate quiz");
  return resp.json();
}

export async function fetchHistory() {
  const resp = await fetch(`${BASE_URL}/history`);
  if (!resp.ok) throw new Error("Failed to load history");
  return resp.json();
}

export async function fetchQuizById(id) {
  const resp = await fetch(`${BASE_URL}/quiz/${id}`);
  if (!resp.ok) throw new Error("Failed to load quiz");
  return resp.json();
}
