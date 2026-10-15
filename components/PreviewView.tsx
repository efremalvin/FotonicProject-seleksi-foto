"use client";

import React from "react";

interface SelectedPhoto {
  id: string;
  name: string;
}

interface PreviewViewProps {
  clientName: string;
  selectedPhotos: SelectedPhoto[];
  maxPhotos: number;
  notes: string;
  onNotesChange: (notes: string) => void;
  isSubmitting: boolean;
  onBackToGallery: () => void;
  onConfirmSubmit: () => void;
  onPreview: (id: string, name: string) => void;
}

export default function PreviewView({
  clientName,
  selectedPhotos,
  maxPhotos,
  notes,
  onNotesChange,
  isSubmitting,
  onBackToGallery,
  onConfirmSubmit,
  onPreview,
}: PreviewViewProps) {
  return (
    <div
      style={{
        maxWidth: "880px",
        margin: "0 auto",
        padding: "24px 16px 80px 16px",
        animation: "fadeIn 0.28s ease-in-out",
      }}>
      {/* Header Halaman Pratinjau */}
      <div style={{ textAlign: "center", marginBottom: "28px" }}>
        <h1
          style={{
            fontSize: "1.65rem",
            fontWeight: 800,
            color: "#ffffff",
            marginBottom: "8px",
            letterSpacing: "-0.5px",
          }}>
          Tinjau Foto Terpilih
        </h1>
        <p style={{ fontSize: "0.9rem", color: "#9496a1", lineHeight: "1.5" }}>
          Pastikan foto-foto berikut adalah pilihan terbaik Anda sebelum dikirim
          ke tim editor Fotonic.
        </p>
        <div
          style={{
            marginTop: "12px",
            display: "inline-block",
            backgroundColor: "rgba(34, 197, 94, 0.15)",
            color: "#22c55e",
            border: "1px solid rgba(34, 197, 94, 0.3)",
            borderRadius: "9999px",
            padding: "4px 14px",
            fontSize: "0.82rem",
            fontWeight: 700,
          }}>
          Terpilih: {selectedPhotos.length} / {maxPhotos} Foto
        </div>
      </div>

      {/* Grid Galeri Foto Terpilih */}
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fill, minmax(260px, 1fr))",
          gap: "20px",
          marginBottom: "32px",
        }}>
        {selectedPhotos.map((photo) => (
          <div
            key={photo.id}
            style={{
              backgroundColor: "#16171e",
              borderRadius: "20px",
              padding: "10px",
              border: "1.5px solid #22c55e",
              boxShadow: "0 8px 24px rgba(0, 0, 0, 0.4)",
              position: "relative",
              display: "flex",
              flexDirection: "column",
            }}>
            {/* Foto Thumbnail */}
            <div
              style={{
                position: "relative",
                width: "100%",
                aspectRatio: "3/4",
                borderRadius: "14px",
                overflow: "hidden",
                backgroundColor: "#101117",
              }}>
              <img
                src={`/api/thumbnail?id=${photo.id}`}
                alt={photo.name}
                loading="lazy"
                style={{
                  width: "100%",
                  height: "100%",
                  objectFit: "cover",
                  display: "block",
                }}
              />
              {/* Tombol Perbesar Pratinjau */}
              <button
                onClick={() => onPreview(photo.id, photo.name)}
                title="Lihat Pratinjau Penuh"
                style={{
                  position: "absolute",
                  top: "10px",
                  right: "10px",
                  backgroundColor: "rgba(0, 0, 0, 0.65)",
                  color: "#ffffff",
                  border: "none",
                  borderRadius: "8px",
                  width: "32px",
                  height: "32px",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  cursor: "pointer",
                  backdropFilter: "blur(4px)",
                }}>
                ⛶
              </button>
            </div>

            {/* Info Nama & Badge Terpilih */}
            <div
              style={{
                display: "flex",
                alignItems: "center",
                justifyContent: "space-between",
                padding: "12px 6px 4px 6px",
              }}>
              <span
                style={{
                  fontSize: "0.82rem",
                  fontWeight: 700,
                  color: "#e2e4ea",
                  whiteSpace: "nowrap",
                  overflow: "hidden",
                  textOverflow: "ellipsis",
                  maxWidth: "65%",
                }}>
                {photo.name}
              </span>
              <span
                style={{
                  fontSize: "0.78rem",
                  fontWeight: 700,
                  color: "#22c55e",
                  display: "flex",
                  alignItems: "center",
                  gap: "4px",
                }}>
                ✓ Terpilih
              </span>
            </div>
          </div>
        ))}
      </div>

      {/* Kotak Catatan Tambahan (Opsional) Sesuai HTML */}
      <div
        style={{
          backgroundColor: "#16171e",
          border: "1px solid rgba(255, 255, 255, 0.08)",
          borderRadius: "18px",
          padding: "20px",
          marginBottom: "32px",
        }}>
        <label
          htmlFor="edit-notes"
          style={{
            display: "block",
            fontSize: "0.92rem",
            fontWeight: 700,
            color: "#ffffff",
            marginBottom: "8px",
          }}>
          📝 Catatan Tambahan untuk Editor (Opsional):
        </label>
        <textarea
          id="edit-notes"
          value={notes}
          onChange={(e) => onNotesChange(e.target.value)}
          placeholder="Contoh: Mohon bersihkan background pada DSC_0003, tone warna dibuat warm tone seperti portofolio Instagram."
          style={{
            width: "100%",
            minHeight: "100px",
            padding: "12px 14px",
            backgroundColor: "#101117",
            border: "1px solid rgba(255, 255, 255, 0.12)",
            borderRadius: "12px",
            color: "#f4f4f6",
            fontSize: "0.88rem",
            lineHeight: "1.5",
            outline: "none",
            resize: "vertical",
          }}
        />
      </div>

      {/* Bagian Tombol Aksi: Group 13.jpg & Konfirmasi.jpg */}
      <div
        style={{
          display: "flex",
          flexDirection: "row",
          gap: "14px",
          alignItems: "center",
        }}>
        {/* Tombol Ubah Pilihan di Galeri (Sesuai Group 13.jpg) */}
        <button
          onClick={onBackToGallery}
          disabled={isSubmitting}
          style={{
            flex: 1,
            backgroundColor: "#1f1f21",
            color: "#ffffff",
            border: "1px solid rgba(255, 255, 255, 0.14)",
            borderRadius: "16px",
            padding: "14px 18px",
            cursor: isSubmitting ? "not-allowed" : "pointer",
            textAlign: "center",
            lineHeight: "1.35",
            transition: "all 0.2s ease",
            boxShadow: "0 4px 14px rgba(0,0,0,0.4)",
          }}>
          <div style={{ fontSize: "0.88rem", fontWeight: 700 }}>
            Ubah Pilihan di
          </div>
          <div
            style={{ fontSize: "0.88rem", fontWeight: 700, marginTop: "2px" }}>
            ← Galeri
          </div>
        </button>

        {/* Tombol Konfirmasi (Sesuai Konfirmasi.jpg) */}
        <button
          onClick={onConfirmSubmit}
          disabled={isSubmitting}
          style={{
            flex: 1.3,
            backgroundColor: isSubmitting ? "#5c3734" : "#dc3522",
            color: "#ffffff",
            border: "none",
            borderRadius: "9999px",
            padding: "16px 24px",
            fontSize: "0.98rem",
            fontWeight: 800,
            cursor: isSubmitting ? "not-allowed" : "pointer",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            gap: "12px",
            boxShadow: "0 6px 20px rgba(220, 53, 34, 0.45)",
            transition: "all 0.2s ease",
          }}>
          <span>{isSubmitting ? "Menyimpan Data..." : "Konfirmasi"}</span>
          <span
            style={{
              backgroundColor: "#ffffff",
              color: "#dc3522",
              borderRadius: "50%",
              width: "24px",
              height: "24px",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              fontSize: "0.85rem",
              fontWeight: 900,
            }}>
            ✓
          </span>
        </button>
      </div>
    </div>
  );
}
