import type { NextConfig } from "next";
import createNextIntlPlugin from "next-intl/plugin";

const nextConfig: NextConfig = {
  output: 'standalone',
  // Skip ESLint during builds (generated Prisma code causes lint errors)
  eslint: {
    ignoreDuringBuilds: true,
  },
  // Skip TypeScript errors during builds for now
  typescript: {
    ignoreBuildErrors: false,
  },
};

const withNextIntl = createNextIntlPlugin();
export default withNextIntl(nextConfig);
