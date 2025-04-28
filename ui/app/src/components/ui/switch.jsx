import React from "react";

export function Switch({ checked, onCheckedChange }) {
  return (
    <label className="inline-flex items-center cursor-pointer">
      <input
        type="checkbox"
        className="sr-only"
        checked={checked}
        onChange={(e) => onCheckedChange(e.target.checked)}
      />
      <div
        className={`w-10 h-6 bg-gray-300 rounded-full shadow-inner transition-all duration-200 ${checked ? 'bg-blue-500' : ''}`}
      >
        <div
          className={`w-4 h-4 bg-white rounded-full shadow transform transition-transform duration-200 ${checked ? 'translate-x-4' : 'translate-x-1'}`}
        />
      </div>
    </label>
  );
}