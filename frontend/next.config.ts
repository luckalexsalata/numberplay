import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Disable service worker in development
  ...(process.env.NODE_ENV === 'development' && {
    experimental: {
      pwa: false,
    },
  }),
  
  // Disable workbox in development
  webpack: (config, { dev }) => {
    if (dev) {
      // Remove workbox plugin in development
      config.plugins = config.plugins.filter(plugin => 
        plugin.constructor.name !== 'WorkboxWebpackPlugin'
      );
    }
    return config;
  },
};

export default nextConfig;
