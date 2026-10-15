"use client";

import React from "react";

interface PhotoModalProps {
  id: string;
  name: string;
  isSelected: boolean;
  onClose: () => void;
  onToggle: (id: string) => void;
}

export default function PhotoModal({
  id,
  name,
  isSelected,
  onClose,
  onToggle,
}: PhotoModalProps) {
  return (
    <div
      style={{
        position: "fixed",
        inset: 0,
        backgroundColor: "rgba(0, 0, 0, 0.95)",
        backdropFilter: "blur(12px)",
        zIndex: 999999,
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        padding: "16px",
      }}>
      {/* Tombol Tutup */}
      <button
        onClick={onClose}
        style={{
          position: "absolute",
          top: "16px",
          right: "16px",
          backgroundColor: "rgba(255, 255, 255, 0.15)",
          color: "#ffffff",
          border: "none",
          borderRadius: "50%",
          width: "40px",
          height: "40px",
          fontSize: "1.2rem",
          cursor: "pointer",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
        }}>
        ✕
      </button>

      {/* Gambar Pratinjau */}
      <div
        style={{
          maxWidth: "90vw",
          maxHeight: "75vh",
          display: "flex",
          justifyContent: "center",
        }}>
        <img
          src={`/api/thumbnail?id=${id}`}
          alt={name}
          style={{
            maxWidth: "100%",
            maxHeight: "75vh",
            objectFit: "contain",
            borderRadius: "12px",
          }}
        />
      </div>

      {/* Informasi & Tombol Toggle */}
      <div
        style={{
          marginTop: "18px",
          display: "flex",
          alignItems: "center",
          gap: "16px",
        }}>
        <span
          style={{ color: "#ffffff", fontSize: "0.95rem", fontWeight: 600 }}>
          {name}
        </span>
        <button
          onClick={() => onToggle(id)}
          style={{
            backgroundColor: isSelected ? "#22c55e" : "#3b82f6",
            color: "#ffffff",
            border: "none",
            borderRadius: "9999px",
            padding: "8px 20px",
            fontSize: "0.85rem",
            fontWeight: 700,
            cursor: "pointer",
          }}>
          {isSelected ? "Batal Pilih" : "Pilih Foto"}
        </button>
      </div>
    </div>
  );
}
