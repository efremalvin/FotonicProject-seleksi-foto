"use client";

import React from "react";

interface ProgressBarProps {
  current: number;
  max: number;
}

export default function ProgressBar({ current, max }: ProgressBarProps) {
  const isFull = current >= max;
  const percentage = Math.min((current / max) * 100, 100);
  const color = isFull ? "#22c55e" : current > 0 ? "#e03828" : "#4b4b4b";

  return (
    <div
      style={{
        position: "sticky",
        top: "14px",
        zIndex: 9999,
        margin: "0 auto 24px auto",
        maxWidth: "500px",
        width: "calc(100% - 32px)",
        backgroundColor: "rgba(125, 125, 130, 0.55)",
        backdropFilter: "blur(12px)",
        WebkitBackdropFilter: "blur(12px)",
        borderRadius: "9999px",
        padding: "10px 18px",
        display: "flex",
        alignItems: "center",
        gap: "14px",
        boxShadow: "0 8px 24px rgba(0,0,0,0.3)",
        border: "1px solid rgba(255,255,255,0.15)",
      }}>
      {/* Bar Track */}
      <div
        style={{
          flex: 1,
          backgroundColor: "#3a3a3c",
          height: "8px",
          borderRadius: "9999px",
          overflow: "hidden",
        }}>
        <div
          style={{
            width: `${percentage}%`,
            height: "100%",
            backgroundColor: color,
            borderRadius: "9999px",
            transition: "width 0.3s ease, background-color 0.3s ease",
          }}
        />
      </div>

      {/* Counter Teks */}
      <span
        style={{
          fontSize: "0.85rem",
          fontWeight: 800,
          color: isFull ? "#22c55e" : "#e03828",
          whiteSpace: "nowrap",
        }}>
        {current} / {max}
      </span>
    </div>
  );
}
