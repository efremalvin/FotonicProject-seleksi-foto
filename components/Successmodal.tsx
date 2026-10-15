"use client";

import React from "react";

interface SuccessModalProps {
  clientName: string;
  selectedFileNames: string[];
}

export default function SuccessModal({
  clientName,
  selectedFileNames,
}: SuccessModalProps) {
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
          padding: "44px 24px",
          maxWidth: "420px",
          width: "100%",
          textAlign: "center",
          boxShadow: "0 24px 60px rgba(0,0,0,0.7)",
          border: "1px solid rgba(255,255,255,0.08)",
        }}>
        {/* Ikon Perayaan */}
        <div style={{ fontSize: "2.8rem", marginBottom: "16px" }}>🎉</div>

        {/* Judul Final */}
        <h2
          style={{
            fontSize: "1.45rem",
            fontWeight: 800,
            color: "#ffffff",
            marginBottom: "14px",
          }}>
          Data Foto Berhasil Disimpan!
        </h2>

        {/* Deskripsi dengan nama klien warna merah */}
        <p
          style={{
            fontSize: "0.85rem",
            color: "#d1d1d6",
            lineHeight: "1.5",
            marginBottom: "26px",
          }}>
          Terima Kasih Kak{" "}
          <strong style={{ color: "#e03828" }}>{clientName}</strong>. Foto
          pilihan Anda sudah tercatat di sistem Fotonic.
        </p>

        {/* Daftar Bernomor File Terpilih */}
        <div
          style={{
            backgroundColor: "#18181a",
            borderRadius: "16px",
            padding: "18px 20px",
            maxHeight: "220px",
            overflowY: "auto",
            textAlign: "left",
            border: "1px solid rgba(255,255,255,0.05)",
          }}>
          {selectedFileNames.map((name, i) => (
            <div
              key={i}
              style={{
                fontSize: "0.82rem",
                color: "#e4e4e7",
                marginBottom: "6px",
              }}>
              {i + 1}. {name}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
