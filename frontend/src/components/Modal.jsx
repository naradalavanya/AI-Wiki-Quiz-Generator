import React from "react";

export default function Modal({ open, onClose, title, children }) {
  if (!open) return null;
  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 backdrop-blur-sm px-4 py-12"
      role="dialog"
      aria-modal="true"
      aria-labelledby="modal-title"
    >
      <div className="w-full max-w-3xl rounded-3xl bg-white shadow-2xl animate-modal-pop">
        <div className="flex items-center justify-between border-b p-4">
          <h3 id="modal-title" className="text-lg font-semibold">{title}</h3>
          <button
            className="rounded-md px-3 py-1 text-sm hover:bg-gray-100"
            onClick={onClose}
            aria-label="Close dialog"
          >
            Close
          </button>
        </div>
        <div className="max-h-[calc(100vh-6rem)] overflow-y-auto p-4">{children}</div>
      </div>
    </div>
  );
}
