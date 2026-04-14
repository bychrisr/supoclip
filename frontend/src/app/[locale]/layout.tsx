import type { Metadata } from "next";
import { NextIntlClientProvider } from "next-intl";
import { getMessages } from "@/i18n/get-messages";
import { AppLocale, intlLocaleByAppLocale, locales } from "@/i18n/config";
import { parseAppLocale } from "@/i18n/locale";

export async function generateMetadata({
  params,
}: {
  params: { locale: string };
}): Promise<Metadata> {
  const { locale } = params;
  const appLocale = parseAppLocale(locale);

  const title = "SupoClip";
  const descriptionByLocale: Record<AppLocale, string> = {
    pt: "Transforme vídeos longos em cortes prontos para viralizar.",
    en: "Turn long videos into viral-ready shorts.",
    es: "Convierte videos largos en shorts listos para viralizar.",
  };

  return {
    title,
    description: descriptionByLocale[appLocale],
    icons: {
      icon: "/icon.svg",
    },
    alternates: {
      languages: Object.fromEntries(
        (locales as readonly AppLocale[]).map((l) => [intlLocaleByAppLocale[l], `/${l}`]),
      ),
    },
  };
}

export default async function LocaleLayout({
  children,
  params,
}: Readonly<{
  children: React.ReactNode;
  params: { locale: string };
}>) {
  const { locale } = params;
  const appLocale = parseAppLocale(locale);

  const messages = await getMessages(appLocale);

  return (
    <NextIntlClientProvider locale={intlLocaleByAppLocale[appLocale]} messages={messages} timeZone="America/Sao_Paulo">
      {children}
    </NextIntlClientProvider>
  );
}

