import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Octohedra",
  description: "Fractal geometry generator - create and 3D print octahedral fractals",
  metadataBase: new URL("https://www.octohedra.com"),
  openGraph: {
    title: "Octohedra",
    description: "Fractal geometry generator - create and 3D print octahedral fractals",
    url: "https://www.octohedra.com",
    siteName: "Octohedra",
    type: "website",
  },
  twitter: {
    card: "summary_large_image",
    title: "Octohedra",
    description: "Fractal geometry generator - create and 3D print octahedral fractals",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        {children}
      </body>
    </html>
  );
}
