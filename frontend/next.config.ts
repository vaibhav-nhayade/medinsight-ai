
import type { NextConfig } from "next";

// Server-side origin of the FastAPI backend.
// Requests are proxied through /api/v1 so the browser never calls
// the backend directly.

const apiOrigin = process.env.API_ORIGIN ?? "http://127.0.0.1:8000";

const nextConfig: NextConfig = {
  // Hide the Next.js development indicator.
  devIndicators: false,

  cacheComponents: true,
  partialPrefetching: true,

  turbopack: {
    rules: {
      "*.css": {
        loaders: ["@tailwindcss/turbopack"],
        as: "*.css",
      },
    },
  },

  async rewrites() {
    return [
      {
        source: "/api/v1/:path*",
        destination: `${apiOrigin}/api/v1/:path*`,
      },
    ];
  },
};

export default nextConfig;
