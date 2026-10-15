import { NextRequest, NextResponse } from "next/server";
import { getPhotosFromFolder } from "@/lib/google/drive";
import { appendSelectionToSheet } from "@/lib/google/sheets";

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { folderId, clientName, max, selectedFileIds, notes } = body;

    if (!folderId || !selectedFileIds || !Array.isArray(selectedFileIds)) {
      return NextResponse.json(
        { error: "Format permintaan tidak valid" },
        { status: 400 },
      );
    }

    const parsedMax = Number(max);
    const effectiveMax =
      !isNaN(parsedMax) && parsedMax > 0 && parsedMax <= 15 ? parsedMax : 15;
    const selectedCount = selectedFileIds.length;

    if (selectedCount < 1) {
      return NextResponse.json(
        { error: "Pilih minimal 1 foto sebelum mengirim seleksi." },
        { status: 400 },
      );
    }

    if (selectedCount > effectiveMax) {
      return NextResponse.json(
        {
          error: `Jumlah foto yang dipilih (${selectedCount}) melebihi batas maksimum (${effectiveMax}).`,
        },
        { status: 400 },
      );
    }

    const photosInFolder = await getPhotosFromFolder(folderId);
    const photoMap = new Map(photosInFolder.map((p) => [p.id, p.name]));

    const resolvedFileNames: string[] = [];
    for (const fileId of selectedFileIds) {
      const fileName = photoMap.get(fileId);
      if (!fileName) {
        return NextResponse.json(
          { error: `File tidak valid atau tidak ditemukan dalam folder ini.` },
          { status: 400 },
        );
      }
      resolvedFileNames.push(fileName);
    }

    await appendSelectionToSheet({
      clientName: clientName || "Klien Fotonic",
      selectedFileNames: resolvedFileNames,
      notes: typeof notes === "string" ? notes.trim() : undefined,
    });

    return NextResponse.json({
      success: true,
      message: "Seleksi berhasil disimpan",
      count: resolvedFileNames.length,
      fileNames: resolvedFileNames,
    });
  } catch (error: any) {
    console.error("Submission error:", error);
    return NextResponse.json(
      {
        error:
          error.message ||
          "Terjadi kesalahan pada server saat memproses seleksi.",
      },
      { status: 500 },
    );
  }
}
