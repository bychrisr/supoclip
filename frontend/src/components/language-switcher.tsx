"use client";

import { useMemo } from "react";
import { Button } from "@/components/ui/button";
import { locales, localeLabels, type AppLocale } from "@/i18n/config";
import { isAppLocale } from "@/i18n/locale";
import { usePathname, useRouter } from "@/i18n/navigation";

function replaceLocaleInPath(pathname: string, nextLocale: AppLocale) {
  const segments = pathname.split("/").filter(Boolean);
  const current = segments[0];
  if (current && isAppLocale(current)) {
    segments[0] = nextLocale;
    return `/${segments.join("/")}`;
  }
  return `/${nextLocale}${pathname === "/" ? "" : pathname}`;
}

export function LanguageSwitcher({ className = "" }: { className?: string }) {
  const pathname = usePathname();
  const router = useRouter();

  const currentLocale = useMemo<AppLocale>(() => {
    const seg0 = pathname.split("/").filter(Boolean)[0];
    return (seg0 && isAppLocale(seg0) ? seg0 : "pt") as AppLocale;
  }, [pathname]);

  return (
    <div className={`flex items-center gap-1 ${className}`}>
      {(locales as readonly AppLocale[]).map((l) => {
        const active = l === currentLocale;
        return (
          <Button
            key={l}
            type="button"
            variant={active ? "default" : "outline"}
            size="sm"
            onClick={() => router.push(replaceLocaleInPath(pathname, l))}
            aria-pressed={active}
            className="h-8 px-2 text-xs"
          >
            {localeLabels[l]}
          </Button>
        );
      })}
    </div>
  );
}

