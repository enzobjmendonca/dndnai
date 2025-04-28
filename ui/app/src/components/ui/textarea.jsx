import React from "react";

export function Textarea({ className = "", ...props }) {
  return (
    <textarea
      className={`w-full rounded-md border border-gray-300 p-2 text-sm shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 ${className}`}
      {...props}
    />
  );
}

export function formatHistory(history) {
  return history.join('\n');
}