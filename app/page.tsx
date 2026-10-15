"use client";

import React, { Suspense, useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";
import WelcomeModal from "@/components/WelcomeModal";
import HeroBanner from "@/components/HeroBanner";
import ProgressBar from "@/components/ProgressBar";
import PhotoCard from "@/components/PhotoCard";
import PhotoModal from "@/components/PhotoModal";
import PreviewView from "@/components/PreviewView";
import SuccessModal from "@/components/Successmodal";

interface Photo {
  id: string;
  name: string;
  mimeType: string;
}

function GalleryContent() {
  const searchParams = useSearchParams();

  const clientName = searchParams.get("klien") || "Klien Fotonic";
  const folderId = searchParams.get("folder_id");
  const rawMax = searchParams.get("max");
  const parsedMax = Number(rawMax);
  const maxPhotos =
    !isNaN(parsedMax) && parsedMax > 0 && parsedMax <= 15 ? parsedMax : 15;

  const [photos, setPhotos] = useState<Photo[]>([]);
  const [selectedIds, setSelectedIds] = useState<string[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  // Status Tampilan: 'gallery' | 'preview' | 'success'
  const [currentView, setCurrentView] = useState<
    "gallery" | "preview" | "success"
  >("gallery");
  const [showWelcome, setShowWelcome] = useState(true);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submittedFileNames, setSubmittedFileNames] = useState<string[]>([]);
  const [notes, setNotes] = useState("");

  // Modal Lightbox Perbesar
  const [previewPhoto, setPreviewPhoto] = useState<{
    id: string;
    name: string;
  } | null>(null);

  useEffect(() => {
    if (!folderId) {
      setErrorMsg("Tautan belum menyertakan parameter folder Google Drive.");
      setIsLoading(false);
      return;
    }

    async function fetchPhotos() {
      try {
        const res = await fetch(`/api/photos?folder_id=${folderId}`);
        const data = await res.json();
        if (!res.ok) throw new Error(data.error || "Gagal mengambil foto.");
        setPhotos(data.photos || []);
      } catch (err: any) {
        setErrorMsg(err.message || "Gagal memuat foto dari Google Drive.");
      } finally {
        setIsLoading(false);
      }
    }

    fetchPhotos();
  }, [folderId]);

  const toggleSelect = (id: string) => {
    setSelectedIds((prev) => {
      if (prev.includes(id)) {
        return prev.filter((item) => item !== id);
      } else {
        if (prev.length >= maxPhotos) return prev;
        return [...prev, id];
      }
    });
  };

  const handleGoToPreview = () => {
    setCurrentView("preview");
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  const handleBackToGallery = () => {
    setCurrentView("gallery");
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  const handleSubmit = async () => {
    if (selectedIds.length === 0 || !folderId) return;
    setIsSubmitting(true);

    try {
      const res = await fetch("/api/submit", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          folderId,
          clientName,
          max: maxPhotos,
          selectedFileIds: selectedIds,
          notes,
        }),
      });

      const data = await res.json();
      if (!res.ok) throw new Error(data.error || "Gagal menyimpan seleksi.");

      setSubmittedFileNames(data.fileNames || []);
      setCurrentView("success");
    } catch (err: any) {
      alert(`Gagal menyimpan: ${err.message}`);
    } finally {
      setIsSubmitting(false);
    }
  };

  // Foto-foto yang sedang terpilih
  const selectedPhotosList = photos
    .filter((p) => selectedIds.includes(p.id))
    .map((p) => ({ id: p.id, name: p.name }));

  if (errorMsg) {
    return (
      <div
        style={{ padding: "80px 16px", textAlign: "center", color: "#f87171" }}>
        <h2 style={{ fontSize: "1.3rem", marginBottom: "8px" }}>Perhatian</h2>
        <p>{errorMsg}</p>
      </div>
    );
  }

  return (
    <div
      style={{
        backgroundColor: "#121214",
        minHeight: "100vh",
        paddingBottom: "100px",
      }}>
      {/* 1. Modal Sapaan Awal */}
      {showWelcome && (
        <WelcomeModal
          clientName={clientName}
          maxPhotos={maxPhotos}
          onStart={() => setShowWelcome(false)}
        />
      )}

      {/* 2. TAMPILAN 1: GALERI UTAMA */}
      {currentView === "gallery" && (
        <>
          <HeroBanner clientName={clientName} folderId={folderId} />
          <ProgressBar current={selectedIds.length} max={maxPhotos} />

          <div
            style={{ maxWidth: "1000px", margin: "0 auto", padding: "0 16px" }}>
            {isLoading ? (
              <div
                style={{
                  textAlign: "center",
                  padding: "60px 0",
                  color: "#a1a1aa",
                }}>
                Memuat foto dari Google Drive...
              </div>
            ) : photos.length === 0 ? (
              <div
                style={{
                  textAlign: "center",
                  padding: "60px 0",
                  color: "#a1a1aa",
                }}>
                Tidak ada foto yang ditemukan di folder ini.
              </div>
            ) : (
              <div
                style={{
                  display: "grid",
                  gridTemplateColumns: "repeat(auto-fill, minmax(280px, 1fr))",
                  gap: "20px",
                }}>
                {photos.map((photo) => (
                  <PhotoCard
                    key={photo.id}
                    id={photo.id}
                    name={photo.name}
                    isSelected={selectedIds.includes(photo.id)}
                    isDisabled={
                      selectedIds.length >= maxPhotos &&
                      !selectedIds.includes(photo.id)
                    }
                    onToggle={toggleSelect}
                    onPreview={(id, name) => setPreviewPhoto({ id, name })}
                  />
                ))}
              </div>
            )}
          </div>

          {/* Tombol Mengambang Konfirmasi ke Preview */}
          {selectedIds.length > 0 && (
            <div
              style={{
                position: "fixed",
                bottom: "20px",
                left: 0,
                right: 0,
                display: "flex",
                justifyContent: "center",
                zIndex: 9999,
                pointerEvents: "none",
              }}>
              <button
                onClick={handleGoToPreview}
                style={{
                  pointerEvents: "auto",
                  backgroundColor: "#dc3522",
                  color: "#ffffff",
                  border: "none",
                  borderRadius: "9999px",
                  padding: "14px 28px",
                  fontSize: "0.95rem",
                  fontWeight: 700,
                  cursor: "pointer",
                  display: "flex",
                  alignItems: "center",
                  gap: "10px",
                  boxShadow: "0 8px 24px rgba(220, 53, 34, 0.45)",
                }}>
                <span>
                  Konfirmasi ({selectedIds.length}/{maxPhotos})
                </span>
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
            </div>
          )}
        </>
      )}

      {/* 3. TAMPILAN 2: HALAMAN PRATINJAU FOTO TERPILIH */}
      {currentView === "preview" && (
        <PreviewView
          clientName={clientName}
          selectedPhotos={selectedPhotosList}
          maxPhotos={maxPhotos}
          notes={notes}
          onNotesChange={setNotes}
          isSubmitting={isSubmitting}
          onBackToGallery={handleBackToGallery}
          onConfirmSubmit={handleSubmit}
          onPreview={(id, name) => setPreviewPhoto({ id, name })}
        />
      )}

      {/* 4. TAMPILAN 3: HALAMAN SUKSES FINAL DENGAN TOMBOL WHATSAPP */}
      {currentView === "success" && (
        <SuccessModal
          clientName={clientName}
          selectedFileNames={submittedFileNames}
          notes={notes}
          adminWaNumber="6285783627177" // Masukkan nomor WhatsApp resmi Fotonic di sini
        />
      )}

      {/* 5. Modal Lightbox Pratinjau Perbesar Layar Penuh */}
      {previewPhoto && (
        <PhotoModal
          id={previewPhoto.id}
          name={previewPhoto.name}
          isSelected={selectedIds.includes(previewPhoto.id)}
          onClose={() => setPreviewPhoto(null)}
          onToggle={toggleSelect}
        />
      )}
    </div>
  );
}

export default function GalleryPage() {
  return (
    <Suspense
      fallback={
        <div
          style={{
            backgroundColor: "#121214",
            minHeight: "100vh",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            color: "#a1a1aa",
          }}>
          Memuat...
        </div>
      }>
      <GalleryContent />
    </Suspense>
  );
}
