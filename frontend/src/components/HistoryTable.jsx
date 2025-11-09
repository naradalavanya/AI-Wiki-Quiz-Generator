import React from "react";

export default function HistoryTable({ rows, onDetails }) {
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
                <a href={r.url} target="_blank" rel="noreferrer">{r.url}</a>
              </td>
              <td className="px-4 py-3">{new Date(r.date_generated).toLocaleString()}</td>
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
