import React, { useEffect, useState } from "react";
import { fetchHistory, fetchQuizById } from "../services/api";
import HistoryTable from "../components/HistoryTable";
import Modal from "../components/Modal";
import QuizDisplay from "../components/QuizDisplay";

export default function HistoryTab() {
  const [rows, setRows] = useState([]);
  const [open, setOpen] = useState(false);
  const [selected, setSelected] = useState(null);
  const [error, setError] = useState("");

  const load = async () => {
    setError("");
    try {
      const data = await fetchHistory();
      // Ensure history is shown in ascending order by id (oldest at top,
      // newest at bottom). Backend may return descending; normalize here.
      const sorted = Array.isArray(data) ? [...data].sort((a, b) => (a.id || 0) - (b.id || 0)) : [];
      setRows(sorted);
    } catch (e) {
      setError(e.message || "Failed to load history.");
    }
  };

  useEffect(() => { load(); }, []);

  const onDetails = async (id) => {
    try {
      const payload = await fetchQuizById(id);
      setSelected(payload);
      setOpen(true);
    } catch (e) {
      setError(e.message || "Failed to open quiz.");
    }
  };

  return (
    <div className="space-y-4 animate-fade-up">
      {error && <p className="text-sm text-red-600">{error}</p>}
      <HistoryTable rows={rows} onDetails={onDetails} />
      <Modal open={open} onClose={() => setOpen(false)} title="Quiz Details">
        <QuizDisplay data={selected} />
      </Modal>
    </div>
  );
}
