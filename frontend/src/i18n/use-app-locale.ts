"use client";

import { useMemo } from "react";
import { type AppLocale, defaultLocale } from "@/i18n/config";
import { isAppLocale } from "@/i18n/locale";
import { usePathname } from "@/i18n/navigation";

export function useAppLocale(): AppLocale {
  const pathname = usePathname();
  return useMemo(() => {
    const seg0 = pathname.split("/").filter(Boolean)[0];
    return (seg0 && isAppLocale(seg0) ? seg0 : defaultLocale) as AppLocale;
  }, [pathname]);
}

