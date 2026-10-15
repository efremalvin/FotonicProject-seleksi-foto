import { driveClient } from "./auth";
import type { drive_v3 } from "googleapis";

export interface DrivePhoto {
  id: string;
  name: string;
  mimeType: string;
  thumbnailLink?: string;
}

export async function getPhotosFromFolder(
  folderId: string,
): Promise<DrivePhoto[]> {
  try {
    const query = `'${folderId}' in parents and mimeType contains 'image/' and trashed = false`;
    const response = await driveClient.files.list({
      q: query,
      fields: "files(id, name, mimeType, thumbnailLink)",
      pageSize: 500,
      orderBy: "name",
    });

    const files: drive_v3.Schema$File[] = response.data.files || [];
    const validPhotos: DrivePhoto[] = [];

    for (const file of files) {
      if (file.id && file.name && file.mimeType) {
        validPhotos.push({
          id: file.id,
          name: file.name,
          mimeType: file.mimeType,
          thumbnailLink: file.thumbnailLink || undefined,
        });
      }
    }

    return validPhotos;
  } catch (error) {
    console.error("Gagal mengambil daftar foto dari Drive:", error);
    throw new Error("Gagal membaca folder Google Drive.");
  }
}

export async function getBannerPhoto(
  parentFolderId: string,
): Promise<DrivePhoto | null> {
  try {
    const folderQuery = `'${parentFolderId}' in parents and mimeType = 'application/vnd.google-apps.folder' and name = 'Cover' and trashed = false`;
    const folderRes = await driveClient.files.list({
      q: folderQuery,
      fields: "files(id, name)",
      pageSize: 1,
    });

    const coverFolder = folderRes.data.files?.[0];
    const targetFolderId = coverFolder?.id ? coverFolder.id : parentFolderId;

    const photos = await getPhotosFromFolder(targetFolderId);
    return photos.length > 0 ? photos[0] : null;
  } catch (error) {
    console.error("Gagal mendeteksi foto banner:", error);
    return null;
  }
}
