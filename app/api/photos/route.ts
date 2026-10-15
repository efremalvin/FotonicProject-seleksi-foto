import { NextRequest, NextResponse } from "next/server";
import { getPhotosFromFolder } from "@/lib/google/drive";

export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url);
  const folderId = searchParams.get("folder_id");

  if (!folderId) {
    return NextResponse.json(
      { error: "Parameter folder_id wajib disertakan" },
      { status: 400 },
    );
  }

  try {
    const photos = await getPhotosFromFolder(folderId);
    return NextResponse.json({ success: true, photos });
  } catch (error: any) {
    return NextResponse.json(
      { error: error.message || "Gagal mengambil daftar foto" },
      { status: 500 },
    );
  }
}
