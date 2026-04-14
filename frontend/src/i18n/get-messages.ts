import "server-only";

import { AppLocale } from "@/i18n/config";

interface Messages {
  [key: string]: string | Messages;
}

async function loadMessages(locale: AppLocale): Promise<Messages> {
  switch (locale) {
    case "pt":
      return (await import("@/i18n/messages/pt.json")).default as Messages;
    case "es":
      return (await import("@/i18n/messages/es.json")).default as Messages;
    case "en":
    default:
      return (await import("@/i18n/messages/en.json")).default as Messages;
  }
}

function mergeDeep(base: Messages, override: Messages): Messages {
  const out: Messages = { ...base };
  for (const [key, value] of Object.entries(override)) {
    const existing = out[key];
    if (
      value &&
      typeof value === "object" &&
      !Array.isArray(value) &&
      existing &&
      typeof existing === "object" &&
      !Array.isArray(existing)
    ) {
      out[key] = mergeDeep(existing as Messages, value as Messages);
    } else {
      out[key] = value as Messages[string];
    }
  }
  return out;
}

export async function getMessages(locale: AppLocale): Promise<Messages> {
  // en is the fallback base; pt/es override it.
  const en = await loadMessages("en");
  if (locale === "en") return en;
  const specific = await loadMessages(locale);
  return mergeDeep(en, specific);
}

