import type { Metadata, Viewport } from "next";
import "./globals.css";
import { AppShell } from "@/components/layout/app-shell";

export const metadata: Metadata = {
  title: {
    default: "MedInsight AI",
    template: "%s · MedInsight AI",
  },
  description:
    "Understand your medical lab reports. Informational only, not a diagnosis.",
};

export const viewport: Viewport = {
  themeColor: "#0e2238",
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html lang="en" className="h-full antialiased">
      <body className="min-h-dvh font-sans">
        <AppShell>{children}</AppShell>
      </body>
    </html>
  );
}
