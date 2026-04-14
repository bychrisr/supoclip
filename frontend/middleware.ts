import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

const LOCALES = ["pt", "en", "es"] as const;
type AppLocale = (typeof LOCALES)[number];

const PUBLIC_FILE = /\.(.*)$/;

export function middleware(request: NextRequest) {
  const isLandingOnlyModeEnabled =
    process.env.NEXT_PUBLIC_LANDING_ONLY_MODE === "true";

  if (!isLandingOnlyModeEnabled) {
    const { pathname } = request.nextUrl;

    // Skip API + static assets
    if (
      pathname.startsWith("/api") ||
      pathname.startsWith("/_next") ||
      PUBLIC_FILE.test(pathname)
    ) {
      return NextResponse.next();
    }

    const seg0 = pathname.split("/").filter(Boolean)[0];
    const hasLocale = !!seg0 && (LOCALES as readonly string[]).includes(seg0);
    if (!hasLocale) {
      const url = request.nextUrl.clone();
      url.pathname = `/pt${pathname === "/" ? "" : pathname}`;
      return NextResponse.redirect(url);
    }

    const res = NextResponse.next();
    res.headers.set("x-supoclip-locale", seg0 as AppLocale);
    return res;
  }

  const { pathname } = request.nextUrl;

  if (
    pathname === "/" ||
    pathname.startsWith("/_next") ||
    pathname.startsWith("/api/billing/webhook") ||
    PUBLIC_FILE.test(pathname)
  ) {
    return NextResponse.next();
  }

  if (pathname.startsWith("/api")) {
    return NextResponse.json(
      { error: "SupoClip is in landing-page-only mode." },
      { status: 503 }
    );
  }

  const url = request.nextUrl.clone();
  url.pathname = "/";
  url.search = "";
  return NextResponse.redirect(url);
}

export const config = {
  matcher: "/:path*",
};
