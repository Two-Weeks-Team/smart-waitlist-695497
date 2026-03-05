import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Smart Waitlist | Host Queue Dashboard",
  description:
    "Replace paper queues with AI ETA prediction, no-show risk alerts, and SMS-ready waitlist operations.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
