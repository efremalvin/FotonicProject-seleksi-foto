import { NextRequest, NextResponse } from "next/server";
import { driveClient } from "@/lib/google/auth";

export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url);
  const fileId = searchParams.get("id");

  if (!fileId) {
    return NextResponse.json({ error: "File ID wajib disertakan" }, { status: 400 });
  }

  try {
    // 1. Ambil URL thumbnail resmi dari metadata file
    const meta = await driveClient.files.get({
      fileId,
      fields: "thumbnailLink",
    });

    let thumbUrl = meta.data.thumbnailLink;

    if (thumbUrl) {
      // Ubah resolusi bawaan (=s220) menjadi lebar 600px (=w600) agar tajam namun sangat ringan (< 100 KB)
      thumbUrl = thumbUrl.replace(/=s\d+$/, "=w600");

      const response = await fetch(thumbUrl);
      const buffer = await response.arrayBuffer();
      const contentType = response.headers.get("content-type") || "image/jpeg";

      return new NextResponse(buffer, {
        headers: {
          "Content-Type": contentType,
          "Cache-Control": "public, max-age=604800, stale-while-revalidate=86400",
        },
      });
    }

    // Fallback jika Google Drive belum selesai memproses thumbnail
    const res = await driveClient.files.get(
      { fileId, alt: "media" },
      { responseType: "arraybuffer" }
    );

    return new NextResponse(res.data as ArrayBuffer, {
      headers: {
        "Content-Type": "image/jpeg",
        "Cache-Control": "public, max-age=604800",
      },
    });
  } catch (error) {
    console.error("Error streaming thumbnail:", error);
    return NextResponse.json({ error: "Gagal memuat gambar" }, { status: 500 });
  }
}