"use client";

import React from "react";

interface SuccessModalProps {
  clientName: string;
  selectedFileNames: string[];
  notes?: string;
  adminWaNumber?: string;
}

export default function SuccessModal({
  clientName,
  selectedFileNames,
  notes,
  adminWaNumber = "6281234567890", // Ganti dengan nomor WhatsApp resmi admin Fotonic
}: SuccessModalProps) {
  // Format pesan WhatsApp otomatis
  const waMessage =
    `Halo Tim Fotonic, saya ${clientName}.\n` +
    `Saya telah selesai memilih ${selectedFileNames.length} foto untuk sesi editing:\n\n` +
    selectedFileNames.map((name, i) => `${i + 1}. ${name}`).join("\n") +
    (notes ? `\n\nCatatan Editing:\n"${notes}"` : "") +
    `\n\nMohon dicek ya, terima kasih!`;

  const waUrl = `https://wa.me/${adminWaNumber}?text=${encodeURIComponent(waMessage)}`;

  return (
    <div
      style={{
        position: "fixed",
        inset: 0,
        backgroundColor: "#121214",
        zIndex: 999999,
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        padding: "20px",
      }}>
      <div
        style={{
          backgroundColor: "#242426",
          borderRadius: "28px",
          padding: "40px 24px",
          maxWidth: "460px",
          width: "100%",
          textAlign: "center",
          boxShadow: "0 24px 60px rgba(0,0,0,0.7)",
          border: "1px solid rgba(255,255,255,0.08)",
        }}>
        <div style={{ fontSize: "2.8rem", marginBottom: "12px" }}>🎉</div>

        <h2
          style={{
            fontSize: "1.45rem",
            fontWeight: 800,
            color: "#ffffff",
            marginBottom: "12px",
          }}>
          Data Foto Berhasil Disimpan!
        </h2>

        <p
          style={{
            fontSize: "0.85rem",
            color: "#d1d1d6",
            lineHeight: "1.5",
            marginBottom: "20px",
          }}>
          Terima Kasih Kak{" "}
          <strong style={{ color: "#e03828" }}>{clientName}</strong>. Foto
          pilihan Anda sudah tercatat di sistem Fotonic.
        </p>

        {/* Daftar Bernomor File Terpilih */}
        <div
          style={{
            backgroundColor: "#18181a",
            borderRadius: "14px",
            padding: "16px 18px",
            maxHeight: "180px",
            overflowY: "auto",
            textAlign: "left",
            border: "1px solid rgba(255,255,255,0.05)",
            marginBottom: "20px",
          }}>
          {selectedFileNames.map((name, i) => (
            <div
              key={i}
              style={{
                fontSize: "0.82rem",
                color: "#e4e4e7",
                marginBottom: "5px",
              }}>
              {i + 1}. {name}
            </div>
          ))}
        </div>

        {/* Kotak Peringatan Langkah Terakhir */}
        <div
          style={{
            backgroundColor: "rgba(30, 58, 138, 0.25)",
            border: "1px solid rgba(96, 165, 250, 0.35)",
            borderRadius: "14px",
            padding: "14px",
            textAlign: "left",
            fontSize: "0.82rem",
            lineHeight: "1.5",
            color: "#bfdbfe",
            marginBottom: "20px",
          }}>
          <strong style={{ color: "#93c5fd" }}>⚠️ Langkah Terakhir:</strong>
          <br />
          Harap konfirmasi ke Admin Fotonic via WhatsApp agar tim editor dapat
          segera memvalidasi dan memproses antrean retouching Anda.
        </div>

        {/* Tombol WhatsApp */}
        <a
          href={waUrl}
          target="_blank"
          rel="noopener noreferrer"
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            gap: "8px",
            backgroundColor: "#22c55e",
            color: "#ffffff",
            textDecoration: "none",
            borderRadius: "9999px",
            padding: "14px 20px",
            fontSize: "0.95rem",
            fontWeight: 700,
            boxShadow: "0 4px 16px rgba(34, 197, 94, 0.35)",
          }}>
          <span>💬</span>
          <span>Konfirmasi ke WhatsApp Admin</span>
        </a>
      </div>
    </div>
  );
}
