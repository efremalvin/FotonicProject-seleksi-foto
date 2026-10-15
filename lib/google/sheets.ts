import { sheetsClient } from "./auth";

const spreadsheetId = process.env.GOOGLE_SPREADSHEET_ID;

export interface SelectionSubmission {
  clientName: string;
  selectedFileNames: string[];
}

export async function appendSelectionToSheet(
  submission: SelectionSubmission,
): Promise<void> {
  if (!spreadsheetId) {
    throw new Error("GOOGLE_SPREADSHEET_ID belum dikonfigurasi.");
  }

  // Format timestamp YYYY-MM-DD HH:MM:SS
  const now = new Date();
  const pad = (n: number) => n.toString().padStart(2, "0");
  const waktu = `${now.getFullYear()}-${pad(now.getMonth() + 1)}-${pad(now.getDate())} ${pad(now.getHours())}:${pad(now.getMinutes())}:${pad(now.getSeconds())}`;

  // Format daftar nama file dengan pemisah baris baru koma (persis seperti data asli)
  const daftarFileStr = submission.selectedFileNames.sort().join(",\n");

  const row = [
    waktu,
    submission.clientName,
    "Selesai",
    submission.selectedFileNames.length,
    daftarFileStr,
  ];

  try {
    await sheetsClient.spreadsheets.values.append({
      spreadsheetId,
      range: "Sheet1!A:E",
      valueInputOption: "USER_ENTERED",
      requestBody: {
        values: [row],
      },
    });
  } catch (error) {
    console.error("Gagal mencatat seleksi ke Google Sheets:", error);
    throw new Error("Gagal menyimpan hasil seleksi ke spreadsheet.");
  }
}
