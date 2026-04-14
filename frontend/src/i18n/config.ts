export const locales = ["pt", "en", "es"] as const;
export type AppLocale = (typeof locales)[number];

export const defaultLocale: AppLocale = "pt";

export const localeLabels: Record<AppLocale, string> = {
  pt: "PT",
  en: "EN",
  es: "ES",
};

export const intlLocaleByAppLocale: Record<AppLocale, string> = {
  pt: "pt-BR",
  en: "en",
  es: "es",
};

