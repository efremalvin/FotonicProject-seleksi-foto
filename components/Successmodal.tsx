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
  adminWaNumber = "6281234567890", // Ganti dengan nomor WhatsApp Admin Fotonic (awali kode negara tanpa tanda +)
}: SuccessModalProps) {
  // Susun daftar file bernomor urut
  const fileListText = selectedFileNames
    .map((name, index) => `${index + 1}. ${name}`)
    .join("\n");

  const notesText = notes ? `\n\nCatatan Editing:\n"${notes}"` : "";

  // Pesan WhatsApp sesuai format dokumen referensi
  const message = `Halo Tim Fotonic, saya ${clientName}.\nSaya telah selesai memilih ${selectedFileNames.length} foto untuk sesi editing:\n\n${fileListText}${notesText}\n\nMohon dicek ya, terima kasih!`;

  const waUrl = `https://wa.me/${adminWaNumber}?text=${encodeURIComponent(message)}`;

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
        {/* Ikon Perayaan */}
        <div style={{ fontSize: "2.8rem", marginBottom: "12px" }}>🎉</div>

        {/* Judul Final */}
        <h2
          style={{
            fontSize: "1.45rem",
            fontWeight: 800,
            color: "#ffffff",
            marginBottom: "12px",
          }}>
          Data Foto Berhasil Disimpan!
        </h2>

        {/* Sapaan Klien */}
        <p
          style={{
            fontSize: "0.85rem",
            color: "#d1d1d6",
            lineHeight: "1.5",
            marginBottom: "20px",
          }}>
          Terima Kasih Kak{" "}
          <strong style={{ color: "#e03828" }}>{clientName}</strong>. Foto
          pilihan Anda sudah tercatat di sistem Fotonic[cite: 8].
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

        {/* Kotak Petunjuk Langkah Terakhir */}
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
            marginBottom: "22px",
          }}>
          <strong style={{ color: "#93c5fd" }}>⚠️ Langkah Terakhir:</strong>
          <br />
          Harap konfirmasi ke Admin Fotonic via WhatsApp agar tim editor dapat
          langsung memvalidasi foto dan memulai proses retouch editing.
        </div>

        {/* Tombol Konfirmasi WhatsApp */}
        <a
          href={waUrl}
          target="_blank"
          rel="noopener noreferrer"
          style={{
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            gap: "10px",
            backgroundColor: "#22c55e",
            color: "#ffffff",
            textDecoration: "none",
            borderRadius: "9999px",
            padding: "15px 24px",
            fontSize: "0.95rem",
            fontWeight: 700,
            boxShadow: "0 6px 20px rgba(34, 197, 94, 0.35)",
            transition: "all 0.2s ease",
          }}
          onMouseEnter={(e) =>
            (e.currentTarget.style.backgroundColor = "#16a34a")
          }
          onMouseLeave={(e) =>
            (e.currentTarget.style.backgroundColor = "#22c55e")
          }>
          {/* Ikon Vektor WhatsApp */}
          <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
            <path d="M12.031 6.172c-3.181 0-5.767 2.586-5.768 5.766-.001 1.298.38 2.27 1.019 3.287l-.582 2.128 2.182-.573c.978.58 1.911.928 3.145.929 3.178 0 5.767-2.587 5.768-5.766.001-3.187-2.575-5.77-5.764-5.771zm3.392 8.244c-.144.405-.837.774-1.17.824-.312.045-.694.062-2.108-.528-1.795-.749-2.951-2.576-3.04-2.695-.089-.12-1.04-1.385-1.04-2.641 0-1.256.657-1.874.891-2.129.234-.255.51-.318.68-.318.17 0 .34.002.489.009.158.007.369-.06.577.44.213.511.727 1.77.791 1.9.064.13.107.283.021.454-.085.171-.128.277-.255.426-.128.149-.27.332-.385.446-.128.127-.261.265-.112.521.149.255.661 1.091 1.417 1.765.972.866 1.792 1.134 2.047 1.262.255.128.404.106.553-.064.149-.17.638-.745.808-.999.17-.255.34-.213.574-.128.234.085 1.488.701 1.743.829.255.128.425.191.489.298.064.106.064.617-.08 1.022z" />
          </svg>
          <span>Konfirmasi ke WhatsApp Admin</span>
        </a>
      </div>
    </div>
  );
}
