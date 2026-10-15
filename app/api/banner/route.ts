import { NextRequest, NextResponse } from "next/server";
import { driveClient } from "@/lib/google/auth";
import { getBannerPhoto } from "@/lib/google/drive";
import { Readable } from "stream";

export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url);
  const folderId = searchParams.get("folder_id") || process.env.BANNER_FOLDER_ID;

  if (!folderId) {
    return NextResponse.json(
      { error: "Parameter folder_id belum ditentukan." },
      { status: 400 }
    );
  }

  try {
    const bannerFile = await getBannerPhoto(folderId);

    if (!bannerFile) {
      return NextResponse.json(
        { error: "Foto banner tidak ditemukan di folder Cover maupun folder utama." },
        { status: 404 }
      );
    }

    const res = await driveClient.files.get(
      { fileId: bannerFile.id, alt: "media" },
      { responseType: "stream" }
    );

    const stream = res.data as unknown as Readable;
    const contentType = (res.headers["content-type"] as string) || "image/jpeg";

    const webStream = new ReadableStream({
      start(controller) {
        stream.on("data", (chunk) => controller.enqueue(chunk));
        stream.on("end", () => controller.close());
        stream.on("error", (err) => controller.error(err));
      },
    });

    return new NextResponse(webStream, {
      headers: {
        "Content-Type": contentType,
        "Cache-Control": "public, max-age=86400, stale-while-revalidate=43200",
      },
    });
  } catch (error: any) {
    console.error("Gagal memuat gambar banner:", error);
    return NextResponse.json(
      { error: "Gagal mengambil gambar banner dari Google Drive." },
      { status: 500 }
    );
  }
}