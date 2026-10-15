"use client";

import React from "react";

interface WelcomeModalProps {
  clientName: string;
  maxPhotos: number;
  onStart: () => void;
}

export default function WelcomeModal({
  clientName,
  maxPhotos,
  onStart,
}: WelcomeModalProps) {
  return (
    <div
      style={{
        position: "fixed",
        inset: 0,
        backgroundColor: "rgba(10, 10, 12, 0.88)",
        backdropFilter: "blur(8px)",
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
          padding: "36px 24px",
          maxWidth: "400px",
          width: "100%",
          textAlign: "center",
          boxShadow: "0 20px 40px rgba(0,0,0,0.6)",
          border: "1px solid rgba(255,255,255,0.08)",
        }}>
        {/* Logo Fotonic */}
        <div style={{ marginBottom: "20px" }}>
          <img
            src="/whitelogo1.png"
            alt="Fotonic Photo & Video Project"
            style={{
              maxWidth: "150px",
              height: "auto",
              margin: "0 auto",
              display: "block",
            }}
          />
        </div>

        {/* Heading Sapaan */}
        <h2
          style={{
            fontSize: "1.45rem",
            fontWeight: 800,
            color: "#ffffff",
            marginBottom: "12px",
          }}>
          Halo, Kak <span style={{ color: "#e03828" }}>{clientName}</span>! ✨
        </h2>

        {/* Deskripsi */}
        <p
          style={{
            fontSize: "0.85rem",
            color: "#d1d1d6",
            lineHeight: "1.5",
            marginBottom: "22px",
          }}>
          Selamat datang diplatform seleksi Fotonic
          <br />
          Silahkan tentukan foto-foto terbaik Anda yang akan diproses ke tahap
          retouch & color grading.
        </p>

        {/* Kotak Ketentuan */}
        <div
          style={{
            backgroundColor: "#1c1c1e",
            borderRadius: "16px",
            padding: "16px",
            textAlign: "left",
            marginBottom: "26px",
            border: "1px solid rgba(255,255,255,0.05)",
          }}>
          <div
            style={{
              fontSize: "0.85rem",
              fontWeight: 700,
              color: "#ffffff",
              marginBottom: "10px",
            }}>
            📌 Ketentuan Pemilihan :
          </div>
          <ul
            style={{
              fontSize: "0.78rem",
              color: "#a1a1aa",
              lineHeight: "1.6",
              paddingLeft: "16px",
              margin: 0,
            }}>
            <li>
              Kuota foto sesi ini{" "}
              <strong style={{ color: "#e03828" }}>{maxPhotos} Foto</strong>
            </li>
            <li>Klik foto untuk memilih atau membatalkan pilihan Anda.</li>
            <li>
              Periksa kembali daftar foto terpilih sebelum mengunci pilihan
              final.
            </li>
          </ul>
        </div>

        {/* Tombol Mulai Pilih Foto */}
        <button
          onClick={onStart}
          style={{
            width: "100%",
            backgroundColor: "#dc3522",
            color: "#ffffff",
            border: "none",
            borderRadius: "9999px",
            padding: "14px 20px",
            fontSize: "0.95rem",
            fontWeight: 700,
            cursor: "pointer",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            gap: "8px",
            transition: "all 0.2s ease",
            boxShadow: "0 6px 16px rgba(220, 53, 34, 0.4)",
          }}
          onMouseEnter={(e) =>
            (e.currentTarget.style.backgroundColor = "#e27468")
          }
          onMouseLeave={(e) =>
            (e.currentTarget.style.backgroundColor = "#dc3522")
          }>
          <span>Mulai Pilih Foto</span>
          <span style={{ fontSize: "1.1rem" }}>→</span>
        </button>
      </div>
    </div>
  );
}
