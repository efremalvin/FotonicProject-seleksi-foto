"use client";

import React from "react";

interface PhotoCardProps {
  id: string;
  name: string;
  isSelected: boolean;
  isDisabled: boolean;
  onToggle: (id: string) => void;
  onPreview: (id: string, name: string) => void;
}

export default function PhotoCard({
  id,
  name,
  isSelected,
  isDisabled,
  onToggle,
  onPreview,
}: PhotoCardProps) {
  const thumbnailUrl = `/api/thumbnail?id=${id}`;

  return (
    <div style={{
      backgroundColor: "#262628",
      borderRadius: "24px",
      padding: "12px",
      border: isSelected ? "2px solid #22c55e" : "1px solid rgba(255,255,255,0.06)",
      boxShadow: isSelected ? "0 4px 20px rgba(34, 197, 94, 0.2)" : "0 4px 16px rgba(0,0,0,0.25)",
      transition: "all 0.2s ease",
      position: "relative",
    }}>
      {/* Kontainer Foto */}
      <div style={{
        position: "relative",
        width: "100%",
        borderRadius: "16px",
        overflow: "hidden",
        backgroundColor: "#18181a",
        aspectRatio: "3/4",
      }}>
        <img
          src={thumbnailUrl}
          alt={name}
          loading="lazy"
          style={{
            width: "100%",
            height: "100%",
            objectFit: "cover",
            display: "block",
          }}
        />

        {/* Tombol Perbesar / Expand */}
        <button
          onClick={() => onPreview(id, name)}
          title="Lihat Pratinjau Penuh"
          style={{
            position: "absolute",
            top: "10px",
            right: "10px",
            backgroundColor: "rgba(0, 0, 0, 0.6)",
            color: "#ffffff",
            border: "none",
            borderRadius: "8px",
            width: "32px",
            height: "32px",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            cursor: "pointer",
            fontSize: "1rem",
            backdropFilter: "blur(4px)",
          }}
        >
          ⛶
        </button>
      </div>

      {/* Bagian Bawah: Nama File & Tombol Pilih */}
      <div style={{
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        padding: "14px 4px 4px 4px",
      }}>
        <span style={{
          fontSize: "0.82rem",
          fontWeight: 700,
          color: "#ffffff",
          whiteSpace: "nowrap",
          overflow: "hidden",
          textOverflow: "ellipsis",
          maxWidth: "70%",
        }}>
          {name}
        </span>

        {isSelected ? (
          // Tombol Terpilih (Kotak Hijau dengan Centang)
          <button
            onClick={() => onToggle(id)}
            style={{
              backgroundColor: "#22c55e",
              color: "#ffffff",
              border: "none",
              borderRadius: "8px",
              width: "34px",
              height: "34px",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              cursor: "pointer",
              fontSize: "1.1rem",
              fontWeight: 800,
              boxShadow: "0 2px 8px rgba(34, 197, 94, 0.4)",
            }}
          >
            ✓
          </button>
        ) : (
          // Tombol Belum Dipilih (Pill Biru)
          <button
            onClick={() => onToggle(id)}
            disabled={isDisabled}
            style={{
              backgroundColor: isDisabled ? "#4b5563" : "#3b82f6",
              color: "#ffffff",
              border: "none",
              borderRadius: "9999px",
              padding: "6px 16px",
              fontSize: "0.8rem",
              fontWeight: 700,
              cursor: isDisabled ? "not-allowed" : "pointer",
              boxShadow: isDisabled ? "none" : "0 2px 8px rgba(59, 130, 246, 0.4)",
              transition: "background-color 0.2s ease",
            }}
          >
            Pilih
          </button>
        )}
      </div>
    </div>
  );
}