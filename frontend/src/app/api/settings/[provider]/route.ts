import { headers } from "next/headers";
import { NextResponse } from "next/server";

import { auth } from "@/lib/auth";
import { buildBackendAuthHeaders } from "@/lib/backend-auth";

export async function PATCH(
  request: Request,
  context: { params: Promise<{ provider: string }> }
) {
  const { provider } = await context.params;
  const session = await auth.api.getSession({ headers: await headers() });
  
  const userId = session?.user?.id || (await headers()).get("user_id");
  if (!userId) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const apiUrl = process.env.BACKEND_INTERNAL_URL || "http://supoclip-backend:8000";
  const normalizedApiUrl = apiUrl.replace(/\/$/, "");
  
  const body = await request.text();

  try {
    const upstream = await fetch(`${normalizedApiUrl}/users/me/youtube-cookies`, {
      method: "PATCH",
      headers: {
        ...buildBackendAuthHeaders(userId),
        "Content-Type": "text/plain",
        "X-Provider": provider, // Repassando o provedor para o backend real
      },
      body: body,
      cache: "no-store",
    });

    const responseText = await upstream.text();
    return new NextResponse(responseText, {
      status: upstream.status,
      headers: { "Content-Type": "application/json" },
    });
  } catch (error) {
    console.error(`Failed to proxy ${provider} settings:`, error);
    return NextResponse.json({ error: "Internal Server Error" }, { status: 500 });
  }
}

export async function GET() {
  const session = await auth.api.getSession({ headers: await headers() });
  const userId = session?.user?.id || (await headers()).get("user_id");

  if (!userId) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const apiUrl = process.env.BACKEND_INTERNAL_URL || "http://supoclip-backend:8000";
  const normalizedApiUrl = apiUrl.replace(/\/$/, "");

  try {
    const upstream = await fetch(`${normalizedApiUrl}/users/me/integrations`, {
      headers: { ...buildBackendAuthHeaders(userId) },
      cache: "no-store",
    });

    const responseText = await upstream.text();
    return new NextResponse(responseText, {
      status: upstream.status,
      headers: { "Content-Type": "application/json" },
    });
  } catch (error) {
    console.error("Failed to proxy integrations fetch:", error);
    return NextResponse.json({ error: "Internal Server Error" }, { status: 500 });
  }
}
