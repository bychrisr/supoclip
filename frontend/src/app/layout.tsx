import type { Metadata } from "next";
import { Geist, Geist_Mono, Syne } from "next/font/google";
import "./globals.css";
import { Toaster } from "@/components/ui/sonner";
import { FeedbackButton } from "@/components/feedback-button";
import { NextIntlClientProvider } from "next-intl";
import { getMessages } from "@/i18n/get-messages";
import { intlLocaleByAppLocale } from "@/i18n/config";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

const syne = Syne({
  variable: "--font-syne",
  subsets: ["latin"],
  weight: ["400", "500", "600", "700", "800"],
});

export const metadata: Metadata = {
  title: "SupoClip",
  description: "Turn long videos into viral-ready shorts.",
  icons: {
    icon: "/icon.svg",
  },
};

export default async function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const messages = await getMessages("pt");
  return (
    <html lang="pt-BR">
      <body
        className={`${geistSans.variable} ${geistMono.variable} ${syne.variable} antialiased`}
      >
        <NextIntlClientProvider
          locale={intlLocaleByAppLocale.pt}
          messages={messages}
          timeZone="America/Sao_Paulo"
        >
          {children}
        </NextIntlClientProvider>
        <FeedbackButton />
        <Toaster />
      </body>
    </html>
  );
}
