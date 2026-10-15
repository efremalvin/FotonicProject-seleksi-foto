import type { Metadata } from "next";
import { Montserrat } from "next/font/google";

const montserrat = Montserrat({
  subsets: ["latin"],
  weight: ["400", "500", "600", "700", "800"],
  display: "swap",
});

export const metadata: Metadata = {
  title: "Fotonic - Seleksi Foto",
  description: "Aplikasi seleksi foto pelanggan Fotonic",
  icons: {
    icon: "/blacklogo2.png", // Mengambil langsung dari public/blacklogo2.png
    apple: "/blacklogo2.png", // Opsional: untuk pintasan layar utama perangkat iOS/Safari
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="id">
      <head>
        <style
          dangerouslySetInnerHTML={{
            __html: `
              * {
                box-sizing: border-box;
                margin: 0;
                padding: 0;
                font-family: inherit;
              }
              body {
                background-color: #121214;
                color: #f4f4f5;
                -webkit-font-smoothing: antialiased;
              }
              ::-webkit-scrollbar {
                width: 8px;
              }
              ::-webkit-scrollbar-thumb {
                background: #ff4b4b;
                border-radius: 8px;
              }
            `,
          }}
        />
      </head>
      <body className={montserrat.className}>{children}</body>
    </html>
  );
}
