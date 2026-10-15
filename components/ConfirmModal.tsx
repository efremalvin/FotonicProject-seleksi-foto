"use client";

import React from "react";

interface ConfirmModalProps {
  selectedCount: number;
  maxPhotos: number;
  selectedFileNames: string[];
  isSubmitting: boolean;
  onBackToGallery: () => void;
  onConfirmSubmit: () => void;
}

export default function ConfirmModal({
  selectedCount,
  maxPhotos,
  selectedFileNames,
  isSubmitting,
  onBackToGallery,
  onConfirmSubmit,
}: ConfirmModalProps) {
  return (
    <div
      style={{
        position: "fixed",
        inset: 0,
        backgroundColor: "rgba(10, 10, 12, 0.9)",
        backdropFilter: "blur(10px)",
        zIndex: 99999,
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        padding: "16px",
      }}>
      <div
        style={{
          backgroundColor: "#262628",
          borderRadius: "28px",
          padding: "32px 24px",
          maxWidth: "420px",
          width: "100%",
          textAlign: "center",
          boxShadow: "0 24px 48px rgba(0,0,0,0.6)",
          border: "1px solid rgba(255,255,255,0.08)",
        }}>
        <h2
          style={{
            fontSize: "1.35rem",
            fontWeight: 800,
            color: "#ffffff",
            marginBottom: "8px",
          }}>
          Konfirmasi Pilihan Foto
        </h2>
        <p
          style={{
            fontSize: "0.85rem",
            color: "#a1a1aa",
            marginBottom: "18px",
          }}>
          Anda telah memilih{" "}
          <strong style={{ color: "#22c55e" }}>{selectedCount}</strong> dari
          maksimal {maxPhotos} foto.
        </p>

        {/* Ringkasan File */}
        <div
          style={{
            backgroundColor: "#1c1c1e",
            borderRadius: "16px",
            padding: "14px",
            maxHeight: "180px",
            overflowY: "auto",
            textAlign: "left",
            marginBottom: "24px",
            fontSize: "0.8rem",
            color: "#e4e4e7",
            lineHeight: "1.6",
          }}>
          {selectedFileNames.map((name, i) => (
            <div key={i}>
              {i + 1}. {name}
            </div>
          ))}
        </div>

        {/* Tombol Aksi */}
        <div style={{ display: "flex", flexDirection: "column", gap: "12px" }}>
          {/* Tombol Konfirmasi Sesuai Konfirmasi.jpg */}
          <button
            onClick={onConfirmSubmit}
            disabled={isSubmitting}
            style={{
              width: "100%",
              backgroundColor: isSubmitting ? "#5c3734" : "#dc3522",
              color: "#ffffff",
              border: "none",
              borderRadius: "9999px",
              padding: "14px 20px",
              fontSize: "0.95rem",
              fontWeight: 700,
              cursor: isSubmitting ? "not-allowed" : "pointer",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              gap: "10px",
              boxShadow: "0 6px 16px rgba(220, 53, 34, 0.4)",
            }}>
            <span>{isSubmitting ? "Menyimpan Data..." : "Konfirmasi"}</span>
            <span
              style={{
                backgroundColor: "#ffffff",
                color: "#dc3522",
                borderRadius: "50%",
                width: "22px",
                height: "22px",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                fontSize: "0.8rem",
                fontWeight: 900,
              }}>
              ✓
            </span>
          </button>

          {/* Tombol Ubah Pilihan Sesuai Group 13.jpg */}
          <button
            onClick={onBackToGallery}
            disabled={isSubmitting}
            style={{
              width: "100%",
              backgroundColor: "#212124",
              color: "#ffffff",
              border: "1px solid rgba(255,255,255,0.1)",
              borderRadius: "16px",
              padding: "12px 18px",
              fontSize: "0.88rem",
              fontWeight: 600,
              cursor: isSubmitting ? "not-allowed" : "pointer",
              lineHeight: "1.3",
            }}>
            <div>Ubah Pilihan di</div>
            <div>← Galeri</div>
          </button>
        </div>
      </div>
    </div>
  );
}
