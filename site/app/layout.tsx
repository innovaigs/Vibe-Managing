import type { Metadata } from 'next';
import { Geist, Geist_Mono } from 'next/font/google';
import './globals.css';

const geistSans = Geist({
  variable: '--font-geist-sans',
  subsets: ['latin'],
});

const geistMono = Geist_Mono({
  variable: '--font-geist-mono',
  subsets: ['latin'],
});

export const metadata: Metadata = {
  title: 'Vibe Managing — Founder Intent to Business Execution',
  description: 'An AI-native operating system that understands, diagnoses, plans, executes, monitors, and learns across the whole business.',
  openGraph: {
    title: 'Vibe Managing — Founder Intent to Business Execution',
    description: 'See the AI-native operating system for understanding, diagnosing, planning, executing, monitoring, and learning across the whole business.',
    images: ['https://raw.githubusercontent.com/innovaigs/Vibe-Managing/main/site/public/og.png'],
    type: 'website',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Vibe Managing — Founder Intent to Business Execution',
    description: 'The AI-native operating system for the whole business.',
    images: ['https://raw.githubusercontent.com/innovaigs/Vibe-Managing/main/site/public/og.png'],
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        {children}
      </body>
    </html>
  );
}
