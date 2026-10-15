import { google } from "googleapis";

const email = process.env.GOOGLE_SERVICE_ACCOUNT_EMAIL;
const rawKey = process.env.GOOGLE_PRIVATE_KEY;

if (!email || !rawKey) {
  throw new Error(
    "Kredensial Service Account Google belum dikonfigurasi di environment variables.",
  );
}

const privateKey = rawKey.replace(/\\n/g, "\n");

export const googleAuth = new google.auth.JWT({
  email,
  key: privateKey,
  scopes: [
    "https://www.googleapis.com/auth/drive.readonly",
    "https://www.googleapis.com/auth/spreadsheets",
  ],
});

export const driveClient = google.drive({ version: "v3", auth: googleAuth });
export const sheetsClient = google.sheets({ version: "v4", auth: googleAuth });
