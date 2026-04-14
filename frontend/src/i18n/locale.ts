import { AppLocale, defaultLocale, locales } from "@/i18n/config";

export function isAppLocale(value: string): value is AppLocale {
  return (locales as readonly string[]).includes(value);
}

export function parseAppLocale(value: string | undefined): AppLocale {
  if (!value) return defaultLocale;
  return isAppLocale(value) ? value : defaultLocale;
}

