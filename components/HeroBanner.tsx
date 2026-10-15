"use client";

import React from "react";
import { Tangerine } from "next/font/google";

const tangerine = Tangerine({
  weight: ["400", "700"],
  subsets: ["latin"],
  display: "swap",
});

interface HeroBannerProps {
  clientName: string;
  folderId?: string | null;
  bannerPhotoUrl?: string;
}

export default function HeroBanner({
  clientName,
  folderId,
  bannerPhotoUrl,
}: HeroBannerProps) {
  const bannerSrc =
    bannerPhotoUrl ||
    (folderId ? `/api/banner?folder_id=${folderId}` : "/api/banner");

  return (
    <div
      style={{
        position: "relative",
        width: "100%",
        height: "300px",
        borderRadius: "0 0 28px 28px",
        overflow: "hidden",
        marginBottom: "20px",
      }}>
      <img
        src={bannerSrc}
        alt={`Banner ${clientName}`}
        style={{ width: "100%", height: "100%", objectFit: "cover" }}
      />
      <div
        style={{
          position: "absolute",
          inset: 0,
          background:
            "linear-gradient(to bottom, rgba(0,0,0,0.2) 0%, rgba(18,18,20,0.95) 100%)",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "flex-end",
          paddingBottom: "24px",
          textAlign: "center",
        }}>
        <h1
          style={{
            fontSize: "1.6rem",
            fontWeight: 800,
            color: "#ffffff",
            letterSpacing: "-0.5px",
            marginBottom: "4px",
          }}>
          Wisuda - {clientName}
        </h1>
        <p
          style={{
            fontSize: "0.8rem",
            color: "#a1a1aa",
            marginBottom: "10px",
          }}>
          Sesi Foto Fotonic
        </p>
        <a
          href="https://instagram.com/fotonicproject"
          target="_blank"
          rel="noopener noreferrer"
          style={{
            display: "inline-flex",
            alignItems: "center",
            gap: "8px",
            backgroundColor: "rgba(0, 0, 0, 0.5)",
            border: "1px solid rgba(255, 255, 255, 0.2)",
            borderRadius: "9999px",
            padding: "4px 16px",
            textDecoration: "none",
            backdropFilter: "blur(4px)",
          }}>
          {/* Logo Vektor Resmi Instagram */}
          <svg
            width="14"
            height="14"
            viewBox="0 0 24 24"
            fill="none"
            stroke="#ffffff"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
            style={{ display: "block" }}
          >
            <rect width="20" height="20" x="2" y="2" rx="5" ry="5" />
            <path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z" />
            <line x1="17.5" x2="17.51" y1="6.5" y2="6.5" />
          </svg>
          <span
            className={tangerine.className}
            style={{
              fontSize: "1.45rem",
              fontWeight: 700,
              color: "#f4f4f5",
              lineHeight: 1,
              letterSpacing: "0.5px",
            }}>
            @fotonicproject
          </span>
        </a>
      </div>
    </div>
  );
}
