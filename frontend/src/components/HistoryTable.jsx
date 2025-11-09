import React from "react";

export default function HistoryTable({ rows, onDetails }) {
  // Robust formatter: accepts numeric timestamps (seconds or ms), numeric strings,
  // ISO date strings, or alternate field names. Returns a friendly fallback when
  // parsing fails.
  const formatDate = (row) => {
    const raw =
      row?.date_generated ??
      row?.generated_at ??
      row?.date_created ??
      row?.created_at ??
      row?.timestamp ??
      row?.createdAt;

    if (raw === null || raw === undefined || raw === "") return "—";

    // If it's a pure numeric string, convert to number
    let v = raw;
    if (typeof v === "string" && /^\d+$/.test(v)) v = parseInt(v, 10);

    // If it's a number, decide if it's seconds (10 digits) or milliseconds
    if (typeof v === "number") {
      // heuristic: anything less than 1e12 is probably seconds (<= ~2001-09-09),
      // so multiply by 1000 to convert to ms. Modern ms timestamps are ~1.7e12+.
      const ms = v < 1e12 ? v * 1000 : v;
      const d = new Date(ms);
      if (!isNaN(d)) return d.toLocaleString();
    }

    // Try parsing as a date string (ISO or other formats)
    const parsed = Date.parse(String(raw));
    if (!isNaN(parsed)) return new Date(parsed).toLocaleString();

    // Fallback: show the raw value (useful when backend stores a non-standard format)
    return String(raw);
  };

  return (
    <div className="overflow-x-auto rounded-2xl bg-white shadow">
      <table className="min-w-full text-left text-sm">
        <thead className="bg-gray-50 text-gray-600">
          <tr>
            <th className="px-4 py-3">ID</th>
            <th className="px-4 py-3">Title</th>
            <th className="px-4 py-3">URL</th>
            <th className="px-4 py-3">Generated</th>
            <th className="px-4 py-3">Action</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((r) => (
            <tr key={r.id} className="border-t">
              <td className="px-4 py-3">{r.id}</td>
              <td className="px-4 py-3 font-medium">{r.title}</td>
              <td className="px-4 py-3 truncate max-w-[280px] text-blue-600">
                <a href={r.url} target="_blank" rel="noreferrer">
                  {r.url}
                </a>
              </td>
              <td
                className="px-4 py-3"
                title={String(r.date_generated ?? r.date_generated_ms ?? r.created_at ?? "")}
              >
                {formatDate(r)}
              </td>
              <td className="px-4 py-3">
                <button
                  onClick={() => onDetails(r.id)}
                  className="rounded-lg bg-indigo-600 px-3 py-1.5 text-white hover:bg-indigo-700"
                >
                  Details
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
