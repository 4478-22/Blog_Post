// src/app/layout.tsx
import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

import Header from "@/components/Header";
import Footer from "@/components/Footer";
import { ToastProvider } from "@/components/Toast";
import ClientHydrate from "@/components/ClientHydrate"; // ✅ new client-only wrapper

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Socially",
  description: "A modern social/blogging platform built with Next.js",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} font-sans bg-background text-foreground antialiased min-h-screen flex flex-col`}
      >
        <ToastProvider>
          {/* Global Header */}
          <Header />

          {/* Main Page Content */}
          <main className="flex-1 container mx-auto px-4">
            <ClientHydrate>{children}</ClientHydrate>
          </main>

          {/* Global Footer */}
          <Footer />
        </ToastProvider>
      </body>
    </html>
  );
}
