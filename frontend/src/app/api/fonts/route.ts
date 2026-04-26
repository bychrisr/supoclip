import { headers } from "next/headers";
import { NextResponse } from "next/server";

import { auth } from "@/lib/auth";
import { buildBackendAuthHeaders } from "@/lib/backend-auth";

export async function GET(request: Request) {
  const session = await auth.api.getSession({ headers: await headers() });
  
  // Fallback: Check for user_id header if session is not available (useful for some client-side environments)
  const clientUserId = (await headers()).get("user_id");
  const userId = session?.user?.id || clientUserId;

  if (!userId) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const apiUrl =
    process.env.BACKEND_INTERNAL_URL ||
    process.env.NEXT_PUBLIC_API_URL ||
    "http://localhost:8000";
  const normalizedApiUrl = apiUrl.replace(/\/$/, "");
  const backendAuthHeaders = buildBackendAuthHeaders(userId);

  let upstream = await fetch(`${normalizedApiUrl}/fonts`, {
    headers: {
      ...backendAuthHeaders,
    },
    cache: "no-store",
  });

  if (upstream.status === 404) {
    upstream = await fetch(`${normalizedApiUrl}/api/fonts`, {
      headers: {
        ...backendAuthHeaders,
      },
      cache: "no-store",
    });
  }

  const responseText = await upstream.text();
  return new NextResponse(responseText, {
    status: upstream.status,
    headers: {
      "Content-Type": upstream.headers.get("content-type") || "application/json",
    },
  });
}
