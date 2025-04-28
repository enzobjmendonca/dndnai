import React from "react";

export function Button({ className = "", ...props }) {
  return (
    <button
      className={`inline-flex items-center justify-center rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white shadow hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-400 ${className}`}
      {...props}
    >
      {props.children}
    </button>
  );
}