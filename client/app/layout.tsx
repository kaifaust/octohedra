import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Octohedra",
  description: "Fractal geometry generator - create and 3D print octahedral fractals",
  metadataBase: new URL("https://octohedra.com"),
  openGraph: {
    title: "Octohedra",
    description: "Fractal geometry generator - create and 3D print octahedral fractals",
    url: "https://octohedra.com",
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
      <body className="font-sans antialiased">
        {children}
      </body>
    </html>
  );
}
